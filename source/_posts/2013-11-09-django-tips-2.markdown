---
layout: post
title: "Django Tips - 2"
date: 2013-11-09 14:40
comments: true
tags: [Django]
---
###在Django中引用静态文件
由于Django对于所有链接的请求都需要经过`url.py`的配置，这虽然可以使得浏览器url非常美观，也方便了开发了，但是在HTML中引入JavaScript和CSS文件时就会发生404错误，因为求情了在`url.py`中不存在的地址。

Django当然也考虑到了这个问题，所以提供了静态文件的配置方法。

<!-- more -->

1.首先在你的工程中新建一个文件夹`static`（名字随意）来存放静态文件，文件路径如图：

![static folder](/images/2013/11/9/project catalog.png)
在`setting.py`文件中找到`STATIC_URL`选项，将其设置为刚才新建的`static`文件夹相对路径，例如：
```
STATIC_URL = './static/'
```
2.在`url.py`文件中加入如下配置：
```
(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
```

##Django模板对日期类型的转换

Django Template会对日期类型进行转换，按'F j, Y'格式显示，比较如下代码：

代码1：

``` python
def current_time(request):
    now = datetime.datetime.now()
    # print '%s' % now
    t = get_template('test/current_date.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
```
输出：

```
It's now Oct. 14, 2013, 7:18 p.m.
```
代码2：

``` python
def current_time1(request):
    now = datetime.datetime.now()
    html = 'It\'s now %s.' % now
    return HttpResponse(html)
```
输出：

```
It's now 2013-10-14 19:17:18.361020.
```
