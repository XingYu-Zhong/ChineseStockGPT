# StockMarketAsisstant ChatGPT plugins quickstart 🚀💼

show video

<div align="center">

https://github.com/XingYu-Zhong/StockMarketAsisstant/assets/42194301/0005ad33-9884-4d7e-9669-27f9df301440

</div>

<div align="center">

https://github.com/XingYu-Zhong/StockMarketAsisstant/assets/42194301/827ab62e-2096-43a7-ba9c-eb1f2d087891

</div>

*Read this in other languages: [English](README.md), [中文](README_ZH.md).*

Get a StockMarketAsisstant ChatGPT plugin up and running in under 5 minutes using Python 🐍. If you do not already have plugin developer access, please [join the waitlist](https://openai.com/waitlist/plugins) 📜.

description: Plugin for accessing stock related data 📊, you can access chinese stock history data, news data, performance data, data called by institutions, etc.

## Setup 🛠

To install the required packages for this plugin, run the following command:

```bash
pip install -r requirements.txt
```

To run the plugin, enter the following command:

```bash
python apiserver.py
```

Once the local server is running 🏃:

1. Navigate to [https://chat.openai.com](https://chat.openai.com/). 🌍
2. In the Model drop down, select "Plugins" 📑 (note, if you don't see it there, you don't have access yet).
3. Select "Plugin store" 🛍
4. Select "Develop your own plugin" 🛠
5. Enter in `localhost:5003` since this is the URL the server is running on locally, then select "Find manifest file" 🔍.

The plugin should now be installed and enabled! ✅ You can start with a question like "What is on my todo list" and then try adding something to it as well! 📝

## Getting help 🙋

If you run into issues or have questions building a plugin, please join openai [Developer community forum](https://community.openai.com/c/chat-plugins/20) 🌐.