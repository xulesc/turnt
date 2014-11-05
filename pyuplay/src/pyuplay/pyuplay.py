import sys, logging

from PyQt4 import QtGui
from ui.mainwindow import MainWindow
from engine.youtube import Engine

if __name__ == "__main__":
	logging.basicConfig()
	logger = logging.getLogger('__main__')
	logger.setLevel(logging.INFO)
	logger.info('Initializing application and loading GUI')
	
	app = QtGui.QApplication(sys.argv)
	ui = MainWindow(Engine())
	ui.show()
	
	sys.exit(app.exec_())



