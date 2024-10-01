# guess
#### 准备工作：

> **1.一台可以联网的电脑**

>  **2.一个可以正常运行的mumu12模拟器**

>  **3.一个文本编辑器，推荐vscode, 下载链接：https://code.visualstudio.com/docs/?dv=win64user**

>  **4.若需要qq机器人，还需准备：**

>       ​	**4.1 nodejs，下载链接：https://nodejs.org/dist/v20.17.0/node-v20.17.0-x64.msi**

>    ​	**4.2 一个qq号(要求绑定的手机号可收手机验证码)**

> **5.若需要群主远程：需准备gameviewer远程工具，最新版mumu自带，若未下载，可至 https://adl.netease.com/d/g/uuremote/c/gw?type=pc 下载**

##### 推荐使用`miniconda`运行`python`虚拟环境，推荐`python3.10`



### 小白推荐执行bat脚本一键启动！！！

#### 分别执行

#### 		1.conda一键安装.bat

#### 		2一键初始化.bat

#### 		3一键启动.bat

### 两种执行方案：

#### 1.全自动：随大流、爬取博主预测

###### 在项目所在目录使用`cmd`执行`python start.py`可运行随大流/爬取博主,如下：切换变量mode的注释来选择是随大流还是爬取博主

```python
#start.py
if __name__ == '__main__':
    # 模式选择
    # mode = '爬取博主预测数据'
    mode = '随大流'
    ......
```

#### 2.半自动：qq机器人指令控制押注

在项目所在目录使用`cmd`执行`python server.py`即可启动服务端

##### 接下来是部署QQ机器人：

一般人不会，可代部署

## 后面的小白不用看，需要改源码的老登可以看！！！

##### 命令行执行教程(脚本目录执行)：

```shell
conda create -n yys python=3.10
conda activate yys
pip install -r requirements.txt
python start.py
```



###### 百度搜索`miniconda`安装教程(也可看此教程：https://blog.csdn.net/ming12131342/article/details/140233867)，根据教程安装miniconda（群文件有安装包），之后直接运行`conda create -n yys python=3.10`

**安装miniconda只需要注意勾选以下这个就行，其他的一路next**

<img src="C:\Users\c1784\Desktop\conda.png" alt="conda" style="zoom: 67%;" />

###### 创建完成后 `conda activate yys`

###### 在脚本目录下执行`pip install -r requirements.txt`下载依赖

