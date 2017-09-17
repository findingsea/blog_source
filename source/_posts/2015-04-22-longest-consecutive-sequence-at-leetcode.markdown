---
layout: post
title: "Longest Consecutive Sequence@LeetCode"
date: 2015-04-22 13:42
comments: true
tags: LeetCode
---
## [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)

<!-- more -->

本题直观的解法就是排序之后遍历，但是题目要求只用`O(n)`的复杂度，那么先排序显然是无法满足要求的。

那么这种『显然要遍历所有元素，但是却只给了`O(n)`的复杂度』，这样就想到了`HashMap`。把数组中的每个元素都放入一个`HashMap`中为`key`，`value`为`boolean`类型，表示该元素有没有访问过。然后，对于数组中的每个元素，要是没有被访问过，就对其进行计数——往前遍历及往后遍历，直到下一个元素不存在于表中为止。那么这样就保证了在整个计数过程中，所有元素都只被访问了一次。

实现代码：

``` java
public class Solution {
    public int longestConsecutive(int[] num) {
        HashMap<Integer, Boolean> visited = new HashMap<Integer, Boolean>();
        int length = num.length, max = 0;
        for (int n : num) {
            visited.put(n, false);
        }
        for (int i = 0; i < num.length; i++) {
            int n = num[i];
            if (visited.get(n)) {
                continue;
            }
            int count = 1;
            for (int left = n - 1; left >= n - length + 1; left--) {
                if (visited.containsKey(left)) {
                    visited.put(left, true);
                    count++;
                } else {
                    break;
                }
            }
            for (int right = n + 1; right <= n + length - 1; right++) {
                if (visited.containsKey(right)) {
                    visited.put(right, true);
                    count++;
                } else {
                    break;
                }
            }
            max = Math.max(max, count);
        }
        return max;
    }
}
```