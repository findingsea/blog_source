---
layout: post
title: "Search in Rotated Sorted Array@LeetCode"
date: 2015-03-30 10:34
comments: true
tags: LeetCode
---
[Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)

<!-- more -->

其实不太能理解为什么这题能标成hard，因为用很直观的算法便可以解出来。由于数组是被翻转过的，所以被分成两个部分，每个部分又都是有序的。所以先判断先判断一下要查找的数是在前半段还是后半段，然后依次查找即可。

```java
public class Solution {
    public int search(int[] A, int target) {
        int index = -1;
        if (A == null || A.length == 0) return index;
        if (A[0] == target) return 0;
        if (A[A.length - 1] == target) return A.length - 1;
        int ALen = A.length;
        boolean hit = false;
        if (A[0] < target) {
            index = 1;
            while (index < ALen && A[index - 1] < A[index]) {
                if (A[index] == target) {
                    hit = true;
                    break;
                }
                index++;
            }
            if (!hit) {
                index = -1;
            }
        } else if (target < A[ALen - 1]){
            index = ALen - 2;
            while (0 <= index && A[index] < A[index + 1]) {
                if (A[index] == target) {
                    hit = true;
                    break;
                }
                index--;
            }
            if (!hit) {
                index = -1;
            }
        } else {
            index = -1;
        }
        return index;
    }
}
```