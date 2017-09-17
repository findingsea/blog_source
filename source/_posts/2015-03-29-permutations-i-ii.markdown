---
layout: post
title: "Permutations I II@LeetCode"
date: 2015-03-29 11:37
comments: true
tags: LeetCode
---
[Permutations](https://leetcode.com/problems/permutations/)

<!-- more -->

递归的方法，设置一个`used`数组，用来记录相应位置是否已经使用过了，然后设置一个`permutation`数组，用来保存当前的序列，如果当前序列长度到达额定长度后，将该序列加入最后结果集合中。

实现代码：

```java
public class Solution {
    public List<List<Integer>> permute(int[] num) {
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        generate(num, new boolean[num.length], result, new ArrayList<Integer>());
        return result;
    }

    private void generate(int[] num, boolean[] used, List<List<Integer>> result, List<Integer> permutation) {
        if (permutation.size() == num.length) {
            result.add(new ArrayList<Integer>(permutation));
        } else {
            for (int i = 0; i < num.length; i++) {
                if (!used[i]) {
                    permutation.add(num[i]);
                    used[i] = true;
                    generate(num, used, result, permutation);
                    permutation.remove(permutation.size() - 1);
                    used[i] = false;
                }
            }
        }
    }
}
```

[Permutations II](https://leetcode.com/problems/permutations-ii/)

难度的提升在于：有数字是重复的。

针对这一点，可以先对原始数据集合进行排序，这样保证了如果有重复元素，那么他们也是相邻的。同时，在递归函数中，同一层递归中，除了判断该位有没有使用过，还要判断当前位之后的元素是否与当前位相同，如果相同则要一直往前找到第一个不相同的且没有使用过的元素，作为下一个当前位插入`permutation`数组中。

实现代码：

```java
public class Solution {
    public List<List<Integer>> permuteUnique(int[] num) {
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        Arrays.sort(num);
        generate(num, new boolean[num.length], result, new ArrayList<Integer>());
        return result;
    }

    private void generate(int[] num, boolean[] used, List<List<Integer>> result, List<Integer> permutation) {
        if (permutation.size() == num.length) {
            result.add(new ArrayList<Integer>(permutation));
        } else {
            int i = 0;
            while (i < used.length) {
                if (!used[i]) {
                    permutation.add(num[i]);
                    used[i] = true;
                    generate(num, used, result, permutation);
                    permutation.remove(permutation.size() - 1);
                    used[i] = false;
                    while (i < used.length - 1 && num[i] == num[i + 1]) {
                        i++;
                    }
                }
                i++;
            }
        }
    }
}
```