---
layout: post
title: "Distinct Subsequences@LeetCode"
date: 2015-04-19 14:46
comments: true
tags: LeetCode
---
## [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/)

<!-- more -->

动态规划题。先用二维动态规划的思路解释下：设`match`是动态规划表，其中`match[i][j]`表示`S.substring(0, i)`对`T.substring(0, j)`有几种组成方式，递推公式为：

* 若`S.charAt(i - 1) == T.charAt(j - )`，则`match[[i][j] = match[i - 1][j - 1] + match[i - 1][j]`。
* 若`S.charAt(i - 1) != T.charAt(j - 1)`，则`match[i][j] = match[i - 1][j]`。

二维动态规划数组的实现代码如下：

``` java
public class Solution {
    public int numDistinct(String S, String T) {
        if (T.length() == 0) return 1;
        int rows = S.length() + 1, cols = T.length() + 1;
        int[][] dp = new int[rows][cols];
        dp[0][0] = 1;
        for (int i = 1; i < rows; i++) {
            dp[i][0] = 1;
            for (int j = 1; j < cols; j++) {
                if (S.charAt(i - 1) == T.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j];
                } else {
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }
        return dp[rows - 1][cols - 1];
    }
}
```

那么能不能改成一维数组？

仔细看一下递推公式，计算`dp[i][j]`需要的额外信息只有左边一格的旧制，那么就直接用`hold`将其保存起来不就好了，于是就可以把二维的动态规划数组优化成了一维的，对空间复杂度进行了改进。同时，进一步改进在于如果对于`T`中的某一位，前一位的构造已经失败（也就是构造到前一位的方位数为0），那么也就不用计算当前位了，直接进入下一层循环即可。

一维动态规划数组实现代码：

``` java
public class Solution {
    public int numDistinct(String S, String T) {
        if (T.length() == 0) {
            return 1;
        }
        int[] dp = new int[T.length() + 1];
        dp[0] = 1;
        for (int i = 0; i < S.length(); i++) {
            int hold = 1;
            for (int j = 1; j < dp.length; j++) {
                if (dp[j - 1] == 0)
                    break;
                int h = dp[j];
                if (S.charAt(i) == T.charAt(j - 1)) {
                    dp[j] = hold + dp[j];
                }
                hold = h;
            }
        }
        return dp[dp.length - 1];
    }
}
```