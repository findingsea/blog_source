---
layout: post
title: "Maximal Rectangle@LeetCode"
date: 2015-04-16 09:19
comments: true
tags: LeetCode
---
## [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/)

<!-- more -->

这一题的核心算法其实和[Largest Rectangle in Histogram](http://segmentfault.com/a/1190000002673098)一样，对每一行都求出每个元素对应的高度，这个高度就是对应的连续`1`的长度，然后对每一行都更新一次最大矩形面积，那么这个问题就变成了[Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)，用相同的方法求解就行了。总结来说就是对矩阵中的每一行，执行一遍[Largest Rectangle in Histogram](http://segmentfault.com/a/1190000002673098)算法。

实现代码：

``` java
public class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0)
            return 0;
        int largestRectangle = 0;
        int[] height = new int[matrix[0].length];
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                int h = matrix[i][j] - '0';
                height[j] = h == 0 ? 0 : height[j] + 1;
            }
            largestRectangle = Math.max(largestRectangle, largestRectangleArea(height));
        }
        return largestRectangle;
    }

    private int largestRectangleArea(int[] height) {
        Stack<Integer> stack = new Stack<Integer>();
        int index = 0, largestArea = 0;
        while (index < height.length) {
            if (stack.isEmpty() || height[stack.peek()] < height[index]) {
                stack.push(index++);
            } else {
                int h = height[stack.pop()];
                int w = stack.isEmpty() ? index : index - stack.peek() - 1;
                largestArea = Math.max(largestArea, h * w);
            }
        }
        while (!stack.isEmpty()) {
            int h = height[stack.pop()];
            int w = stack.isEmpty() ? height.length : height.length - stack.peek() - 1;
            largestArea = Math.max(largestArea, h * w);
        }
        return largestArea;
    }
}
```