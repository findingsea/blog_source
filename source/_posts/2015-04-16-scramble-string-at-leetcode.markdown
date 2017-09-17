---
layout: post
title: "Scramble String@LeetCode"
date: 2015-04-16 10:09
comments: true
tags: LeetCode
---
## [Scramble String](https://leetcode.com/problems/scramble-string/)

<!-- more -->

这一题的解法其实很简单，就是递归遍历所有情况，那么需要增加的就是提前检验，然后排出以减少递归的次数，从而改进效率。

提前检验的内容就是检验两个字符串的内容是否相同，这个内容是否相同指的是：两个字符串所包含的字符种类和每种字符出现的个数是否相同，如果这个不同就可以直接返回，不需要执行接下来的代码。

实现代码如下：

``` java
public class Solution {
    public boolean isScramble(String s1, String s2) {
        
        if (s1.equals(s2))
            return true;

        char[] s1chars = s1.toCharArray();
        char[] s2chars = s2.toCharArray();
        Arrays.sort(s1chars);
        Arrays.sort(s2chars);
        for (int i = 0; i < s1chars.length; i++) {
            if (s1chars[i] != s2chars[i])
                return false;
        }

        int half = 1;
        boolean result = false;
        while (half < s1.length()) {
            result = (isScramble(s1.substring(0, half), s2.substring(0, half))
                    && isScramble(s1.substring(half, s1.length()), s2.substring(half, s2.length())))
                    || (isScramble(s1.substring(0, half), s2.substring(s2.length() - half, s2.length()))
                    && isScramble(s1.substring(half, s1.length()), s2.substring(0, s2.length() - half)));
            if (result)
                break;
            half++;
        }

        return result;
    }
}
```