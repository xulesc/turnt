from PyQt4.QtGui import QListWidgetItem 

class QTrackListWidgetItem(QListWidgetItem):
    
    def __init__(self, track):
        super(QTrackListWidgetItem, self).__init__()
        self.track = track
        self.setText(track.get_name())
    
    def add_item_to_queue(self):
        print self.track
  
    def get_track(self):
        return self.track
