# -*- Mode: python; coding: utf-8; tab-width: 8; indent-tabs-mode: t; -*-
#
# Copyright (C) 2012 He Jian <hejian.he@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# The Rhythmbox authors hereby grant permission for non-GPL compatible
# GStreamer plugins to be used and distributed together with GStreamer
# and Rhythmbox. This permission is above and beyond the permissions granted
# by the GPL license by which Rhythmbox is covered. If you modify this code
# you may extend this exception to your version of the code, but you are not
# obligated to do so. If you do not wish to do so, delete this exception
# statement from your version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

import rb
import urllib.parse
import re
import syslog

class AzlyricsParser (object):
	def __init__ (self, artist, title):
		self.artist = artist
		self.title = title
		self.url = None

	def search (self, callback, *data):
		#artist = urllib.parse.quote_plus(self.artist)
		artist = self.artist.replace(" ","")
		#title = urllib.parse.quote_plus(self.title)
		title = self.title.replace(" ","")

		self.url = 'http://www.azlyrics.com/lyrics/%s/%s.html' % (artist, title)
		#debug
		syslog.syslog('search()::rb.Loader()')
		loader = rb.Loader()
		syslog.syslog('search()::loader.get_url() url://search azlyrics: '+self.url)
		loader.get_url (self.url, self.got_results, callback, *data)
		syslog.syslog('search() end')

	def got_results (self, result, callback, *data):
		if result is None:
			syslog.syslog('get_results()::result is None')
			callback (None, *data)
			return
		syslog.syslog('get_results()::result is not None')

		result = result.decode('utf-8')

		syslog.syslog('get_results()::re.search')

		m = re.search('<div class=\"lyricsh\">', result)

		if m is None:
			callback (None, *data)
			return

		loader = rb.Loader()
		#debug
		#url = 'http://www.azlyrics.com' + m.group(1)
		syslog.syslog('get_results()::loader.get_url: ')
		loader.get_url (self.url, self.parse_lyrics, callback, *data)

	def parse_lyrics (self, result, callback, *data):
		syslog.syslog('parse_lyrics()')

		if result is None:
			syslog.syslog('parse_lyrics()::None')
			callback (None, *data)
			return

		result = result.decode('utf-8')
		lyrics = re.split('<div>',result)[1]
		lyrics = re.split('</div>',lyrics)[0]
		lyrics = re.sub('<br>', '', lyrics)
		lyrics = re.sub (r'<.*?>', "", lyrics)
		lyrics = lyrics.replace ('\r', "")
		lyrics = lyrics.strip ("\n")
		lyrics = self.title + "\n\n" + lyrics
		lyrics += "\n\nLyrics provided by azlyrics.com"
		syslog.syslog('parse_lyrics()::lyrics::'+lyrics)

		callback (lyrics, *data)
