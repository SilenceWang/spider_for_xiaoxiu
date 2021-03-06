#! /bin/python
#! coding:utf-8

import urllib2
import re
import sys
import os
import threading

class Spider_images(threading.Thread):
    """蜘蛛的主类，主要用来爬图片"""

    def __init__(self, t_name):
        threading.Thread.__init__(self,name = t_name)
        self.url = ""
        self.image_urls = [] #图片的url集合
        self.image_rect = [] #图片尺寸
        self.image_large = 200000 #默认收藏的最小的文件大小

    def run(self,url):
        self.url = url
        self.getAllImagesUrls()
        self.getLagerImage()

    def getAllImagesUrlsFromJS(self):
        """

        """
        pass

    def getAllImagesUrls(self):
        """
            获取所有的图片地址，按照标签<img src= 进行正则匹配
        """
        resp = ""
        try:
            resp = urllib2.urlopen(self.url).read()
            # print resp
        except Exception, e:
            print e
            print "抓取图片源代码失败，赶紧拿起手机联系老王吧"
            sys.exit()

        #页面都是把图片地址返回了，所以这里只需要拆分就好了
        pattern = r"<script type='application\/ld\+json.*?\<\/script\>"
        img_re = re.search(pattern, resp ,re.S)
        image_str = img_re.group()
        image_str = image_str.replace("<script type='application/ld+json'>","")
        image_str = image_str.replace("</script>","")
        image_str = image_str.replace("true","True")
        image_str = image_str.replace("false","False")
        image_str = image_str.replace("\/","/")
        image_pro = eval(image_str)

        self.image_urls.append(image_pro["image"])
        self.image_urls.append(image_pro["thumbnailUrl"])

        # 保险起见，这里用两层结构，第一层，把所有img标签都抓下来，第二层，把所有的src都抓下来
        img_div_pattern = r'<img.*?>'
        images_url_pattern = r'src=".*?"'
        img_divs = re.findall(img_div_pattern,resp)

        for item in img_divs:
            m = re.search(images_url_pattern, item)
            if m:
              self.image_urls.append(m.group(0)[5:-1])

        print "这个网页上一共找出来了%d个文件"%(len(self.image_urls))
        print self.image_urls


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
                print "%s  大小为 %f "%(item,sys.getsizeof(resp))
                if int(sys.getsizeof(resp)) < int(self.image_large):
                    print "小于200k的文件不是好文件，小修看不上的"
                    continue
                name_pre = self.getImageName(item)
                # try:
                if self.is_jpg(resp):
                    image_name = "%s.jpg"%name_pre
                else:
                    image_name = "%s.jpg"%name_pre

                f1 = file(image_name, 'w+')
                f1.write(resp)
                f1.close()
                print "保存文件%s完毕！"%image_name
                # except Exception, e:
                #     print e
                #     print "保存图片失败，[%s] 联系下老王，虽然老王也许也不知道"%item                

    def getImageName(self, url):
        """
            根据链接地址得到图片的名字，其实就是链接最后的那串
        """
        tmp = url.split('/')
        return tmp[len(tmp)-1]

    def is_jpg(self,resp):
        """
            判断返回的图片是否是jpg/jpeg格式；如果是就返回True，否则返回false
        """
        data = resp[:10]
        if data[:4] != '\xff\xd8\xff\xe0': return False
        if data[6:10] != 'JFIF\0': return False
        return True


if __name__ == '__main__':
    url = "https://500px.com/photo/80626185/refreshments-by-tim-santasombat"
    if len(sys.argv) == 2:
        print """
            亲爱的小修修，你又忘记怎么用了啊。。
            usage:  python spider_500px.py [url]
            [url]是你要爬的图片的地址
        """
        # sys.exit()
        url = sys.argv[1]
    si = Spider_images("thread 1")
    si.run(url)
