#! /bin/python
#! coding:utf-8
class Utils:
	"""
		tools 
	"""
		
	def is_jpg(self, resp):
		"""
		    判断返回的图片是否是jpg/jpeg格式；如果是就返回True，否则返回false
		"""
		data = resp[:10]
		if data[:4] != '\xff\xd8\xff\xe0': return False
		if data[6:10] != 'JFIF\0': return False
		return True


