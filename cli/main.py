# import asyncio
# from rich.console import Console
# from rich.prompt import Prompt
# from rich.panel import Panel
# from rich.markdown import Markdown
# from agent_sdk.sdk_client import run_agent

# console = Console()

# def banner():
#     console.print(Panel.fit(
#         "[bold cyan]🚀 MY OWN CLI — AI Terminal Assistant[/bold cyan]",
#         border_style="cyan",
#         padding=(1, 4)
#     ))

# async def start_chat():
#     """Main chat loop."""
#     banner()
#     while True:
#         user_input = Prompt.ask("[bold green]You[/bold green]")
#         if user_input.lower() in ["exit", "quit"]:
#             console.print("[red]Exiting...[/red]")
#             break

#         with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
#             try:
#                 response = await run_agent(user_input) or "No Response Received"
#             except Exception as e:
#                 console.print(f"[red]Error: {e}[/red]")
#                 continue

#         console.print(Markdown(response))
#         console.print()

# def main():
#     """Entry point for CLI."""
#     asyncio.run(start_chat())


# if __name__ == "__main__":
#     main()
# =================================================================================
# import asyncio
# import os
# from pathlib import Path
# from rich.console import Console
# from rich.prompt import Prompt
# from rich.panel import Panel
# from rich.markdown import Markdown

# console = Console()
# ENV_FILE = Path(__file__).parent.parent / ".env"  # Path to .env file in project root

# def banner():
#     console.print(Panel.fit(
#         "[bold cyan]🚀 MY OWN CLI — AI Terminal Assistant[/bold cyan]",
#         border_style="cyan",
#         padding=(1, 4)
#     ))

# def ensure_api_key():
#     """Prompt for API key if not set and save it to .env."""
#     api_key = os.environ.get("API_KEY")
    
#     if not api_key:
#         api_key = Prompt.ask("[bold yellow]Enter your API key[/bold yellow]").strip()
#         if not api_key:
#             console.print("[red]API key is required! Exiting.[/red]")
#             exit(1)
        
#         # Save to .env file
#         lines = []
#         if ENV_FILE.exists():
#             with open(ENV_FILE, "r") as f:
#                 lines = f.readlines()

#         # Update or add API_KEY line
#         new_lines = []
#         found = False
#         for line in lines:
#             if line.startswith("API_KEY="):
#                 new_lines.append(f"API_KEY={api_key}\n")
#                 found = True
#             else:
#                 new_lines.append(line)
#         if not found:
#             new_lines.append(f"API_KEY={api_key}\n")

#         with open(ENV_FILE, "w") as f:
#             f.writelines(new_lines)

#         console.print("[green]API key saved successfully![/green]")

#     # Set environment variable
#     os.environ["API_KEY"] = api_key

# # Import run_agent only after API_KEY is set
# ensure_api_key()
# from agent_sdk.sdk_client import run_agent

# async def start_chat():
#     """Main chat loop."""
#     banner()
#     while True:
#         user_input = Prompt.ask("[bold green]You[/bold green]")
#         if user_input.lower() in ["exit", "quit"]:
#             console.print("[red]Exiting...[/red]")
#             break

#         with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
#             try:
#                 response = await run_agent(user_input) or "No Response Received"
#             except Exception as e:
#                 console.print(f"[red]Error: {e}[/red]")
#                 continue

#         console.print(Markdown(response))
#         console.print()

# def main():
#     """Entry point for CLI."""
#     asyncio.run(start_chat())

# if __name__ == "__main__":
#     main()
# =====================================================================
import asyncio
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
ENV_FILE = Path(__file__).parent.parent / ".env"  # Path to .env file in project root

def banner():
    console.print(Panel.fit(
        "[bold cyan]🚀 MY OWN CLI — AI Terminal Assistant[/bold cyan]",
        border_style="cyan",
        padding=(1, 4)
    ))

def ensure_api_key():
    """Load API key from .env or prompt the user if missing."""
    api_key = None

    # Check if .env exists and read API_KEY
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            for line in f:
                if line.startswith("API_KEY="):
                    api_key = line.strip().split("=", 1)[1]
                    break

    # If no key found, prompt user
    if not api_key:
        api_key = Prompt.ask("[bold yellow]Enter your API key[/bold yellow]").strip()
        if not api_key:
            console.print("[red]API key is required! Exiting.[/red]")
            exit(1)

        # Save to .env
        with open(ENV_FILE, "a") as f:
            f.write(f"API_KEY={api_key}\n")

        console.print("[green]API key saved successfully![/green]")

    # Set environment variable for SDK
    os.environ["API_KEY"] = api_key

# Load API key before importing run_agent
ensure_api_key()
from agent_sdk.sdk_client import run_agent

async def start_chat():
    """Main chat loop."""
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
    """Entry point for CLI."""
    asyncio.run(start_chat())

if __name__ == "__main__":
    main()
