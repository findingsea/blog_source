---
layout: post
title: "Largest Number@LeetCode"
date: 2015-03-18 10:39
comments: true
tags: LeetCode
---
[Largest Number](https://leetcode.com/problems/largest-number/)

<!-- more -->

典型的窍门题，就是知道了诀窍之后很简单就能搞定。不像有些题目，比如动态规划，即便知道了是用什么方法，但求递推公式还是要花很大的力气。

这题最大的难点就在于：当一个数是另一个数的前缀时，如何排列它们顺序。（其他情况很简单，就按照字符串默认的排序规则就行）

解决方法是：比较两个数o1和o2时，不要直接比较他们自身的大小，而是比较o1+o2和o2+o1的大小。

实现方法就是要自己写一个比较器，那么这里也有一个技巧，网上的实现代码有些是这样写的：

``` java
return (int) (Long.parseLong(o1 + o2) - Long.parseLong(o2 + o1));
```

虽然这样的实现在编写上非常简单，但是其实这样需要完整地转换两个字符串，这在大多数情况是不需要的，大多数情况下只要比较前几个数字就可以判断出大小了，所以我采用的比较器写法如下：

``` java
String str1 = o1 + o2;
String str2 = o2 + o1;
int length = str1.length();
for (int i = 0; i < length; i++) {
	if (str1.charAt(i) > str2.charAt(i)) {
		return 1;
	} else if (str1.charAt(i) < str2.charAt(i)) {
		return -1;
	}
}
return 0;
```

实现代码如下：

``` java
public class Solution {
    public String largestNumber(int[] num) {
        int length = num.length;
        String[] numStr = new String[length];
        for (int i = 0; i < length; i++) {
            numStr[i] = String.valueOf(num[i]);
        }
        Arrays.sort(numStr, new StringComparator());
        StringBuilder stringBuilder = new StringBuilder();
        for (int i = length - 1; i >= 0; i--) {
            stringBuilder.append(numStr[i]);
        }
        int index = 0;
        while (index < stringBuilder.length() - 1 && stringBuilder.charAt(index) == '0') {
            index++;
        }
        return stringBuilder.substring(index, stringBuilder.length()).toString();
    }

    class StringComparator implements Comparator<String> {

        @Override
        public int compare(String o1, String o2) {
            String str1 = o1 + o2;
            String str2 = o2 + o1;
            int length = str1.length();
            for (int i = 0; i < length; i++) {
                if (str1.charAt(i) > str2.charAt(i)) {
                    return 1;
                } else if (str1.charAt(i) < str2.charAt(i)) {
                    return -1;
                }
            }
            return 0;
        }
    }
}
```