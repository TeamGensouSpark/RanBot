<div align=center>
  <img width=200 src="doc/image/Avatar.png"  alt="image"/>
  <h1 align="center">RanBot</h1>
</div>
<div align=center>
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">
  <img src="https://img.shields.io/badge/nonebot-2-red" alt="nonebot">
</div>

### 八云蓝 🦊

---

八云蓝（Yakumo Ran）是拥有相当高智力，尤其擅长数学的妖怪，我以她为原型制作了这一款bot，希望能带给各位欢乐。

*果然爱吃油豆腐的妖怪狐狸还是很可爱吧（笑）*

### 实现功能 ✨

---

🚧 重写中......

### 演示 ▶️

---

<details>
<summary>GIF演示</summary>

to do

</details>

### 快速部署 🚀

---

1. 下载Bot本体 🚥

```shell
git clone https://github.com/TeamGensouSpark/RanBot.git # 下载Bot文件
```

2. 安装虚拟环境以及依赖 📖

#### Windows 🪟

```powershell
cd RanBot # 进入文件夹
./setup.ps1
```

#### Linux 🐧

```bash
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip install pdm -i https://pypi.tuna.tsinghua.edu.cn/simple
pdm config pypi.url https://pypi.tuna.tsinghua.edu.cn/simple
pdm install
eval $(pdm venv activate)
python -m ensurepip
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 进入虚拟环境 ⚙️

#### Windows 🪟

```powershell
./virtualshell.ps1 
# 手动进入 Invoke-Expression (pdm venv activate)
```

#### Linux 🐧

```bash
eval $(pdm venv activate)
```

4. 添加插件 💡

参考`nb-cli`用法

```shell
nb install <插件名称>
```

5. 配置环境变量 🔧

+ 在Bot目录下新建.env文件

```python
PORT=8088 #连接端口号

SUPERUSERS=["123456"] #超管
NICKNAME=["koishi"] #bot名称
COMMAND_START=["/", ""]
COMMAND_SEP=["."]
```

6. 启动 🎉

记得先进入虚拟环境

```shell
nb run
```

### FAQ (Frequently Asked Questions)

#### Bot不理我怎么办

+ 按照上方方法添加超管
+ 在你需要授权的会话中向运行中的bot发送`授权`，便可获取当前会话的权限

### 感谢项目

---

[nonbot2](https://github.com/nonebot/nonebot2)：NoneBot2框架
[CirnoBot](https://github.com/summerkirakira/CirnoBot) ：README模板
[setu-nonebot2](https://github.com/yuban10703/setu-nonebot2) ：setu插件基本框架
[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) ：~~一顿狠抄~~

以及其他一些提供代码细节参考的项目，这里便不一一列出
