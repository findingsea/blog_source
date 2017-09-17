---
layout: post
title: "Reverse Nodes in k-Group@LeetCode"
date: 2015-03-26 20:44
comments: true
tags: LeetCode
---
[Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)

<!-- more -->

翻转链表的升级版，由于在以前阿里的面试中遇到过，所以特别在意，这次写题解之前又重新把原来通过的代码优化了一下。

其实这题很简单，知道了翻转链表的通用写法之后，解这一题其实就是循环翻转的过程（知道最后一个group长度不足）。

先介绍下翻转链表的写法：
1. 首先设置一个前置节点，将前置节点的`next`设置为头节点，以头节点为当前节点，开始循环
2. 将当前节点的next赋给一个临时节点，然后将当前节点的`next`指向前置节点，随后依次位移前置节点指针和当前节点指针：前置节点指针指向当前节点，当前节点指针指向临时节点，这样就完成了一次循环
3. 当前置节点指针指向尾节点时，循环结束

有个这个翻转函数之后，只要对链表进行循环，当计数长度不`k`时，指针继续前进；当计数长度到达k时，将头尾节点作为参数传入翻转函数进行翻转，然后重新拼接到原链表中。直至到达链表末尾。

实现代码：

``` java
public class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        if (k == 1 || head == null || head.next == null)
            return head;
        ListNode first = head, last = head;
        ListNode preHead = new ListNode(-1);
        preHead.next = head;
        ListNode preGroup = preHead, nextGroup = preHead;
        int count = 1;
        while (last != null) {
            if (count == k) {
                nextGroup = last.next;
                reverseList(first, last);
                preGroup.next = last;
                preGroup = first;
                first.next = nextGroup;
                first = nextGroup;
                last = nextGroup;
                count = 1;
                continue;
            }
            last = last.next;
            count++;
        }
        return preHead.next;
    }

    private void reverseList(ListNode head, ListNode tail) {
        ListNode pre = new ListNode(-1), node = head;
        pre.next = head;
        while (pre != tail) {
            ListNode temp = node.next;
            node.next = pre;
            pre = node;
            node = temp;
        }
    }
}
```