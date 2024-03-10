import chainlit as cl

from controllerplugins import OpenPlugins


op = OpenPlugins()

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    result = op.stock_market_assistants(message.content)
    print(result)
    # Send a response back to the user
    await cl.Message(
        content=result['response'],
    ).send()
