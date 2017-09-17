---
layout: post
title: "Python异号除法需要注意的问题"
date: 2014-03-12 12:32
comments: true
tags: [Python]
---
Python在整型除法上的运算规则和别的语言不同，对于被除数和除数同号的情况下，大部分语言的处理方法都是相似的：计算结果向下取整。但对于被除数和除数异号的情况下，像Java，C++等语言采用向上取整，而Python仍然采用向下取整。这在有些应用场景上会产生和我们预期不同的结果。

<!-- more -->
对于同号的情况，大部分语言的处理方法都相似：

```
In [1]: 10 / 3
Out[1]: 3

In [2]: 1 / 100
Out[2]: 0
```

对于异号的情况，Python仍然采用向下取整：
```
In [3]: -10 / 3
Out[3]: -4

In [4]: -1 / 100
Out[4]: -1
```
而其他语言（Java，C++）的计算结果为-3和0。

这一点区别在[LeetCode OJ](http://oj.leetcode.com)的[Evaluate Reverse Polish Notation](http://oj.leetcode.com/problems/evaluate-reverse-polish-notation/)体现地尤其明显。对于该题可采用如下策略：
```python
if num1 * num2 <0:
    result.append(-(-num1 / num2))
```
[Evaluate Reverse Polish Notation](http://oj.leetcode.com/problems/evaluate-reverse-polish-notation/)完整的Python代码如下：

```python
class Solution:
    # @param tokens, a list of string
    # @return an integer
    def evalRPN(self, tokens):
        result = []
        for i in range(len(tokens)):
            tk = tokens[i]
            if tk not in ['+', '-', '*', '/']:
                result.append(int(tk))
            else:
                num2 = result.pop()
                num1 = result.pop()
                if tk == '+':
                    result.append(num1 + num2)
                elif tk == '-':
                    result.append(num1 - num2)
                elif tk == '*':
                    result.append(num1 * num2)
                elif tk == '/':
                    if num1 * num2 <0:
                        result.append(-(-num1 / num2))
                    else:
                        result.append(num1 / num2)
        return result[0]
```