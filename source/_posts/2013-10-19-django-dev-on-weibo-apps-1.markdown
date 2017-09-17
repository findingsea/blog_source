---
layout: post
title: "Django Tips - 1"
date: 2013-10-19 15:49
comments: true
tags: [Django]
---
近来想用Django做一个微博的站内应用，虽说一个简单的站内应用用Django开发有点『杀鸡用牛刀』的意思，但是由于之前用Django开发的经验为零，作为第一个练手项目，微博应用还是相当合适的。顺便把遇到的一些问题和解决方案记录下来，以备回看、

<!-- more -->

###本地调试
在实际运行中，用户当然是通过微博应用页面来访问我们的服务器，使用我们的应用，但是在开发调试的时候，如果每次都需要把代码同步到服务器才能看到效果的话那简直要『疯了』，所以设置本地调试必不可少。

所幸设置本地调试并不复杂。

首先，在『应用信息』-->『高级信息』-->『安全设置』中，将『应用的服务IP地址』设置为：`127.0.0.1`。注意，『基本信息』中的『应用实际地址』必须是线上地址，不要把这个地址改为`127.0.0.1`。

然后，修改hosts文件。Mac下修改hosts的方法，可以参考[果迷网](http://www.guomii.com/)的文章——[在 Mac OS X Lion 下修改 Hosts 的四种方法](http://www.guomii.com/posts/8644)。在hosts中添加这样一行：

```
127.0.0.1    www.xxxx.com
```
`www.xxxx.com`是你的应用服务器地址。这样浏览器在根据hosts解析的时候，会将对`www.xxxx.com`的访问重定向到本地。这时候在浏览器地址栏中输入`www.xxxx.com`，你会发现访问的是本地，同理，微博页面向`www.xxxx.com`发送的请求其实是发到本地，它包含的也是本地的页面。这样我们就可以在本地对我们的应用进行修改，然后通过微博应用页面直接开效果了，等开发和调试工作完成后在部署到服务器上即可。

###新浪POST请求的CSRF问题
微博站内应用其实就是把你应用的页面嵌在它规定的一个iframe里面，当用户访问的你的应用时，新浪微博会在该月面通过一个form发送一个POST请求到你的『应用实际地址』上，这样带来的一个问题就是：Django处于防止CSRF攻击的考虑对于发送POST请求的form要求有csrf_token，否则就会发生403错误，如下：

```
[18/Oct/2013 18:13:40] "POST /friendscare/ HTTP/1.1" 403 2294
```
但是这个POST请求是从微博页面发送过来的，不是由我们控制的，那解决方法就是在接收微博请求的view函数上禁止csrf，利用`@csrf_exempt`修饰符可以做到这一点，可以查看相关[文档](https://docs.djangoproject.com/en/dev/ref/contrib/csrf/)。

###X-Frame-Options问题
在解决了POST请求的CSRF问题之后，访问应用界面发现还是没有任何现实，打开Chrome开发者工具，发现Console中有错误：

![X-Frame-Options](/images/2013/10/19/xframe_options.png)
报错的意思直译就是无法在框架中现实`http://www.findingsea.com:8000/friendscare/`页面，因为该页面把`X-Frame-Options`的值设为了`SAMEORIGIN`，之前没有见过这类报错，参考不在水中的鱼
的博文[HTTP X-Frame-Options](http://jiandong.iteye.com/blog/1319517)得知：
>X-Frame-Options response header 可用于指示是否应该允许浏览器呈现在一个页面\<FRAME\>或\<IFRAME\>中. 以确保网站内容是不是嵌入到其它网站

而`X-Frame-Options`的值为`SAMEORIGIN`表示`页面只能显示在页面本网站的框架中`，所以我的应用页面就不能被包含在微博页面的iframe框架中了。而这个值是Django默认设置的，同样是出于安全性的考虑，如果要对一个特定视图允许被第三方页面包含，只要加上`@xframe_options_exempt`修饰符即可，可以查看[文档](https://docs.djangoproject.com/en/dev/ref/clickjacking/)。