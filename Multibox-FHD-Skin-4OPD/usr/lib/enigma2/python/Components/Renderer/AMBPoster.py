# -*- coding: utf-8 -*-
# by digiteng...06.2020
# mod by ostende
# <widget source="session.Event_Now" render="poster" position="0,0" size="185,278" zPosition="1" />
from Renderer import Renderer
from enigma import ePixmap, eTimer, loadJPG
from urllib2 import urlopen, quote
import json
import re
import os
import socket

tmdb_api = "3c3efcf47c3577558812bb9d64019d65"

if not os.path.isdir("/tmp/poster"):
	os.makedirs("/tmp/poster")
	path_folder = "/tmp/poster/"
else:
	path_folder = "/tmp/poster/"

class FroidPoster(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pstrNm = ''
		self.evntNm = ''
		self.intCheck()
		

	def intCheck(self):
		try:
			socket.setdefaulttimeout(0.5)
			socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
			return True
		except:
			return False

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
			if what[0] != self.CHANGED_CLEAR:
				self.delay()
				self.filterSearch()
		except:
			pass

	def showPoster(self):
		self.event = self.source.event
		if self.event:
			evnt = self.event.getEventName()
			evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt)
			evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
			self.evntNm = evntNm
			pstrNm = path_folder + evntNm + ".jpg"
			if os.path.exists(pstrNm):
				self.instance.setPixmap(loadJPG(pstrNm))
				self.instance.show()
			else:
				self.downloadPoster()
				self.instance.hide()
		else:
			self.instance.hide()
			return

	def downloadPoster(self):
		try:
			if self.intCheck():
				url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(self.srch, tmdb_api, quote(self.evntNm))
				poster = json.load(urlopen(url_tmdb))['results'][0]['poster_path']
				if poster:
					url_poster = "https://image.tmdb.org/t/p/w185{}".format(poster)
					dwn_poster = path_folder + "{}.jpg".format(self.evntNm)
					with open(dwn_poster,'wb') as f:
						f.write(urlopen(url_poster).read())
						f.close()
			else:
				return
		except:
			return

	def filterSearch(self):
		try:
			sd = self.event.getShortDescription() + "\n" + self.event.getExtendedDescription()
			w = [
				"serial", 
				"series", 
				"serie", 
				"serien", 
				"séries", 
				"serious", 
				"folge", 
				"episodio", 
				"episode", 
				"ep.", 
				"staffel", 
				"soap", 
				"doku", 
				"tv", 
				"talk", 
				"show", 
				"news", 
				"factual", 
				"entertainment", 
				"telenovela", 
				"dokumentation", 
				"dokutainment", 
				"documentary", 
				"informercial", 
				"information", 
				"sitcom", 
				"reality", 
				"program", 
				"magazine", 
				"mittagsmagazin"
				]

			for i in w:
				if i in sd.lower():
					self.srch = "tv"
					break
				else:
					self.srch = "multi"

		except:
			return

	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showPoster)
		self.timer.start(100, True)
