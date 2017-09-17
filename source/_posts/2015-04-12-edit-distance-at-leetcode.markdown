---
layout: post
title: "Edit Distance@LeetCode"
date: 2015-04-12 14:47
comments: true
tags: LeetCode
---
## [Edit Distance](https://leetcode.com/problems/edit-distance/)

<!-- more -->

典型的动态规划题目。维护一个二维数组`dis[][]`，`dis[i][j]`表示：`word1`的前`i`个元素与`word2`的前`j`个元素的`edit distance`值。递推关系为：


* 当`word1[i] == word2[j]`，`dis[i][j] = dis[i][j - 1]`。
* 当`word[i] != word2[j]`，`dis[i][j] = min(dis[i - 1][j - 1], dis[i] [j - 1], dis[i - 1][j]) + 1`。

解释一下第二种情况下的递推公式：

* `dis[i][j] = dis[i - 1][j - 1] + 1`意味着替换字符
* `dis[i][j] = dis[i - 1][j] + 1`意味着删除字符
* `dis[i][j] = dis[i][j - 1] + 1`意味着插入字符

实现代码：

``` java
public class Solution {
    public int minDistance(String word1, String word2) {
        int[] result = new int[word1.length() + 1];
        for (int i = 0; i < result.length; i++)
            result[i] = i;
        for (int i = 0; i < word2.length(); i++) {
            int[] newResult = new int[result.length];
            newResult[0] = i + 1;
            for (int j = 0; j < word1.length(); j++) {
                if (word1.charAt(j) == word2.charAt(i)) {
                    newResult[j + 1] = result[j];
                } else {
                    newResult[j + 1]  = Math.min(result[j], Math.min(result[j + 1], newResult[j])) + 1;
                }
            }
            result = newResult;
        }
        return result[result.length - 1];
    }
}
```