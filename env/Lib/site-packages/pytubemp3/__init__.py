# -*- coding: utf-8 -*-
# flake8: noqa: F401
# noreorder
"""
Pytube: a very serious Python library for downloading YouTube Videos.
"""
__title__ = "pytube3"
__author__ = "Nick Ficano, Harold Martin"
__license__ = "MIT License"
__copyright__ = "Copyright 2019 Nick Ficano"

from pytubemp3.version import __version__
from pytubemp3.streams import Stream
from pytubemp3.captions import Caption
from pytubemp3.query import CaptionQuery
from pytubemp3.query import StreamQuery
from pytubemp3.__main__ import YouTube
#from pytubemp3.contrib.playlist import Playlist
