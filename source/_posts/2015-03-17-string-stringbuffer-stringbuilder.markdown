---
layout: post
title: "String, StringBuffer和StringBuilder"
date: 2015-03-17 14:59
comments: true
tags: Java
---
在Java中，String是不可变类型，所以对于字符串的操作提供了两个辅助类：StringBuffer和StringBuilder。

<!-- more -->

这个两个类的主要区别在于：

* StringBuilder的效率更高
* StringBuffer是线程安全的，而StringBuilder不是

不过，需要注意的是，在利用`+`对String对象直接进行拼接的时候，Java内部其实还是用StringBuilder来实现的，但是和显式地调用StringBuilder略有区别。

考虑如下代码：

``` java
String[] strings = new String[]{"one", "two", "three", "four", "five"};
String resultStr = "";
StringBuilder resultBuilder = new StringBuilder();
for (int i = 0; i < strings.length; i++) {
    resultStr += strings[i];
}
for (int i = 0; i < strings.length; i++) {
    resultBuilder.append(strings[i]);
}
```

在利用`+`直接进行拼接时，每次循环都会生成一个新的StringBuilder对象，也就是说等同：

``` java
StringBuilder stringBuilder = new StringBuilder(resultStr);
stringBuilder.append(strings[i]);
resultStr = stringBuilder.toString();
```

这样运行的效率明显是低于显式调用StringBuilder的。

但是在有一种情况下，利用`+`拼接的速度会远远快于用StringBuilder或者StringBuffer，考虑如下代码：

``` java
String str = "one" + "two" + "three";
StringBuilder strBuilder = new StringBuilder().append("one").append("two").append("three");
```

在这种情况下，JVM会直接把`String str = "one" + "two" + "three";`理解为`String str = "onetwothree”;`，也就说不需要像通常情况下生成StringBuilder对象然后再拼接，速度自然快很多。不过需要强调的一点是，当然字符串来自其他对象的时候，JVM不会做这种特殊处理，也就说如下代码：

``` java
String one = "one";
String two = "two";
String three = "three";
String str = one + two + three;
```

效率仍然是非常低的。