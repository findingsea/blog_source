---
layout: post
title: "Candy@LeetCode"
date: 2015-04-24 09:47
comments: true
tags: LeetCode
---
## [Candy](https://leetcode.com/problems/candy/)

<!-- more -->

双向爬坡。从左到右爬一边，再从右到左爬一边。再累加所有值即可。

``` java
public class Solution {
    public int candy(int[] ratings) {
        int[] candies = new int[ratings.length];
        int last = ratings.length - 1;
        int result = 0;
        for (int i = 1; i <= last; i++) {
            if (ratings[i - 1] < ratings[i]) {
                candies[i] = candies[i - 1] + 1;
            }
        }
        for (int i = last - 1; i >= 0; i--) {
            if (ratings[i] > ratings[i + 1]) {
                candies[i] = Math.max(candies[i], candies[i + 1] + 1);
            }
            result += candies[i];
        }
        result += ratings.length + candies[last];
        return result;
    }
}
```