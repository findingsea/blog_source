title: C++拷贝构造、移动构造与返回值优化
date: 2017-06-21 22:29:43
tags: C++
---

## 拷贝构造函数

拷贝构造函数（又称复制构造函数），是用来创建已存在对象的副本。对应的还有一个概念是拷贝赋值运算符，当需要显示地声明拷贝构造函数时，一般建议同时声明拷贝赋值运算符，以使得代码的含义明确。

<!-- more -->

如果不声明拷贝构造函数（或拷贝赋值运算符），编译器将会生一个默认的拷贝构造函数（或拷贝赋值运算符）（当被调用时生成）。参阅[声明构造函数的规则](https://msdn.microsoft.com/zh-cn/library/s16xw1a8.aspx)。

看一段典型的代码：

```
class TextFile {
public:
   TextFile() {};
   TextFile(const TextFile& tf) {
      cout << "copy" << endl;
   };
   TextFile& operator=(TextFile& tf) {
      cout << "operator=" << endl;
      return *this;
   };
};

int main() {

   vector<TextFile> text_files;
   text_files.push_back(TextFile());

   TextFile text_file_a;
   TextFile text_file_b;
   text_file_b = text_file_a;
}
```

输出如下：

```
copy
operator=
```

`TextFile`类显示地定义了拷贝构造函数与拷贝赋值运算符，分别在`text_files.push_back(TextFile());`和`text_file_b = text_file_a;`两处调用。

*需要注意的是，如果写成`TextFile text_file_b = text_file_a;`，那么被调用的将会是拷贝构造函数（也就是输出`copy`）。*

## 移动构造函数

上文的程序中，`text_files.push_back(TextFile());`该行构造了两个一模一样的`TextFile`对象，一次是在`TextFile`临时对象构造时，一次是向量在`push_back`时将临时对象又拷贝一份，而第二次构造明显是可以避免的。

因此，C++11中引入了`移动构造`的概念，与临时对象发生拷贝时不需要重新分配内存而是使用被拷贝对象的资源，即临时对象的资源。移动构造函数配合右值引用完成从临时对象数据转移到新的对象中，避免了数据拷贝。

```
class TextFile {
public:
	TextFile() {};
    
    // 移动构造函数
	TextFile(TextFile && tf) {
		cout << "move" << endl;
	};
};

int main() {

	vector<TextFile> text_files;
	text_files.push_back(TextFile());
}
```

输出：

```
move
```

可以看到，当再需要`push_back`时，调用的就是移动构造而不是拷贝构造函数了，其他情况同理，以此可以节省内存分配上的性能开支。

## 返回值优化

这一点是我在编写样例代码时遇到的问题，讲到拷贝构造函数时，常举的一个例子如下：

```
class TextFile {
public:
	TextFile() {};
	TextFile(const TextFile& tf) {
		cout << "copy" << endl;
	};
	TextFile& operator=(TextFile& tf) {
		cout << "operator=" << endl;
		return *this;
	};
};

TextFile get_tmp_text_file() {
	TextFile tf;
	return tf;
}

int main() {

	TextFile tf = get_tmp_text_file();
}
```

这是很经典的例子，很多文章都会讲`TextFile tf = get_tmp_text_file();`会调用两次拷贝构造函数，一次是`get_tmp_text_file`函数返回时，将函数返回拷贝到临时变量里，第二次是在`main`函数内构造`TextFile`对象时，将临时变量拷贝到`tf`对象上。所以，程序会输出两遍`copy`。

然而，如果你现在写了这么一个程序，真的跑一遍，它什么都不会输出。

不要怀疑自己，代码没错，教程也没错，这是因为G++的[返回值优化](https://zh.wikipedia.org/wiki/%E8%BF%94%E5%9B%9E%E5%80%BC%E4%BC%98%E5%8C%96)。

> 当一个函数返回一个对象实例，一个临时对象将被创建并通过复制构造函数把目标对象复制给这个临时对象。C++标准允许省略这些复制构造函数，即使这导致程序的不同行为，即使编译器把两个对象视作同一个具有副作用。

这是C++标准允许编译器独立实现的优化。被称为返回值优化（RVO/NRVO）。

*关于RVO/NRVO历史可以参见维基百科[Return value optimization](https://en.wikipedia.org/wiki/Return_value_optimization)词条*

G++编译时，会默认对代码进行返回值优化，优化后的等价代码如下：

```
TextFile get_tmp_text_file(TextFile * tf) {
	// 直接在tf上构造
}

int main() {
    TextFile tf;
	get_tmp_text_file(&tf);
}
```

因此就不需要再调用`TextFile`对象的拷贝构造函数。

要关闭这种优化，只要在编译时加上`-fno-elide-constructors`强制G++总是使用拷贝构造函数。

```
g++ 2DimensionArray.cpp -o run -fno-elide-constructors && ./run
```

输出：

```
copy
copy
```