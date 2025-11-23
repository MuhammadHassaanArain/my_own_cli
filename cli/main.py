import asyncio
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from agent_sdk.sdk_client import run_agent

console = Console()

def banner():
    console.print(Panel.fit(
        "[bold cyan]🚀 MY OWN CLI — AI Terminal Assistant[/bold cyan]",
        border_style="cyan",
        padding=(1, 4)
    ))

async def main():
    banner()

    while True:
        user_input = Prompt.ask("[bold green]You[/bold green]")

        if user_input.lower() in ["exit", "quit"]:
            console.print("[red]Exiting...[/red]")
            break

        with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
            response = await run_agent(user_input) or "No response received."



        console.print(Markdown(response))
        console.print()

if __name__ == "__main__":
    asyncio.run(main())
