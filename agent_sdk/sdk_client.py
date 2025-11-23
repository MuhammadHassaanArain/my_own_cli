import os
from dotenv import load_dotenv
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, RunConfig
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

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
config = RunConfig(
    model=model,
    model_provider=client,
)

async def run_agent(user_input:str):
    mcpparams = MCPServerStreamableHttpParams(url="http://localhost:8000/mcp/")
    async with MCPServerStreamableHttp(name="my_own_cli", params=mcpparams) as server:
        agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        
        mcp_servers=[server],
        model_settings=ModelSettings(tool_choice="auto"),
        )
        result = await Runner.run(agent, input=user_input, run_config=config)
        print(result.final_output)
