import json
import asyncio
from typing import Optional
from mcp import ClientSession
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import( ListToolsResult, CallToolResult, ListResourcesResult, 
ListResourceTemplatesResult, ReadResourceResult, ListPromptsResult,  GetPromptResult)

class MCPClient:
    def __init__(self, server_url):
        self._server_url : str = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack:AsyncExitStack= AsyncExitStack()

    async def connection(self):
        _read, _write, _ = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read,_write)
        )
        await self._session.initialize()
        return self._session
    
    async def Cleanup(self):
        await self._exit_stack.aclose()

    async def __aenter__(self):
        await self.connection()
        return self
    
    async def __aexit__(self,*args):
        await self.Cleanup()
        self._session = None

    # Tools
    async def tool_list(self)-> ListToolsResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_tools()
        return res.tools
    
    async def tool_call(self, tool_name:str, arguments:dict[str,any])->CallToolResult:
        assert self._session, "Session Not Found"
        res = await self._session.call_tool(name=tool_name, arguments=arguments)
        return res.content
    
    # Resources
    async def list_resource(self)-> ListResourcesResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_resources()
        return res.resources
    async def list_template_res(self)-> ListResourceTemplatesResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_resource_templates()
        return res.resourceTemplates
    async def get_resource(self, uri:str)-> ReadResourceResult:
        assert self._session, "Session Not Found"
        res = await self._session.read_resource(uri)
        return res
    # Prompts
    async def list_prompt(self)-> ListPromptsResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_prompts()
        return res
    async def get_prompt(self, prompt_name:str)-> GetPromptResult:
        assert self._session, "Session Not Found"
        res = await self._session.get_prompt(name=prompt_name)
        return res
    

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        print("-"*100)
        tool_list = await client.tool_list()
        for tool in tool_list:
            print("Tools : ", tool.name)

        # call_Shell_tool = await client.tool_call(tool_name=tool.name, arguments={"cmd":"dir"})
        # raw_output = call_Shell_tool[0].text
        # shell_response = json.loads(raw_output)
        # cmd_output = shell_response.get("error") or shell_response.get("output")
        # print("Shell Tool Output : ", cmd_output)

        # call_read_file_tool = await client.tool_call(tool_name="read_files", arguments={"path":r"D:\Hassaan_Work\quarter_3_sdk\sdk_level_two_quiz_prep\linkedin_post_contribution.txt"})
        # print("Read File Tool Call: ", call_read_file_tool[0].text)

        # call_write_file_tool = await client.tool_call(tool_name="write_file", arguments={"path":r"D:\Hassaan_Work\quarter_4\self_study\ai_native_apps\my_own_cli\mcp_server\README.md","content":"Hello written by tool"})
        # print("Write File Tool : ", call_write_file_tool[0].text)

        # call_list_dir_tool = await client.tool_call(tool_name="list_dir", arguments={"path":r"D:\Hassaan_Work\quarter_4\self_study\ai_native_apps\my_own_cli\mcp_server"})                                    
        # print("List Dir Tool : ", call_list_dir_tool[0].text)

        # call_search_in_file_tool = await client.tool_call(tool_name="search_in_files", arguments={"query":"this","path":r"D:\Hassaan_Work\quarter_4\self_study\ai_native_apps\my_own_cli\mcp_server\README.md"})
        # print("Search In Files Tool: ",call_search_in_file_tool[0].text)


asyncio.run(main())