title: C++ 结构体操作符重载
date: 2019-07-05 11:38:07
tags: c++
---

同事在工作中与到的一个问题，组装资源的时候，往`std::set`里插入自定义结构体失败，导致使用时查找失败。几个人一起排查了一下，最后发现是对自定义结构`operator<`操作符进行重载时有歧义，导致了线上问题。

<!-- more -->

## 错误示例

``` c++
class Range {
public:
  int min;
  int max;

  // 错误示例：a.min=b.min，那么a<(b)的判断为false，b<(a)的判断为false，就会判断a=b，无法插入
  bool operator<(Range const& b) const {
    if (min == b.min && max == b.max) {
      return false;
    } else {
      return min < b.min;
    }
  }
  Range(int min, int max) {
    this->min = min;
    this->max = max;
  }
};
```

`std::set`是去重的，那么如何判断两个元素是否相同？这就依赖`operator<`，对于`a`、`b`两个元素，分别调用`a<b`以及`b<a`，如果两个都返回`false`，那么就判断`a=b`。这种判断机制，也是造成如上定义会出现问题的关键。

执行代码：

``` c++
int main() {
  set<Range> range_set;
  Range r1(1, 2);
  Range r2(1, 2);
  Range r3(1, 1);
  range_set.insert(r1);
  range_set.insert(r2);
  range_set.insert(r3);  
  for (auto &r : range_set) {
    cout << "[" << r.min << ", " << r.max << "]" << endl;
  }
}
```

输出：
```
[1, 2]
```

可以看到`r1`和`r2`的确是相同的，只能插入其中一个，这个符合预期；`r1`和`r3`是两个不同的区间，但是`r3`的插入失败了。这里就是由于在`Range`中定义的`operator<`仅仅对区间的左边界进行来判断。`return min < b.min;`这个判断，对于`a<b`和`b<a`都是返回`false`，此时程序就会认为`a`和`b`是相等的，导致其中一个插入失败。

单独比较一下`r1`跟`r3`：
```
cout << "r1 < r3: " << (r1 < r3) << endl;  // 0
cout << "r3 < r1: " << (r3 < r1) << endl;  // 0
```

可以发现两次判断都是`false`，这样就会被`set`判断为是相等的两个元素。

## 正确示例

``` c++
class Range {
public:
  int min;
  int max;

  bool operator<(Range const& b) const {
    if (min == b.min && max == b.max) {
      return false;
    } else if (min < b.min) {
      return true;
    } else if (min == b.min) {
      return max < b.max;
    } else {
      return false;
    }
  }
  Range(int min, int max) {
    this->min = min;
    this->max = max;
  }
};
```

执行代码：
``` c++
int main() {
  set<Range> range_set;
  Range r1(1, 2);
  Range r2(1, 2);
  Range r3(1, 1);
  range_set.insert(r1);
  range_set.insert(r2);
  range_set.insert(r3);  
  for (auto &r : range_set) {
    cout << "[" << r.min << ", " << r.max << "]" << endl;
  }
}
```

输出：
```
[1, 2]
[1, 1]
```

输出符合预期。

这个问题其实在UT阶段就应该被发现，这里还是因为项目上线比较紧，而导致很多质量把控环节都疏忽了。