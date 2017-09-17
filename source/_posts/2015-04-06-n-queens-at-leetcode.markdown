---
layout: post
title: "N-Queens I II@LeetCode"
date: 2015-04-06 14:39
comments: true
tags: LeetCode
---
## [N-Queens](https://leetcode.com/problems/n-queens/)

<!-- more -->

N皇后问题，非常经典。同时也是非常传统的递归方法解决。

递归的主体很简单：对于当前位置，分别尝试下放皇后和不放皇后两种情况。这里有两个需要注意的地方：

1. 在递归函数中，在一次递归中，对整行进行遍历，这样相当于在检查的时候就不需要对当前行进行检查了，因为赋值的时候已经保证了当前行只有一个皇后。

2. 定义一个检查函数，分别对之前已经赋值过的位置上同一列和斜列上是否有皇后存在，如果有就返回`false`；遍历全部位置之后都没有就返回`true`。

实现代码：

``` java
public class Solution {
    public List<String[]> solveNQueens(int n) {
        List<String[]> result = new ArrayList<String[]>();
        if (n == 0)
            return result;
        generate(new int[n][n], 0, result);
        return result;
    }

    private void generate(int[][] board, int row, List<String[]> queens) {
        int n = board.length;
        if (row == n) {
            String[] strArr = new String[n];
            for (int i = 0; i < n; i++) {
                StringBuffer sb = new StringBuffer("");
                for (int j = 0; j < n; j++) {
                    if (board[i][j] == 0)
                        sb.append(".");
                    else
                        sb.append("Q");
                }
                strArr[i] = sb.toString();
            }
            queens.add(strArr);
            return;
        }
        for (int col = 0; col < board.length; col++) {
            board[row][col] = 1;
            if (!check(board, row, col)) {
                board[row][col] = 0;
                continue;
            } else {
                generate(board, row + 1, queens);
                board[row][col] = 0;
            }
        }
    }

    private boolean check(int[][] board, int row, int col) {
        int i = row - 1, j = col;
        while (i >= 0) {
            if (board[i][j] == 1 || (j - row + i >= 0 && board[i][j - row + i] == 1)
                    || (j + row - i < board.length && board[i][j + row - i] == 1)) {
                return false;
            }
            i--;
        }
        return true;
    }
}
```

## [N-Queens II](https://leetcode.com/problems/n-queens-ii/)

最后顺便提一句这题的进阶版——[N-Queens II](https://leetcode.com/problems/n-queens-ii/)，在这个系列中，这个设置也是很奇怪，如果用如上方法解决了第一题，那么第二题只要改一下返回值就行了，即求一下集合的的`size()`。

详细代码如下：

``` java
public class Solution {
    public int totalNQueens(int n) {
        List<Integer> result = new ArrayList<Integer>();
        if (n == 0)
            return 0;
        generate(new int[n][n], 0, result);
        return result.size();
    }

    private void generate(int[][] board, int row, List<Integer> queens) {
        int n = board.length;
        if (row == n) {
            queens.add(1);
            return;
        }
        for (int col = 0; col < board.length; col++) {
            board[row][col] = 1;
            if (!check(board, row, col)) {
                board[row][col] = 0;
                continue;
            } else {
                generate(board, row + 1, queens);
                board[row][col] = 0;
            }
        }
    }

    private boolean check(int[][] board, int row, int col) {
        int i = row - 1, j = col;
        while (i >= 0) {
            if (board[i][j] == 1 || (j - row + i >= 0 && board[i][j - row + i] == 1)
                    || (j + row - i < board.length && board[i][j + row - i] == 1)) {
                return false;
            }
            i--;
        }
        return true;
    }
}
```