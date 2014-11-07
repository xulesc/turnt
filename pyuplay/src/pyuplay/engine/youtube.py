# -*- coding: utf-8 -*-

"""
This module performs all transactions with Youtube.
"""
from .datatypes import Track, YouPlaylist

import logging
import gdata.urlfetch
import gdata.youtube.service

from google.appengine.api import urlfetch_stub
from google.appengine.api import apiproxy_stub_map

BASE_URI = 'http://gdata.youtube.com/feeds/api/playlists'
logging.basicConfig()

class Engine:
    logger = logging.getLogger('Engine')
    logger.setLevel(logging.INFO)
  
    def __init__(self):
        self.DEF_DEV_KEY = 'AI39si78QjL3GbzQ-1B_37KRc2E6vdzF4MIugOJVib3OH83BsDZKz_5teF5rWq8HSeUaK65ogp8xFJzphH_vrgHRnOI2CkZrxw'

    def login(self, email='anuj.sharma80@gmail.com', password='#1', source='PyUPlay', dev_key=None):
        if dev_key == None:
            dev_key = self.DEF_DEV_KEY
      
        yt_service = gdata.youtube.service.YouTubeService()
        yt_service.email = email
        yt_service.password = password
        yt_service.source = source
        yt_service.developer_key = dev_key
        yt_service.ProgrammaticLogin()
        return yt_service
 
    def search(self, query_string='metallica', max_results=5):
        self.logger.debug(query_string)
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())

        gdata.service.http_request_handler = gdata.urlfetch

        client = gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = query_string
        query.max_results = max_results
        query.racy = 'include'
        query.orderby = 'relevance'

        feed = client.YouTubeQuery(query)
        tracks = []
        for entry in feed.entry:
            tracks.append(Track(entry.media.title.text, entry.media.player.url, entry.media.thumbnail))

        return tracks

    def get_user_playlists(self):
        self.logger.info('retreiving user playlists ')
        playlists = {}

        ## get playlists
        yt_service = self.login()
        playlist_feed = yt_service.GetYouTubePlaylistFeed(username='default')
        self.logger.debug(vars(playlist_feed))

        ## parse playlists and get songs belonging to them
        for playlist_entry in playlist_feed.entry:
            self.logger.debug(playlist_entry)
            self.logger.debug(playlist_entry.title.text)
            id_start_index = playlist_entry.id.text.rfind('/')
            playlist_id = playlist_entry.id.text[id_start_index + 1 :]
            youPlaylist = YouPlaylist(playlist_entry.title.text, playlist_id)

            ## get songs of the playlist
            playlist_video_feed = yt_service.GetYouTubePlaylistVideoFeed(uri='%s/%s' % (BASE_URI, playlist_id))
            self.logger.debug(playlist_video_feed)
            for video in playlist_video_feed.entry:
                self.logger.debug(video.title.text)
                youPlaylist.add_track(Track(video.title.text, video.media.player.url, video.media.thumbnail))
    
            ## put playlist on map
            if youPlaylist.get_size() > 0:
                playlists[playlist_entry.title.text] = youPlaylist

        return playlists

    def add_tracks_to_playlist(self, playlist, tracks):
        yt_service = self.login()
        failed_tracks = []
        for track in tracks:
            video_entry = yt_service.AddPlaylistVideEntryToPlaylist('%s/%s' % (BASE_URI, id), track.get_identifier())
            if isinstance(video_entry, gdata.youtube.YouTubePlaylistVideoEntry):
                continue
            failed_tracks.add(track)
        return failed_tracks

