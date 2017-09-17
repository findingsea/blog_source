---
layout: post
title: "堆和堆排序"
date: 2015-03-18 12:47
comments: true
tags: Algorithm
---

### 堆的定义

堆是一种常见的数据结构，具体定义可以见[维基百科](http://zh.wikipedia.org/wiki/%E5%A0%86_\(%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84\))。

<!-- more -->

[程序设计中实用的数据结构](http://book.douban.com/subject/7063664/)中对于堆的定义如下：

> 二叉堆是一棵满足下列性质的完全二叉树。

> 1. 如果某节点有孩子，且根节点的值都小于孩子节点的值，我们称之为小根堆。
> 2. 如果某节点有孩子，且根节点的值都大于孩子节点的值，我们称之为大根堆。

> 二叉堆的树结构同其他完全二叉树一样，所有叶子都在同一层或两个连续层上，最后一层的节点占据尽量左的位置。

利用堆的特性（最大堆和最小堆）可以对数列进行排序，堆排序的性能如下：

| 平均时间        | 最差情形           | 稳定度  | 额外空间
| ----------------- |:---------------------:| ----------:|
| O(nlogn)      | O(nlogn)           | 不稳定  | O(1)

堆排序的步骤如下：

1. 建堆
2. 弹出堆顶元素
3. 调整堆
4. 重复2和3步骤

### 建堆

建堆有两种方法：

* 先填数后调整
* 边插入边调整

这里介绍前一种方法，也就是先填数后调整。由于堆满足完全二叉树的性质，所以可以用一个一维数组来保存堆中的数据。其中的性质如下：

> 在一维数组heap[1...n]中，其中heap[i]节点的父节点是heap[i div 2]，左子节点是heap[2i]，右子节点是heap[2i+1]，若2i>n，则节点i为叶节点。

这里需要注意的是，定义中数组的编号是从1开始的，并且在算法描述中都将采用从1开始编号的方式，而我的代码中，为了统一操作，编号是从0开始的。

由于我们已知2i>n的点都是叶节点，也就是无法向下调整的节点，所以我们的自下而上的调整节点从n div 2节点开始，到根节点为止。

建堆的代码如下：

```java
public MinHeap(int[] array) {
    length = array.length;
    num = array.clone();
    int index = length / 2 - 1;
    while (index >= 0) {
        int toSwapIndex = num[index * 2 + 1] < num[index * 2 + 2] ? index * 2 + 1 : index * 2 + 2;
        if (num[toSwapIndex] < num[index]) {
            int temp = num[index];
            num[index] = num[toSwapIndex];
            num[toSwapIndex] = temp;
            topDownBuild(toSwapIndex);
        }
        index--;
    }
}

private void topDownBuild(int top) {
    while (top < length / 2) {
        int toSwapIndex = num[top * 2 + 1] < num[top * 2 + 2] ? top * 2 + 1 : top * 2 + 2;
        if (num[toSwapIndex] < num[top]) {
            int temp = num[top];
            num[top] = num[toSwapIndex];
            num[toSwapIndex] = temp;
        } else {
            break;
        }
        top = toSwapIndex;
    }
}
```

### 弹出堆顶元素

堆顶元素就是当前数据集中的最小（或者最大）元素，弹出的操作很简单，就是获取`num[0]`的值，然后将`num[0]`重新赋值为`num[length - 1]`，并且`length--`即可。

### 调整堆

弹出堆顶元素之后，显而易见当前堆的状态被破坏了，那么就需要调整堆，其实也就是直接的调用`build(int top)`方法。这一步中的调整堆算法其实和建堆时的很像，但是有如下区别：

1. 建堆时，采用的是自下而上的调整策略；调整堆时，采用的自下而上的调整策略。因为如果刨去当前的堆顶元素，整个堆其他位置的元素其实是处在合理的位置。
2. 调整堆时，只要当前位置已经是合理的了，那就不需要继续调整，可以马上跳出循环。

### 重复

重复弹出堆顶元素和调整堆两步骤，直到堆空了为止（成员变量length等于0）。

完整代码如下：

```java
/**
 * Created by findingsea on 3/12/15.
 * 对于一个包含了n个节点的二叉堆来说，叶子的数量为n为奇数：(n / 2 + 1)或者n为偶数：(n / 2)
 */
public class HeapSort {

    public int[] sort(int[] num) {
        int[] result = new int[num.length];
        MinHeap minHeap = new MinHeap(num);
        for (int i = 0; i < result.length; i++) {
            result[i] = minHeap.pop();
        }
        return result;
    }

    class MinHeap {

        int[] num;
        int length;

        public MinHeap(int[] array) {
            length = array.length;
            num = array.clone();
            int index = length / 2 - 1;
            while (index >= 0) {
                int toSwapIndex = num[index * 2 + 1] < num[index * 2 + 2] ? index * 2 + 1 : index * 2 + 2;
                if (num[toSwapIndex] < num[index]) {
                    int temp = num[index];
                    num[index] = num[toSwapIndex];
                    num[toSwapIndex] = temp;
                    topDownBuild(toSwapIndex);
                }
                index--;
            }
        }
        
        // 边插入边调整
        public void add(int n) {
        
        }

        public int pop() {
            int top = num[0];
            num[0] = num[length - 1];
            length--;
            topDownBuild(0);
            return top;
        }

        private void topDownBuild(int top) {
            while (top < length / 2) {
                int toSwapIndex = num[top * 2 + 1] < num[top * 2 + 2] ? top * 2 + 1 : top * 2 + 2;
                if (num[toSwapIndex] < num[top]) {
                    int temp = num[top];
                    num[top] = num[toSwapIndex];
                    num[toSwapIndex] = temp;
                } else {
                    break;
                }
                top = toSwapIndex;
            }
        }
    }
}

```