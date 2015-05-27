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

class spider_(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		
    def run(self,url):
        self.url = url
        self.getAllImagesUrls()
        self.getLagerImage()

    def getAllImagesUrls(self):
        """
            获取所有的图片地址，按照标签<img src= 进行正则匹配
        """
        resp = ""
        try:
            resp = urllib2.urlopen(self.url).read()
        except Exception, e:
            print e
            print "抓取图片源代码失败，赶紧拿起手机联系老王吧"
            sys.exit()

        # 保险起见，这里用两层结构，第一层，把所有img标签都抓下来，第二层，把所有的src都抓下来
        img_div_pattern = r'<img.*?>'
        images_url_pattern = r'src=".*?"'
        img_divs = re.findall(img_div_pattern,resp)

        for item in img_divs:
            m = re.search(images_url_pattern, item)
            if m:
              self.image_urls.append(m.group(0)[5:-1])

        print "这个网页上一共找出来了%d个文件"%(len(self.image_urls))


    def getLagerImage(self):
        """
            如果设置了image_rect的大小，则取大于等于该尺寸的图片
            否则获取尺寸最大的图片保存
        """
        for item in self.image_urls:
            resp = ""
            try:
                resp = urllib2.urlopen(item).read()
            except Exception, e:
                print "下载图片地址失败，赶紧拿起手机联系老王吧"
                continue
            else:
                if sys.getsizeof(resp) < self.image_large:
                    print "小于200k的文件不是好文件，小修看不上的"
                    continue
                name_pre = self.getImageName(item)
                try:
                    if self.is_jpg(resp):
                        image_name = "%s.jpg"%name_pre
                    else:
                        image_name = "%s.jpg"%name_pre

                    f1 = file(image_name, 'w')
                    f1.write(resp)
                    f1.close()
                    print "保存文件%s完毕！"%image_name
                except Exception, e:
                    print e
                    print "保存图片失败，[%s] 联系下老王，虽然老王也许也不知道"%item       

			

if __name__ == '__main__':
	s_500 = Spider_500Px("https://500px.com/")
	s_500.start()
