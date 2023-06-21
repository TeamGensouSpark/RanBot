<div align=center>
  <img width=200 src="doc/image/Avatar.png"  alt="image"/>
  <h1 align="center">RanBot</h1> 
</div>
<div align=center>
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">
  <img src="https://img.shields.io/badge/nonebot-2-red" alt="nonebot">
</div>




### 蓝Bot

---

八云蓝（Yakumo Ran）是拥有相当高智力，尤其擅长数学的妖怪，我以她为原型制作了这一款bot，希望能带给各位欢乐。

*果然爱吃油豆腐的妖怪狐狸还是很可爱吧（笑）*

### 实现功能

---

+ Bot相关
  + [x] 较为完善权限系统
  + [x] 干净的文件管理
  + [x] 网易云点歌卡片支持
  + [x] 查找东方专辑以及其他专辑支持（doujinstyle）
  + [x] 乱七八糟的功能（例如占卜）

+ TODO
  + [x] TODO

### 演示

---

<details>
<summary>GIF演示</summary>

to do

</details>

### 快速部署

---
1. 下载Bot本体

```shell
git clone https://github.com/TeamGensouSpark/RanBot.git # 下载Bot文件
```

2. 安装虚拟环境（PDM）以及依赖

```shell
cd RanBot # 进入文件夹
./setup.bat
```

3. 添加插件（例子）

```shell
pdm run nb install nonebot_plugin_gocqhttp
```

4. 添加超管

 - 在Bot目录下新建.env文件，写入`ENVIRONMENT=prod`
 - 新建.env.prod文件，写入`SUPERUSERS=["超管QQ"]`

5. 启动！

```shell
./run.bat
```

### FAQ (Frequently Asked Questions)

#### 安装插件(需使用`python ./boot.py`启动)

```shell
bot install <插件名称>
```

#### Bot不理我怎么办

 - 按照上方方法添加超管

 - 在你需要授权的会话中向运行中的bot发送`授权`，然后输入`Y`进行确认，便可获取当前会话的权限



### 感谢项目

---

[nonbot2](https://github.com/nonebot/nonebot2)：NoneBot2框架

[CirnoBot](https://github.com/summerkirakira/CirnoBot) ：README模板

[setu-nonebot2](https://github.com/yuban10703/setu-nonebot2) ：setu插件基本框架

[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) ：~~一顿狠抄~~

以及其他一些提供代码细节参考的项目，这里便不一一列出
