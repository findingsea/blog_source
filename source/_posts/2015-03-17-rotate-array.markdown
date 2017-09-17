---
layout: post
title: "Rotate Array@LeetCode"
date: 2015-03-17 13:31
comments: true
tags: LeetCode
---
[Rotate Array](https://leetcode.com/problems/rotate-array/)

这题当然有很朴素的解法，例如利用`k%nums.length`次循环每次循环都将原字符串向右推移1位，或者直接计算出每个字符最终所应该在的位置直接进行赋值。

<!-- more -->

那么这两种方法，前者复杂度太高，或者不够清晰简单。

我选用的是在[编程珠玑](http://book.douban.com/subject/3227098/)中提到的翻转方法，比如我们的输入是`[1,2,3,4,5,6,7]`和`k = 3`，那么翻转需要如下三部：

1. 翻转`[1,2,3,4]`部分，得到`[4,3,2,1,5,6,7]`
2. 翻转`[5,6,7]`部分，得到`[4,3,2,1,7,6,5]`
3. 翻转整个数组，得到`[5,6,7,1,2,3,4]`，也就是最终答案

可以看到这种方法，只要写一个翻转数组的函数，然后调用三次即可。

实现代码如下：

``` java
public class Solution {
    public void rotate(int[] nums, int k) {
        if (nums.length == 0 || nums.length == 1 || k % nums.length == 0)
            return;
        k %= nums.length;
        int length = nums.length;
        reverse(nums, 0, length - k - 1);
        reverse(nums, length - k, length - 1);
        reverse(nums, 0, length - 1);
    }

    private void reverse(int[] nums, int begin, int end) {
        for (int i = 0; i < (end - begin + 1) / 2; i++) {
            int temp = nums[begin + i];
            nums[begin + i] = nums[end - i];
            nums[end - i] = temp;
        }
    }
}
```