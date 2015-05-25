#! /bin/python
#! coding:utf-8

import urllib2
import re
import sys
import random

class Spider_base:
	"""
		This class is create for base spider.

	"""
	def __init__(self, url):
		self.url = url
		self.userAgent = [
				'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36',
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2272.104 Safari/536.36',
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15'
				]

	def start(self):
		"""
			start spider. I split it to three step 
		"""
		self.get_url_resp()

	def get_url_resp(self):
		"""
			获取页面的所有返回结果
		"""
		# random userAgent to protect forbining by website which we do spider.
		userAgentIndex = random.randint(0,len(self.userAgent)-1)
		headers = {
            		'User-Agent' : self.userAgent[userAgentIndex]
        	}

		req = urllib2.Request(url = self.url,headers = headers)
		try:
			pageResponse = urllib2.urlopen(req).read()
		except Exception,e:
			print "there is some problem while getting url resp \n %s"%e
			pageResponse = ""
			pass
		return pageResponse
	
	def get_regx_groups(self, pattern_str, contents):
		"""
			return regx groups by paramters[pattern_str]
		"""
		pageRex = re.compile(pattern_str)
		pages = pageRex.findall(contents)
		return pages	
