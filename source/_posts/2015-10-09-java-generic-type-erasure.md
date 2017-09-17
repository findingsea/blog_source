title: Java泛型：类型擦除
date: 2015-10-09 11:59:43
tags: Java
---
## 前情回顾

[Java泛型：泛型类、泛型接口和泛型方法](http://segmentfault.com/a/1190000002646193)

<!-- more -->

## 类型擦除

### 代码片段一

``` java
Class c1 = new ArrayList<Integer>().getClass();
Class c2 = new ArrayList<String>().getClass(); 
System.out.println(c1 == c2);

/* Output
true
*/
```

显然在平时使用中，`ArrayList<Integer>()`和`new ArrayList<String>()`是完全不同的类型，但是在这里，程序却的的确确会输出`true`。

这就是Java泛型的类型擦除造成的，因为不管是`ArrayList<Integer>()`还是`new ArrayList<String>()`，都在编译器被编译器擦除成了`ArrayList`。那编译器为什么要做这件事？原因也和大多数的Java让人不爽的点一样——兼容性。由于泛型并不是从Java诞生就存在的一个特性，而是等到SE5才被加入的，所以为了兼容之前并未使用泛型的类库和代码，不得不让编译器擦除掉代码中有关于泛型类型信息的部分，这样最后生成出来的代码其实是『泛型无关』的，我们使用别人的代码或者类库时也就不需要关心对方代码是否已经『泛化』，反之亦然。

在编译器层面做的这件事（擦除具体的类型信息），使得Java的泛型先天都存在一个让人非常难受的缺点：

> 在泛型代码内部，无法获得任何有关泛型参数类型的信息。

### 代码片段二

``` java
List<Integer> list = new ArrayList<Integer>();
Map<Integer, String> map = new HashMap<Integer, String>();
System.out.println(Arrays.toString(list.getClass().getTypeParameters()));
System.out.println(Arrays.toString(map.getClass().getTypeParameters()));

/* Output
[E]
[K, V]
*/
```

关于`getTypeParameters()`的解释：

> Returns an array of TypeVariable objects that represent the type variables declared by the generic declaration represented by this GenericDeclaration object, in declaration order. Returns an array of length 0 if the underlying generic declaration declares no type variables.

我们期待的是得到泛型参数的类型，但是实际上我们只得到了一堆占位符。

### 代码片段三

``` java
public class Main<T> {

    public T[] makeArray() {
        // error: Type parameter 'T' cannot be instantiated directly
        return new T[5];
    }
}
```

我们无法在泛型内部创建一个`T`类型的数组，原因也和之前一样，`T`仅仅是个占位符，并没有真实的类型信息，实际上，除了`new`表达式之外，`instanceof`操作和转型（会收到警告）在泛型内部都是无法使用的，而造成这个的原因就是之前讲过的编译器对类型信息进行了擦除。

同时，面对泛型内部形如`T var;`的代码时，记得多念几遍：它只是个Object，它只是个Object……

### 代码片段四

``` java
public class Main<T> {

    private T t;

    public void set(T t) {
        this.t = t;
    }

    public T get() {
        return t;
    }

    public static void main(String[] args) {
        Main<String> m = new Main<String>();
        m.set("findingsea");
        String s = m.get();
        System.out.println(s);
    }
}

/* Output
findingsea
*/
```

虽然有类型擦除的存在，使得编译器在泛型内部其实完全无法知道有关`T`的任何信息，但是编译器可以保证重要的一点：**内部一致性**，也是我们放进去的是什么类型的对象，取出来还是相同类型的对象，这一点让Java的泛型起码还是有用武之地的。

代码片段四展现就是编译器确保了我们放在`t`上的类型的确是`T`（即便它并不知道有关`T`的任何类型信息）。这种确保其实做了两步工作：

* `set()`处的类型检验
* `get()`处的类型转换

这两步工作也成为**边界动作**。

### 代码片段五

``` java
public class Main<T> {

    public List<T> fillList(T t, int size) {
        List<T> list = new ArrayList<T>();
        for (int i = 0; i < size; i++) {
            list.add(t);
        }
        return list;
    }

    public static void main(String[] args) {
        Main<String> m = new Main<String>();
        List<String> list = m.fillList("findingsea", 5);
        System.out.println(list.toString());
    }
}

/* Output
[findingsea, findingsea, findingsea, findingsea, findingsea]
*/
```

代码片段五同样展示的是泛型的内部一致性。

## 擦除的补偿

如上看到的，但凡是涉及到确切类型信息的操作，在泛型内部都是无法共工作的。那是否有办法绕过这个问题来编程，答案就是显示地传递类型标签。

### 代码片段六

``` java
public class Main<T> {

    public T create(Class<T> type) {
        try {
            return type.newInstance();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void main(String[] args) {
        Main<String> m = new Main<String>();
        String s = m.create(String.class);
    }
}
```

代码片段六展示了一种用类型标签生成新对象的方法，但是这个办法很脆弱，因为这种办法要求对应的类型必须有默认构造函数，遇到`Integer`类型的时候就失败了，而且这个错误还不能在编译器捕获。

进阶的方法可以用限制类型的显示工厂和模板方法设计模式来改进这个问题，具体可以参见《Java编程思想 （第4版）》P382。

### 代码片段七

``` java
public class Main<T> {

    public T[] create(Class<T> type) {
        return (T[]) Array.newInstance(type, 10);
    }

    public static void main(String[] args) {
        Main<String> m = new Main<String>();
        String[] strings = m.create(String.class);
    }
}
```

代码片段七展示了对泛型数组的擦除补偿，本质方法还是通过显示地传递类型标签，通过`Array.newInstance(type, size)`来生成数组，同时也是最为推荐的在泛型内部生成数组的方法。

以上，泛型的第二部分的结束。