#!/home/themylogin/www/apps/virtualenv/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import mpd
import os
import pylast
import sys

config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "settings.ini"))
lastfm_api_key = config.get("last.fm", "api_key")
lastfm_api_secret = config.get("last.fm", "api_secret")
lastfm_username = config.get("last.fm", "username")
lastfm_password = config.get("last.fm", "password")
mpd_host = config.get("mpd", "host")

current_song = None
for i in range(5):
    try:
        client = mpd.MPDClient()
        client.connect(mpd_host, 6600)
        current_song = client.currentsong()
        break
    except:
        pass

ok = False
if current_song is not None:
    if current_song.has_key("artist"):
        artist = current_song["artist"]
    else:
        if current_song.has_key("performer"):
            artist = current_song["performer"]
        else:
            artist = "Unknown Artist"

    for i in range(5):
        try:
            pylast.get_lastfm_network(api_key=lastfm_api_key, api_secret=lastfm_api_secret, username=lastfm_username, password_hash=pylast.md5(lastfm_password)).get_track(artist, current_song["title"]).love()
            print "Content-type: text/plain\n"
            print "1"
            ok = True
            break
        except:
            pass

if not ok:
    print "Content-type: text/plain\n"
    print "0"
