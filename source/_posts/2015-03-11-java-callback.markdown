---
layout: post
title: "Java Callback"
date: 2015-03-11 16:51
comments: true
tags: Java
---
如何编写回调函数？

回调函数其实就是将某个特定接口的实现作为参数传入目标对象，让目标对象在适当的时候对齐进行调用。

<!-- more -->

`Response`接口包含了两个方法：`success`和`fail`，分别需要在请求成功和失败时调用，但是具体这两个方法需要做写什么事情，这在接口的定义中是无从知道的，因为这是根据每个发送请求的主体的具体情况而确定的。

`Request`是发送请求类，是执行人物的主体，在其`send(Response response)`方法中，会接受一个`Response`接口的实现，并在请求完成后，根据请求的结果调用`Response`中相应的方法。

`CallbackSample`是测试的主体，在`main`函数中，产生一个`Request`对象，然后调用其`send`方法，同时传入一个匿名类实现了`Response`接口。

``` java
/**
 * Created by findingsea on 3/11/15.
 */
public interface Response {

    void success();

    void fail();
}

```

``` java
/**
 * Created by findingsea on 3/11/15.
 */
public class Request {

    public void send(Response response) {
        System.out.println("Send Request");

        response.fail();
    }
}

```

``` java
/**
 * Created by findingsea on 3/11/15.
 */
public class CallbackSample {

    public static void main(String[] args) {
        Request request = new Request();
        request.send(new Response() {
            @Override
            public void success() {
                System.out.println("Request Success");
            }

            @Override
            public void fail() {
                System.out.println("Request Fail");
            }
        });
    }
}

```

以下是输出：

``` java
Send Request
Request Fail
```