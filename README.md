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
  + [x] 多种API的setu插件
  + [x] 网易云点歌卡片支持
  + [x] 查找东方专辑以及其他专辑支持（doujinstyle）
  + [x] 乱七八糟的功能（例如占卜）
  + [x] 自定义入群欢迎（试验）
  + [ ] 关键词系统

+ 命令行相关
  + [x] 脱离于nonebot的命令系统 <small>*~~本来想用curse弄一个，结果处理不好输出，将就用一下罢~~*</small>
  + [x] 可扩展自定义命令
  + [x] 方便快捷的插件安装方式

+ 其他
  + [x] 懒人式部署方式
  + [x] 专用的配置bot一些参数的工具（如配置pixiv的refresh_token）

### 演示

---

<details>
<summary>GIF演示</summary>

to do

</details>

### 快速部署

---
1.下载Bot本体

```shell
git clone https://github.com/TeamGensouSpark/RanBot.git # 下载Bot文件
```

1.5 使用懒人安装脚本（如果不需要可跳过，否则无需进行以下步骤）

```shell
cd RanBot # 进入文件夹
python ./setup.py #国内用户请输入 python ./setup.py cn
python ./boot.py
```

2.安装依赖(**强烈建议**使用你喜欢的 Python 环境管理工具创建新的虚拟环境)
```shell
cd RanBot # 进入文件夹

pip install pip --upgrade # 更新pip

pip install -r requirements.txt # 安装python依赖
```
3. 启动RanBot！
```shell
python ./boot.py # 启动bot！
```

### FAQ (Frequently Asked Questions)

#### 安装插件(需使用`python ./boot.py`启动)

```shell
bot install <插件名称>
```

#### Bot不理我怎么办

 - 配置.env.prod修改超级用户

```env
`SUPERUSERS=["你的QQ号1","你的QQ号2","...以此类推"]`
```

 - 向运行中的bot发送`授权`，然后输入`Y`进行确认，便可获取当前会话的权限



### 感谢项目

---

[nonbot2](https://github.com/nonebot/nonebot2)：NoneBot2框架

[CirnoBot](https://github.com/summerkirakira/CirnoBot) ：README模板

[setu-nonebot2](https://github.com/yuban10703/setu-nonebot2) ：setu插件基本框架

[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) ：~~一顿狠抄~~

以及其他一些提供代码细节参考的项目，这里便不一一列出
