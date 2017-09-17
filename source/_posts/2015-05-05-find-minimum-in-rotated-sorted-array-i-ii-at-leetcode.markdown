---
layout: post
title: "Find Minimum in Rotated Sorted Array I II@LeetCode"
date: 2015-05-05 09:40
comments: true
tags: LeetCode
---
## [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

<!-- more -->

其实直接遍历也是可以也可以`AC`，但是更加优化的解法应该是采用二分查找的思想。如果中间值比起点大就收缩起点，如果中间值比终点大就收缩终点，直到收缩到起点和终点相邻，也就是找到了翻转的部分。这里需要注意的是，数组可能是没有翻转过的，所以`mid`的初值赋`0`。

实现代码：

``` java
public class Solution {
    public int findMin(int[] num) {
        int begin = 0, end = num.length - 1, mid = 0;
        while (num[begin] > num[end]) {
            if (end - begin == 1) {
                mid = end;
                break;
            }
            mid = (begin + end) / 2;
            if (num[begin] < num[mid])
                begin = mid;
            else 
                end = mid;
        }
        return num[mid];
    }
}
```

## [Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)

理论上这题应该也用二分法，碰到起点终点相同的情况就只能进行遍历，但是那样代码会更复杂并且效率上并不见得提高多少，所以这里我直接采用遍历的方法。

实现代码：

``` java
public class Solution {
    public int findMin(int[] num) {
        int min = num[0], length = num.length;
        if (num[0] >= num[length - 1]) {
            int index = 1;
            while (index < length) {
                if (num[index - 1] > num[index]) {
                    break;
                }
                index++;
            }
            min = index == length ? num[index - 1] : num[index];
        }
        return min;
    }
}
```