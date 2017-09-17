---
layout: post
title: "Interleaving String@LeetCode"
date: 2015-04-17 10:18
comments: true
tags: LeetCode
---
## [Interleaving String](https://leetcode.com/problems/interleaving-string/)

<!-- more -->

动态规划题。用一个二维（也可以简化成一维的）`boolean`数组`match[i][j]`来表示`str3.substring(0, i + j)`能不能由`str1.substring(0, i)`和`str2.substring(0, j)`组成，递推公式：

```
match[i][j] = (match[i - 1][j] && str1.charAt(i - 1) == str3.charAt(i + j)) || (match[i][j - 1] && str2.charAt(j - 1) == str3.charAt(i + j))
```

需要注意的是，这里的`match`中，第一行代表了用`str1`去组成`str3`的情况，而第一列代表了用`str2`去组成`str3`的情况，这是为了方便循环中的递推计算，所以要注意`match`中的索引和`str1`以及`str2`中的索引并不是直接对应的。

最后，怎么把这个二维的`DP`优化成一维的呢，其实只要记住一个简单的道理：在递推公式中，`dp[i][j]`的计算不依赖`dp[i - 1][j - 1]`，那么这个二维`DP`就可以优化成一维的。因为在计算`dp[i][j]`时，`dp[i - 1][j]`和`dp[i][j - 1]`本来就是已知的。那么如果计算需要依赖`dp[i - 1][j - 1]`，还能优化吗？形式上可以，那就是在循环内用两个数组，前一个数组记录`dp`中上一行的结果，后一个数组用来计算当前行的，但其实这个方法并没有对内存进行太多优化，因为Java对于垃圾回收并不是发生在对象引用计数归0的那一刻，而是会选取一个时间进行统一回收，所以这种优化，该分配的内容一样还是分配出去了，并且本身一维数组的直观程度不如二维来得好，所以这种优化并不提倡。

实现代码：

``` java
public class Solution {
    public boolean isInterleave(String s1, String s2, String s3) {
        if (s1.length() + s2.length() != s3.length())
            return false;
        if (s1.length() == 0 || s2.length() == 0)
            return s3.equals(s1) || s3.equals(s2);
        boolean[] match = new boolean[s1.length() + 1];
        match[0] = false;
        for (int i = 1; i <= s1.length(); i++) {
            match[i] = s1.charAt(i - 1) == s3.charAt(i - 1);
        }
        for (int i = 0; i < s2.length(); i++) {
            match[0] = s3.charAt(i) == s2.charAt(i);
            for (int j = 1;j < match.length; j++) {
                match[j] = (match[j - 1] && s1.charAt(j - 1) == s3.charAt(i + j))
                        || (match[j] && s2.charAt(i) == s3.charAt(i + j));
            }
        }
        return match[match.length - 1];
    }
}
```