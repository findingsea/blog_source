---
layout: post
title: "Median of Two Sorted Arrays@LeetCode"
date: 2015-03-23 09:18
comments: true
tags: LeetCode
---
[Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)

<!-- more -->

这题记得当时也是查了网上的资料才做出来的，而且采用的是一个通用算法`findKth`。

其实思想很简单：要寻找第k小的元素，那么总是保持数组A的当前元素（即A[a]）为当前最小元素（如果不是，则交换A和B数组，使这一条成立），然后弹出该元素（即++a），然后再递归调用寻找第k-1小的元素。

这需要注意的地方在于：

* `A.length + B.length`为偶数的时候，中位数有两个，要取平均。
* `A.length + B.length`为奇数的时候，中位数只有一个。

实现代码如下：

``` java
/**
 * Created by findingsea on 14/11/16.
 */
public class Solution {
    public double findKth(int A[], int a, int B[], int b, int k) {
        if (A.length == a || (b < B.length && A[a] > B[b])) {
            int tmp[] = A;
            A = B;
            B = tmp;
            int t = a;
            a = b;
            b = t;
        }
        if (k == 1) return A[a];
        return findKth(A, ++a, B, b, --k);
    }
    public double findMedianSortedArrays(int A[], int B[]) {
        int len = A.length + B.length;
        if (len == 1) return A.length == 0 ? B[0] : A[0];
        if (len % 2 == 0) {
            return (findKth(A, 0, B, 0, len / 2) + findKth(A, 0, B, 0, len / 2 + 1)) / 2;
        }
        else {
            return findKth(A, 0, B, 0, len / 2 + 1);
        }
    }
}

```