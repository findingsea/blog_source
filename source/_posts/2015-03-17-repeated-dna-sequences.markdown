---
layout: post
title: "Repeated DNA Sequences@LeetCode"
date: 2015-03-17 11:57
comments: true
tags: 
---
[Repeated DNA Sequences](https://leetcode.com/problems/repeated-dna-sequences/)

这一题经典的用二进制序列表示字符串序列，以减少内存消耗的例子。

<!-- more -->

题目中提到DNA序列只包含四种碱基对，分别用A，C，G和T表示，那么就可以用二进制数来分别代表它们：

* A：00
* C：01
* G：10
* T：11

那么形如`ACGT`的DNA序列就可以表示为`00011011`，也就是27。而且这个值对于所有DNA序列都是唯一的，那么就可以把它作为key，出现的次数作为value，将已出现过的key都放入哈希表中即可。

代码如下：

``` java
public class Solution {
    public List<String> findRepeatedDnaSequences(String s) {
        List<String> result = new LinkedList<String>();
        HashMap<Character, Integer> tokenValueMap = new HashMap<Character, Integer>();
        tokenValueMap.put('A', 0);
        tokenValueMap.put('C', 1);
        tokenValueMap.put('G', 2);
        tokenValueMap.put('T', 3);
        HashMap<Integer, Integer> sequenceCountMap = new HashMap<Integer, Integer>();
        int length = s.length();
        for (int index = 0; index <= length - 10; index++) {
            int value = 0;
            for (int i = 0; i < 10; i++) {
                value <<= 2;
                value += tokenValueMap.get(s.charAt(index + i));
            }
            if (!sequenceCountMap.containsKey(value)) {
                sequenceCountMap.put(value, 1);
            } else if (sequenceCountMap.get(value) == 1) {
                sequenceCountMap.put(value, 2);
                result.add(s.substring(index, index + 10));
            }
        }
        return result;
    }
}
```