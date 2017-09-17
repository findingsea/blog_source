---
layout: post
title: "面试查漏补缺——阿里"
date: 2015-03-17 10:05
comments: true
tags: Interview
---
# 阿里电话面试

面试时间：2015-03-16

<!-- more -->

### Java StringBuffer和StringBuilder的区别的问题。

[String,StringBuffer与StringBuilder的区别??](http://blog.csdn.net/rmn190/article/details/1492013)

[StringBuilder and StringBuffer](http://stackoverflow.com/questions/355089/stringbuilder-and-stringbuffer)

简单来说：StringBuilder的效率更高；StringBuffer是线程安全的，而StringBuilder不是线程安全的。

### 快排性能

* 平均时间：O(nlogn)
* 最差情况：O(n ^ 2)
* 稳定度：不稳定
* 额外空间：O(logn)或者O(n)

解释为什么最坏情况是O(n ^ 2)：考虑类似`5 4 3 2 1`的输入，那么每个数都会被选为基准，因此每个数都会和其他数进行比较，所以比较的次数就是n ^ 2。

### 查看Linux负载情况

top命令

### Thread vs Runnable

[Thread和Runnable的区别](http://blog.csdn.net/michellehsiao/article/details/7639788)

Thread是类，Runnable是接口。在实际使用中，更多地使用Runnable，因为接口的性质，值得实现接口可以给类提供更多的灵活性。

### TCP vs UDP

* TCP：传输控制协议，面向链接，可靠，提供了超时重发、丢弃重复数据、检验数据、流量控制等，保证数据从一端传到另一端。
* UDP：用户数据报协议，面向数据包，不可靠，只管发送，不保证送达，也没有超时重传机制，故而速度很快。


### 创建索引

create index index_name on table_name


***2015-03-18 Upate***


阿里视频面试

### 堆和栈的区别

[堆和栈的区别（转过无数次的文章）](http://blog.csdn.net/hairetz/article/details/4141043)

简单来讲，形如`int a = 1`的基本类型，都分配在栈上，且栈上的对象可以共享；形如`Object obj = new Object()`的对象，都分配在堆上，不可共享。

栈的速度要比堆快，在C++中，分配在栈上的空间由系统回收，分配在堆上的空间由程序员回收，也就是`del`。但是由于Java有JVM的存在，所以基本不用自己回收任何资源。

### TCP/IP协议断开时需要几次

[图解TCP-IP协议](http://www.cricode.com/3568.html)

[TCP\IP三次握手连接，四次握手断开分析](http://www.cnblogs.com/kesal/p/3285415.html)

简单形容的话，建立连接时的三次握手：

1. 客户端 —> 服务器，客户端请求连接
2. 服务器 —> 客户端，服务器确认连接信息
3. 客户端 —> 服务器，客户端确认连接信息，开始连接

断开连接时的四次握手：

1. A —> B，A请求断开连接
2. B —> A，B确认请求并准备断开连接
3. B —> A，B关闭连接并通知A
4. A —> B，A确认关闭