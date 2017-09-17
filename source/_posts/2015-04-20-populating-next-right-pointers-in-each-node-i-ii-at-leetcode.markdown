---
layout: post
title: "Populating Next Right Pointers in Each Node I II@LeetCode"
date: 2015-04-20 08:23
comments: true
tags: LeetCode
---
## [Populating Next Right Pointers in Each Node I](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/)

<!-- more -->

树的广度优先搜索题。记录下每一层的节点总个数，然后根据广度优先搜索的原则进行遍历，将非`null`节点都加入到队列中，对于同一层中的节点，将其`next`指向队列中的下一个节点即可。

实现代码：

``` java
public class Solution {
    public void connect(TreeLinkNode root) {
        if (root == null)
            return;
        LinkedList<TreeLinkNode> nodes = new LinkedList<TreeLinkNode>();
        nodes.add(root);
        int numOfLevelTotal = 1;
        while (!nodes.isEmpty()) {
            TreeLinkNode treeLinkNode = nodes.poll();
            numOfLevelTotal--;
            if (treeLinkNode.left != null) {
                nodes.add(treeLinkNode.left);
            }
            if (treeLinkNode.right != null) {
                nodes.add(treeLinkNode.right);
            }
            if (numOfLevelTotal > 0) {
                treeLinkNode.next = nodes.getFirst();
            } else {
                numOfLevelTotal = nodes.size();
            }
        }
    }
}
```

## [Populating Next Right Pointers in Each Node II](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)

根据题目来说，这一题和上一次的区别在于：

> What if the given tree could be any binary tree? Would your previous solution still work?

但是由于之前所采用的方法并没有这种局限，所以直接拷贝过来也可以`AC`。

不过这里存在一个问题，仔细看题目里的要求：

> You may only use constant extra space.

理论上，采用队列的话是肯定没办法只是用常数额外内存的，但是LeetCode好像在这件事上没有检测的这么严，起码我写的Java代码和我看到的用递归解决的C++代码都可以通过。

那么如果硬要纠结一下这一条呢？不使用队列怎么做？

其实也不难，只是思路要转变一下，就不能是遍历这一层同时连接这一层，而是遍历这一层连接下一层。那么比较重要的就是要记录每一层的头节点，由于每一层在被遍历的时候是已经连接好了的，所以不必担心找不到节点的问题，如果挨个找寻`next`节点的子节点即可，子节点先内部（相同父节点）连接，然后再连接到总链表中即可。

实现代码：

``` java
public class Solution {
    public void connect(TreeLinkNode root) {
        TreeLinkNode levelHead = root, nextLevelHead = null;
        while (levelHead != null) {
            TreeLinkNode node = levelHead, tail = null;
            while (node != null) {
                if (node.left != null && node.right != null) {
                    node.left.next = node.right;
                }
                TreeLinkNode sub;
                if (node.left != null)
                    sub = node.left;
                else if (node.right != null)
                    sub = node.right;
                else
                    sub = null;
                if (sub != null) {
                    if (nextLevelHead == null) {
                        nextLevelHead = sub;
                        tail = sub;
                    } else {
                        tail.next = sub;
                    }
                    while (tail.next != null)
                        tail = tail.next;
                }
                node = node.next;
            }
            levelHead = nextLevelHead;
            nextLevelHead = null;
        }
    }
}
```