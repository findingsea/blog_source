---
layout: post
title: "Dungeon Game@LeetCode"
date: 2015-05-06 10:45
comments: true
tags: LeetCode
---
## [Dungeon Game](https://leetcode.com/problems/dungeon-game/)

<!-- more -->

典型的动态规划题。维护一个二维数组`dungeon`，`dungeon[i][j]`表示从第`i`行第`j`出发到终点所需要的最低血量（包含当前位置的消耗），最低血量不大于1。

递推公式为：

```
dungeon[i][j] = Math.max(1, -dungeon[i][j] + Math.min(dungeon[i + 1][j], dungeon[i][j + 1]));
```

实现代码：

``` java
public class Solution {
    public int calculateMinimumHP(int[][] dungeon) {
        int rows = dungeon.length, cols = dungeon[0].length;
        dungeon[rows - 1][cols - 1] = Math.max(1, -dungeon[rows - 1][cols - 1] + 1);
        for (int j = cols - 2; j >= 0; j--) {
            dungeon[rows - 1][j] = Math.max(1, -(dungeon[rows - 1][j]) + dungeon[rows - 1][j + 1]);
        }
        for (int i = rows - 2; i >= 0; i--) {
            for (int j = cols - 1; j >= 0; j--) {
                if (j == cols - 1) {
                    dungeon[i][j] = Math.max(1, -(dungeon[i][j]) + dungeon[i + 1][j]);
                } else {
                    dungeon[i][j] = Math.max(1, -dungeon[i][j] + Math.min(dungeon[i + 1][j], dungeon[i][j + 1]));
                }
            }
        }
        return dungeon[0][0];
    }
}
```