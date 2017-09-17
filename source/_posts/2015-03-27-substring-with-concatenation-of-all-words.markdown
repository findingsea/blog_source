---
layout: post
title: "Substring with Concatenation of All Words@LeetCode"
date: 2015-03-27 09:24
comments: true
tags: LeetCode
---
[Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)

<!-- more -->

比较复杂的一题，首先是要明确用滑块的概念来解决，始终保持`L`集合中的字符串在滑块中都只出现了一次，当然设置一个总计数`count`，当`cout`等于`L`集合长度时，即使找了一段符合要求的字符串。

需要用到的内存空间：

* 两张哈希表，一张保存`L`集合中的单词，一张用来保存当前滑块中的单词，`key`为单词，`value`为出现次数
* `cout`计数，保存当前滑块中的单词总数
* `left`标记，记录滑块左起点

实现的步骤：

1. 遍历一遍单词数组`L`集合，构造总单词表
2. 以单词长度为步长，遍历目标字符串，如果当前单词在总单词表内，则进入步骤3；反之，则清空当前滑块单词表，将`cout`置零，将`left`移动到下一位置
3. 当前滑块档次表中的相应单词计数加1，检查该单词的计数是否小于等于总单词表中该单词的总数，如果是，则将`count`计数加1，进入步骤5；反之，进入步骤4
4. 根据左起点`left`收缩滑块，直到收缩到与当前单词相同的字符串片段，将其剔除之后，滑块的收缩工作完成
5. 如果当前`count`计数等于单词集合长度，记录下`left`左起点的位置后，将`left`右移，当前滑块中相应单词计数减1，总计数减1，继续循环

这里解释下步骤4中的收缩滑块，这是因为当前滑块中有单词的出现次数超过了额定的出现次数，那么就是需要收缩滑块来剔除这个单词，相当于是从滑块的左起点开始寻找该单词，找到之后，将该单词的右端点作为滑块新的左起点，这样就保证了滑块中所有单词都是小于等于额定出现次数，这样也保证了`count`计数的有效性。

遇到总单词表中不存在的单词的情况，在步骤2中已经说明，清空当前数据之后继续循环，也就是保证了滑块中是不会出现不存在单词表中的单词的。

最后，考虑最外圈循环，如果是从0开始作为滑块的初始起点，那么其实并没有遍历字符串中的所有可能子串，因为步长是单词长度，所以移动滑块的时候会跨过很多可能子串，所以要在外圈再加一层循环，这个循环的作用就是移动滑块的初始起点，所以循环次数就是单词的长度。

实现代码：

``` java
public class Solution {
    public List<Integer> findSubstring(String S, String[] L) {
        ArrayList<Integer> result = new ArrayList<Integer>();
        if (S == null || S.length() == 0 || L == null || L.length == 0)
            return result;
        int strLen = S.length();
        int wordLen = L[0].length();
        HashMap<String, Integer> map = new HashMap<String, Integer>();
        for (int i = 0; i < L.length; i++) {
            if (map.containsKey(L[i])) {
                map.put(L[i], map.get(L[i]) + 1);
            } else {
                map.put(L[i], 1);
            }
        }
        for (int i = 0; i < wordLen; i++) {
            HashMap<String, Integer> curMap = new HashMap<String, Integer>();
            int count = 0, left = i;
            for (int j = i; j <= strLen - wordLen; j += wordLen) {
                String curStr = S.substring(j, j + wordLen);
                if (map.containsKey(curStr)) {
                    if (curMap.containsKey(curStr)) {
                        curMap.put(curStr, curMap.get(curStr) + 1);
                    } else {
                        curMap.put(curStr, 1);
                    }
                    if (curMap.get(curStr) <= map.get(curStr)) {
                        count++;
                    } else {
                        while (true) {
                            String tmp = S.substring(left, left + wordLen);
                            curMap.put(tmp, curMap.get(tmp) - 1);
                            left += wordLen;
                            if (curStr.equals(tmp)) {
                                break;
                            } else {
                                count--;
                            }
                        }
                    }
                    if (count == L.length) {
                        result.add(left);
                        String tmp = S.substring(left, left + wordLen);
                        curMap.put(tmp, curMap.get(tmp) - 1);
                        left += wordLen;
                        count--;
                    }
                } else {
                    curMap.clear();
                    count = 0;
                    left = j + wordLen;
                }
            }
        }
        return result;
    }
}
```