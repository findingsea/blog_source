---
layout: post
title: "Copy List with Random Pointer@LeetCode"
date: 2015-04-25 13:03
comments: true
tags: LeetCode
---
## [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/)

<!-- more -->

节点中需要拷贝的两个引用是`next`和`random`。`next`引用比较好拷贝，相当直接复制普通列表。而对于`random`则需要目标节点已存在才比较容易些拷贝代码，采用的办法就是构造一个`HashMap`，其中`key`是原节点，`value`是拷贝节点，在拷贝`random`引用的过程中，直接用`map.get(node.random)`来获取相应的目标节点即可。

实现代码：

``` java
/**
 * Definition for singly-linked list with a random pointer.
 * class RandomListNode {
 *     int label;
 *     RandomListNode next, random;
 *     RandomListNode(int x) { this.label = x; }
 * };
 */
public class Solution {
    public RandomListNode copyRandomList(RandomListNode head) {
        if (head == null)
            return null;
        RandomListNode targetNode = head, copyPreHead = new RandomListNode(-1), copyNode = copyPreHead;
        HashMap<RandomListNode, RandomListNode> copiedMap = new HashMap<RandomListNode, RandomListNode>();
        while (targetNode != null) {
            copyNode.next = new RandomListNode(targetNode.label);
            copiedMap.put(targetNode, copyNode.next);
            targetNode = targetNode.next;
            copyNode = copyNode.next;
        }
        targetNode = head;
        copyNode = copyPreHead.next;
        while (targetNode != null) {
            if (targetNode.random != null) {
                copyNode.random = copiedMap.get(targetNode.random);
            }
            targetNode = targetNode.next;
            copyNode = copyNode.next;
        }
        return copyPreHead.next;
    }
}
```