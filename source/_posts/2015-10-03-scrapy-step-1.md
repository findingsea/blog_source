title: Scrappy入门：百度贴吧图片爬虫
date: 2015-10-03 20:11:27
tags: Python
---
[Scrapy](http://scrapy.org/)是Python非常有名的爬虫框架，框架本身已经为爬虫性能做了很多优化：多线程、整合xpath和图片专用管道等等，开发人员只要专注在功能需求上。

<!-- more -->

基本Scrapy使用教程参考：[初窥Scrapy](http://scrapy-chs.readthedocs.org/zh_CN/latest/intro/overview.html)和[Scrapy入门教程](http://scrapy-chs.readthedocs.org/zh_CN/latest/intro/tutorial.html)。

学习一种技术或者一个框架最好的方式当然是用它做一些小工程，入门第一步我先选择了百度贴吧图片爬虫，因为既够简单又比较实用。

因为这次涉及到图片的下载，而Scrapy本身为此提供了特殊的图片管道，所以果断直接用Scrapy的图片管道来帮助完成。Scrapy中管道的定义如下：

> 当Item在Spider中被收集之后，它将会被传递到Item Pipeline，一些组件会按照一定的顺序执行对Item的处理。
> 每个item pipeline组件(有时称之为“Item Pipeline”)是实现了简单方法的Python类。他们接收到Item并通过它执行一些行为，同时也决定此Item是否继续通过pipeline，或是被丢弃而不再进行处理。

对于管道的典型应用场景如下：

> 清理HTML数据
> 验证爬取的数据(检查item包含某些字段)
> 查重(并丢弃)
> 将爬取结果保存到数据库中

Scrappy图片管道的使用教程参考：[下载项目图片](http://scrapy-chs.readthedocs.org/zh_CN/latest/topics/images.html)。

使用Scrapy最重要的就是编写特定的spider类，本文指定的spider类是`BaiduTieBaSpider`，来看下它的定义：

```
import scrapy
import requests
import os
from tutorial.items import TutorialItem
class BaiduTieBaSpider(scrapy.spiders.Spider):
    name = 'baidutieba'
    start_urls = ['http://tieba.baidu.com/p/2235516502?see_lz=1&pn=%d' % i for i in range(1, 38)]
    image_names = {}
    def parse(self, response):
        item = TutorialItem()
        item['image_urls'] = response.xpath("//img[@class='BDE_Image']/@src").extract()
        for index, value in enumerate(item['image_urls']):
            number = self.start_urls.index(response.url) * len(item['image_urls']) + index
            self.image_names[value] = 'full/%04d.jpg' % number
        yield item
```

这里要关注Scrappy做的两件事情：

* 根据`start_urls `中的URL地址访问页面并得到返回
* `parse(self, response)`函数就是抓取到页面之后的解析工作

那么首先就是`start_urls`的构造，这里是观察了百度贴吧里的URL规则，其中`see_lz=1`表示只看楼主，`pn=1`表示第一页，根据这些规则得出了一个URL数组。然后再观察单个页面的HTML源码，得出每个楼层发布的图片对应的`img`标签的类为`BDE_Image`，这样就可以得出xpath的表达式：`xpath("//img[@class='BDE_Image']/@src")`，来提取楼层中所有图片的`src`，赋值到`item`对象的`image_urls`字段中，当spider返回时，`item`会进入图片管道进行处理（即Scrapy会自自动帮你下载图片）。

对应的`item`类的编写和`setting.py`文件的修改详见上文的教程。

到这里下载图片的基本功能都完成了，但是有个问题：我想要按顺序保存图片怎么办？

造成这个问题的关键就是Scrapy是多线程抓取页面的，也就是对于`start_urls`中地址的抓取都是异步请求，以及`item`返回之后到图片管道后对每张图片的URL也是异步请求，所以是无法保证每张图片返回的顺序的。

那么这个问题怎么解决呢？试了几种办法之后，得到一个相对理想的解决方案就是：制作一个字典，key是图片地址，value是对应的编号。所以就有了代码中的`image_names`和`number = self.start_urls.index(response.url) * len(item['image_urls']) + index`，然后再定制图片管道，定制的方法详见上文给出的教程链接，在本文中定制需要做的事情就是重写`file_path`函数，代码如下：

```
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from tutorial.spiders.BaiduTieBa_spider import BaiduTieBaSpider

class MyImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        image_name = BaiduTieBaSpider.image_names[request.url]
        return image_name

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
```

`file_path`函数就是返回每张图片保存的路径，当我们有一张完整的字典之后，只要根据`request`的URL去取相应的编号即可。

这个方法显然是比较消耗内存的，因为如果图片很多的话，需要维护的字典的条目也会很多，但从已经折腾过的几个解决方案（例如不用管道而采用手动阻塞的方式来下载图片）来看，它的效果是最好的，付出的代价也还算可以接受。

Scrappy入门第一个小demo就写到这里。