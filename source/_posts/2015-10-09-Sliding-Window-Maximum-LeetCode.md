title: Sliding Window Maximum@LeetCode
date: 2015-10-09 17:17:07
tags: LeetCode
---
## [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

核心的思路是：既然要达到`O(n)`的复杂度，那么就要保持窗口内的最大值在窗口边界上。<!-- more -->达到这个效果的方法就是滤掉窗口中没用的元素。维护一个双向队列，队列保存数组的下标，每当有新元素进入队列时，从队尾开始，删掉连续的比新元素小的元素，然后将其插入到队列末尾。之所以可以这样删掉元素是基于：这些元素永远都不会在一个窗口中成为最大的元素。这样就保证了队首的元素始终是窗口（队列）中最大的，并且队列中始终保持了所有可能在一个窗口中成为最大元素的元素。至于队首元素的弹出，则只要判断目前窗口的位置即可。

实现代码：

```
public class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        if (nums == null || nums.length == 0)
            return nums;
        int[] result = new int[nums.length - k + 1];
        LinkedList<Integer> queue = new LinkedList<Integer>();
        for (int i = 0; i < nums.length; i++) {
            while (!queue.isEmpty() && nums[queue.peekLast()] < nums[i])
                queue.pollLast();
            queue.add(i);
            if (queue.peekFirst() == i - k)
                queue.pollFirst();
            if (i >= k - 1)
                result[i - k + 1] = nums[queue.peekFirst()];
        }
        return result;
    }
}
```