---
layout: post
title: "Word Ladder I II@LeetCode"
date: 2015-02-27 18:41
comments: true
tags: LeetCode
---
### [Word Ladder](https://oj.leetcode.com/problems/word-ladder/)

这个系列的两题都是靠了看别人的解法才做出来的，很有必要好好总结下。

<!-- more -->

看到这题的时候我其实就没什么想法，对这种类型题的经验太少。上网查完之后，确定要用图的思想解决，思路就是从起点出发对字典中可达的字符串进行BFS（广度优先搜索）并记录当前节点与起点的距离，一旦找到了目标字符串即返回。

```java
public class Solution {
    public int ladderLength(String start, String end, Set<String> dict) {
        HashMap<String, Integer> disMap = new HashMap<String, Integer>();
        LinkedList<String> queue = new LinkedList<String>();
        queue.add(start);
        disMap.put(start, 1);
        while (!queue.isEmpty()) {
            String word = queue.poll();
            for (int i = 0; i < word.length(); i++) {
                for (char ch = 'a'; ch <= 'z'; ch++) {
                    StringBuffer buffer = new StringBuffer(word);
                    buffer.setCharAt(i, ch);
                    String nextWord = buffer.toString();
                    if (end.equals(nextWord)) {
                        return disMap.get(word) + 1;
                    }
                    if (dict.contains(nextWord) && !disMap.containsKey(nextWord)) {
                        disMap.put(nextWord, disMap.get(word) + 1);
                        queue.add(nextWord);
                    }
                }
            }
        }
        return 0;
    }
}
```

### [Word Ladder II](https://oj.leetcode.com/problems/word-ladder-ii/)

一开始以为做了I之后，用一样的思路解决II应该会容易很多。但做了才发现，II对效率的要求更高，而且这使得这一题成为了LeetCode上通过率最低的题之一。

先讲一下自己做的时候的思路，和I相似，用图的思想，只不过是该用DFS（深度优先搜索），从起点出发，对字典中的每一个可达字符串进行DFS并记录路径，到达目标之后在当前路径和之间的最短路径中取较短者。代码如下，大数据集合超时。

```java
public class Solution {
    public List<List<String>> findLadders(String start, String end, Set<String> dict) {
        List<List<String>> result = new LinkedList<List<String>>();
        LinkedList<String> sequence = new LinkedList<String>();
        HashMap<String, Boolean> usedMap = new HashMap<String, Boolean>();
        sequence.add(start);
        usedMap.put(start, true);
        find(result, sequence, start, end, dict, usedMap);
        return result;
    }

    private void find(List<List<String>> result, LinkedList<String> sequence,  String word, String end,
                      Set<String> dict, HashMap<String, Boolean> usedMap) {
        for (int i = 0; i < word.length(); i++) {
            for (char ch = 'a'; ch <= 'z'; ch++) {
                if (word.charAt(i) == ch)
                    continue;
                StringBuffer buffer = new StringBuffer(word);
                buffer.setCharAt(i, ch);
                String nextWord = buffer.toString();
                if (end.equals(nextWord)) {
                    int minLength = result.size() == 0 ? 0 : result.get(result.size() - 1).size();
                    if (minLength == 0 || sequence.size() + 1 <= minLength) {
                        if (sequence.size() + 1 < minLength) {
                            result.clear();
                        }
                        List<String> res = new LinkedList<String>();
                        for (String str : sequence) {
                            res.add(str);
                        }
                        res.add(nextWord);
                        result.add(res);
                    }
                    return;
                }
                if (dict.contains(nextWord) && (!usedMap.containsKey(nextWord) || !usedMap.get(nextWord))) {
                    sequence.add(nextWord);
                    usedMap.put(nextWord, true);
                    find(result, sequence, nextWord, end, dict, usedMap);
                    sequence.pollLast();
                    usedMap.put(nextWord, false);
                }
            }
        }
    }
}
```
仔细分析最初的代码，发现耗时的地方在于：对于每一个可达的点都要尝试一下，相当于遍历了所以从起点可达终点的线路（也导致了很多点其实多次重复遍历），但是这其中很多线路本身的遍历是没有价值的，如果当前线路已经比最短可达路径长度长了，那接着往下遍历是没有意义的。所以改进的算法也是针对这一点来减少需要遍历的点和线路。

参考了网上的做法之后，确定了基本的解决方案：
1. 从起点出发，对字典中的所有字符串都遍历一遍，并记录它们到起点的距离，相当于先做BFS，由于是深度优先搜索，所以保证保存下来的距离都是起点到每个节点的最短距离。
2. 在从起点出发，根据可达性和与起点的距离进行深度优先搜索，并记录路径，在搜索时，要根据层来搜索，也就说确定下一个搜索节点，不光是根据从当前节点是否可达，还要根据下一节点和当前节点是否处在相邻的两层，这样能够避免对节点的重复遍历包含同时也时刻保持当前路径是最短的。

下面是代码。

```java
public class Solution {
    public List<List<String>> findLadders(String start, String end, Set<String> dict) {
        LinkedList<String> queue = new LinkedList<String>();
        HashMap<String, Integer> disMap = new HashMap<String, Integer>();
        queue.add(start);
        disMap.put(start, 1);

        while (!queue.isEmpty()) {
            String word = queue.poll();
            for (int i = 0; i < word.length(); i++) {
                for (char ch = 'a'; ch <= 'z'; ch++) {
                    if (word.charAt(i) == ch)
                        continue;
                    StringBuffer buffer = new StringBuffer(word);
                    buffer.setCharAt(i, ch);
                    String nextWord = new String(buffer);
                    if (end.equals(nextWord)) {
                        disMap.put(end, disMap.get(word) + 1);
                        i = word.length();
                        ch = 'z';
                        queue.clear();
                    }
                    if (dict.contains(nextWord)
                            && !disMap.containsKey(nextWord)) {
                        queue.add(nextWord);
                        disMap.put(nextWord, disMap.get(word) + 1);
                    }
                }
            }
        }
        List<List<String>> result = new LinkedList<List<String>>();
        find(result, new LinkedList<String>(), end, start, dict, disMap);

        return result;
    }

    private void find(List<List<String>> result, LinkedList<String> sequence, String word, String end,
                      Set<String> dict, HashMap<String, Integer> disMap) {
        if (disMap.get(word) == disMap.get(end) && !end.equals(word)) {
            return;
        } else if (end.equals(word)) {
            List<String> res = new LinkedList<String>(sequence);
            res.add(word);
            Collections.reverse(res);
            result.add(res);
            return;
        }
        sequence.add(word);
        for (int i = 0; i < word.length(); i++) {
            for (char ch = 'a'; ch <= 'z'; ch++) {
                if (word.charAt(i) == ch)
                    continue;
                StringBuffer buffer = new StringBuffer(word);
                buffer.setCharAt(i, ch);
                String nextWord = buffer.toString();
                if (dict.contains(nextWord) && disMap.containsKey(nextWord) && disMap.get(nextWord) == disMap.get(word) - 1) {
                    find(result, sequence, nextWord, end, dict, disMap);
                }
            }
        }
        sequence.remove(sequence.size() - 1);
    }
}
```
这个代码仍然超时，仔细对照了我自己写的代码和[参考的代码](http://blog.csdn.net/worldwindjp/article/details/19301355)之后，唯一做法上的不同在于：在DFS时，我的做法是从起点开始去找终点；而在参考代码的做法则是从终点开始找起点。我对这部分进行修改之后就能顺利AC了，关于这个问题，我猜测LeetCode的测试数据很可能都是前密后疏的类型，也就是从越靠近起点，线路越多，越靠近终点，线路越少。如果是这种数据的话，从终点出发的确是可以节省很多时间的。

虽然对DFS部分的代码进行修改之后能够AC了，但是我还是发现我写的代码的运行耗时（900ms左右）比[参考的代码](http://blog.csdn.net/worldwindjp/article/details/19301355)的运行耗时要长（700ms左右），虽说这点差距都是在允许范围内的，但是在考虑到总体代码结构都一致的情况下，这个差距还是不小的，所以我又仔细比较了两份代码，发现了一处处理方式的不同。

在参考代码中，对当前字符串进行变换采用的是如下形式：

```java
for (int i = 0; i < current.length(); i++) {
    char[] strCharArr = current.toCharArray();
    for (char ch = 'a'; ch <= 'z'; ch++) {
        if (strCharArr[i] == ch) {
            continue;
        }
        strCharArr[i] = ch;
        String newWord = new String(strCharArr);
        if (newWord.equals(end) == true || dict.contains(newWord)) {
            //每个单词在path中只能出现一次，也就是每个单词只能出现在一层中，这样就很巧妙的解决了环的问题。
            if (path.get(newWord) == null) {
                int depth = (int) path.get(current);
                path.put(newWord, depth + 1);
                queue.add(newWord);
            }
        }
    }
}
```

而我的代码采用是如下形式

```java
for (int i = 0; i < word.length(); i++) {
    for (char ch = 'a'; ch <= 'z'; ch++) {
        if (word.charAt(i) == ch)
            continue;
        StringBuffer buffer = new StringBuffer(word);
        buffer.setCharAt(i, ch);
        String nextWord = buffer.toString();
        if (end.equals(nextWord)) {
            disMap.put(end, disMap.get(word) + 1);
            i = word.length();
            ch = 'z';
            queue.clear();
        }
        if (dict.contains(nextWord)
                && !disMap.containsKey(nextWord)) {
            queue.add(nextWord);
            disMap.put(nextWord, disMap.get(word) + 1);
        }
    }
}
```

也就说，差别主要在于是把字符串转换成字符数组来进行修改还是还是创建一个`StringBuffer`来进行修改。于是我对自己的代码的这一部分也进行了修改，果然耗时减少了，这也说明字符数组的操作还是要比`StringBuffer`的操作省时很多。

最后，在参考代码基础上，我又做出了一点小改进。

提前结束层序图的构建。在构建每个节点到七点距离时（也就是构建图结构时），一旦遇到end点（终点）就终止遍历。这是因为使用BFS，每个点第一次出现时的距离，即为该点到起点的最短距离。也就是说，一旦出现了end点，那么当前所记录的end点所在的层位置，即为end点到start点的最短距离，同时之后出现的所有点（同样考虑BFS），它们到start点的距离是大于等于end点的，那么遍历那些点是没有意义的。

当考虑如下输入集合：

```
start = "hit"

end = "hoo"

dict = ["hot", "mit", "mot", "moo", "aoo", "boo", "coo"]
```

我改进之后的代码运行效率要比[参考的代码](http://blog.csdn.net/worldwindjp/article/details/19301355)高，因为构建层序图（BFS）时遍历的点更少（提到end点就结束了），构建出来的层序图点更少（去除了一些无用点），那么在DFS中遍历的点也更少，所以结合两方面的省时来提高了程序整体的运行效率。

如下是最后的完整代码。

```java
public class Solution {
    
    private HashMap<String, Integer> disMap;
    
    public List<List<String>> findLadders(String start, String end, Set<String> dict) {
        LinkedList<String> queue = new LinkedList<String>();
        disMap = new HashMap<String, Integer>();
        queue.add(start);
        disMap.put(start, 1);

        while (!queue.isEmpty()) {
            String word = queue.poll();
            for (int i = 0; i < word.length(); i++) {
                char[] chars = word.toCharArray();
                for (char ch = 'a'; ch <= 'z'; ch++) {
                    if (chars[i] == ch)
                        continue;
                    chars[i] = ch;
                    String nextWord = new String(chars);
                    if (end.equals(nextWord)) {
                        disMap.put(end, disMap.get(word) + 1);
                        i = word.length();
                        ch = 'z';
                        queue.clear();
                    }
                    if (dict.contains(nextWord)
                            && !disMap.containsKey(nextWord)) {
                        queue.add(nextWord);
                        disMap.put(nextWord, disMap.get(word) + 1);
                    }
                }
            }
        }
        List<List<String>> result = new LinkedList<List<String>>();
        find(result, new LinkedList<String>(), end, start);

        return result;
    }

    private void find(List<List<String>> result, LinkedList<String> sequence, String word, String end) {
        if (disMap.get(word) == disMap.get(end) && !end.equals(word)) {
            return;
        } else if (end.equals(word)) {
            List<String> res = new LinkedList<String>(sequence);
            res.add(word);
            Collections.reverse(res);
            result.add(res);
            return;
        }
        sequence.add(word);
        for (int i = 0; i < word.length(); i++) {
            char[] chars = word.toCharArray();
            for (char ch = 'a'; ch <= 'z'; ch++) {
                if (chars[i] == ch)
                    continue;
                chars[i] = ch;
                String nextWord = new String(chars);
                if (disMap.containsKey(nextWord) && disMap.get(nextWord) == disMap.get(word) - 1) {
                    find(result, sequence, nextWord, end);
                }
            }
        }
        sequence.remove(sequence.size() - 1);
    }
}
```

