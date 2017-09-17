---
layout: post
title: "LRU Cache@LeetCode"
date: 2015-04-28 10:25
comments: true
tags: LeetCode
---
## [LRU Cache](https://leetcode.com/problems/lru-cache/)

<!-- more -->

数据结构用列表。`get()`和`set()`方法就不多讲，重要的是遇到下两种情况：

* 元素被访问过，要将其放到列表头部，实现函数：`moveToHead(Node node)`
* 元素个数达到最大值，删除尾部元素，实现函数：`removeTail()`

同时为了快速选中元素，就采用`HashMap<Integer, Node>`来保存键值。

``` java
public class LRUCache {

    private int capacity;
    private Node head, tail;
    private HashMap<Integer, Node> keyNodeMap;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head = new Node(-1, -1);
        tail = new Node(0, 0);
        head.next = tail;
        tail.pre = head;
        this.keyNodeMap = new HashMap<Integer, Node>();
    }

    public int get(int key) {
        Node node = keyNodeMap.get(key);
        if (node != null) {
            moveToHead(node);
            return node.value;
        }
        return -1;
    }

    public void set(int key, int value) {
        Node node = null;
        if (keyNodeMap.containsKey(key)) {
            node = keyNodeMap.get(key);
            node.value = value;
        } else {
            node = new Node(key, value);
            if (keyNodeMap.size() == capacity) {
                keyNodeMap.remove(removeTail());
            }
            keyNodeMap.put(key, node);
        }
        moveToHead(node);
    }

    private void moveToHead(Node node) {
        if (node.pre != null || node.next != null) {
            node.next.pre = node.pre;
            node.pre.next = node.next;
        }
        node.next = head.next;
        head.next.pre = node;
        node.pre = head;
        head.next = node;
    }

    private int removeTail() {
        int lastKey = -1;
        if (tail.pre != head) {
            Node lastNode = tail.pre;
            lastKey = lastNode.key;
            lastNode.pre.next = tail;
            tail.pre = lastNode.pre;
            lastNode = null;
        }
        return lastKey;
    }

    class Node{
        int key;
        int value;
        Node pre;
        Node next;
        public Node(int k, int v) {
            key = k;
            value = v;
        }
    }
}
```