---
layout: post
title: "项目总结：PHP在线词典"
date: 2014-04-03 14:12
comments: true
tags: 项目总结
---

前段时间接了小项目，用PHP做一个在线词典。大概花了两个星期不到的时候做完，整理一份项目总结，方便以后回看。

<!-- more -->

##需求
整个在线词典算个Web应用吧，包含两类使用者：用户和管理员。用户需要查单词、整句翻译、背单词三大功能模块，具体如下：

- 查单词
	- 如果用户所查询的单词数据库里有，就直接从数据库中读取
	- 如果用户所查询的单词数据库里没有，就从网上爬，然后把爬回来的数据存进数据库
	- 用户查询查询过的单词，可以选择将其加入生词本
- 整句翻译
	- 采用谷歌翻译API
	- 提供中翻英、英翻中两种模式
- 背单词
	- 背诵的单词主要来自用户添加到生词本的单词
	- 对当前正在背诵的单词，提供提示功能

管理员需要添加单词、例句，查看所有用户两个功能模块。

##语言和工具
采用的服务端语言是PHP，工具用了PHPStorm，因为PHPStorm很好的继承了WebStorm在编写Web应用方面的超强性能，对PHP的支持也十分到位，是个非常彪悍的IDE。

前端框架用的是Bootstrap+Flat UI，以前用过比较顺手。

服务端持久化框架用的是Medoo，这个第一次用，功能很强大，编写也很方便，最主要是整个框架也才几K，非常轻量级。

数据库用的是MySQL。

##项目笔记
####jQuery插件
用Bootstrap的alert样式写了个jQuery插件，简单实现在用户操作之后，在页面中部顶端slideDown出现提示框，停留一秒钟再slideUp消失。这里主要是用到jQuery DOM操作和CSS绝对居中的技术。不过这个提示框到现在也不是很完美，因为没有办法根据提示内容自适应调整提示框宽度，由于我对CSS只是半吊子，所以基本也都是在网站找代码，为了快点完成项目也就没有在这个问题上继续纠结下去了。

jQuery代码：
``` javascript
(function($) {
    $.alert = function(type, text) {
        var info_alert = $('<div id="info-alert" class="alert absolute-center"></div>');
        switch (type) {
            case 'success':
                info_alert.addClass('alert-success');
                break;
            case 'info':
                info_alert.addClass('alert-info');
                break;
            case 'warning':
                info_alert.addClass('alert-warning');
                break;
            case 'danger':
                info_alert.addClass('alert-danger');
                break;
            default :
                info_alert.addClass('alert-info');
        }
        info_alert.text(text);
        info_alert.prependTo('body');
        info_alert.slideDown('slow');
        setTimeout(function() {
            info_alert.slideUp('slow', function() {
                $(this).remove();
            });
        }, 1000);
    };
})(jQuery);
```
`absolute-center`类代码：
``` css
.absolute-center {
    position: absolute;
    margin-left: auto;
    margin-right: auto;
    min-width:40px;
    max-width:400px;
    left: 0;
    right: 0;
    text-align: center;
    overflow: auto;
}
```

####Cookie操作
Cookie操作应该是写任何Web应用都避不开的，这次写的时候我就很后悔以前为什么没有整理出一套Cookie操作的代码方便以后重用。这次主要写了`setCookie`、`getCookie`、`delCookie`三个基本操作。虽然说Cookie的操作有很现成的jQuery插件，但是我觉得这种基本的和原理性的东西还是要自己多写写，频繁使用各种插件的结果往往是没了插件之后连最简单的东西也写不出来，毕竟面试笔试的时候你不能就告诉考官我知道有个插件能实现这个功能，具体怎么写我不清楚。
``` javascript
function setCookie(info, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    for (key in info) {
        document.cookie = key + '=' + info[key]
            + ((expiredays==null) ? "" : ";expires=" + exdate.toGMTString());
    }
}

function getCookie(key) {
    if (document.cookie.length>0) {
        var start = document.cookie.indexOf(key + "=");
        if (start != -1) {
            start = start + key.length + 1;
            var end = document.cookie.indexOf(";",start);
            if (end == -1)
                end = document.cookie.length;
            return document.cookie.substring(start,end);
        }
    }
    return '';
}

function delCookie() {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() - 1);
    var username = getCookie('username'),
        password = getCookie('password');
    if (username && password) {
        document.cookie = 'username=;expires=Thu, 01-Jan-70 00:00:01 GMT';
        document.cookie = 'password=;expires=Thu, 01-Jan-70 00:00:01 GMT';
    }
}
```

####32位随机ID生成
数据库数据32位ID的随机生成函数：

```php
<?php
function Random_string($len = 32) {
    return substr(md5(time()), rand(1,( 32 - $len)), $len);
}
```

 
  
  
  
   
   
   
   
 
     
      
##问题和遗憾
####项目管理和代码管理
这一直是我心中的痛呀，每次做项目之前总是想这次一定定要好好地注重模块化、注重代码重用等等，刚开始的时候还能坚持一下，到后面项目快要完结的时候就开始撒欢地写了。虽然这次项目的管理已经比以前好多了，不过我还是有很多不满意的地方，不过也只能在下次项目里再改进了。

####面向对象
因为刚开始用PHP的时候，就当成脚本语言一直这样写，所以没有太注重PHP的面向对象式编程。本来这次是想在这方面下点功夫的，可惜最后还是为了赶进度没有研究地太深。感觉面向对象这点一直是我的软肋，是应该有个时间好好学习梳理下。

####随时总结
项目中总是会遇到很多问题，也解决很多问题，这次项目也不例外。但是很多时候我都在纠结先继续写代码呢，还是先停一停总结当前的问题和解决方法，可惜的是大多数时候我都选择了前者，所以导致了这次项目做的过程中我其实有很多收获，但是现在真的要我一下子全都写下来我又觉得没太多可写的。











