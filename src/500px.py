#! /bin/python
#! coding:utf-8

import sys
sys.path.append('./')
import re
from spider_base import Spider_base
from spider_500px import Spider_images

class Spider_500Px(Spider_base):
	"""
		spider for 500px
	"""
	def __init__(self, url):
		Spider_base.__init__(self, url)
		self.photos_pattern = r"window\.photos.*?};"
		self.photo_list = []

	def start(self):
		resp = self.get_url_resp()

		photos = re.search(self.photos_pattern, resp ,re.S)
		photo_str = photos.group()
		photo_str = photo_str[photo_str.find('{')-1 : -1 ]

		#change str into list
		photo_dict = {}
		try:
			photo_str = photo_str.replace('{\n','{\n"')
			photo_str = photo_str.replace(':','":')
			photo_str = photo_str.replace(']],\n',']],\n"')
			photo_dict =  eval(photo_str)
		except Exception, e:
			print "there is some exception I don't expect \n %s"%e

		for value in photo_dict.values():
			for v in value:
				url = "https://500px.com/photo/%s/%s"%(v[0],v[-1])
				self.photo_list.append(url)

		index = 1
		for item in self.photo_list:
			si = Spider_images()
			si.run(item)
			index += 1
			if index >= 10:
				return


			

if __name__ == '__main__':
	s_500 = Spider_500Px("https://500px.com/")
	s_500.start()
