import json
import os
import chainlit as cl
import functioncall as fc
from datetime import datetime
client = fc.openai_client()
model = os.getenv("openai_tool_model")
@cl.on_chat_start
def start_chat():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": f"You are a helpful chinese stockmarket assistant.Current time: {current_time}"}],
    )
@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()
    one_message = message_history
    print(one_message)
    tools = fc.load_tools()
    stream = await client.chat.completions.create(
            model=model,
            messages=one_message,
            tools=tools,
            stream=True
        )
    func_call_list = []
    async for part in stream:
        if token := part.choices[0].delta.content:
            await msg.stream_token(token)
        delta= part.choices[0].delta
        if delta.tool_calls:
            for tcchunk in delta.tool_calls:
                if len(func_call_list) <= tcchunk.index:
                    func_call_list.append({
                        "id": "",
                        "name": "",
                        "type": "function", 
                        "function": { "name": "", "arguments": "" } 
                    })
                tc = func_call_list[tcchunk.index]
                if tcchunk.id:
                    tc["id"] += tcchunk.id
                if tcchunk.function.name:
                    tc["function"]["name"] += tcchunk.function.name
                if tcchunk.function.arguments:
                    tc["function"]["arguments"] += tcchunk.function.arguments 
 
    if len(func_call_list)>0:
        print(func_call_list)
        message_history.append(
            {"role": "assistant", "tool_calls": func_call_list}
        )
        path_operation_id_map = fc.load_path_operation_id_map()
        for tool_call in func_call_list:
            function_name = tool_call["function"]['name']
            function_args = json.loads(tool_call["function"]["arguments"])
            function_args_str = '&'.join([f"{k}={v}" for k, v in function_args.items()])
            path_operation_id_url = path_operation_id_map.get(function_name)
            path_url = fc.URL+path_operation_id_url+"?"+function_args_str
            function_response = await fc.acyget_request_data(path_url)
            async with cl.Step(name="step") as step:
                step.input = tool_call
                step.output = function_response
            message_history.append(
                {
                    "tool_call_id": tool_call['id'],
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )
        stream = await client.chat.completions.create(
            model=model,
            messages=message_history,
            tools=tools,
            tool_choice=None,
            stream=True
        )
        async for part in stream:
            if token := part.choices[0].delta.content or "":
                await msg.stream_token(token)
        message_history.append({"role": "assistant", "content": msg.content})
        await msg.update()
    else:
        message_history.append({"role": "assistant", "content": msg.content})
        await msg.update()

    

