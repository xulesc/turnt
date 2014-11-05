
import utils

from QTrackListWidgetItem import QTrackListWidgetItem

from PyQt4.QtGui import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton
from PyQt4.QtGui import QLineEdit, QListWidget
from PyQt4.QtGui import QAction, QMenu
from PyQt4.QtCore import Qt
from PyQt4 import QtCore

class SearchPanel(QWidget):

    def __init__(self, engine=None, double_click_listeners=[], queue_listeners=[]):
        super(SearchPanel, self).__init__()
        self.initUI()
        self.engine = engine
        self.double_click_listeners = double_click_listeners
        self.queue_listeners = queue_listeners

    def initUI(self):
        vbox = QVBoxLayout()
        
        ##TODO: make a title bar for now just a label
        vbox.addWidget(QLabel('Search'))
        
        ## make horizontal box and add a text field and a button
        search_widget = QWidget()
        hbox = QHBoxLayout()
        self.search_text_box = QLineEdit()
        search_button = QPushButton('Go')
        search_button.clicked.connect(self.do_search)
        utils.add_widgets_to_component(hbox, [self.search_text_box, search_button])
        search_widget.setLayout(hbox)
        utils.set_button_width(search_button)
        vbox.addWidget(search_widget)

        ## make the list view
        lv = QListWidget()
        lv.doubleClicked.connect(self.item_select)
        lv.setContextMenuPolicy(Qt.CustomContextMenu)

        def onContext(point):
            ## make action
            qaction = QAction('Add to Queue', lv)
            qaction.triggered.connect(self.add_item_to_queue)
            
            # Create a menu
            menu = QMenu("Menu", lv)
            menu.addAction(qaction)
            # Show the context menu.
            menu.exec_(lv.mapToGlobal(point))
      
        lv.connect(lv, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                        onContext)
        self.lv = lv
        vbox.addWidget(lv)
        
        self.setLayout(vbox)

    def do_search(self):
        self.lv.clear()
        for r in self.engine.search(str(self.search_text_box.text())):
            self.lv.addItem(QTrackListWidgetItem(r))

    def item_select(self):
        ## get the current selected track
        current_track = self.lv.currentItem().get_track()
        ## pass url of the track to ALL listeners. the listeners must provide
        ## setUrl method
        url_string = current_track.get_url()
        url_string = utils.extract_video_url(url_string)
        for l in self.double_click_listeners:
            #l.setUrl(QUrl(QString(url_string)))
            l.set_track(current_track)
            l.play()
    
    def add_item_to_queue(self):
        #print self.lv.currentItem().get_track()
        ## get the current selected track
        current_track = self.lv.currentItem().get_track()
        ## pass track to all add_queue listeners
        for l in self.queue_listeners:
            l.addItem(QTrackListWidgetItem(current_track))  
