---
layout: post
title: "Binary Tree Maximum Path Sum@LeetCode"
date: 2015-04-21 10:27
comments: true
tags: LeetCode
---

## [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

<!-- more -->

动态规划+深度优先搜索。把大问题（求整棵树的路径最大值）拆分成小问题（每颗子树的路径最大值），递推公式为：`当前树的路径最大值=max(左子树的路径最大值, 右子树的路径最大值)+当前根节点的值。`以此来推出最后全树的最大路径值。

实现代码：

``` java
public class Solution {

    private int max;

    public int maxPathSum(TreeNode root) {
        if (root == null)
            return 0;
        max = root.val;
        traversal(root);
        return max;
    }

    private int traversal(TreeNode node) {
        int left = node.left == null ? 0 : traversal(node.left);
        int right = node.right == null ? 0 : traversal(node.right);
        left = left <= 0 ? 0 : left;
        right = right <= 0 ? 0 : right;
        max = Math.max(max, left + node.val + right);
        node.val = node.val + Math.max(left, right);
        return node.val;
    }
}
```