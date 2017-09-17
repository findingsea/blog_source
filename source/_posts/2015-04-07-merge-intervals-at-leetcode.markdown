---
layout: post
title: "Merge Intervals@LeetCode"
date: 2015-04-07 09:22
comments: true
tags: LeetCode
---
## [Merge Intervals](https://leetcode.com/problems/merge-intervals/)

<!-- more -->

这也是一题我有点不太能理解为什么可以标为hard的题目。解法其实很直观，就是先对`interval`进行排序，然后遍历一遍。这里需要注意的点有两个：

1. 对`interval`进行排序需要构造一个比较器。

2. 在遍历过程中，如果结果集合为空或者当前`interval`与结果集合中的最后一个`interval`不重叠，那么就直接将当前`interval`直接加入到结果集合中；如果发生了重叠，那么将结果集合的最后一个`interval`的右端点改为当前`interval`的右端点。

实现代码：

``` java
public class Solution {
    public List<Interval> merge(List<Interval> intervals) {
        List<Interval> result = new ArrayList<Interval>();
        Comparator<Interval> comparator = new Comparator<Interval>() {
            @Override
            public int compare(Interval o1, Interval o2) {
                if (o1.start == o2.start) {
                    return o1.end - o2.end;
                }
                return o1.start - o2.start;
            }
        };
        Collections.sort(intervals, comparator);
        for (Interval interval : intervals) {
            int last = result.size();
            if (last == 0 || result.get(last - 1).end < interval.start) {
                Interval newInterval = new Interval(interval.start, interval.end);
                result.add(newInterval);
            } else {
                result.get(last - 1).end = Math.max(interval.end, result.get(last - 1).end);
            }
        }
        return result;
    }
}
```