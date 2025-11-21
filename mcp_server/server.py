from  mcp.server.fastmcp import FastMCP
import subprocess
import os
import aiofiles
import asyncio

mcp = FastMCP("MY-OWN-CLI-Server", stateless_http=True)

@mcp.tool(name="run_shell")
async def run_shell(cmd:str):
    """Run a shell command and return output"""
    try:
        result = subprocess.check_output(cmd, shell=True,text=True)
        return {"output":result}
    except Exception as e:
        return {"error":str(e)}

@mcp.tool(name="read_files")
async def read_file(path:str):
    """Read a file asynchronousley and return its contents"""
    if not os.path.exists(path):
        return f"Error: Files not found -> {path}"
    if os.path.isdir(path):
        return f"Error: Path is a Directory, not a file -> {path}"
    try:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool(name="write_file")
async def write_file(path:str, content:str):
    """Create or overwrite a file with the given content using asyncio.to_thread 
    so no external libraries are needed"""
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        try:
            os.mkdir(folder, exist_ok=True)
        except Exception as e:
            return f"Error: Unable to create directories -> {str(e)}"
    try:
        def _write():
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "File written successfully!"
        result = await asyncio.to_thread(_write)
        return result
    except Exception as e:
        return f"Error writing file : {str(e)}"

@mcp.tool(name="list_dir")
async def list_dir(path:str):
    """List the contents of a directory (files + folders)"""
    if not os.path.exists(path):
        return f"Error: Directory does not exist -> {path}"
    if not os.path.isdir(path):
        return f"Error: Path is not a directory -> {path}"
    try:
        def _list():
            items = os.listdir(path)
            if not items:
                return "Directory is empty"
            result = ["Contents:"]
            for item in items:
                full = os.path.join(path, item)
                if os.path.isdir(full):
                    result.append(f"[DIR] {item}")
                else:
                    result.append(f"[FILE] {item}")
            return "\n".join(result)
        return await asyncio.to_thread(_list)

    except Exception as e:
        return f"Error reading dirctory: {str(e)}"

@mcp.tool(name="search_in_files")
async def search_in_files(query:str, path:str):
    """Search for a string in all files under the given path.
    Returns file paths and matching lines."""
    if not os.path.exists(path):
        return f"Error: Path does not exist -> {path}"
    if os.path.isfile(path):
        files_to_search = [path]
    else:
        files_to_search = []
        for root, dirs, files in os.walk(path):
            for file in files:
               files_to_search.append(os.path.join(root, file))

    matches = []
    def _search():
        for file_path in files_to_search:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f,1):
                        if query in line:
                            matches.append(f"{file_path} [Line {i}] : {line.strip()}")
            except Exception:
                continue
        if not matches:
            return f"No matches found for '{query}' in {path}"
        return "\n".join(matches)
    return await asyncio.to_thread(_search)




mcp_app = mcp.streamable_http_app()