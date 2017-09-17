---
layout: post
title: "Insert Interval@LeetCode"
date: 2015-04-08 12:04
comments: true
tags: LeetCode
---
## [Insert Interval](https://leetcode.com/problems/insert-interval/)

<!-- more -->

这道题我今天重新看我以前提交的代码时，差点看吐了，巨复杂无比，先上代码，然后再分析为什么我当初会这样写。

``` java
public class Solution {
    public List<Interval> insert(List<Interval> intervals, Interval newInterval) {
        Comparator<Interval> comparator = new Comparator<Interval>() {
            @Override
            public int compare(Interval o1, Interval o2) {
                if (o1.start == o2.start)
                    return o1.end - o2.end;
                return o1.start - o2.start;
            }
        };
        Collections.sort(intervals, comparator);
        boolean inserted = false;
        int index = 0;
        while (index < intervals.size()) {
            int re = cmpInterval(newInterval, intervals.get(index));
            switch (cmpInterval(newInterval, intervals.get(index))) {
                case -2:
                    if ((0 < index && intervals.get(index - 1).end < newInterval.start) || index == 0)
                        intervals.add(index, newInterval);
                    inserted = true;
                    break;
                case -1:
                    intervals.get(index).start = newInterval.start;
                    if (0 < index && intervals.get(index - 1).end >= intervals.get(index).start) {
                        intervals.get(index - 1).end = Math.max(intervals.get(index).end, intervals.get(index - 1).end);
                        intervals.remove(intervals.get(index));
                    }
                    inserted = true;
                    break;
                case 0:
                    inserted = true;
                    break;
                case 1:
                    intervals.get(index).end = newInterval.end;
                    index++;
                    break;
                case 2:
                    if (index == intervals.size() - 1) {
                        intervals.add(newInterval);
                        inserted = true;
                    } else {
                        index++;
                    }
                    break;
                case 3:
                    intervals.remove(intervals.get(index));
                    break;
                default:
                    continue;
            }
            if (inserted)
                break;
        }
        if (intervals.size() == 0 || intervals.get(intervals.size() - 1).end < newInterval.start) {
            intervals.add(newInterval);
        }
        return intervals;
    }

    public int cmpInterval(Interval toInsert, Interval interval) {
        if (toInsert.start < interval.start) {
            if (toInsert.end < interval.start)
                return -2;
            else if (interval.start <= toInsert.end && toInsert.end <= interval.end)
                return -1;
            else
                return 3;
        } else if (interval.start <= toInsert.start && toInsert.start <= interval.end) {
            if (interval.start <= toInsert.end && toInsert.end <= interval.end)
                return 0;
            else
                return 1;
        } else {
            return 2;
        }
    }
}
```

我当时的想法非常朴素，就是用带插入的区间去原区间列表中一个个比较，问题就出在这个比较的结果会很多，可以看到我代码里面用了5个值来代表5中不同的比较结果（这里的前后是以数轴为坐标）：

* -2：待插入区间位于当前区间前方，且无重叠部分
* -1：待插入区间位于当前区间前方，但有重叠部分
* 3： 待插入区间包含当前区间
* 0：待插入区间包含于当前区间
* 1：待插入区间位于当前区间后方，但有重叠部分
* 2：待插入区间位于当前区间后方，且无重叠部分

是不是看着都蛋疼，的确，重新看代码的时候，我也是花了好久才理清这所有情况，这样的代码可读性实在太差，而且是在太复杂。其实这题非常非常容易想到思路，尤其是当你已经做过前一题[Merge Intervals](https://leetcode.com/problems/merge-intervals/)，只要稍微细看就知道这题只是前一题的稍微变形，解决的方法只要把新区间插入到原区间数组中，然后重新合并下即可，具体的合并方法在[Merge Intervals@LeetCode](http://segmentfault.com/a/1190000002653068)中给出。

本题的具体的实现代码如下：

``` java
public class Solution {
    public List<Interval> insert(List<Interval> intervals, Interval newInterval) {
        List<Interval> result = new ArrayList<Interval>();
        if (intervals == null) return result;
        intervals.add(newInterval);
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
                Interval interval1 = new Interval(interval.start, interval.end);
                result.add(interval1);
            } else {
                result.get(last - 1).end = Math.max(interval.end, result.get(last - 1).end);
            }
        }
        return result;
    }
}
```