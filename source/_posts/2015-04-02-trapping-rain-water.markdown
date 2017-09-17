---
layout: post
title: "Trapping Rain Water@LeetCode"
date: 2015-04-02 10:59
comments: true
tags: LeetCode
---
[Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)

<!-- more -->

这道题当时也是花了我不少脑力呀，总感觉方法就在边上了，但是总是差一点点。

这一题的主要问题就在于：如何找到『坑』。

* 其一，理论上来讲，如果当前处在上升阶段（`y`在增大），那么就应该正在形成一个『坑』。
* 其二，知道现在处在『坑』了，就该算坑有多大，但是这里的难点在于如果以当前点为『坑』的右边缘，那么会遇到下一个位置可能更高，那么下一个位置才应该是『坑』的右边缘，同时还要注意左右边缘高度的比较，如果右边缘已经高于左边缘了，那么当前这个『坑』的大小就无法再增加了，反之则还有继续增大的可能。那么这里就要执行一个动作来方便之后的计算和判断：『填坑』。如果当前位置的高度低于左边缘，那么就先把已知的『坑』填平，也就是把『坑』中的每个位置就填到和右边缘一样高，并记录下来填坑的大小，再继续下一个位置；如果当前位置的高度高于左边缘，那么当前『坑』的大小不会再变了，直接用左边缘的高度高度为标尺扫一遍『坑』，把不平的地方填平即可，当然也要记录下填坑的大小。这个方法的好处在于，『坑』的每一个位置都不会被重复填，可以使代码简化并且不容易出错。

实现代码：

```java
public class Solution {
    public int trap(int[] A) {
        if (A == null || A.length == 0)
            return 0;
        int leftHeight = 0, left, cap = 0, index = 0;
        while (index < A.length && A[index] == 0) {
            index++;
        }
        if (index == A.length)
            return cap;
        left = index;
        leftHeight = A[index++];
        for (; index < A.length; index++) {
            int height = A[index];
            if (A[index - 1] < A[index]) {
                if (leftHeight > height) {
                    int i = index - 1, min = 0;
                    for (; A[i] < A[index]; i--) {
                        cap += A[index] - A[i];
                        A[i] = A[index];
                    }
                } else {
                    for (int i = index - 1; i > left; i--) {
                        cap += leftHeight - A[i];
                    }
                    leftHeight = height;
                    left = index;
                }
            }
        }
        return cap;
    }
}
```