title: 关于 C++ vector 的两个小 tips
date: 2019-05-02 16:34:28
tags: c++
---

本来这篇文章标题我想起成《关于 vector 的两个小坑》，后来想想，其实也不算是坑，还是自己对原理性的东西理解的没做那么透彻。工作中遇到的很多问题，后来归根到底都是基础不牢靠。

<!-- more -->

## vector 扩容

这个问题很经典了，但还是不小心踩到。有一个需求是要对目标元素进行复制，而目标元素集合是保存在 `vector` 里面，于是简单思考下就有如下代码（大致含义）：

``` cpp
void Duplidate(vector<Element>* element_list, Element* element) {
  element_list.push_back(*element);
}

void Process() {
  for (auto& package : package_list) {
    if (IsNeedDuplicate()) {
      Duplicate(element_list, package->element);
    }
  }
}
```

看起来好像没什么问题，就是当前的 `package` 对象是否满足复制的要求，需要的话，就对 `package` 的成员 `origin_element` 进行复制。跑 UT 也正常，然后在测试的时候就 coredump 了。看 core 文件就是挂在了复制的时候。这里我一开始就没明白，一个简单的复制为什么会有 coredump。

检查了很久 element 复制的场景，甚至想要专门写一个拷贝构造函数。最后才恍然大悟，`origin_element` 指针指向的就是 `element_list` 里面的元素，`element_list` 是整体流程的数据源，`packge` 对象是封装的中间处理对象。之前的开发人员为了方便，直接在 `package` 对象上保存了原始的 `element` 指针，而这个指针指向的是一个 vector 里的元素。而我新加的逻辑会往原始的 vector 里面再添加元素，那么就有可能导致 vector 扩容，而 vector 扩容会导致整体的复制，从而导致原来指向这些元素的指针都失效了，靠后的 `package` 对象再去访问 `origin_element` 就产生了 coredump。

当然，从设计上来说，就不应该保存指向 vector 元素的指针，但是这里有太多旧代码牵涉，这里就不做讨论。

## vector::erase()

起因是我在代码里面新增了如下代码（大致）：

``` cpp
void EraseElement(const vector<Element>::iterator& element_iter,
                vector<Element>& element_list) {
  while (element_iter != element_list.end()) {
    element_list.erase(element_iter);
  }
}
```

然后 cr 的同学提出了一个疑问是 `element_iter` 是 `const` 不可变的，但是在函数里有擦除了对应的元素，这里会不会有问题？虽然 UT 都已经跑过了，但是这种写法的确比较奇怪，于是就借机学习了一下 `vector::erase()` 的实现原理跟用法。

`erase(iterator)` 的实现原理其实不会改变 `iterator`，而是把后面的元素一个个往前移动，相当于是 `iterator` 指向的元素本身发生了变化，所以可以用 `const` 来修饰这个 `iterator`。但是这里用 `cosnt &` 其实是没有错但是无用的修饰，除了容易让人误判之外，其实没有什么实际用途。我之前是为了修正 cpplint 才把reference 改成 const reference。

另外 `erase` 本身的确比较危险，主要还是 `erase` 的时候 `iterator` 本身没发生变化，但是指向的元素变了，，在很多时候 `iterator` 会自然地指向下一个元素，但是由于这是未定义的行为，这里面可能会有不可预期的地方，所以最终改成显示的获取返回重新赋值（`erase()` 会返回下一个迭代器，但这一点常常被忽略），这样就能保证安全性了。更安全更推荐的做法应该是使用 `remove_if()` 这里就不展开讲了。

``` cpp
void EraseElement(vector<Element>& element_list,
                vector<Element>::iterator element_iter ) {
  while (element_iter != element_list.end()) {
    element_iter = element_list.erase(element_iter);
  }
}
```