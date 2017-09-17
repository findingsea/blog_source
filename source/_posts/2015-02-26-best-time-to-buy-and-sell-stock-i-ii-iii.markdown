---
layout: post
title: "Best Time to Buy and Sell Stock I II III IV@LeetCode"
date: 2015-02-26 10:12
comments: true
tags: LeetCode
---
## [Best Time to Buy and Sell Stock](https://oj.leetcode.com/problems/best-time-to-buy-and-sell-stock/)

相对比较简单的方法是用DP，思路是对于每个i都求出从0到i区间内的最大获益，而对于i+1只需要比较第i+1天的价格和前i天最低价的关系，就可以直接求出0到i+1天区间内的最大获益。也就是说对0到i天的最大获益的计算复杂度是O(1)，总体复杂度是O(n)。

<!-- more -->

详细解释下从第i天的最大获益如何推出第i+1天的最大获益，已知是的是前i天的最大获益以及前i天的最低价，那么对于第i+1天的价格而言：

1. 第i+1天的价格大于minPrice（已遍历数据的最低价），此时只要对max(i)（前i天的最大获益）和prices[i + 1] - minPrice（第i+1天卖出所能得到的获益）取大值就能得出max(i + 1)
2. 第i+1天的价格小于等于minPrice，那么在第i+1天卖出所得到的获益必然是小于max(i)（这里哪怕考虑极端情况：给出的数据是整体递减的，那么最佳的卖出时机也是当天买当天卖，获益为0，所以不会存在获益是负值的情况），所以max(i + 1) = max(i)。而且，对于之后的数据而言，minPrice需要更新了，因为对于之后的数据，在第i+1天买进必然比在0到i天之间的任何时候买进的获益都要多（因为第i+1天是0到i+1区间内的最低价）。

相较于网上一般的DP做法，我的小改进在于没有维护整个max数组，而是指用了一个max整型值来保存当前的最大获益，空间复杂度是O(1)。这个技巧其实在很多DP解法中都可以用到，只要之前的数据不需要回朔（或者是只需要回朔某几个位置的数据），很多情况下都可以把DP的数组从O(n^2)降到O(n)，从O(n)降到O(1)。

```java
public class Solution {
    public int maxProfit(int[] prices) {
        if (prices == null || prices.length == 0)
            return 0;
        int max = 0, minPrice = prices[0];
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] <= minPrice) {
                minPrice = prices[i];
            } else {
                max = Math.max(max, prices[i] - minPrice);
            }
        }
        return max;
    }
}
```

## [Best Time to Buy and Sell Stock II](https://oj.leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

这个进阶版和基础版的不同在于可以进行任意多次交易，这样其实限制更少，只要把所有递增区间的获益求和就行了。

```java
public class Solution {
    public int maxProfit(int[] prices) {
        int max = 0;
        int i = 0;
        while (i < prices.length - 1) {
            if (prices[i] >= prices[i + 1]) {
                i++;
                continue;
            }
            int j = i + 1;
            for (; j < prices.length; j++) {
                if (j < prices.length - 1 && prices[j] <= prices[j + 1]) {
                    continue;
                }
                max += prices[j] - prices[i];
                break;
            }
            i = j + 1;
        }
        return max;
    }
}
```

## [Best Time to Buy and Sell Stock III](https://oj.leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

高级版的难度一下子就提升了，刚一开始我的**错误想法**是：将两个获益最大区间的获益相加，后来很快就证明了这个解法是错误的。

借助网络之后，确定了正确解法：构造两个数组，left和right，left[i]表示从0到i天的最大获益，right[i]表示从i到最后一天的最大获益。

求left的方法其实就解题I的方法，不再赘述。

求right的方法其实是求left的对称解法：

+ 求left时，记录前i天的最低价minPrice与最大获益max，求left[i]：考虑要在第i天卖出，那么买进的时间必然是在0到i之间（闭区间），这个时候只需要比较prices[i]-minPrice和max就可以求出截止到第i天的最大获益，然后根据需要更新minPrice。
+ 求right时，记录从第i天往后的最高价maxPrice与最大获益max，求right[i]：考虑要再第i天买进，那么卖出时间必然是在i到最后一天之间（闭区间），这个时候只需要比较maxPrice-prices[i]和max就可以求出从第i天开始的最大获益，然后根据需要更新maxPrice。

对于left和right的构造算法复杂度都是O(n)。

构造完left和right之后，只要求left[i]+right[i]的最大值就行了。

```java
public class Solution {
    public int maxProfit(int[] prices) {
        if (prices == null || prices.length == 0)
            return 0;
        int max = 0;
        int[] left = new int[prices.length];
        int[] right = new int[prices.length];
        int minPrice = prices[0];
        for (int i = 1; i < prices.length; i++) {
            if (minPrice < prices[i]) {
                left[i] = Math.max(left[i - 1], prices[i] - minPrice);
            } else {
                left[i] = left[i - 1];
                minPrice = prices[i];
            }
        }
        int maxPrice = prices[prices.length - 1];
        for (int i = prices.length - 2; i >= 0; i--) {
            if (prices[i] < maxPrice) {
                right[i] = Math.max(right[i + 1], maxPrice - prices[i]);
            } else {
                right[i] = right[i + 1];
                maxPrice = prices[i];
            }
        }
        for (int i = 0; i < prices.length; i++) {
            max = Math.max(max, left[i] + right[i]);
        }
        return max;
    }
}
```

## [Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

这一题的难度要远高于前面几题，需要用到动态规划，但是需要额外的辅助。

先按照之前的方法对数组进行统计，计算出无限制条件下的最少交易次数`tradeCount`和最大获益`profitCount`。如果这个最少交易次数已经小于`k`了，那么直接返回最大获益即可。同时也因为在`k < tradeCount`的情况下，进行动态规划的效率很低，所以要先进行处理来避免。

在动态规划的部分，维护两个数组：`local`和`global`。其中`local[i][j]`表示总交易次数为`i`截止到第`j`天并且在最后一天要做交易的情况下的最大获益，`global[i][j]`表示总交易次数为`i`截止到第`j`天的最大获益。

之所以在`global`之外还要维护一个`local`数组，是因为在计算`global[i][j]`时，面临两种情况：

1. 最后一天不做交易，那么直接等于`global[i][j - 1]`
2. 最后一天要做交易，那么又需要分别考虑罪有一天是否有收益的问题，所以要增加一个`local`数组进行辅助

递推公式：
```
int diff = prices[j] - prices[j - 1];
local[i][j] = Math.max(global[i - 1][j - 1], local[i][j - 1] + diff);
global[i][j] = Math.max(global[i][j - 1], local[i][j]);
```

解释一下`local[i][j] = Math.max(global[i - 1][j - 1], local[i][j - 1] + diff);`这一条，当`diff < 0`时，在最后一条做交易必然是亏的，所以其实此时`local[i][j]`直接等于`global[i - 1][j - 1]`；当`diff > 0`时，本来应该比较两种情况的，`global[i - 1][j - 1] + diff`和`local[i][j - 1] + diff`，但是通过以下推断我们可以知道`local[i][j - 1] > global[i - 1][j - 1]`，所以无须比较。

推断：

```
因为global[i - 1][j - 1] = Math.max(global[i - 1][j - 2], local[i - 1][j - 1])
所以global[i - 1][j - 1] = global[i - 1][j - 2]或者global[i - 1][j - 1] = local[i - 1][j - 1])

由题意可知：local[i][j - 1] > local[i - 1][j - 1])

又因为local[i][j - 1] = Math.max(global[i - 1][j - 2], local[i][j - 2] + diff)
所以local[i][j - 1] >= global[i - 1][j - 2]

综上local[i][j - 1] > local[i - 1][j - 1])并且local[i][j - 1] >= global[i - 1][j - 2]，即local[i][j - 1] > global[i - 1][j - 1]
```

这里还有一个性质，就是当`i`大于最大收益所需的交易次数时，其实`local[i][j] == global[i][j]`，多出来的交易都是当天买卖，不会产生收益。

实现代码：

``` java
public class Solution {
    public int maxProfit(int k, int[] prices) {
        int days = prices.length;
        int tradeCount = 0, profitCount = 0, rangeProfitCount = 0;
        for (int i = 1; i < days; i++) {
            if (prices[i - 1] < prices[i]) {
                rangeProfitCount += prices[i] - prices[i - 1];
                if (i == days - 1) {
                    profitCount += rangeProfitCount;
                    tradeCount += 1;
                }
            } else if (rangeProfitCount > 0) {
                profitCount += rangeProfitCount;
                tradeCount += 1;
                rangeProfitCount = 0;
            }
        }
        if (tradeCount <= k)
            return profitCount;
        int[][] global = new int[k + 1][days];
        int[][] local = new int[k + 1][days];
        for (int i = 1; i <= k; i++) {
            for (int j = 1; j < days; j++) {
                int diff = prices[j] - prices[j - 1];
                local[i][j] = Math.max(global[i - 1][j - 1], local[i][j - 1] + diff);
                global[i][j] = Math.max(global[i][j - 1], local[i][j]);
            }
        }
        return global[global.length - 1][global[0].length - 1];
    }
}
```