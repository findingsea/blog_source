---
layout: post
title: "Recover Binary Search Tree@LeetCode"
date: 2015-04-19 09:47
comments: true
tags: LeetCode
---
## [Recover Binary Search Tree](https://leetcode.com/problems/recover-binary-search-tree/)

<!-- more -->

根据`BST`树的特性来，对`BST`的中序遍历，得到的是一个升序数列。所以在遍历过程中检测出两个异常的位置，对其进行交换即可。

一旦有两个位置的节点被交换了，那么中序遍历就会出现有两个：`Node[i] > Node[i + 1]`其中`i`是错误位置，`Node[j] < Node[j - 1]`其中`j`是错误位置，遵循这个规律，找到相应的`Node[i]`和`Node[j]`对其进行交换（只交换`val`值）即可。

实现代码如下：

``` java
public class Solution {

    private TreeNode wrongLessNode;
    private TreeNode wrongLargerNode;
    private TreeNode preNode;

    public void recoverTree(TreeNode root) {
        recover(root);
        if (wrongLessNode != null && wrongLargerNode != null) {
            int temp = wrongLessNode.val;
            wrongLessNode.val = wrongLargerNode.val;
            wrongLargerNode.val = temp;
        }
    }

    private void recover(TreeNode root) {
        if (root == null)
            return;
        if (preNode == null && root.left == null) {
            preNode = root;
        }
        recover(root.left);
        if (preNode != null && root.val < preNode.val) {
            if (wrongLessNode == null) {
                wrongLessNode = preNode;
                wrongLargerNode = root;
            }
            else {
                wrongLargerNode = root;
                return;
            }
        }
        preNode = root;
        recover(root.right);
    }
}
```