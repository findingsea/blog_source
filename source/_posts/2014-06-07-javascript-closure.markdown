---
layout: post
title: "JavaScript闭包和this绑定"
date: 2014-06-07 11:22
comments: true
tags: JavaScript
---
本文最主要讲讲JavaScript闭包和this绑定相关的我的小发现，鉴于这方面的基础知识已经有很多很好的文章讲过了，所以基本的就不讲了，推荐看看[酷壳](http://coolshell.cn/)上的[理解Javascript的闭包](http://coolshell.cn/articles/6731.html)和[阮一峰](http://www.ruanyifeng.com/blog/)的[学习Javascript闭包（Closure）](http://www.ruanyifeng.com/blog/2009/08/learning_javascript_closures.html)，写的都非常好。

<!-- more -->

首先来讲讲阮一峰的文章中的两道思考题。

**代码片段一**

```js
var name = "The Window";
var object = {
    name : "My Object",
    getNameFunc : function(){
        return function(){
            return this.name;
        };
    }
};
alert(object.getNameFunc()());
```

这段代码最后输出的是

```
The Window
```

原因在同一片文章的评论中已经有人指出了

> George Wing 说：
> 
> 上面本人说得不太正确。
this的指向是由它所在函数调用的上下文决定的，而不是由它所在函数定义的上下文决定的。

对于最后返回的这个匿名函数

```js
function(){
    return this.name;
};
```

它是作为一个独立的函数返回的，它的调用域是在全局上，所以会输出全局变量name。

**代码片段二**

```js
var name = "The Window";
var object = {
    name : "My Object",
    getNameFunc : function(){
        var that = this;
        return function(){
            return that.name;
        };
    }
};
alert(object.getNameFunc()());
```

代码片段二最后输出的是

```
My Object
```

这里就要考虑`var that = this;`这句的作用了，由于`getNameFunc`是`object`内部的函数，所以它调用的上下文`this`保存的是`object`的信息，将其保存到`that`变量，这样作为内部函数的匿名函数就可以直接访问了。

可以注意到的是，阮一峰文章中的代码，都是将通过一个JSON对象来访问内部的函数，这样其实有些地方还不够清晰，毕竟不怎么严格地说，闭包就是函数内部的函数，所以我借用CoolShell上的文章中的例子来进一步说明。

**代码片段三**

```js
function greeting(name) {
    var text = 'Hello ' + name; // local variable
    // 每次调用时，产生闭包，并返回内部函数对象给调用者
    return function() { alert(text); }
}
var sayHello=greeting("Closure");
sayHello()  // 通过闭包访问到了局部变量text
```

这段代码输出

```
Hello Closure
```

看上去好像很好理解，接下来看代码片段四：

**代码片段四**

```js
var text = 'findingsea';
function greeting(name) {
    var text = 'Hello ' + name; // local variable
    // 每次调用时，产生闭包，并返回内部函数对象给调用者
    return function() { alert(this.text); }
}
var sayHello=greeting("Closure");
sayHello()  // 通过闭包访问到了局部变量text
```

这段代码输出

```
findingsea
```

这是为什么呢？

针对代码片段三，CoolShell上的原文有解释：

>文法环境中用于解析函数执行过程使用到的变量标识符。我们可以将文法环境想象成一个对象，该对象包含了两个重要组件，环境记录(Enviroment Recode)，和外部引用(指针)。环境记录包含包含了函数内部声明的局部变量和参数变量，外部引用指向了外部函数对象的上下文执行场景。全局的上下文场景中此引用值为NULL。这样的数据结构就构成了一个单向的链表，每个引用都指向外层的上下文场景。

![closure](http://findingsea-blog-images.qiniudn.com/closure.png)
	
针对代码片段四，就是我们之前讲过的，`this`保存是调用环境下的上下文内容，所以会输出全局的`text`。

####总结
本文想说明的是以下两点：

1. 在函数闭包中，不使用`this`对变量进行访问时，函数会通过文法环境中的外部引用（指针），一级级地往上找（单向链表），直到找到（或者最终找不到）对应的变量。这个结构是在函数定义的时候就决定了的。
2. 在函数闭包中，使用`this`对变量进行访问时，和绝大多数语言不同，JavaScript的`this`保存的是调用环境的上下文，也就是说`this`中的内容是在调用的时候决定的，所以访问到的是当前环境下的对应变量，并不会像前一种情况一样进行逐级查找。