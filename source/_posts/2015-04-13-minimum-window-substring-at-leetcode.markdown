---
layout: post
title: "Minimum Window Substring@LeetCode"
date: 2015-04-13 10:24
comments: true
tags: LeetCode
---
## [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)

<!-- more -->

典型的窗口操作题，维护两个哈希表，`stdMap`标准表，`map`当前表，标准表用来保存`T`中的字符信息，当前表用来保存当前窗口的字符信息。

对窗口的操作包括以下两个：

* 扩充窗口：将窗口的右端点尽力向右扩展，直至到包含所有标准表中的字符（窗口中的每个有效字符的数量大于等于标准表中对应字符的数量），一旦窗口中的有效字符的总数达到字典字符串的长度，就停止扩充。
* 收缩窗口：当扩充窗口结束时，表明当前窗口已经至少包含了标准表中的所有字符（以及相应的数量），但这时窗口还不是最小的，因为在扩充窗口的时候，可能对某一个字符串包含了多于标准表中的次数，由于窗口是要连续的，所以只要对左端点进行收缩即可，即将位于最左端的那些出现次数过多的字符进行舍弃，知道舍弃到当前字符在窗口中的出现字数刚好等于该字符在标准表中的次数，则说明窗口左端点已经无法再右移了，收缩窗口完成。然后计算一下当前窗口的长度，与所记录的最短长度进行比较，再进入下一轮的窗口扩充。

实现代码如下：

``` java
public class Solution {
    public String minWindow(String S, String T) {
        int begin = 0, end = 0, minBegin = 0, minSize = S.length(), count = 0;
        HashMap<Character, Integer> stdMap = new HashMap<Character, Integer>();
        HashMap<Character, Integer> map = new HashMap<Character, Integer>();
        for (int i = 0; i < T.length(); i++) {
            char ch = T.charAt(i);
            if (stdMap.containsKey(ch)) {
                stdMap.put(ch, stdMap.get(ch) + 1);
            } else {
                stdMap.put(ch, 1);
            }
            map.put(ch, 0);
        }
        for (end = 0; end < S.length(); end++) {
            char ch = S.charAt(end);
            if (!stdMap.containsKey(ch)) {
                continue;
            }
            if (map.get(ch) < stdMap.get(ch)) {
                count++;
            }
            map.put(ch, map.get(ch) + 1);
            if (count == T.length()) {
                while (true) {
                    char c = S.charAt(begin);
                    if (stdMap.containsKey(c)) {
                        if (map.get(c) > stdMap.get(c)) {
                            map.put(c, map.get(c) - 1);
                        } else {
                            break;
                        }
                    }
                    begin++;
                }
                if (end - begin + 1 < minSize) {
                    minSize = end - begin + 1;
                    minBegin = begin;
                }
            }
        }
        return count == T.length() ? S.substring(minBegin, minBegin + minSize) : "";
    }
}
```