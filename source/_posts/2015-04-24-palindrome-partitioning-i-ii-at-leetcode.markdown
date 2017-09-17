---
layout: post
title: "Palindrome Partitioning I II@LeetCode"
date: 2015-04-24 09:01
comments: true
tags: LeetCode
---
## [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)

<!-- more -->

递归解法。遍历每一种组合情况，其实这样的解法并不是很高效，但是还是是可以顺利`AC`。

实现代码：

``` java
public class Solution {
    public List<List<String>> partition(String s) {
        List<List<String>> result = new LinkedList<List<String>>();
        generate(result, new LinkedList<String>(), s);
        return result;
    }

    private void generate(List<List<String>> result, LinkedList<String> list, String s) {
        if (s.length() == 0) {
            List<String> res = new LinkedList<String>(list);
            result.add(res);
            return;
        }
        int length = s.length();
        for (int i = 1; i <= length; i++) {
            String sub = s.substring(0, i);
            if (isPalindrome(sub)) {
                list.add(sub);
                generate(result, list, s.substring(i, length));
                list.remove(list.size() - 1);
            }
        }
    }

    private boolean isPalindrome(String s) {
        int len = s.length();
        for (int i = 0; i < len / 2; i++) {
            if (s.charAt(i) != s.charAt(len - 1 - i)) {
                return false;
            }
        }
        return true;
    }
}
```

## [Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/)

动态规划。维护一个`boolean[][] isPalindrome`二维数组，`isPalindrome[i][j]`表示`s.substring(i, j)`是否为回文串。递推公式：检查`s.charAt(begin)`和`s.charAt(end)`是否相等，如果相等就检查`isPalindrome[begin + 1][end - 1]`的值，也就是对一个`isPalindrome[begin][end]`的赋值复杂度是`O(1)`。另外维护一个`numOfCuts`数组，`numOfCuts[i]`表示分割`s.substring(1, i)`最少需要几个`cut`，这个值需要在每次找到一个回文串的时候就相应的更新一遍。

简单来说，就是找出所有的回文串，找的方法就是先判断当前起点和终点字符串是否相等，如果相等就进一步检查起点和终点之间的字符串是否是回文的，找到了回文串之后表示从当前起点前的位置到当前终点只需切一刀即可分割，以此与已有的分割方案进行比较即可。

实现代码：

``` java
public class Solution {

    public int minCut(String s) {
        int length = s.length();
        boolean[][] isPalindrome = new boolean[length][length];
        int[] numOfCuts = new int[length + 1];
        numOfCuts[0] = -1;
        for (int i = 1; i < length + 1; i++) {
            numOfCuts[i] = numOfCuts[i - 1] + 1;
        }
        for (int end = 0; end < length; end++) {
            for (int begin = end; begin >= 0; begin--) {
                if (s.charAt(begin) == s.charAt(end) && (end - begin < 2 || isPalindrome[begin + 1][end - 1])) {
                    isPalindrome[begin][end] = true;
                    numOfCuts[end + 1] = Math.min(numOfCuts[end + 1], numOfCuts[begin] + 1);
                }
            }
        }
        return numOfCuts[numOfCuts.length - 1];
    }
}
```