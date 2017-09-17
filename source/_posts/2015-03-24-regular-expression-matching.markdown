---
layout: post
title: "Regular Expression Matching@LeetCode"
date: 2015-03-24 13:31
comments: true
tags: LeetCode
---
[Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/)

比较典型的动态规划题，重点就在于`*`号的匹配上。

<!-- more -->

分三步走：

* 当模式串为空时。检查内容串是否为空（为空则返回`true`，反之返回`false`）。注意这里反过来是不成立的，也就是不能检查当内容穿为空时，模式串是否为空，因为如果模式串最后一个字符是`*`，那么即便此时模式串不为空，总结结果也有可能是`true`。
* 当模式串长度为1或者模式串的第二个字符不为`*`时。这种情况比较简单，只要比较这个字符串的第一个字符即可，两个字符串的第一个字符相等或者模式串的第一个字符为`.`则返回`true`，反之就是`false`。
* 最后，就是要处理模式串第二个字符是`*`的情况了，这种情况下，模式串的第一个字符可以匹配内容串中任意多个连续的相同字符（包括0个），那么就从『一个都匹配』到『匹配所有符合要求的字符』进行一遍循环，那么在循环中，问题就变为两个字符串的字串是否匹配的问题了，对函数进行递归调用即可，判断返回结果以决定是否返回`true`。最后如果循环结束之后仍没有返回，就证明无论如何匹配，`*`都无法合理匹配，那就证明两个字符串无法匹配，所以返回`false`。

实现代码：

``` java
public class Solution {
    public boolean isMatch(String s, String p) {
        if (p.length() == 0) return s.length() == 0;
        if (p.length() == 1 || p.charAt(1) != '*') {
            if (s.length() > 0 && (p.charAt(0) == s.charAt(0)
                    || p.charAt(0) == '.')) {
                return isMatch(s.substring(1, s.length()),
                        p.substring(1, p.length()));
            } else {
                return false;
            }
        } else {
            int i = 0;
            do {
                if (isMatch(s.substring(i, s.length()), p.substring(2, p.length()))) {
                    return true;
                }
                i++;
            } while (i <= s.length() && (p.charAt(0) == s.charAt(i - 1) || p.charAt(0) == '.'));
            return false;
        }
    }
}
```