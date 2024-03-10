import openplugins
import os
from dotenv import load_dotenv
class OpenPlugins:
    def __init__(self) -> None:
        load_dotenv()  # 加载.env文件
        self.assistant_id = None
        self.openai_api_key = os.getenv('openai_api_key')  
        self.tools_model = os.getenv('openai_tool_model')  
        self.assistant = None
        self.yaml_file_path = os.getenv('yaml_file_path')  
    def create_assistants(self):
        if self.assistant_id:
                assistant = openplugins.Assistants(assistant_id=self.assistant_id, tools_model=self.tools_model, openai_api_key=self.openai_api_key)
                self.assistant = assistant
        else:
            assistant = openplugins.Assistants(yaml_file_path=self.yaml_file_path, tools_model=self.tools_model, openai_api_key=self.openai_api_key)
            self.assistant_id = assistant.id
            self.assistant = assistant

    def stock_market_assistants(self,context:str):
        if self.assistant is None:
             self.create_assistants()
        result = self.assistant.run(context)
        return result