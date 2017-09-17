---
layout: post
title: "Java泛型 泛型类、泛型接口和泛型方法"
date: 2015-04-03 10:01
comments: true
tags: Java
---
根据[《Java编程思想 （第4版）》](http://book.douban.com/subject/2130190/)中的描述，泛型出现的动机在于：

> 有许多原因促成了泛型的出现，而最引人注意的一个原因，就是为了创建**容器类**。

<!-- more -->

## 泛型类

容器类应该算得上最具重用性的类库之一。先来看一个没有泛型的情况下的容器类如何定义：

``` java
public class Container {
    private String key;
    private String value;

    public Container(String k, String v) {
        key = k;
        value = v;
    }
    
    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
```

`Container`类保存了一对`key-value`键值对，但是类型是定死的，也就说如果我想要创建一个键值对是`String-Integer`类型的，当前这个`Container`是做不到的，必须再自定义。那么这明显重用性就非常低。

当然，我可以用`Object`来代替`String`，并且在Java SE5之前，我们也只能这么做，由于`Object`是所有类型的基类，所以可以直接转型。但是这样灵活性还是不够，因为还是指定类型了，只不过这次指定的类型层级更高而已，有没有可能不指定类型？有没有可能在运行时才知道具体的类型是什么？

所以，就出现了泛型。

``` java
public class Container<K, V> {
    private K key;
    private V value;

    public Container(K k, V v) {
        key = k;
        value = v;
    }

    public K getKey() {
        return key;
    }

    public void setKey(K key) {
        this.key = key;
    }

    public V getValue() {
        return value;
    }

    public void setValue(V value) {
        this.value = value;
    }
}
```

在编译期，是无法知道`K`和`V`具体是什么类型，只有在运行时才会真正根据类型来构造和分配内存。可以看一下现在`Container`类对于不同类型的支持情况：

``` java
public class Main {

    public static void main(String[] args) {
        Container<String, String> c1 = new Container<String, String>("name", "findingsea");
        Container<String, Integer> c2 = new Container<String, Integer>("age", 24);
        Container<Double, Double> c3 = new Container<Double, Double>(1.1, 2.2);
        System.out.println(c1.getKey() + " : " + c1.getValue());
        System.out.println(c2.getKey() + " : " + c2.getValue());
        System.out.println(c3.getKey() + " : " + c3.getValue());
    }
}
```

输出：

```
name : findingsea
age : 24
1.1 : 2.2
```

## 泛型接口

在泛型接口中，生成器是一个很好的理解，看如下的生成器接口定义：

``` java
public interface Generator<T> {
    public T next();
}
```

然后定义一个生成器类来实现这个接口：

``` java
public class FruitGenerator implements Generator<String> {

    private String[] fruits = new String[]{"Apple", "Banana", "Pear"};

    @Override
    public String next() {
        Random rand = new Random();
        return fruits[rand.nextInt(3)];
    }
}
```

调用：

``` java
public class Main {

    public static void main(String[] args) {
        FruitGenerator generator = new FruitGenerator();
        System.out.println(generator.next());
        System.out.println(generator.next());
        System.out.println(generator.next());
        System.out.println(generator.next());
    }
}
```

输出：

```
Banana
Banana
Pear
Banana
```

## 泛型方法

一个基本的原则是：**无论何时，只要你能做到，你就应该尽量使用泛型方法。**也就是说，如果使用泛型方法可以取代将整个类泛化，那么应该有限采用泛型方法。下面来看一个简单的泛型方法的定义：

``` java
public class Main {

    public static <T> void out(T t) {
        System.out.println(t);
    }

    public static void main(String[] args) {
        out("findingsea");
        out(123);
        out(11.11);
        out(true);
    }
}
```

可以看到方法的参数彻底泛化了，这个过程涉及到编译器的类型推导和自动打包，也就说原来需要我们自己对类型进行的判断和处理，现在编译器帮我们做了。这样在定义方法的时候不必考虑以后到底需要处理哪些类型的参数，大大增加了编程的灵活性。

再看一个泛型方法和可变参数的例子：

``` java
public class Main {

    public static <T> void out(T... args) {
        for (T t : args) {
            System.out.println(t);
        }
    }

    public static void main(String[] args) {
        out("findingsea", 123, 11.11, true);
    }
}
```

输出和前一段代码相同，可以看到泛型可以和可变参数非常完美的结合。

以上，泛型的第一部分的结束。