import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import requests
import json
import aiohttp
path_operation_id_map = 'tmp/path_operation_id_map.json'
path_tools = 'tmp/tools.json'


URL = os.getenv("stock_asisstants_url")

def openai_client():
    load_dotenv()
    apikey = os.getenv("openaiapikey")
    if not apikey:
        raise ValueError(".env file:API key for OpenAI is missing.")
    return AsyncOpenAI(api_key = apikey)

def get_request_data(path_url):
    try:
        response = requests.get(path_url)
        # 确保请求成功
        response.raise_for_status()
        # 返回JSON格式的数据，如果响应内容不是JSON格式，这里会抛出异常
        if response.headers.get('Content-Type', '').startswith('application/json'):
            return response.json()
        else:
            return response.text()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Other error occurred: {err}')
    except ValueError as json_err:
        print(f'JSON decode error: {json_err}')
    return None



async def acyget_request_data(path_url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(path_url) as response:
                # 确保请求成功
                response.raise_for_status()
                # 返回JSON格式的数据，如果响应内容不是JSON格式，这里会抛出异常
                # 根据Content-Type处理响应
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    return await response.json()
                elif 'text/' in content_type:
                    return await response.text()
                else:
                    # 对于非文本和非JSON响应，返回原始数据
                    return await response.read()
        except aiohttp.ClientResponseError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except aiohttp.ClientError as err:
            print(f'Other error occurred: {err}')
        except ValueError as json_err:
            print(f'JSON decode error: {json_err}')
    return None


def load_tools():
    with open(path_tools, 'r', encoding='utf-8') as file:
        tools = json.load(file)
    return tools

def load_path_operation_id_map():
    with open(path_operation_id_map, 'r', encoding='utf-8') as file:
        tools = json.load(file)
    return tools



