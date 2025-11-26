import asyncio
import os
import http.client
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
ENV_FILE = Path(__file__).parent.parent / ".env"

def banner():
    console.print(Panel.fit(
        "[bold cyan]🚀 MY OWN CLI — AI Terminal Assistant[/bold cyan]",
        border_style="cyan",
        padding=(1, 4)
    ))

def ensure_api_key():
    """Load API key from .env or prompt if missing."""
    api_key = os.environ.get("API_KEY")

    if not api_key and ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            for line in f:
                if line.startswith("API_KEY="):
                    api_key = line.strip().split("=", 1)[1]

    if not api_key:
        api_key = Prompt.ask("[bold yellow]Enter your API key[/bold yellow]").strip()
        if not api_key:
            console.print("[red]API Key is required! Exiting.[/red]")
            exit(1)

        with open(ENV_FILE, "a") as f:
            f.write(f"\nAPI_KEY={api_key}\n")

        console.print("[green]API key saved in .env[/green]")

    os.environ["API_KEY"] = api_key


def check_mcp_server():
    """Check if MCP server is running on 127.0.0.1:8000"""
    try:
        conn = http.client.HTTPConnection("127.0.0.1", 8000, timeout=1)
        conn.request("GET", "/")
        conn.close()
        return True
    except:
        return False


def show_server_instructions():
    console.print("""
[bold red]⚠️ MCP SERVER NOT RUNNING![/bold red]

You must run the MCP server manually in another terminal.

Open a NEW terminal and paste this command:

[bold yellow]uv run uvicorn mcp_server.server:mcp_app --host 127.0.0.1 --port 8000 --reload[/bold yellow]

After starting the server, return to this terminal and use the CLI.
""")


# Load API key before importing run_agent
ensure_api_key()
from agent_sdk.sdk_client import run_agent


async def start_chat():
    banner()

    # Check if server is running
    if not check_mcp_server():
        show_server_instructions()

    console.print("[cyan]Type your commands. Type 'exit' to quit.[/cyan]\n")

    while True:
        user_input = Prompt.ask("[bold green]You[/bold green]")

        if user_input.lower() in ["exit", "quit"]:
            console.print("[red]Exiting...[/red]")
            break

        with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
            try:
                response = await run_agent(user_input) or "No response received."
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue

        console.print(Markdown(response))
        console.print()


def main():
    asyncio.run(start_chat())


if __name__ == "__main__":
    main()
