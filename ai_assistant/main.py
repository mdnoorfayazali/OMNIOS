import sys
import argparse
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich import box

from ai_assistant.config import settings
from ai_assistant.commands.interpreter import interpret_command
from ai_assistant.executor.actions import execute_action
from ai_assistant.utils.logger import setup_logger

# Optional Voice Imports
try:
    from ai_assistant.voice.listener import listen
    from ai_assistant.voice.speaker import speak
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

# Optional Vision/Web Imports
try:
    import pyautogui
    from PIL import Image
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

logger = setup_logger(__name__)
console = Console()

def print_banner():
    # Clear screen for dramatic effect
    console.clear()
    
    banner = """
    ██████╗ ███╗   ███╗███╗   ██╗██╗ ██████╗ ███████╗
   ██╔═══██╗████╗ ████║████╗  ██║██║██╔═══██╗██╔════╝
   ██║   ██║██╔████╔██║██╔██╗ ██║██║██║   ██║███████╗
   ██║   ██║██║╚██╔╝██║██║╚██╗██║██║██║   ██║╚════██║
   ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║╚██████╔╝███████║
    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚══════╝
    """
    
    # Create the main layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=10),
        Layout(name="status", size=6)
    )

    # Header
    layout["header"].update(Panel(Text(banner, justify="center", style="bold cyan"), 
                        title=f"{settings.APP_NAME} v{settings.VERSION}", 
                        subtitle="Advanced AI Agent", 
                        border_style="blue"))

    # System Status Table
    table = Table(box=box.SIMPLE, show_header=False, expand=True)
    table.add_column("Module", style="cyan")
    table.add_column("Status", justify="right")
    
    table.add_row("🧠 Core Intelligence", "[bold green]ONLINE[/bold green]")
    table.add_row("🎙️ Voice System", "[bold green]ONLINE[/bold green]" if VOICE_AVAILABLE else "[bold red]OFFLINE[/bold red]")
    table.add_row("👁️ Omni-Vision", "[bold green]ONLINE[/bold green]" if VISION_AVAILABLE else "[bold red]OFFLINE[/bold red]")
    table.add_row("🌐 Web Agent", "[bold green]ONLINE[/bold green]" if WEB_AVAILABLE else "[bold red]OFFLINE[/bold red]")
    table.add_row("📁 Workspace", f"[dim]{settings.BASE_WORKSPACE_DIR}[/dim]")

    layout["status"].update(Panel(table, title="System Status", border_style="green"))

    console.print(layout)
    console.print("\n")

def main():
    parser = argparse.ArgumentParser(description=settings.APP_NAME)
    parser.add_argument("--voice", action="store_true", help="Enable voice interaction mode")
    args = parser.parse_args()

    voice_mode = args.voice and VOICE_AVAILABLE
    
    print_banner()

    if voice_mode:
        speak(f"Welcome back. Systems are online.")

    # 2. REPL Loop
    while True:
        try:
            # Input
            if voice_mode:
                with console.status("[bold green]Listening...[/bold green]", spinner="dots"):
                    user_input = listen()
                if not user_input:
                    continue
                console.print(f"[bold cyan]YOU >[/bold cyan] {user_input}")
                if user_input.lower() in ["quit", "stop", "exit"]:
                    speak("Goodbye.")
                    break
            else:
                user_input = console.input("\n[bold cyan]YOU >[/bold cyan] ").strip()
                if not user_input: continue
            
            if not voice_mode and user_input.lower() in ["quit", "exit"]:
                console.print("[bold red]System Shutdown Initiated...[/bold red]")
                break

            # A. Interpret
            with console.status("[bold blue]Analyzing Intent...[/bold blue]", spinner="bouncingBar"):
                # Simulate a little thinking time for effect if too fast
                # time.sleep(0.5) 
                commands = interpret_command(user_input)
            
            # Helper to handle list or single
            if isinstance(commands, dict):
                commands = [commands]

            for i, command in enumerate(commands):
                action = command.get("action")
                params = command.get("params", {})
                confidence = command.get("confidence", 0.0)

                # B. Safety Checks
                if action == "respond":
                    message = params.get('message', '')
                    console.print(Panel(message, title="AI Response", border_style="green", expand=False))
                    if voice_mode:
                        speak(message)
                    continue

                # Create a status table
                table = Table(title=f"Proposed Action ({i+1}/{len(commands)})", box=box.ROUNDED)
                table.add_column("Property", style="cyan", no_wrap=True)
                table.add_column("Value", style="magenta")
                table.add_row("Action", action)
                table.add_row("Confidence", f"{confidence:.2f}")
                for k, v in params.items():
                    table.add_row(f"Param: {k}", str(v))
                
                console.print(table)

                # C. Explicit User Permission
                if voice_mode:
                    speak(f"I am about to {action}. Should I proceed?")
                    with console.status("[bold yellow]Waiting for confirmation...[/bold yellow]", spinner="clock"):
                        confirmation = listen()
                    
                    if confirmation and "yes" in confirmation.lower():
                        choice = 'y'
                    else:
                        choice = 'n'
                        console.print("[bold red](Voice confirmation failed or rejected.)[/bold red]")
                else:
                    choice = console.input("    [bold yellow]EXECUTE?[/bold yellow] (y/n) > ").lower()

                if choice != 'y':
                    console.print("[bold red]Action cancelled.[/bold red]")
                    if voice_mode: speak("Action cancelled.")
                    continue

                # D. Execute
                with console.status("[bold green]Executing...[/bold green]", spinner="dots12"):
                    result = execute_action(command)
                
                console.print(f"[bold green]AI >[/bold green] {result}\n")
                if voice_mode:
                    speak("Done.")

        except KeyboardInterrupt:
            console.print("\n[bold red]Force Exit.[/bold red]")
            break
        except Exception as e:
            logger.error(f"System Error: {e}")
            message = "I encountered a system error."
            console.print(f"[bold red]{message}[/bold red]")
            if voice_mode: speak(message)

if __name__ == "__main__":
    main()
