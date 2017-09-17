---
layout: post
title: "Maximum Gap@LeetCode"
date: 2015-05-06 09:01
comments: true
tags: LeetCode
---
## [Maximum Gap](https://leetcode.com/problems/maximum-gap/)

<!-- more -->

要求连续元素的最大差值，那必然要排序，但是又要求在`O(n)`的复杂度内完成，自然就想到了桶排序。维护`left`和`right`两个数组，`left[i]`表示第`i`个桶的最左端元素，`right[i]`表示第`i`个桶的最右端点元素。除最后一个桶之外，每个桶都是前闭后开，最后一个桶是前闭后闭。当元素落到相应的桶内就更新相应桶的最左最右元素值，当所有元素都放入桶中之后，对桶区间进行遍历，计算相邻桶的前桶最大元素和后桶最小元素的差值，最大差值即是题目所求。

这里需要注意的是，对于最小值为`min`，最大值为`max`，个数为`n`的数组，相邻元素的最大差值必然大于等于`(max - min) / (n - 1)`，所以用这个值作为桶区间的长度，这样可以保证最大差值必然出现在桶和桶之间。特别考虑最大差值等于`(max - min) / (n - 1)`的情况，此时数组中每个相邻元素的差值都是`(max - min) / (n - 1)`，那么每个桶内只要一个元素，同样最大差值出现在桶和桶之间，之前的计算方法依然适用。

``` java
public class Solution {
    public int maximumGap(int[] num) {
        if (num.length < 2)
            return 0;
        int minNum = num[0], maxNum = num[0], lengthOfNum = num.length;
        for (int i = 1; i < lengthOfNum; i++) {
            minNum = Math.min(minNum, num[i]);
            maxNum = Math.max(maxNum, num[i]);
        }
        int step = (maxNum - minNum) / (lengthOfNum - 1);
        step = step == 0 ? 1 : step;
        int[] left = new int[(maxNum - minNum) / step + 1];
        int[] right = new int[(maxNum - minNum) / step + 1];
        for (int i = 0; i < lengthOfNum; i++) {
            int range = (num[i] - minNum) / step;
            if (range == left.length)
                range--;
            left[range] = left[range] == 0 ? num[i] : Math.min(left[range], num[i]);
            right[range] = right[range] == 0 ? num[i] : Math.max(right[range], num[i]);
        }
        int maxGap = 0, leftMax = 0, rightMin = 0;
        for (int i = 0; i < left.length; i++) {
            if (left[i] == 0 && right[i] == 0)
                continue;
            if (leftMax == 0) {
                leftMax = right[i];
                continue;
            }
            rightMin = left[i];
            maxGap = Math.max(maxGap, rightMin - leftMax);
            leftMax = right[i];
        }
        return maxGap;
    }
}
```