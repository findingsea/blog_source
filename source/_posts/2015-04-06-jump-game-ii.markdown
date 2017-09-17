---
layout: post
title: "Jump Game II@LeetCode"
date: 2015-04-06 11:05
comments: true
tags: LeetCode
---
[Jump Game II](https://leetcode.com/problems/jump-game-ii/)

<!-- more -->

比较典型的贪心。维护一个区间，区间表示第i步所能到达的索引范围。递推的方法为：每次都遍历一遍当前区间内的所有元素，从一个元素出发的最远可达距离是`index+array[index]`，那么下一个区间的左端点就是当前区间的右端点+1，下一个区间的右端点就是当前区间的`max(index+array[index])`，以此类推，直到区间包含了终点，统计当前步数即可。

实现代码：

``` java
public class Solution {
    public int jump(int[] A) {
        if (A.length == 1)
            return 0;
        int max = 0, count = 1, begin = 0, end = A[0];
        while (end < A.length - 1) {
            count++;
            int index = begin;
            for (; index <= end; index++) {
                max = Math.max(max, index + A[index]);
            }
            begin = index;
            end = max;
        }
        return count;
    }
}
```