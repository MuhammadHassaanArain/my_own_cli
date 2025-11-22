import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, set_tracing_export_api_key
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

async def main():
    # async with streamablehttp_client("http://localhost:8000/mcp/") as (read,write,session_id):
    #     async with ClientSession(read_stream=read, write_stream=write) as session:
    #         await session.initialize()
    #         list_tools = await session.list_tools()
    #         for tool in list_tools.tools:
    #             print("Tools: ", tool.name)

    mcpparams = MCPServerStreamableHttpParams(url="http://localhost:8000/mcp/")
    async with MCPServerStreamableHttp(name="my_own_cli", params=mcpparams) as server:
        agent = Agent(
        name="Assistant",
        instructions="""
You are a helpful assistant.
"""
,
        model=model,
        mcp_servers=[server],
        model_settings=ModelSettings(tool_choice="auto"),
        )

        result =await  Runner.run(agent, input=input("Write here : "))
        print(result.final_output)



asyncio.run(main())