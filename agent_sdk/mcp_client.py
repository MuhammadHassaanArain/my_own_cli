import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


async def main():
    async with streamablehttp_client(url="http://localhost:8000/mcp") as (read,write,id):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            list_tools = await session.list_tools()
            for tool in list_tools.tools:
                print("Tool Name: ", tool.name)

asyncio.run(main())