'''
Created on Oct 16, 2012

@author: xule
'''
from PyQt4.QtGui import QListWidgetItem 

class QPlaylistWidgetItem(QListWidgetItem):
    
    def __init__(self, playlist):
        super(QPlaylistWidgetItem, self).__init__()
        self.playlist = playlist
        self.setText(playlist.get_name())
    
    def add_item_to_queue(self):
        print self.playlist
  
    def get_playlist(self):
        return self.playlist