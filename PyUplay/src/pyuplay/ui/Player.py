import logging

from PyQt4.QtWebKit import QWebView, QWebSettings
from PyQt4.QtCore import QObject, pyqtSlot
from PyQt4 import QtCore

logging.basicConfig()

class Player(QWebView):
	logger = logging.getLogger('Player')
	logger.setLevel(logging.INFO)
		
	track_finished = QtCore.pyqtSignal()
	
	def __init__(self):
		super(Player, self).__init__()
		self.__instantiated = 'yes'
		self.settings = self.settings() # self.webView is the QWebView 
		self.settings.setAttribute(QWebSettings.PluginsEnabled, True)    
		self.logger.info('initalized')

	def set_track(self, track):
		self.__track = track
		
	def get_track(self):
		return self.track
		
	def play(self):	
		player = self;
		class Foo(QObject):
			@pyqtSlot()
			def trackEnd(self):		
				player.logger.debug('emiting finished signal')
				player.track_finished.emit()			
			@pyqtSlot()
			def statusChange(self):
				player.logger.debug('status changed')

		self.setHtml(self.__make_yt_html())
		self.page().mainFrame().addToJavaScriptWindowObject("foo", Foo(self)) 
		player.logger.debug(self.page().mainFrame().toHtml())

	def pause(self):
		print 'pause'
		
	def stop(self):
		print 'stop'
		
	def __make_yt_html(self):
		html = """
<html>
  <body>
    <div id="player"></div>

    <script>
      var tag = document.createElement('script');
      tag.src = "http://www.youtube.com/player_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      var player;
      function onYouTubePlayerAPIReady() {
        player = new YT.Player('player', {
          videoId: '%s',
          controls: 0,
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
          }
        });
      }

      function onPlayerReady(event) {
        event.target.playVideo();
      }

      var done = false;
      function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.ENDED) {
          foo.trackEnd()
        }
      }
      function stopVideo() {
        player.stopVideo();
      }
    </script>
  </body>
</html>
		""" % self.__track.get_identifier()
		return html		
		

