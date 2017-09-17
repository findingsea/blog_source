---
layout: post
title: "Binary Tree Preorder/Postorder Traversal"
date: 2015-04-27 09:28
comments: true
tags: LeetCode
---
树的前序和后序遍历是树相关算法的基本。就不多加解释了，直接上代码。

<!-- more -->

## [Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/)

``` java
public class Solution {
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new LinkedList<Integer>();
        generate(result, root);
        return result;
    }

    private void generate(List<Integer> sequence, TreeNode node) {
        if (node == null)
            return;
        sequence.add(node.val);
        generate(sequence, node.left);
        generate(sequence, node.right);
    }
}
```

## [Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/)

``` java
public class Solution {
    public List<Integer> postorderTraversal(TreeNode root) {
        List<Integer> result = new LinkedList<Integer>();
        generate(result, root);
        return  result;
    }

    private void generate(List<Integer> result, TreeNode node) {
        if (node == null)
            return;
        generate(result, node.left);
        generate(result, node.right);
        result.add(node.val);
    }
}
```