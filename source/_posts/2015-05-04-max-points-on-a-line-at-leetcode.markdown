---
layout: post
title: "Max Points on a Line@LeetCode"
date: 2015-05-04 19:26
comments: true
tags: LeetCode
---
## [Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/)

<!-- more -->

题目本身不难，一次`AC`可能有点困难，因为要考虑的东西还是挺多的。两层循环，外层遍历所以点，内层遍历外层点之后的所有点，同时在内层循环用一个`HashMap`来保存每个斜率对应的，这样在内存循环中，斜率相同就代表是在同一条直线上了。这里要注意的有两点：

1. 对于垂直与`x`轴的直线，采用`Float.POSITIVE_INFINITY`来表示它的斜率。
2. 相同点，用一个变量专门来记录相同点有多少，在内层循环结束之后，加到总计数中。

其实总体思想就是：求出一点所在直线的最多点数是多少，然后对每个点都求一遍，那么最后必然得到了全局点数最多的直线，同时注意在外层循环算过的点在内层就不必再算，因为再算也不会比之前得到的点数更多，这样可以减少循环次数。

实现代码：

``` java
/**
 * Definition for a point.
 * class Point {
 *     int x;
 *     int y;
 *     Point() { x = 0; y = 0; }
 *     Point(int a, int b) { x = a; y = b; }
 * }
 */
public class Solution {
    public int maxPoints(Point[] points) {
        int length = points.length;
        if (length < 3)
            return length;
        int max = 2;
        for (int i = 0; i < length; i++) {
            int pointMax = 1, samePointCount = 0;
            HashMap<Double, Integer> slopeCount = new HashMap<Double, Integer>();
            Point origin = points[i];
            for (int j = i + 1; j < length; j++) {
                Point target = points[j];
                if (origin.x == target.x && origin.y == target.y) {
                    samePointCount++;
                    continue;
                }
                double k;
                if (origin.x == target.x) {
                    k = Float.POSITIVE_INFINITY;
                } else if (origin.y == target.y) {
                    k = 0;
                } else {
                    k = ((float) (origin.y  -target.y)) / (origin.x - target.x);
                }
                if (slopeCount.containsKey(k)) {
                    slopeCount.put(k, slopeCount.get(k) + 1);
                } else {
                    slopeCount.put(k, 2);
                }
                pointMax = Math.max(pointMax, slopeCount.get(k));
            }
            pointMax += samePointCount;
            max = Math.max(pointMax, max);
        }
        return max;
    }
}
```