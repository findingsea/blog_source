---
layout: post
title: "Word Break I II@LeetCode"
date: 2015-04-26 09:32
comments: true
tags: LeetCode
---
## [Word Break](https://leetcode.com/problems/word-break/)

<!-- more -->

递归，基本属于暴力求解。但是纯暴力应该是过不了的，参考网上的办法，增加了一个`unmatch`集合，类型是`HashSet`，用来存放那些已经被验证过无法匹配的字符串，这样可以剪掉很多分支。

实现代码：

``` java
public class Solution {
    private Set<String> unmatch = new HashSet<String>();

    public boolean wordBreak(String s, Set<String> dict) {
        for (String prefix : dict) {
            if (s.equals(prefix))
                return true;
            if (s.startsWith(prefix)) {
                String suffix = s.substring(prefix.length(), s.length());
                if (!unmatch.contains(suffix)) {
                    if (wordBreak(suffix, dict))
                        return true;
                    else
                        unmatch.add(suffix);
                }
            }
        }
        return false;
    }
}
```

## [Word Break II](https://leetcode.com/problems/word-break-ii/)

解法基本差不多，无非是增加记录路径的要求。这里唯一需要注意的是，在前面我们只要一找到符合条件的组合即可返回了，在这题中，一定要遍历所有情况之后再返回。当然，还是用了一个`mismatch`来剪分支。

实现代码：

``` java
public class Solution {
    public List<String> wordBreak(String s, Set<String> dict) {
        List<String> result = new LinkedList<String>();
        if (s.length() == 0)
            return result;
        generate(s, dict, new HashSet<String>(), result, new StringBuilder());
        return result;
    }

    private boolean generate(String s, Set<String> dict, Set<String> mismatch,
                             List<String> result, StringBuilder sentence) {
        if (s.length() == 0) {
            result.add(sentence.toString());
            return true;
        }
        boolean canBreak = false;
        for (String word : dict) {
            if (s.startsWith(word)) {
                String suffix = s.substring(word.length(), s.length());
                if (!mismatch.contains(suffix)) {
                    StringBuilder newSentence = new StringBuilder(sentence);
                    if (newSentence.length() != 0) newSentence.append(" ");
                    newSentence.append(word);
                    if (generate(suffix, dict, mismatch,
                            result, newSentence)) {
                        canBreak = true;
                    } else {
                        mismatch.add(suffix);
                    }
                }
            }
        }
        return canBreak;
    }
}
```