#!/usr/bin/python

from pyuplay.engine.youtube import Engine
from pyuplay.engine.datatypes import Track


engine = Engine()
#engine.login()
#print engine.search('the sound of goodbye', 5)
print engine.get_user_playlists()



