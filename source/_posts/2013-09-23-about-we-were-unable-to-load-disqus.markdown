---
layout: post
title: "可能引起「We were unable to load Disqus」错误的一种情况分析"
date: 2013-09-23 14:06
comments: true
tags: [Octopress]
---
今天想往Octopress里加评论，之前看了网上的教程，应该是简单的事情，因为Octopress本来为你准备好了评论插件Disqus的代码，只需要去Disqus注册个帐号，然后在\_config.yml里面打开配置就行了，没想到这么简单的事情却被之前埋的的一个坑给坑惨了。

<!-- more -->

之前在[《利用Octopress在Github上搭建博客及后续问题总汇》](http://findingsea.github.io/blog/2013/09/20/li-yong-octopresszai-githubshang-da-jian-bo-ke-ji-hou-xu-wen-ti-zong-hui/)这篇文章提到过，我利用Octopress建站主要参考的教程就是破船的[《利用Octopress搭建一个Github博客》](http://beyondvincent.com/blog/2013/08/03/108-creating-a-github-blog-using-octopress/)，其中对于\_config.yml的设置提到过：

>config.yml是博客重要的一个配置文件，在config.yml文件中有三大配置项：Main Configs、Jekyll & Plugins和3rd Party Settings。

>一般，该文件中其中url是必须要填写的，这里的url是在github上创建的一个仓库地址，具体请看第四步中创建的地址。另外再修改一下title、subtitle和author，根据需求，在开启一些第三方组件服务。

而其中的坑就在于文章说\_config.yml中的url需要配置成GitHub上的仓库地址，当时根据这种说法，我配置的url为：

```
url: https://github.com/findingsea/findingsea.github.com.git
```

当时启动部署一切都正常，我也根本没想到这样配置其实是错误的。要知道为什么这样配置是错误的，就要先讲讲Disqus。一般情况下，Disqus想要引入正常，就要保证/source/\_includes/disqus.html文件中的`disqus_url`和\_config.yml文件中的`disqus_short_name`这两个值的正确。`disqus_url`是Disqus需要嵌入评论插件的地址，`disqus_short_name`是Disqus对你的站点的标识。`disqus_short_name`是自己手动设置的，而且是在要启动Disqus插件的时候才设置的，一般不会出错，而`disqus_url`的值是Octopress读取你的配置文件自动生成的，这里如果发生错误是很难发现的。而我们看`disqus_url`的定义：

```
var disqus_url = '{{ site.url }}{{ page.url }}';
```
很明显，`disqus_url`的值由\_config.yml配置文件中的`url`和当前页面的路径决定。我在/source/\_includes/disqus.html中将`disqus_url`的值进行输出，发现在上述配置方法下，`disqus_url`的值为：

```
https://github.com/findingsea/findingsea.github.com.git/blog/2013/09/23/about-we-were-unable-to-load-disqus/
```
也就是说现在变成了我们要求Disqus在GitHub仓库子页面下插入评论插件，这不是作死是什么！

所以正确的设置方法，应该是在\_config.yml中将`url`设置为你站点的地址，对应我就应该是`http://findingsea.github.io`。[Octopress官网的配置说明页面](http://octopress.org/docs/configuring/)也对url的值进行了描述：

![_config.yml](/images/2013/10/19/QQ20131019-1@2x.png)

最值得信赖的还是官方的文档，老是看网上的教程就难免踩到坑。