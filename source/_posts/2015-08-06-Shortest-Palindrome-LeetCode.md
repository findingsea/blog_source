title: Shortest Palindrome@LeetCode（以及关于KMP的理解）
date: 2015-08-06 15:09:08
tags: LeetCode
---
## [Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/)

用Java暴力是可以过的，思路也很简单：补充完成之后的回文串中心必定在原字符串中，所以原字符串以第一个字符为起点必然存在至少一个回文串（长度可以为1），那么任务就变为找到原字符串中以第一个字符为起点最长的回文串，找到之后剩下的工作就是把剩余部分的翻转补充到原字符串头部即可。

<!-- more -->

这样代码逻辑就很简单，就是从原字符串的头部开始截取子串，长度递减，直到获取到第一个是回文串的子串，此时就找到了需要截断的部分，从该位置开始到原字符串末尾就是需要截取并翻转拼接的部分。算法复杂度是`O(n^2)`。

实现代码：

``` java
public class Solution {
    public String shortestPalindrome(String s) {
        if (s == null || s.length() == 0 || s.length() == 1) return s;
        int len = s.length(), tail = len;
        StringBuilder builder = new StringBuilder();
        while (1 < tail) {
            if (isPalindrome(s.substring(0, tail))) {
                builder = builder.append(s.substring(tail, len)).reverse();
                break;
            }
            tail--;
        }
        if (builder.length() == 0) {
            builder = builder.append(s.substring(tail, len)).reverse();
        }
        return builder.append(s).toString();
    }

    private boolean isPalindrome(String str) {
        int len = str.length();
        for (int i = 0; i < len / 2; i++) {
            if (str.charAt(i) != str.charAt(len - i - 1))
                return false;
        }
        return true;
    }
}
```

LeetCode做多了也就知道`O(n^2)`的算法必然有改进版，自己思考了下没有悟出来，就参考了这篇文章：[[LeetCode] Shortest Palindrome 最短回文串](http://www.cnblogs.com/grandyang/p/4523624.html)。

其实思路也很简单：

1. 求字符串`s`的翻转`s_rev`
2. 将两个字符串进行拼接：`{s}#{s_rev}`
3. 找出新字符串中最长公共前缀后缀长度`comLen`
4. `s_rev.substring(0, s.length() - comLen)`就是在原字符串头部插入的子串部分

举个例子：

对于字符串`s`：`babcd`，先求`rev_s`：`dcbaba`，拼接之后：`babcd#dcbaba`。上文已经解释过，`s`的前缀必然是一个回文串（长度可能为1），任务就是求这个回文串的最长长度，因此拼接之后的`{s}#{s_rev}`必然有公共前缀后缀，任务就是求这个公共前缀后缀的最长长度，那么这个时候就需要祭出KMP算法了。有了解的同学，估计一看就看出这个就是求KMP里的`next`数组。由于之前学KMP的时候也只学了个一知半解，所以这次又重新学习了下[从头到尾彻底理解KMP（2014年8月22日版）](http://blog.csdn.net/v_july_v/article/details/7041827)，这下对KMP又有更好的理解了。

详细的KMP算法上面提到的文章里讲的非常详细，就不从头说了。这里讲一讲我之前一直困惑现在理解了的点。

对于KMP算法，核心的地方就是求`next`数组，而求`next`数组中比较难理解的地方就是当当前位置的字符和目标字符不匹配的时候。对于字符串`s`，已经有`p[0]`到`p[i-1]`，且`p[i-1]=j`，求`p[i]`（`p`即`next`数组，其中`p[k]`表示从`0`到`k`位置为止公共前缀后缀的长度，例如：`abacaba`，公共前缀后缀长度是3，当`p[k]=m`则表示`s.substring(0,m)`和`s.substring(k-m+1,k+1)`是相等的）：

1. 若`s[i]=s[j]`，也就是当前字符延续了之前的公共前缀后缀，那么`p[i]=p[i-1]+1`即可
2. 若`s[i]!=s[j]`，即`s.substring(0,j)`和`s.substring(i-j+1,i+1)`是不匹配的，但是仍然可能存在`s.substring(0,x)`和`s.substring(i-x+1,i+1)`，这一点就是我以前最不能理解的地方，这次结题的经历加深了我这部分的理解。

到目前位置，期望`i`位置的最长公共前缀后缀为`j+1`的期望已经失败，那我是否可以期望下缩短长度之后能有匹配的公共前缀后缀呢？答案是肯定的，因为对于位置`i-1`来说，其实是可能存在多个公共前缀后缀的，只是`p[i-1]`只记录其中最长的，那么次长的是多少呢，答案就在`p[j-1]`里。对于位置`i-1`来说，已知`0`到`j-1`的子串和`i-j+1`到`i-1`子串是相等的，而对于位置`j-1`来说，从`0`到`p[j-1]-1`的子串和从`j-p[j-1]`到`j-1`的子串是相同的，更进一步和`i-p[j-1]`到`i-1`的子串也是相同的，那如果现在比较一下`i`和`p[j-1]`是否相等同样可以求出最长公共前缀后缀的值（因为`p`中记录是到每个位置为止的最长公共前缀后缀，所以这样每次递推下去每次得到都是当前可能的最长公共前缀后缀）。

梳理一下，就是对于位置`i-1`而言，公共前缀后缀的长度依次为：`p[i-1]`,`p[p[i-1]-1]`,`p[p[p[i-1]-1]-1]`,……。在此基础上，对于位置`i`而言，只要比对某几个特定的位置，看`s[i]`是否能符合条件（即是否和当前公共前缀后缀后的第一个字符相等）就能求得`p[i]`的值。当然，如果比对某个位置的时候`p[x]`已经为`0`，那么就可以马上结束比较跳出循环，然后只要和首字母比对下就行了（因为这种情况说明可能的公共前缀后缀都已经被比对完了，`s[i]`依然不符合条件，那么只能从头开始了）。

应用了KMP之后的实现代码：

``` java
public class Solution {
    public String shortestPalindrome(String s) {
        StringBuilder builder = new StringBuilder(s);
        return builder.reverse().substring(0, s.length() - getCommonLength(s)) + s;
    }

    private int getCommonLength(String str) {
        StringBuilder builder = new StringBuilder(str);
        String rev = new StringBuilder(str).reverse().toString();
        builder.append("#").append(rev);
        int[] p = new int[builder.length()];
        for (int i = 1; i < p.length; i++) {
            int j = p[i - 1];
            while (j > 0 && builder.charAt(i) != builder.charAt(j)) j = p[j - 1];
            p[i] = j == 0 ? (builder.charAt(i) == builder.charAt(0) ? 1 : 0) : j + 1;
        }
        return p[p.length - 1];
    }
}
```