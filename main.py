import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, ItemHelpers
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent
import asyncio, random
from dotenv import load_dotenv
import chainlit as cl
from agents.mcp import MCPServer, MCPServerStdio


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)



@cl.on_chat_start
def start_chat():
    """Initialize session with conversation history."""
    cl.user_session.set(
        "message_history",
        []
    )
    



@function_tool
async def order_inquiry(order_id: str) -> str:
     
    return "The order is dispatched and will be delivered to you soon"


async def handle_message(message: cl.Message, mcp_server: MCPServer):

    thinking_msg = cl.Message(content="Processing your request...")
    await thinking_msg.send()

    message_history = cl.user_session.get("message_history")

    # Save response to conversation history
    message_history.append({"role": "user", "content": message.content})

    # result = await Runner.run(agent1, input=message_history, run_config=config)


    agent1 = Agent(
        instructions="""
            You are a helpful Gmail assistant whose primary focus is to assist with Gmail queries and operations. When replying to user inquiries about emails, you might want to use multiple tools to fulfill user request make sure to do that before giving response, always format your responses to clearly display the email details in the following order:

            From: The sender's email address.

            Timestamp: The time of the email

            Subject: The subject of the email.

            Body: The main content of the email.

            Your responses should present these details in a clean and organized manner so that the user can quickly verify the important parts of each email. Keep your language friendly, concise, and clear, and ensure that you only include the necessary fields mentioned above.""",

        name = "Gmail Support Agent",
        tools=[order_inquiry],
        mcp_servers=[mcp_server]
    )

    result = Runner.run_streamed(agent1, input=message_history, run_config=config)


    await thinking_msg.remove()
    msg = cl.Message(content="")
    await msg.send()

    async for event in result.stream_events():

        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    message_history.append({"role": "assistant", "content": result.final_output})

    await msg.send()



@cl.on_message
async def run(message: cl.Message):
    async with MCPServerStdio(
        params={"command": "npx", "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"]}
        ) as server:
                        
            await handle_message(message, server)
            
    
    

