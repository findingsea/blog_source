---
layout: post
title: "利用Octopress在Github上搭建博客及后续问题总汇"
date: 2013-09-20 15:03
comments: true
tags: [Octopress, GitHub]
---
用Octopress在GitHub上搭建博客已经不是什么新鲜事了，网上的教程也多了去了，大题的方法什么都差不多，这篇Blog就把这些资源总汇一下，然后再加几点我遇到的问题和解决办法。

<!-- more -->

## 搭建和配置
搭建的大致过程大概包括：安装Ruby --> 安装Octopress --> 配置Octopress --> 部署到GitHub上 --> 提交博客。我主要参考的是[破船](http://beyondvincent.com/)的这篇教程——[《利用Octopress搭建一个Github博客》](http://beyondvincent.com/blog/2013/08/03/108-creating-a-github-blog-using-octopress/)。一路按教程走下来大问题应该不会有，但是小问题可能就不断了，这待会会讲到。

其他比较推荐的教程还有，[唐巧](http://blog.devtang.com/)的这篇[《象写程序一样写博客：搭建基于github的博客》](http://blog.devtang.com/blog/2012/02/10/setup-blog-based-on-github/)(好吧，他还把『像』写错了)。这里面还提到了一些提高访问速度的技巧和介绍了一个支持微博评论的工具，都挺有用的。

另外，还有这篇[《Octopress - 像黑客一样写博客》](http://williamherry.com/blog/2012/07/20/octopress-setup/)，介绍地非常详细，并介绍了很多个性化配置的技巧，其中对CSS的修改我觉得非常值得学习和借鉴。

//--- 2013-09-21 update ---//

以及这篇[《Octopress博客问题解决方案与技巧》](http://agiledon.github.io/blog/2012/12/25/octopress-issues-solution-and-tips/)，里面汇总了很多Octopress的设置技巧，在首页输出摘要的设置方法和zsh报错的原因（下面会提到），我都是从这篇文章里面找到。

## 遇到的问题
### 安装失败问题

在运行下面这些语句的时候，终端直接就没反应了，然后过很久报error，据说是访问的地址可能被墙了，但是我在浏览器里访问http://rubygems.org/这个地址是可以的，所以就很纠结，当时就卡在这里下不去，最后无奈就多试了几次，结果就好了。你只能服了天朝的网络了。（从目前情况来看，应该识没有被墙，如果报类似could not download这种错误，只能多试几次，也没别的办法了）

```
gem install bundler
rbenv rehash    # If you use rbenv, rehash to be able to run the bundle command
bundle install
```

### 引号问题
根据[唐巧的教程](http://beyondvincent.com/blog/2013/08/03/108-creating-a-github-blog-using-octopress/)，新建文章的指令应该是：

```
rake new_post["title"]
```
然后在相应的markdown文件中头部自动生成的信息中会有：

```
title: "title"
```
当时当我按照这个指令去执行的执行的时候，终端报错：

```
zsh: no matches found: new_post[title]
```
我在网上找到的解决办法是将指令改成：

```
rake 'new_post["title"]'
```
这样创建新文章是成功了，但是立马引发了另一个问题。生成好文章之后，执行`rake generate`指令，终端报错：

```
/Users/findingsea/.rvm/rubies/ruby-1.9.3-p448/lib/ruby/1.9.1/psych.rb:203:in `parse': (<unknown>): did not find expected key while parsing a block mapping at line 2 column 1 (Psych::SyntaxError)
	from /Users/findingsea/.rvm/rubies/ruby-1.9.3-p448/lib/ruby/1.9.1/psych.rb:203:in `parse_stream'
	from /Users/findingsea/.rvm/rubies/ruby-1.9.3-p448/lib/ruby/1.9.1/psych.rb:151:in `parse'
	from /Users/findingsea/.rvm/rubies/ruby-1.9.3-p448/lib/ruby/1.9.1/psych.rb:127:in `load'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/gems/jekyll-0.11.2/lib/jekyll/convertible.rb:33:in `read_yaml'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/gems/jekyll-0.11.2/lib/jekyll/post.rb:39:in `initialize'
	from /Users/findingsea/Workspace/Github/octopress/plugins/preview_unpublished.rb:23:in `new'
	from /Users/findingsea/Workspace/Github/octopress/plugins/preview_unpublished.rb:23:in `block in read_posts'
	from /Users/findingsea/Workspace/Github/octopress/plugins/preview_unpublished.rb:21:in `each'
	from /Users/findingsea/Workspace/Github/octopress/plugins/preview_unpublished.rb:21:in `read_posts'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/gems/jekyll-0.11.2/lib/jekyll/site.rb:128:in `read_directories'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/gems/jekyll-0.11.2/lib/jekyll/site.rb:98:in `read'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/gems/jekyll-0.11.2/lib/jekyll/site.rb:38:in `process'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/gems/jekyll-0.11.2/bin/jekyll:250:in `<top (required)>'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/bin/jekyll:23:in `load'
	from /Users/findingsea/.rvm/gems/ruby-1.9.3-p448/bin/jekyll:23:in `<main>'
```
当时差点没吓死，以为怎么了，把关键错误描述上网搜了下，找到了这篇[《Linked List Posts: From Movable Type to Octopress》](http://www.nealsheeran.com/archives/2012/09/linked-list-posts-mt-to-octopress/)这个老兄（暂且认为是男的吧）和我遇到了一样的错误，他新建的markdown文件里title的内容里，出现双引号嵌套双引号，这违反了markdown的语法规则，所以解析出错了。我立马查看了我新建的问题，果然如此：

```
title: ""title""
```
着就相当于中间的title不包含在任何引号中，所以生成的时候会报错。最后我把指令改成如下所示，就一切正常了。

```
rake 'new_post[title]'
```
至于原因现在还不是很清楚，我怀疑很有可能是shell造成的，我用的zsh，而教程上一般用bash的比较多。

//--- 2013-09-21 update ---//

上面提到的问题已在[《Octopress博客问题解决方案与技巧》](http://agiledon.github.io/blog/2012/12/25/octopress-issues-solution-and-tips/)中找打，的确是shell引起的问题，用zsh的同学可以借鉴下。

## 字体问题
由于对字体方面有洁癖，所以在这上面耗费了很久，看了很多博客采用的字体方案，其中[Aiur](http://blog.yxwang.me/)最让我喜欢，尤其是正文的英文字体，所以我立马留言向博主询问他采用的是哪种字体，最后得知是Google的开源字体Open Sans。

Octopress字体的设置文件是：sass/custom/\_fonts.scss，其中`$heading-font-family`定义的是文章标题的字体，`$header-title-font-family`定义的是博客标题的字体，`$header-subtitle-font-family`定义的是博客子标题的字体，`$sans`和`$serif`定义的是正文的字体，`$mono`定义的是代码的字体。这里需要注意的是，/sass/custom/\_style.scss里定义的样式会覆盖其他地方定义的样式，但唯独\_font.scss里的这几个值不会被覆盖，也就说如果你在\_fonts.scss里已经定义了`$mono`的值，还想在\_style.scss中修改`<code></code>`的字体样式是不行的，最后渲染出的结果还是`$mono`的字体。（一开始我不知道这一点，在\_style.scss里折腾了好久）。

特别说明的是我对编程字体尤其在意，我最喜欢的是Adobe的开源字体Source Code Pro，而且是跨平台的，不过这在很多机器上不一定有装，而且貌似GoogleFonts没有收录这个字体，所以我依次补充了Mac上最适宜的编程字体Monaco，Windows上最适宜的编程字体Consolas，和Ubuntu上最适宜的编程字体Ubuntu Mono，这里的设置是依次序寻找到第一个可以使用的字体。（也就说浏览器会先寻找本机是否装有Source Code Pro，如果没有就寻找下一个Monaco，以此类推，直到找到一个可用的字体进行渲染，另外，我所选的三款字体都是三个平台默认安装的，这样可以最大程度地保证代码阅读质量）

下面是我的\_fonts.scss文件中的定义：

```
$sans: Open Sans;
$serif: Open Sans;
$mono: Soure Code Pro, Monaco, Consolas, Ubuntu Mono;
$heading-font-family: "PT Serif",Georgia,"STHeiti","SimHei","Helvetica Neue",Arial,sans-serif;
$header-title-font-family: "Futura", sans-serif;
$header-subtitle-font-family: "Futura", sans-serif;
```

最后说一点，在上文中提到的唐巧的[《象写程序一样写博客：搭建基于github的博客》](http://blog.devtang.com/blog/2012/02/10/setup-blog-based-on-github/)中，他提到了一个优化博客load速度的方法是：删除/source/\_includes/custom/head.html文件中的谷歌字体，因为GFW的关系，这部分载入会特别慢。但这会引发一个问题就是你无法使用PT Serif和Open Sans这些优质的谷歌字体了，解决方法是可以讲他们下载到本地，然后在/sass/custom/_style.scss中添加：

``` css
@font-face {
	font-family: Open Sans;
	src: url(fonts/OpenSans-Regular.ttf)
}
```
不过这种方法的弊端在于需要把你用到的每个本地可能没有安装的字体都下载下来，我嫌太麻烦，就没有按这种方法，而且英文字体库不像中文字体库动辄上M，基本都维持在K这个级别，速度慢了这么一点还是可以忍受的。