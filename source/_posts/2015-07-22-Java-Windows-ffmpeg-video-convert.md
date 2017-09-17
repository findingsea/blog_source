title: Java+Windows+ffmpeg实现视频转换
date: 2015-07-22 11:15:50
tags: [Windows, Java, ffmpeg]
---

旧文，源地址见[这里](http://www.cnblogs.com/findingsea/archive/2013/03/14/2959634.html)。

最近由于项目需要，研究了一下如何用Java实现视频转换，“着实”废了点心思，整理整理，写出给自己备忘下。

<!-- more -->

## 思路

由于之前没有没法过相关功能的经验，一开始来真不知道从哪里入手。当然，这个解决，google一下立马就发现了ffmpeg，网上讲解用Java+ffmpeg来进行视频转换的文章也不在少数，我主要参考的[这篇文章](http://blog.csdn.net/jimzhai/article/details/7853005)。

上文提到的这篇文章，基本已经把开发流程什么的讲的很清楚了，这里总结下：

1. 核心是利用ffmpeg进行视频转换，我们自己并不写转换视频的代码，只是调用ffmpeg，它会帮我们完成视频的转换。ffmpeg支持的类型有：asx，asf，mpg，wmv，3gp，mp4，mov，avi，flv等，这些类型，可以利用ffmpeg进行直接转换。ffmpeg不支持的类型有：wmv9，rm，rmvb等，这些类型需要先用别的工具（mencoder）转换为avi(ffmpeg能解析的)格式。

2. 了解Java如何调用外部程序，这会是最困难的，也会是坑最多的地方。

3. 根据我们的需求设置ffmpeg的参数。（这类文章网上已经有很多了，我也不用复制黏贴了，见[这里](http://blog.csdn.net/hemingwang0902/article/details/4382205)）

## 代码

上文中提到的那篇文章中的代码其实已经写的很友好了，基本拿来就能用，不过仍然存在许多问题，接下来会讲到，下面是文中的代码：

``` java
import java.io.File;  
import java.util.ArrayList;  
import java.util.Calendar;  
import java.util.List;  
  
public class ConvertVideo {  
  
    private final static String PATH = "c:\\ffmpeg\\input\\c.mp4";  
  
    public static void main(String[] args) {  
        if (!checkfile(PATH)) {  
            System.out.println(PATH + " is not file");  
            return;  
        }  
        if (process()) {  
            System.out.println("ok");  
        }  
    }  
  
    private static boolean process() {  
        int type = checkContentType();  
        boolean status = false;  
        if (type == 0) {  
            System.out.println("直接将文件转为flv文件");  
            status = processFLV(PATH);// 直接将文件转为flv文件  
        } else if (type == 1) {  
            String avifilepath = processAVI(type);  
            if (avifilepath == null)  
                return false;// avi文件没有得到  
            status = processFLV(avifilepath);// 将avi转为flv  
        }  
        return status;  
    }  
  
    private static int checkContentType() {  
        String type = PATH.substring(PATH.lastIndexOf(".") + 1, PATH.length())  
                .toLowerCase();  
        // ffmpeg能解析的格式：（asx，asf，mpg，wmv，3gp，mp4，mov，avi，flv等）  
        if (type.equals("avi")) {  
            return 0;  
        } else if (type.equals("mpg")) {  
            return 0;  
        } else if (type.equals("wmv")) {  
            return 0;  
        } else if (type.equals("3gp")) {  
            return 0;  
        } else if (type.equals("mov")) {  
            return 0;  
        } else if (type.equals("mp4")) {  
            return 0;  
        } else if (type.equals("asf")) {  
            return 0;  
        } else if (type.equals("asx")) {  
            return 0;  
        } else if (type.equals("flv")) {  
            return 0;  
        }  
        // 对ffmpeg无法解析的文件格式(wmv9，rm，rmvb等),  
        // 可以先用别的工具（mencoder）转换为avi(ffmpeg能解析的)格式.  
        else if (type.equals("wmv9")) {  
            return 1;  
        } else if (type.equals("rm")) {  
            return 1;  
        } else if (type.equals("rmvb")) {  
            return 1;  
        }  
        return 9;  
    }  
  
    private static boolean checkfile(String path) {  
        File file = new File(path);  
        if (!file.isFile()) {  
            return false;  
        }  
        return true;  
    }  
  
    // 对ffmpeg无法解析的文件格式(wmv9，rm，rmvb等), 可以先用别的工具（mencoder）转换为avi(ffmpeg能解析的)格式.  
    private static String processAVI(int type) {  
        List<String> commend = new ArrayList<String>();  
        commend.add("c:\\ffmpeg\\mencoder");  
        commend.add(PATH);  
        commend.add("-oac");  
        commend.add("lavc");  
        commend.add("-lavcopts");  
        commend.add("acodec=mp3:abitrate=64");  
        commend.add("-ovc");  
        commend.add("xvid");  
        commend.add("-xvidencopts");  
        commend.add("bitrate=600");  
        commend.add("-of");  
        commend.add("avi");  
        commend.add("-o");  
        commend.add("c:\\ffmpeg\\output\\a.avi");  
        try {  
            ProcessBuilder builder = new ProcessBuilder();  
            builder.command(commend);  
            builder.start();  
            return "c:\\ffmpeg\\output\\a.avi";  
        } catch (Exception e) {  
            e.printStackTrace();  
            return null;  
        }  
    }  
  
    // ffmpeg能解析的格式：（asx，asf，mpg，wmv，3gp，mp4，mov，avi，flv等）  
    private static boolean processFLV(String oldfilepath) {  
  
        if (!checkfile(PATH)) {  
            System.out.println(oldfilepath + " is not file");  
            return false;  
        }  
          
        // 文件命名  
        Calendar c = Calendar.getInstance();  
        String savename = String.valueOf(c.getTimeInMillis())+ Math.round(Math.random() * 100000);  
        List<String> commend = new ArrayList<String>();  
        commend.add("c:\\ffmpeg\\ffmpeg");  
        commend.add("-i");  
        commend.add(oldfilepath);  
        commend.add("-ab");  
        commend.add("56");  
        commend.add("-ar");  
        commend.add("22050");  
        commend.add("-qscale");  
        commend.add("8");  
        commend.add("-r");  
        commend.add("15");  
        commend.add("-s");  
        commend.add("600x500");  
        commend.add("c:\\ffmpeg\\output\\a.flv");  
  
        try {  
            Runtime runtime = Runtime.getRuntime();  
            Process proce = null;  
            String cmd = "";  
            String cut = "     c:\\ffmpeg\\ffmpeg.exe   -i   "  
                    + oldfilepath  
                    + "   -y   -f   image2   -ss   8   -t   0.001   -s   600x500   c:\\ffmpeg\\output\\"  
                    + "a.jpg";  
            String cutCmd = cmd + cut;  
            proce = runtime.exec(cutCmd);  
            ProcessBuilder builder = new ProcessBuilder(commend);  
             builder.command(commend);  
            builder.start();  
  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
}
```

接下来是我自己经过修改后的代码：

``` java
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
public class ConvertVideo {
    
    private static String inputPath = "";
    
    private static String outputPath = "";
    
    private static String ffmpegPath = "";
    
    public static void main(String args[]) throws IOException {
        
        getPath();
        
        if (!checkfile(inputPath)) {
            System.out.println(inputPath + " is not file");
            return;
        }
        if (process()) {
            System.out.println("ok");
        }
    }
    
    private static void getPath() { // 先获取当前项目路径，在获得源文件、目标文件、转换器的路径
        File diretory = new File("");
        try {
            String currPath = diretory.getAbsolutePath();
            inputPath = currPath + "\\input\\test.wmv";
            outputPath = currPath + "\\output\\";
            ffmpegPath = currPath + "\\ffmpeg\\";
            System.out.println(currPath);
        }
        catch (Exception e) {
            System.out.println("getPath出错");
        }
    }
    
    private static boolean process() {
        int type = checkContentType();
        boolean status = false;
        if (type == 0) {
            System.out.println("直接转成flv格式");
            status = processFLV(inputPath);// 直接转成flv格式
        } else if (type == 1) {
            String avifilepath = processAVI(type);
            if (avifilepath == null)
                return false;// 没有得到avi格式
            status = processFLV(avifilepath);// 将avi转成flv格式
        }
        return status;
    }

    private static int checkContentType() {
        String type = inputPath.substring(inputPath.lastIndexOf(".") + 1, inputPath.length())
                .toLowerCase();
        // ffmpeg能解析的格式：（asx，asf，mpg，wmv，3gp，mp4，mov，avi，flv等）
        if (type.equals("avi")) {
            return 0;
        } else if (type.equals("mpg")) {
            return 0;
        } else if (type.equals("wmv")) {
            return 0;
        } else if (type.equals("3gp")) {
            return 0;
        } else if (type.equals("mov")) {
            return 0;
        } else if (type.equals("mp4")) {
            return 0;
        } else if (type.equals("asf")) {
            return 0;
        } else if (type.equals("asx")) {
            return 0;
        } else if (type.equals("flv")) {
            return 0;
        }
        // 对ffmpeg无法解析的文件格式(wmv9，rm，rmvb等),
        // 可以先用别的工具（mencoder）转换为avi(ffmpeg能解析的)格式.
        else if (type.equals("wmv9")) {
            return 1;
        } else if (type.equals("rm")) {
            return 1;
        } else if (type.equals("rmvb")) {
            return 1;
        }
        return 9;
    }

    private static boolean checkfile(String path) {
        File file = new File(path);
        if (!file.isFile()) {
            return false;
        }
        return true;
    }

    // 对ffmpeg无法解析的文件格式(wmv9，rm，rmvb等), 可以先用别的工具（mencoder）转换为avi(ffmpeg能解析的)格式.
    private static String processAVI(int type) {
        List<String> commend = new ArrayList<String>();
        commend.add(ffmpegPath + "mencoder");
        commend.add(inputPath);
        commend.add("-oac");
        commend.add("lavc");
        commend.add("-lavcopts");
        commend.add("acodec=mp3:abitrate=64");
        commend.add("-ovc");
        commend.add("xvid");
        commend.add("-xvidencopts");
        commend.add("bitrate=600");
        commend.add("-of");
        commend.add("avi");
        commend.add("-o");
        commend.add(outputPath + "a.avi");
        try {
            ProcessBuilder builder = new ProcessBuilder();
            Process process = builder.command(commend).redirectErrorStream(true).start();
            new PrintStream(process.getInputStream());
            new PrintStream(process.getErrorStream());
            process.waitFor();
            return outputPath + "a.avi";
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    // ffmpeg能解析的格式：（asx，asf，mpg，wmv，3gp，mp4，mov，avi，flv等）
    private static boolean processFLV(String oldfilepath) {

        if (!checkfile(inputPath)) {
            System.out.println(oldfilepath + " is not file");
            return false;
        }
        
        List<String> command = new ArrayList<String>();
        command.add(ffmpegPath + "ffmpeg");
        command.add("-i");
        command.add(oldfilepath);
        command.add("-ab");
        command.add("56");
        command.add("-ar");
        command.add("22050");
        command.add("-qscale");
        command.add("8");
        command.add("-r");
        command.add("15");
        command.add("-s");
        command.add("600x500");
        command.add(outputPath + "a.flv");

        try {
            
            // 方案1
//            Process videoProcess = Runtime.getRuntime().exec(ffmpegPath + "ffmpeg -i " + oldfilepath 
//                    + " -ab 56 -ar 22050 -qscale 8 -r 15 -s 600x500 "
//                    + outputPath + "a.flv");
            
            // 方案2
            Process videoProcess = new ProcessBuilder(command).redirectErrorStream(true).start();
            
            new PrintStream(videoProcess.getErrorStream()).start();
            
            new PrintStream(videoProcess.getInputStream()).start();
            
            videoProcess.waitFor();
            
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}

class PrintStream extends Thread 
{
    java.io.InputStream __is = null;
    public PrintStream(java.io.InputStream is) 
    {
        __is = is;
    } 

    public void run() 
    {
        try 
        {
            while(this != null) 
            {
                int _ch = __is.read();
                if(_ch != -1) 
                    System.out.print((char)_ch); 
                else break;
            }
        } 
        catch (Exception e) 
        {
            e.printStackTrace();
        } 
    }
}

```

问题

原文的代码中有一个很大的问题，便是不知道视频转换到底什么时候结束。看原文中的这两处代码：

98行处


```
builder.command(commend);  
builder.start();  
return "c:\\ffmpeg\\output\\a.avi"; 

```

145行处

```
builder.start();  
  
return true;

```

在进程开始之后，直接就返回结果了。要知道，这样的写法，是不会阻塞当前进程的，也就是说，当然程序返回的时候，转码程序（ffmpeg和mencoder）还在执行。如果需要mencoder进行中间转码，那原文中的写法会造成在avi文件还未转换完成时，程序就调用了ffmpeg进行转换。而对于最终的flv文件，我们也无法知道到底是什么时候转换好的，这显然是无法满足我们的业务需求的 。

解决方案

最先想到的办法自然就是阻塞当前进程（主进程），实例代码：


```
Process process = new ProcessBuilder(command).start();
process.waitFor();
return true;
```


采用这种的方案运行程序，发现视频转到十几秒的时候就不转了，但是程序还没返回，打开进程管理器一开，ffmpeg进程还在，内存还占着，但是CPU为0。

当时不知道什么原因，在网上查了半天，才明白这是死锁了，但是不知道是什么原因造成的。当时就一直觉得死锁是`waitFor()`函数造成了，看来用它来判断子进程是否结果是不行了，所以又在网上查了半天其他判断子进程结束的办法（这里其实就已经走弯路了）。有人说可以用`exitValue()`，于是就有了下面的代码：

```
Process process = new ProcessBuilder(command).start();
while (true) {
    try {
        if (process.exitValue() == 0)
            break;
    }
    catch (IllegalThreadStateException e) {
        continue;
    }
}
return true;
```

当子进程没有结束的时候，如果执行exitValue()就会抛出异常，我采用的办法是捕获这个异常然后不去理他，直到程序结束exitValue()返回0为止。但是，还是失败了，出现的情况和用waitFor()方式时的一模一样，我才觉得可能是另外的原因，在去google，发现可能是是由于JVM只提供有限缓存空间，当外部程序（子进程）的输出流超出了这个有限空间而父进程又不读出这些数据，子进程会被阻塞waitFor()永远都不会返回，就会造成死锁。

官方解释：

> Because some native platforms only provide limited buffer size for standard input and output streams, failure to promptly write the input stream or read the output stream of the subprocess may cause the subprocess to block, and even deadlock.

知道问题了就要对症下药（其实当时我也不知道这是不是就是我遇到的问题，只能各种打散弹了，打中了算）。关于如何读出子进程的输出流，如何解决这个死锁，网上的办法都大同小异，写的比较好的可以看这个地址。

于是程序被改成这样：

```
Process process = new ProcessBuilder(command).start();
                        
new PrintStream(process.getInputStream()).start();
            
process.waitFor();
PrintStream类如下：

class PrintStream extends Thread 
{
    java.io.InputStream __is = null;
    public PrintStream(java.io.InputStream is) 
    {
        __is = is;
    } 

    public void run() 
    {
        try 
        {
            while(this != null) 
            {
                int _ch = __is.read();
                if(_ch != -1) 
                    System.out.print((char)_ch); 
                else break;
            }
        } 
        catch (Exception e) 
        {
            e.printStackTrace();
        } 
    }
}
```

运行，发现还是不对，症状和之前的一模一样，我还以为是不是输出流太多了，一个线程读的不够快（好吧，真的很傻很天真，人被逼急了真的什么想法都有），于是我就再开了几个一模一样的线程，结果还是一样。

就在我快要放弃的时候，在百度知道上，看了个无关痛痒的例子，于是做了个小修改，在进程启动之前，重定向了下错误输出流，如下：

```
Process videoProcess = new ProcessBuilder(command).redirectErrorStream(true).start();
                        
new PrintStream(videoProcess.getInputStream()).start();
            
videoProcess.waitFor();
            
return true;
```

然后，然后，然后就可以了，凌乱。。。

结论

其实有两种写法可以解决这个问题，这种事像我上面那样写，还有一种如下：

```
Process videoProcess = new ProcessBuilder(command).start();
            
new PrintStream(videoProcess.getErrorStream()).start();
            
new PrintStream(videoProcess.getInputStream()).start();
            
videoProcess.waitFor();
            
return true;
```

其实道理还是一样的，就是读出ffmpeg的输出流，避免ffmpeg的输出流塞满缓存造成死锁。但是不知道为什么，ffmpeg的输出信息是在错误输出流里面的，我看了下控制台打印结果，发现只是一些当前转换状态的信息，并没有错误，令人费解。

在Process类中，getInputStream用来获取进程的输出流，getOutputStream用来获取进程的输入流，getErrorStream用来获取进程的错误信息流。为了保险起见，在读出的时候，最好把子进程的输出流和错误流都读出来，这样可以保证清空缓存区。

其实，我深刻地感觉到，这些解决的问题的经历是标准的散弹式编程，打到哪算哪，以后引以为戒。

 

  

 