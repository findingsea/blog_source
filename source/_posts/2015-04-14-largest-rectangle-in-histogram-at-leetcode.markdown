---
layout: post
title: "Largest Rectangle in Histogram@LeetCode"
date: 2015-04-14 10:50
comments: true
tags: LeetCode
---
## [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)

<!-- more -->

这道题目有一个规则要掌握：当图形处在上升期时（`height[i] < height[i + 1]`），其实是不用计算面积的，因为在这种情况下再往前移动一格（`i -> i + 1`）所能得到的面积必然更大；当图形处在下降期时（`height[i] > height[i + 1]`），就要开始计算当前矩形的面积了，但是这个时候只知道右端点，如何知道左端点在哪呢？这就需要在遍历的时候，维护一个栈，这个栈里面保存的是最有可能的右端点，那么压栈呢？当每次出现比栈顶元素大的块是，就将其索引压栈，反之就是要计算机一次当前的矩形面积并和当前最大面积进行比较。

再多解释一下这个左端点栈的维护，因为这是做这一题的关键。

* 入栈：入栈的情形很简单，就是遇到了比当前栈顶元素还大的元素，那就把它的索引入栈，这其实是一种贪心，相当于先不计算矩阵的大小，因为如果下一个元素还要大，那么所能得到的矩阵大小必然比现在计算要来的大。
* 出栈：遇到当前元素对栈顶元素要小，那就说明以栈顶元素为高度的矩阵边界到了，那么就要将栈顶元素出栈，然后计算以其为高度的矩形的大小。

那么这个栈中的元素有两个性质：
1. 栈顶元素和当前索引之间的所有元素（前闭后开的区间）都大于等于栈顶元素：因为一旦中间遇到了比栈顶元素小的元素，那么栈需要连续弹出，直至当前栈顶元素小于当前元素。
2. 栈顶元素和栈中的第二元素之间的所有元素（前开后闭的区间）都大于等于栈顶元素：因为如果这中间有一个元素既大于栈中的第二个元素又小于栈顶元素，那么它应该在这中间被入栈，继而成为栈中第二个元素。

其实这个做法就是把数组中的每个元素都作为矩形高度，计算了一遍该高度下矩形的最大面积。只是每次都贪心最大，避免了重复计算，所以效率高。

实现代码如下：

``` java
public class Solution {
    public int largestRectangleArea(int[] height) {
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