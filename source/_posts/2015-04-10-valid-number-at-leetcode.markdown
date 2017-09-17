---
layout: post
title: "Valid Number@LeetCode"
date: 2015-04-10 09:52
comments: true
tags: LeetCode
---
## [Valid Number](https://leetcode.com/problems/valid-number/)

这一题主要的难点还是要考虑的边界条件太多，而且有些情况下，指数和底数需要考虑的还不一样，就更增加了难度。

<!-- more -->

我的做法如下：

首先，对字符串左右去空格，然后根据字符`e`来进行划分，`e`之前的归为底数，`e`之后的归为指数。这个时候在使用Java的`split()`函数时要注意的时当分隔符是原字符串的首字母时，拆分之后的数组的第一个元素会是空字符串。所以，其实我们在去空格之后就可以对原字串做一些判断，直接筛选掉一些明显错误的情况。

然后，对指底数字符串和指数字符串分别进行遍历，那么遍历过程中最需要注意的就是对小数点`.`的检测。专门设置一个`boolean`变量还表示当前检测的字符串是不是小数，在第一次检测到小数点`.`且其后还有内容的时候，对这个值赋`true`，当再一次出现小数点的时候即可判断当前字符串不合法。还有一点就是遍历前先检测符号，这一点不需多说。

实现代码：

``` java
public class Solution {
    public boolean isNumber(String s) {
        boolean result = true;
        s = s.trim();
        if (s.length() == 0 || s.charAt(0) == 'e' || s.charAt(s.length() - 1) == 'e' || splitArr.length > 2)
            return false;
        String[] splitArr = s.split("e");
        for (int k = 0; k < splitArr.length; k++) {
            String str = splitArr[k];
            boolean isDecimal = false;
            if (str.charAt(0) == '-' || str.charAt(0) == '+')
                str = str.substring(1, str.length());
            if (str.length() == 0) {
                result = false;
                break;
            }
            for (int i = 0; i < str.length(); i++) {
                if ('0' <= str.charAt(i) && str.charAt(i) <= '9')
                    continue;
                else if (str.charAt(i) == '.' && !isDecimal) {
                    if (k != 1 && str.length() > 1) {
                        isDecimal = true;
                    }
                    else {
                        result = false;
                        break;
                    }
                }
                else {
                    result = false;
                    break;
                }
            }
            if (!result)
                break;
        }
        return result;
    }
}
```