---
layout: post
title: "Longest Valid Parentheses@LeetCode"
date: 2015-03-29 11:10
comments: true
tags: LeetCode
---
[Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/)

<!-- more -->

这也是不知道方法前很纠结，知道方法之后很简单就能搞定的题目。解题的核心就是维护一个左括号栈和站内元素起点索引，之所以要维护一个匹配起始索引，是因为在匹配过程中先前已经匹配的元素可能已经出栈了，其索引无法获取所以要提前记录下来，在维护的过程中可能遇到两种情况：

1. 当前字符是`(`，那么就直接压栈。
2. 当前字符是`)`，那么如果栈内为空，就说明当前匹配失效且不是起始索引移动起始索引；如果栈内不为空，则先弹出栈顶元素，如果此时栈内为空了，说明当前已经匹配到了起始索引出，则从起始索引开始计算长度，反之，说明当前还在连续匹配串内，那么只要从当前栈顶元素索引开始计算长度即可。


具体实现代码：
	
```java
public class Solution {
    public int longestValidParentheses(String s) {
        Stack<Integer> left = new Stack<Integer>();
        int max = 0, matchBegin = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                left.push(i);
            } else {
                if (left.isEmpty()) {
                    matchBegin = i + 1;
                } else {
                    left.pop();
                    if (left.isEmpty()) {
                        max = Math.max(max, i - matchBegin + 1);
                    } else {
                        max = Math.max(max, i - left.peek());
                    }
                }
            }
        }
        return max;
    }
}
```