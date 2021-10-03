#integrate model to website

from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):

  def init(self, properties):
    # Set Form properties and Data Bindings.
    self.init_components(properties)

    # Any code you write here will run when the form opens.

  def drop_down_1_change(self, event_args):
    """This method is called when an item is selected"""
    pass

  def button_1_click(self, event_args):
    meh = self.drop_down_1.selected_value
    if (meh == "South East Asia"):
      self.image_1.visible = 1
      self.image1.source = "https://slidetect.anvil.app//theme/unknown3.png"
    elif (meh == "South America"):
      self.image_1.visible = 1
      self.image1.source = "https://slidetect.anvil.app//theme/unknown.png"
    elif (meh == "Nordic Countries"):
      self.image_1.visible = 1
      self.image1.source = "https://slidetect.anvil.app//theme/unknown2.png"
    pass
