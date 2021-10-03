import numpy as np
from train import train
from loader import LandslideDataset, DistLandslideDataset
from torch.utils.data import DataLoader
# from dimension_reduction import reduce_dim
from time import ctime
from sacred import Experiment
# from sacred.observers import MongoObserver

ex = Experiment('CNNPatch')

@ex.config
def ex_cfg():
    train_param = {
        'optim': 'Adam',
        'lr': 0.0001,
        'n_epochs': 100,
        'bs': 4,
        'decay': 1e-3,
        'patience': 2,
        'pos_weight': 1,
        'model': 'UNet'
    }
    data_param = {
        'n_workers': 4,
        'region': 'Veneto',
        'pix_res': 10,
        'stride': 500,
        'ws': 500,
        'pad': 64,
        'feature_num': 94,
        'oversample': False,
        'prune': 64,
        'dist_num': 3, #corresponding to 30,100,300
        'dist_feature': False
    }
    loc_param = {
        'load_model': '',
        'data_path': '/tmp/Veneto_data.h5',
        'index_path': '/home/ainaz/Projects/Landslides/image_data/new_partitioning/',
        'save': 20
    }

# def plot_grid(x, y):
#     import matplotlib.pyplot as plt
#     fig = plt.figure()
#     fig.add_subplot(1,1,1)
#     plt.scatter(x, y['Adam'], c='b')
#     plt.scatter(x, y['SGD'], c='r')
#     plt.show()

@ex.automain
def main(train_param, data_param, loc_param, _log, _run):
    data = []
    if data_param['dist_feature']:
        for flag in ['train', 'validation']:
            data.append(
                DistLandslideDataset(
                    loc_param['data_path'],
                    np.load(loc_param['index_path']+'{}_{}_indices.npy'.format(data_param['region'], flag)),
                    data_param['region'],
                    data_param['ws'],
                    data_param['pad'],
                    data_param['prune'],
                    data_param['dist_num']
                )
            )
    else:    
        for flag in ['train', 'validation']:
            data.append(
                LandslideDataset(
                    loc_param['data_path'],
                    np.load(loc_param['index_path']+'{}_{}_indices.npy'.format(data_param['region'], flag)),
                    data_param['region'],
                    data_param['ws'],
                    data_param['pad'],
                    data_param['prune']
                )
            )
    loader = [DataLoader(d, batch_size=train_param['bs'], shuffle=True, num_workers=data_param['n_workers']) for d in data]

    _log.info('[{}]: created train and validation datasets.'.format(ctime()))
    _log.info('[{}]: starting to train ...'.format(ctime()))
    train(loader[0], loader[1], train_param, data_param, loc_param, _log, _run)
    _log.info('[{}]: training is finished!'.format(ctime()))
