---
layout: post
title: "Merge k Sorted Lists@LeetCode"
date: 2015-03-26 09:36
comments: true
tags: LeetCode
---
[Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

<!-- more -->

当初看到这题的第一反应是每次都遍历一遍所有头节点，然后选出最小的连接到已排序链表的末尾。这个想法当然能够解决问题，但是性能上肯定是过不去的。因为这样相当于没排序一个元素就是需要比较`m`次（`m`为链表条数），那么最后的复杂度就是`O(nm)`（`n`为元素总数）。

那么更加高效的办法就是对链表进行两两合并，两条链表的合并复杂度为`O(l + k)`，`l`和`k`分别代表了两条链表的元素个数，那么最终的复杂度为`O(n)`（`n`为元素总数）。

实现代码：

``` java
public class Solution {
    public ListNode mergeKLists(List<ListNode> lists) {
        if (lists.isEmpty())
            return null;
        return merge(lists, 0, lists.size() - 1);
    }

    public ListNode merge(List<ListNode> lists, int start, int end) {
        if (start == end)
            return lists.get(start);
        int mid = (start + end) / 2;
        ListNode one = merge(lists, start, mid);
        ListNode two = merge(lists, mid + 1, end);
        return mergeTwoLists(one, two);
    }

    public ListNode mergeTwoLists(ListNode node1, ListNode node2) {
        ListNode head = new ListNode(-1), node = head;
        while (node1 != null && node2 != null) {
            if (node1.val < node2.val) {
                node.next = node1;
                node1 = node1.next;
            } else {
                node.next = node2;
                node2 = node2.next;
            }
            node = node.next;
        }
        if (node1 == null && node2 != null) {
            node.next = node2;
        } else if (node1 != null && node2 == null) {
            node.next = node1;
        }
        return head.next;
    }
}
```