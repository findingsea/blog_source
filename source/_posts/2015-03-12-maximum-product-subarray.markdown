---
layout: post
title: "Maximum Product Subarray@LeetCode"
date: 2015-03-12 11:18
comments: true
tags: LeetCode
---
[Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/)

<!-- more -->

一开始题目没有看清楚，以为还是求和，但是这一题其实是求乘积，那么相对于求和的题目，求乘积需要注意的有两点：

* 元素为0的点，只要包含了元素为0的点，那么整段的乘积必为0
* 正负数，不能简单地依靠动态规划的方法做，因为之后的信息对之前的信息是有影响的：i点之前的乘积为负数，但如果之后还有负数，则乘积会变成正数且将大于之前的乘积

解题的思想如下：

1. 以0为界，分割数组，计算每个0之间（以及0和短点之间）的乘积
2. 针对每一段乘积，如果乘积为正数，则直接返回与当前最大值比较；如果乘积为负数，则取最短负数前缀和最短负数后缀（连续的乘积为负的数字段），分别用整段乘积去除之后就能得到该段最大乘积

代码如下：

``` java
public class Solution {
    public int maxProduct(int[] A) {
        int max = A[0], length = A.length;
        int begin = 0, end, product;
        while (begin < length && A[begin] == 0) {
            begin++;
        }
        if (begin == length)
            return 0;
        end = begin + 1;
        product = A[begin];
        while (end < length) {
            if (A[end] == 0) {
                max = Math.max(max, Math.max(0, countMax(begin, end, A, product)));
                begin = end + 1;
                while (begin < length && A[begin] == 0) {
                    begin++;
                }
                if (begin == length)
                    break;
                product = A[begin];
                end = begin + 1;
            } else {
                product *= A[end++];
            }
        }
        if (begin != length)
            max = Math.max(max, countMax(begin, length, A, product));
        return max;
    }

    private int countMax(int begin, int end, int[] A, int product) {
        if (product > 0 || end - begin == 1) {
            return product;
        }
        int index = begin;
        int preProduct = 1, sufProduct = 1;
        while (index < end - 1 && A[index] > 0) {
            preProduct *= A[index];
            index++;
        }
        preProduct *= A[index];
        index = end - 1;
        while (begin < index && A[index] > 0) {
            sufProduct *= A[index];
            index--;
        }
        sufProduct *= A[index];
        return Math.max(product / preProduct, product / sufProduct);
    }
}
```