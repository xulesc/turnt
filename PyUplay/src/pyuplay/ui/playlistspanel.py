'''
Created on Oct 16, 2012

@author: xule
'''
import utils
from QPlaylistWidgetItem import QPlaylistWidgetItem
from QTrackListWidgetItem import QTrackListWidgetItem

from PyQt4.QtGui import QVBoxLayout, QLabel, QWidget, QListWidget

class PlaylistsPanel(QWidget):

    def __init__(self, engine=None, double_click_listeners=[], queue_listeners=[]):
        super(PlaylistsPanel, self).__init__()
        self.initUI(engine)
        self.engine = engine
        self.double_click_listeners = double_click_listeners
        self.queue_listeners = queue_listeners
        
    def initUI(self, engine):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Playlists'))
        
        ## make the list view
        lv = QListWidget()
        lv.doubleClicked.connect(self.item_select)
        for playlist in engine.get_user_playlists().values():
            lv.addItem(QPlaylistWidgetItem(playlist))
        self.lv = lv
        vbox.addWidget(lv)
        
        self.setLayout(vbox)
        
    def item_select(self):
        current_playlist = self.lv.currentItem().get_playlist()
        print current_playlist.get_name()
        for current_track in current_playlist.get_tracks():
            url_string = current_track.get_url()
            url_string = utils.extract_video_url(url_string)
            for l in self.queue_listeners:
                l.addItem(QTrackListWidgetItem(current_track))
