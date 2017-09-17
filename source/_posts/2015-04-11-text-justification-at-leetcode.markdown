---
layout: post
title: "Text Justification@LeetCode"
date: 2015-04-11 10:47
comments: true
tags: LeetCode
---
## [Text Justification](https://leetcode.com/problems/text-justification/)

这一题主要考察的还是对边界条件的控制，并没有太高深的算法，但是编写的难度不低，而且想一次通过非常难。

<!-- more -->

我采用的办法：

首先，筛选出一行中应该包括的单词，这里要考虑空格还要占用掉的长度，也就是除了当前的总长度之外，还需要记录下纯单词的长度，这样方便之后生成相应的空格。

然后，当当前记录的长度大于等于额定长度之后，就需要对当前内容进行格式化。单词的索引很容易算出，难点在于空格，因为空格需要遵循以下两个规则：
1. 每两个单词之间必须要有一个空格
2. 单词实现左右对齐之后，空格应该尽量平均，并且有需要的话越往左空格应该越多
基于这两条原则，我的办法是先计算平均空格长度，那么所有的空格要么是等于平均空格长度，要么是等于平均空格长度加1，在拼接空格的时候，计算当前剩余的空格总数以每个位置填入平均空格数是否可以填满，以此来判断具体当前位置需要填入的空格数。

实现代码：

``` java
public class Solution {
    public List<String> fullJustify(String[] words, int L) {
        int index = 0, last = 0, count = 0, wordsLenCount = 0, wordsCount = 0;
        List<String> result = new ArrayList<String>();
        if (L == 0) {
            result.add(words[0]);
            return result;
        }
        while (index < words.length) {
            if (count + words[index].length() >= L) {
                int spaceCount;
                int aveSlot = 0;
                if (count + words[index].length() > L) {
                    spaceCount = L - wordsLenCount;
                    if (wordsCount > 1)
                        aveSlot = spaceCount / (wordsCount - 1);
                    index--;
                } else {
                    wordsLenCount += words[index].length();
                    wordsCount++;
                    spaceCount = L - wordsLenCount;
                    if (wordsCount > 1)
                        aveSlot = spaceCount / (wordsCount - 1);
                }
                StringBuffer buffer = new StringBuffer("");
                for (int i = index - wordsCount + 1; i <= index; i++) {
                    buffer.append(words[i]);
                    int sCount;
                    if (wordsCount > 1) {
                        if (spaceCount % aveSlot == 0 && spaceCount / aveSlot == wordsCount - 1) {
                            sCount = aveSlot;
                        } else {
                            sCount = aveSlot + 1;
                        }
                        spaceCount -= sCount;
                        wordsCount--;
                    } else {
                        sCount = spaceCount;
                    }
                    for (int j = 0; j < sCount; j++) {
                        buffer.append(' ');
                    }
                }
                result.add(buffer.toString());
                count = 0;
                wordsLenCount = 0;
                wordsCount = 0;
                last = index + 1;
            } else {
                count += words[index].length() + 1;
                wordsLenCount += words[index].length();
                wordsCount++;
            }
            index++;
        }
        if (last < words.length) {
            StringBuffer buffer = new StringBuffer("");
            for (int i = last; i < words.length; i++) {
                buffer.append(words[i]);
                if (words[i].length() > 0)
                    buffer.append(" ");
            }
            for (int i = buffer.length(); i < L; i++) {
                buffer.append(" ");
            }
            result.add(buffer.toString());
        }
        return result;
    }
}
```