---
layout: post
title: "Python生成器"
date: 2013-09-20 13:48
comments: true
tags: [Python]
---

生成器可以说是Python和其他语言较为不同的地方，刚开始看到[《Python基础教程》](http://book.douban.com/subject/4866934/)里的Python生成器内容时，还是很不适应，因为以前学过的语言都没有这种特性，所以理解不能，好在经过反复阅读书上的内容和自己编写代码测试之后，终于感觉理解到点上了，这里写篇Blog用来备忘。

<!-- more -->

## 生成器基本概念
从概念上来说，生成器就是用普通方法定义的迭代器，或者更直观点的讲法就是任何包含yield语句的函数都是一个生成器。看一个简单生成器的代码1：

``` python
def repeater():
	for i in range(10):
		yield 1
print list(repeater())
```

输出如下：

	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	
这个生成器生成了一组长度为10，每个元素都为1的数据，我们最后将其转换成列表形式进行输出。

在这个例子中，如果用print来代替yield我们也能得到『相似』的输出。但是yield的一个显著特征就是它不是返回任何值，而是产生值，代码1中，就是每次循环产生一个1。而当函数执行完之后，并不返回值，也不返回None（这一点很重要，如果只是简单地把yield当成print的一种变形就很容易犯这个错误），而是返回一个生成器，如果我们直接输出代码1中的repeater()函数：

``` python
print repeater()
```
	
将会得到：

	<generator object repeater at 0x101a4e410>
	
就像上面所说的，生成器并不直接返回值，而是返回一个根据你的函数定义的生成器，当用类似list(generator)方法调用的时候，就可以根据相应的数据结构生成数据。

再来看一个较为复杂的生成器代码2：

``` python
def flatten(nested):
	try:
		for sublist in nested:
			for element in flatten(sublist):
				yield element
	except TypeError:
		yield nested

print list(flatten([[0,1,2],3,4,[[5,6]],7]))
```

代码2的输出为：

	[0, 1, 2, 3, 4, 5, 6, 7]
	
代码2的作用就是将一棵树进行展开，采用了递归的思想，它的工作原理就是，如果当前的对象还是可以展开的，那就继续展开，如果无法展开（Python中int是无法展开的），就会抛出TypeError这个异常，而且这个引发TypeError的值就是我们希望得到的值，所以捕获这个异常后生成值。

代码2同样来自《Python基础教程》，如果要深究起运行过程，则先需要理解生成器是可迭代的，是可以为作为for循环的展开对象的。并且，yield每次产生一个值，都会将函数冻结，下次则再从该冻结的点继续执行。拿第一个元素0举例来说明代码2的运行过程（以下为我根据测试程序结果推断的）：

1. 第一层，运行flatten([[0,1,2],3,4,[[5,6]],7])，展开后sublist为[0,1,2]，进入第二层
2. 第二层，运行flatten([0,1,2])，展开后sublist为0，进入第三层
3. 第三层，运行flatten(0)，代码试图对0进行展开，Python抛出TypeError，由代码捕获到，生成数据0，并返回生成器
4. 返回第二层，对生成器进行迭代（含数据0），生成数据0，函数冻结，并返回生成器
5. 返回第一层，对生成器进行迭代（含数据0），生成数据0，函数回到第二层的冻结点继续执行。

## next()方法
next()方法的示例代码如下：

``` python
	def repeater():
		while True:
			yield 1
	r = repeater()
	print r.next()
```
	
以上代码会输出1，而且如果你继续调用r.next()，就会继续输出1。next()其实就是迭代器，读取生成器生成的下一个值，这里可以看出生成器相较于列表更有优势的一点就是：列表总是先将数据生成并储存起来，当需要用的时候就去读取，而生成器都是当需要使用的时候才生成数据，这一点在处理大数据量甚至是无限生成的数据时尤其有用。

next()方法还需要注意的一点是，对于yield n语句，next()返回的是n的值，而yield n本身的返回值为None，这一点在send()方法中还会再一次被提到。

## send(value)方法
send()方法允许外界向生成器内部传递数据，当调用send()方法时，内部将会挂起生成器，yield作为表达式而非语句使用，yield n将会有一个返回值，该值就是外界通过send()方法传递进来的值。send()方法的示例代码如下：
	
``` python
	# When you call next(), n is ever None. When you call send(num), yield is hold up,
	# so (yield value) return num
	def repeater(value):
	while True:
		n = (yield value)	
		if n is not None:
			value = n

	r = repeater(11)
	print r.next()
	r.send(10)
	print r.next()
```

输出为：

	11
	10
	
可以看到在生成器初始化完后，调用next()得到的值是我们初始化时传递进去的11，而当调用send()方法向生成器传了一个值10之后，在调用next()方法，得到就是后传进去的值10了。

send()方法需要注意的有两点：

1. 通过send()方法传入生成器的值，由n = (yield value)的形式被生成器内部接收，n即为传进来的参数的值。而如果未调用send()方法，n的值为None。
2. send()方法不能在生成器刚初始化完成的时候调用，也就说必须要等到yield函数至少执行1次之后，才能调用send()方法，这是因为send()会在内部使生成器挂起，所以必须要求yield已经执行过，如果去掉上述代码中的第一个r.next()，则会得到错误：`TypeError: can't send non-None value to a just-started generator`。如果一定要在刚刚启动的生成器使用send()方法，可以采用send(None)来解决。
	
	
