# 股市助手 ChatGPT 插件快速入门 🚀💼

视频展示
<div align="center">

https://github.com/XingYu-Zhong/StockMarketAsisstant/assets/42194301/0005ad33-9884-4d7e-9669-27f9df301440

</div>

<div align="center">

https://github.com/XingYu-Zhong/StockMarketAsisstant/assets/42194301/827ab62e-2096-43a7-ba9c-eb1f2d087891

</div>

使用其他语言阅读: [English](README.md), [中文](README_ZH.md).

如果开了科学上网记得设置代理
```python
#设置代理
import os
os.environ['http_proxy'] = 'http://127.0.0.1:10809'
os.environ['https_proxy'] = 'http://127.0.0.1:10809'
```

使用Python在5分钟内启动并运行股市助手 ChatGPT 插件🐍。如果你还没有插件开发者权限，请[加入等待名单](https://openai.com/waitlist/plugins) 📜。

简介: 本插件用于访问股票相关数据📊，你可以访问中国股票历史数据、新闻数据、绩效数据、机构调用的数据等。

## 设置 🛠

为了安装此插件所需的包，请运行以下命令：

```bash
pip install -r requirements.txt
```

要运行插件，请输入以下命令：

```bash
python apiserver.py
```

当本地服务器运行起来后🏃：

1. 导航至 [https://chat.openai.com](https://chat.openai.com/) 🌍。
2. 在模型下拉菜单中，选择 "插件" 📑（注意，如果你在那里看不到它，说明你还没有访问权限）。
3. 选择 "插件商店" 🛍。
4. 选择 "开发你自己的插件" 🛠。
5. 输入 `localhost:5003`，因为这是本地服务器运行的URL，然后选择 "查找清单文件" 🔍。

插件现在应该已经安装并启用了！✅ 你可以从提问 "我的待办事项上有什么" 开始，然后尝试添加一些内容！📝

## 获取帮助 🙋

如果在构建插件过程中遇到问题或有任何疑问，请加入 openai [开发者社区论坛](https://community.openai.com/c/chat-plugins/20) 🌐。