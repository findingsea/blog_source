---
layout: post
title: "Wildcard Matching@LeetCode"
date: 2015-04-03 10:10
comments: true
tags: LeetCode
---
[Wildcard Matching](https://leetcode.com/problems/wildcard-matching/)

<!-- more -->

一开始是非常想用递归的方法做的，因为前面已经有做正则表达式的经验了，所以认为这一题应该是同样的思路做。但是小数据集还好，大数据集根本过不去，分析了一下，主要是要回朔的地方太多了，或者是需要处理的分支实在太多。

参考了网上一个挺巧妙的方法，对目标字符串和通配符字符串分别设置索引，指向当前位置。在`*`和`*`之间自然是逐个匹配；当遇到`*`号时，在目标字符串和通配符字符串都记录下当前位置；如果遇到无法匹配的情况，先检查之前没有`*`号的位置记录，如果有则将目标字符串和通配符字符串的索引都回退到当时保存的位置，然后字符串索引自加之后继续开始匹配。

这个算法对`*`的处理就是，当第一次遇到时，默认不匹配目标字符串中的任何内容，当后面的内容遇到了无法匹配的情况时，再进行回退，每次回退相当于利用之前的`*`多匹配一个目标字符串中的字符，直到全部匹配完或是无法匹配退出。

实现代码：

``` java
public class Solution {
    public boolean isMatch(String s, String p) {
        int posS = 0, posP = 0;
        int posStar = -1, flagInS = -1;
        while (posS < s.length()) {
            if (posP < p.length() && (s.charAt(posS) == p.charAt(posP) || p.charAt(posP) == '?')) {
                posS++;
                posP++;
            } else if (posP < p.length() && (p.charAt(posP) == '*')) {
                flagInS = posS;
                posStar = posP;
                posP++;
            } else if (posStar != -1) {
                posS = ++flagInS;
                posP = posStar + 1;
            } else {
                return false;
            }
        }
        while (posP < p.length() && p.charAt(posP) == '*') {
            posP++;
        }
        return posS == s.length() && posP == p.length();
    }
}
```