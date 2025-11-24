import asyncio
import sys
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

from agent_sdk.sdk_client import run_agent
from cli.config import save_key, load_key

console = Console()

def banner():
    console.print(Panel.fit(
        "[bold cyan]🚀 MY OWN CLI — AI Terminal Assistant[/bold cyan]",
        border_style="cyan",
        padding=(1, 4)
    ))


async def start_chat():
    """Main loop that handles user chat."""
    banner()

    while True:
        user_input = Prompt.ask("[bold green]You[/bold green]")

        if user_input.lower() in ["exit", "quit"]:
            console.print("[red]Exiting...[/red]")
            break

        with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
            try:
                response = await run_agent(user_input) or "No Response Received"
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue

        console.print(Markdown(response))
        console.print()


def main():
    """Entry point for CLI command."""
    args = sys.argv

    # ------------------------------------------
    # CONFIG COMMANDS
    # ------------------------------------------
    if len(args) >= 2 and args[1] == "config":
        if len(args) == 4 and args[2] == "set-key":
            key = args[3]
            save_key(key)
            console.print("[green]API key saved successfully![/green]")
            return

        console.print("[red]Invalid config command.[/red]")
        console.print("Usage: my-own-cli config set-key <API_KEY>")
        return

    # ------------------------------------------
    # NORMAL MODE (chat)
    # ------------------------------------------
    api_key = load_key()
    if not api_key:
        console.print("[red]API key not set![/red]")
        console.print("Run: [cyan]my-own-cli config set-key <your_key>[/cyan]")
        return

    # Inject key for your agent
    os.environ["API_KEY"] = api_key

    asyncio.run(start_chat())


if __name__ == "__main__":
    main()

