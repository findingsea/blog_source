---
layout: post
title: "系统日志"
date: 2014-02-20 20:54
comments: true
tags: 日志
---
整理Evernote的时候发现有一篇很零散的系统日志，所以整理一下放上来。

<!-- more -->


###[2013-12-4]
程序运行的时候，需要内存空间存放数据。一般来说，系统会划分出两种不同的内存空间：一种叫做stack（栈），另一种叫做heap（堆）。它们的主要区别是：stack是有结构的，每个区块按照一定次序存放，可以明确知道每个区块的大小；heap是没有结构的，数据可以任意存放。因此，stack的寻址速度要快于heap。
其他的区别还有，一般来说，每个线程分配一个stack，每个进程分配一个heap，也就是说，stack是线程独占的，heap是线程共用的。此外，stack创建的时候，大小是确定的，数据超过这个大小，就发生stack overflow错误，而heap的大小是不确定的，需要的话可以不断增加。根据上面这些区别，数据存放的规则是：只要是局部的、占用空间确定的数据，一般都存放在stack里面，否则就放在heap里面。
```
public void Method1(){
	int i=4;
	int y=2;
	class1 cls1 = new class1(); 
}
```

上面代码的Method1方法，共包含了三个变量：i, y 和 cls1。其中，i和y的值是整数，内存占用空间是确定的，而且是局部变量，只用在Method1区块之内，不会用于区块之外。cls1也是局部变量，但是类型为指针变量，指向一个对象的实例。指针变量占用的大小是确定的，但是对象实例以目前的信息无法确知所占用的内存空间大小。 
这三个变量和一个对象实例在内存中的存放方式如下。

![example](/images/2014/2/20/example.jpeg)

从上图可以看到，i、y和cls1都存放在stack，因为它们占用内存空间都是确定的，而且本身也属于局部变量。但是，cls1指向的对象实例存放在heap，因为它的大小不确定。作为一条规则可以记住，所有的对象都存放在heap。
接下来的问题是，当Method1方法运行结束，会发生什么事？
回答是整个stack被清空，i、y和cls1这三个变量消失，因为它们是局部变量，区块一旦运行结束，就没必要再存在了。而heap之中的那个对象实例继续存在，直到系统的垃圾清理机制（garbage collector）将这块内存回收。因此，一般来说，内存泄漏都发生在heap，即某些内存空间不再被使用了，却因为种种原因，没有被系统回收。

###[2013-09-18]
今天想配置一下在终端中启动MacVim，按网上的教程配置了在$PATH中设置了路径之后，在终端中用命令mvim中启动MacVim总是出现很诡异的情况，MacVim的确是启动起来了，但是没有新建窗口，而终端也进入vim但是无法做任何操作（按任何键都会在插入字符）。并且由于原来就存在的两个问题：终端中的vim无法识别transparency属性和用Homebrew安装的vim于YouCompleteMe存在冲突，而MacVim在这两方面都没问题，所以决定干脆直接把终端中的vim替换成MacVim，替换的方法十分简单：
1.找到MacVim.app所在目录，在此目录下启动终端，运行：`cp mvim /usr/local/bin/`
2.在.zshrc中写入`alias vim='mvim -v'`
配置完之后，当在终端中输入`vim test.txt`，终端讲会用MacVim打开文件（但还是显示在终端中，不过读取的配置文件都是MacVim的，并且不会出现上述的两个错误）

###[2013-09-19]
昨天晚上和今天上，给Mac和台式机上的Vim都装了ConqueTerm，一个用来在Vim中启动终端的插件。这主要是因为在tmux下，Vim在插入模式下，按方向键会输出字母，具体原因还没有弄清楚。（[问题](http://ruby-china.org/topics/4866)，[相关文章1](http://jeetworks.org/node/89)，[相关文章2](http://vim.wikia.com/wiki/Fix_arrow_keys_that_display_A_B_C_D_on_remote_shell)）虽然设置了:`set term=cons25`之后能解决tmux下Vim的方向键问题，但是又引入了新问题：在终端中正常启动Vim进行编辑时，任何按键都输出乱码，加之我对于tmux这种模式不是很有好感（需要先进入tmux模式才能进行多窗口，感觉总是比直接在终端操作多了一层），所以转换思路，在Vim中使用终端。我的最终目的无非是为了能在编写代码时不退出Vim而直接运行调试，ConqueTerm很好的满足了我的需求。ConqueTerm的安装方法：
在[这里](http://www.vim.org/scripts/script.php?script_id=2771)中下载.vba或.vmb，直接用Vim打开然后运行:`so %`即可。