# -*- coding: utf-8 -*-

"""
This module contains the class MainWindow.
"""
import utils

from searchpanel import SearchPanel
from playlistspanel import PlaylistsPanel
from Player import Player

from PyQt4.QtGui import QMainWindow, QVBoxLayout, QSplitter, QHBoxLayout, QLabel, QWidget, QPushButton
from PyQt4.QtGui import QApplication, QStyleFactory, QListWidget, QAction, QMenu
from PyQt4.QtCore import Qt
from PyQt4 import QtCore

class MainWidget(QWidget):
    
    def __init__(self, engine):
        super(MainWidget, self).__init__()
        self.initUI(engine)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        
    def initUI(self, engine):
        splitter = QSplitter(Qt.Horizontal)      
        
        # make the right panel
        right_panel = QSplitter(Qt.Vertical)        
        player = Player()
        track_queue = QListWidget()
        
        ## set play on double click
        def play_track():
            player.set_track(track_queue.currentItem().get_track())
            player.play()
        track_queue.doubleClicked.connect(play_track)

        ## advance list on track finish
        def track_finish_task():		
            print 'track finished'
            if track_queue.currentRow() == track_queue.count() - 1:
                track_queue.setCurrentRow(0)
            else:
                track_queue.setCurrentRow(track_queue.currentRow() + 1)
            play_track()
        player.track_finished.connect(track_finish_task)

        ## put some entry controls on menu
        track_queue.setContextMenuPolicy(Qt.CustomContextMenu)
        def onContext(point):
            ## make action
            qaction = QAction('Delete item', track_queue)
            def remove_entry():
                track_queue.takeItem(track_queue.currentRow())
            qaction.triggered.connect(remove_entry)	  
            # Create a menu
            menu = QMenu("Menu", track_queue)
            menu.addAction(qaction)
            # Show the context menu.
            menu.exec_(track_queue.mapToGlobal(point))      
        track_queue.connect(track_queue, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                        onContext)
        utils.add_widgets_to_component(right_panel, [player, track_queue])     
        
        ## make the left panel
        left_panel = QWidget()
        vbox = QVBoxLayout()
        utils.add_widgets_to_component(vbox, 
                    [PlaylistsPanel(engine, [player], [track_queue]),
	                   SearchPanel(engine, [player], [track_queue])])
        left_panel.setLayout(vbox)  
        
        utils.add_widgets_to_component(splitter, [left_panel, right_panel])
        splitter.setSizes([1, 10])
        
        bottomBar = self.make_bottom_bar()        

        # Application UI layout
        vBox = QVBoxLayout(self)        
        vBox.addWidget(splitter)
        vBox.addWidget(bottomBar)        
        self.setLayout(vBox)
        
    def make_bottom_bar(self):
        """
        The bottom panel of the application main window. It contains three 
        controls - clear, shuffle, repeat.
        """
        bottomBar = QWidget()
        label1 = QLabel("Actions: ")
        clear = QPushButton('Clear')
        shuffle = QPushButton('Shuffle')
        replay = QPushButton('Replay')
        hBox = QHBoxLayout()
        utils.add_widgets_to_component(hBox, [label1, clear, shuffle, replay])
        bottomBar.setLayout(hBox)
        return bottomBar

class MainWindow(QMainWindow):
    """
    MainWindow: this is the class that manages all the funcionality of receiving 
    input from the user, and navigating the internet.
    """
    def __init__(self, engine=None, parent=None):
        """
        Default Constructor. It can receive a top window as parent. 
        """
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('PyUplay')
        self.setCentralWidget(MainWidget(engine))
