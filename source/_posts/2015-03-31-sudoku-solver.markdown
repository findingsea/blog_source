---
layout: post
title: "Sudoku Solver@LeetCode"
date: 2015-03-31 09:08
comments: true
tags: LeetCode
---
[Sudoku Solver](https://leetcode.com/problems/sudoku-solver/)

<!-- more -->

题目看起来有些难，但是其实解法很通俗，就是每一步就尝试一遍所有9个数字，然后看哪个数字是可以当前合理的。

主体还是一个递归函数，找出当前适合的数后再递归调用。找出合适的数的方法就是遍历9个数字填充到当前位置，然后用验证函数进行验证，然后验证通过就继续调用递归函数解出下一个位置，如果验证不通过就再尝试下一个数字。如果遍历了一遍都没有发现合适的数字，那么就返回`false`。当发现所有空位都填充满了之后，就可以返回`true`了。

```java
public class Solution {
    public void solveSudoku(char[][] board) {
        if (board == null || board.length != 9 || board[0].length != 9)
            return;
        solve(board, 0, 0);
    }

    private boolean solve(char[][] board, int i, int j) {
        if (j >= 9)
            return solve(board, i + 1, 0);
        if (i == 9)
            return true;
        if (board[i][j] == '.') {
            for (int k = 1; k <= 9; k++) {
                board[i][j] = (char) (k + '0');
                if (isValid(board, i, j)) {
                    if (solve(board, i, j + 1))
                        return true;
                }
                board[i][j] = '.';
            }
        } else {
            return solve(board, i, j + 1);
        }
        return false;
    }

    private boolean isValid(char[][] board, int i, int j) {
        for (int k = 0; k < 9; k++) {
            if (k != i && board[k][j] == board[i][j])
                return false;
        }
        for (int k = 0; k < 9; k++) {
            if (k != j && board[i][k] == board[i][j])
                return false;
        }
        for (int row = i / 3 * 3; row < i / 3 * 3 + 3; row++) {
            for (int col = j / 3 * 3; col < j / 3 * 3 + 3; col++) {
                if (row != i && col != j && board[i][j] == board[row][col])
                    return false;
            }
        }
        return true;
    }
}
```