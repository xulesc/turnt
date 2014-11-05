# -*- coding: utf-8 -*-

"""
This module contains the data types used in the application.
"""
import logging
logging.basicConfig()

class Track:
    logger = logging.getLogger('Track')
    logger.setLevel(logging.INFO)

    def __init__(self, name, url, thumbnail):
        self.__name = name
        self.__url = url
        self.__thumbnail = thumbnail    
        self.__id = url.split('=')[1].split('&')[0]
        self.logger.debug('url: %s, id: %s' % (url, self.__id))
    
    def get_name(self):
        return self.__name
    
    def get_url(self):
        return self.__url
    
    def get_thumbnail(self):
        return self.__thumbnail
    
    def get_identifier(self):
        return self.__id
    
    def __str__(self):
        return '%s\t%s\t%s' % (self.__name, self.__url, self.__thumbnail)
    
    def __repr__(self):
        return self.__str__()


class YouPlaylist:
    logger = logging.getLogger('YouPlaylist')
    logger.setLevel(logging.INFO)

    def __init__(self, name, uri):
        self.__name = name
        self.__uri = uri
        self.__tracks = []

    def get_name(self):
        return self.__name

    def get_uri(self):
        return self.__uri

    def add_track(self, track):
        self.__tracks.append(track)

    def get_size(self):
        return len(self.__tracks)

    def get_tracks(self):
        return self.__tracks

    def __str__(self):
        return '%s\t%s\%s' % (self.__name, self.__uri, self.__tracks)

    def __repr__(self):
        return self.__str__()


