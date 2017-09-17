---
layout: post
title: "Java 用自定义类型作为HashMap的键"
date: 2015-04-07 17:53
comments: true
tags: Java
---
这是Java中很经典的问题，在面试中也经常被问起。其实很多书或者文章都提到过要重载`hashCode()`和`equals()`两个方法才能实现自定义键在`HashMap`中的查找，但是为什么要这样以及如果不这样做会产生什么后果，好像很少有文章讲到，所以写这么一篇来说明下。

<!-- more -->

首先，如果我们直接用以下的`Person`类作为键，存入`HashMap`中，会发生发生什么情况呢？

``` java
public class Person {

    private String id;

    public Person(String id) {
        this.id = id;
    }
}
```

``` java
import java.util.HashMap;

public class Main {
    public static void main(String[] args) {

        HashMap<Person, String> map = new HashMap<Person, String>();
        
        map.put(new Person("001"), "findingsea");
        map.put(new Person("002"), "linyin");
        map.put(new Person("003"), "henrylin");
        map.put(new Person("003"), "findingsealy");
        
        System.out.println(map.toString());
        
        System.out.println(map.get(new Person("001")));
        System.out.println(map.get(new Person("002")));
        System.out.println(map.get(new Person("003")));
    }
}
```

那么输出结果是什么呢？

```
{Person@6e4d4d5e=henrylin, Person@275cea3=findingsea, Person@15128ee5=findingsealy, Person@4513098=linyin}
null
null
null
```

我们可以看到，这里出现了两个问题：

1. 在添加的过程中，我们将`key=new Person("003")`的键值对添加了两次，那么在期望中，`HashMap`中应该只存在一对这样的键值对，因为`key`（期望中）是相同的，所以不应该重复添加，第二次添加的`value="findingsealy"`应该替换掉原先的`value="henrylin"`。但是在输入中，我们发现期望中的情况并没有出现，而是在`HashMap`同时存在了`value="findingsealy"`和`value="henrylin"`的两个键值对，并且它们的`key`值还是不相同的，这显然是错误的。

2. 在获取`value`值时，我们分别用三个`Person`对象去查找，这三个对象和我们刚刚存入的三个`key`值（在期望中）是相同的，但是查找出的却是三个`null`值，这显然也是错误的。

那么，正确的方法其实在很多地方都是被描述过了，直接对`Person`类进行修改，重载`equals`和`hashCode`方法，修改过后的`Person`类如下：

``` java
public class Person {

    private String id;

    public Person(String id) {
        this.id = id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Person person = (Person) o;

        if (id != null ? !id.equals(person.id) : person.id != null) return false;

        return true;
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
}
```

那么，当我们重新执行上述的检验程序时，得到的结果如下：

```
{Person@ba31=findingsea, Person@ba32=linyin, Person@ba33=findingsealy}
findingsea
linyin
findingsealy
```

可以看到，之前指出的亮点错误都得到了改正。那么，为什么会这样呢？

在`HashMap`中，查找`key`的比较顺序为：

1. 计算对象的`Hash Code`，看在表中是否存在。
2. 检查对应`Hash Code`位置中的对象和当前对象是否相等。

显然，第一步就是要用到`hashCode()`方法，而第二步就是要用到`equals()`方法。在没有进行重载时，在这两步会默认调用`Object`类的这两个方法，而在`Object`中，`Hash Code`的计算方法是根据对象的地址进行计算的，那两个`Person("003")`的对象地址是不同的，所以它们的`Hash Code`也不同，自然`HashMap`也不会把它们当成是同一个`key`了。同时，在`Object`默认的`equals()`中，也是根据对象的地址进行比较，自然一个`Person("003")`和另一个`Person("003")`是不相等的。

理解了这一点，就很容易搞清楚为什么需要同时重载`hashCode()`和`equals`两个方法了。

* 重载`hashCode()`是为了对同一个`key`，能得到相同的`Hash Code`，这样`HashMap`就可以定位到我们指定的`key`上。
* 重载`equals()`是为了向`HashMap`表明当前对象和`key`上所保存的对象是相等的，这样我们才真正地获得了这个`key`所对应的这个键值对。

还有一个细节，在`Person`类中对于`hashCode()`的重在方法为：

``` java
@Override
public int hashCode() {
    return id != null ? id.hashCode() : 0;
}
```

这里可能有疑惑的点在于：为什么可以用`String`类型的变量的`Hash Code`作为`Person`类的`Hash Code`值呢？这样`new Person(new String("003"))`和`new Person(new String("003"))`的`Hash Code`是相等的吗？

来看看以下代码的输出：

``` java
System.out.println("findingsea".hashCode());
System.out.println("findingsea".hashCode());
System.out.println(new String("findingsea").hashCode());
System.out.println(new String("findingsea").hashCode());
```

```
728795174
728795174
728795174
728795174
```

可以看到四条语句的输出都是相等的，很直观的合理的猜测就是`String`类型也重载了`hashCode()`以根据字符串的内容来返回`Hash Code`值，所以相同内容的字符串具有相同的`Hash Code`。

同时，这也说明了一个问题：为什么在已知`hashCode()`相等的情况下，还需要用`equals()`进行比较呢？就是因为避免出现上述例子中的出现的情况，因为根据对`Person`类的`hashCode()`方法的重载实现，`Person`类会直接用`id`这个`String`类型成员的`Hash Code`值作为自己的`Hash Code`值，但是很显然的，一个`Person("003")`和一个`String("003")`是不相等的，所以在`hashCode()`相等的情况下，还需要用`equals()`进行比较。

以下例子可以作为上述说明的佐证：

``` java
System.out.println(new Person("003").hashCode()); // 47667
System.out.println(new String("003").hashCode()); // 47667

System.out.println(new Person("003").equals(new String("003"))); // false
```

以上即是全部。