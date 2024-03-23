import os
import subprocess

from dotenv import load_dotenv
load_dotenv()
python_path = os.getenv("pythonpath")
# 启动 apiserver.py 脚本
subprocess.Popen([python_path if python_path else "python", "StockMarketAsisstant-master/apiserver.py"])
subprocess.Popen([python_path if python_path else "python", "toTools.py"])
subprocess.Popen(["chainlit", "run", "chainlitweb.py", "-w"])
