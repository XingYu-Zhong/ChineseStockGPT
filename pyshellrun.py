import subprocess

from controllerplugins import OpenPlugins

# 启动 apiserver.py 脚本
subprocess.run(["python", "StockMarketAsisstant-master/apiserver.py"])

subprocess.run(["chainlit", "run", "chainlitweb.py", "-w"])
