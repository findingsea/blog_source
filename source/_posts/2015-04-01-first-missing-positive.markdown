---
layout: post
title: "First Missing Positive@LeetCode"
date: 2015-04-01 09:21
comments: true
tags: LeetCode
---
[First Missing Positive](https://leetcode.com/problems/first-missing-positive/)

<!-- more -->

同样是一道我不太能理解为什么能标为hard的题目。

我的解法是将所有正数都先放到map里面，然后就从小正数——也就是1——开始检查map，遇到的第一个不包含在map中的正数便是答案。最坏情况下的复杂度是`O(n)`。

``` java
public class Solution {
    public int firstMissingPositive(int[] A) {
        HashMap<Integer, Boolean> map = new HashMap<Integer, Boolean>();
        for (int a : A) {
            if (a > 0) {
                map.put(a, true);
            }
        }
        int v = 1;
        while (true) {
            if (!map.containsKey(v)) {
                break;
            }
            v++;
        }
        return v;
    }
}
```