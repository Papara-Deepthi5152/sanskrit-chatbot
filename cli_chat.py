"""
Vagdevi - Sanskrit Conversational AI Chatbot (CLI Interface)
Run directly in your terminal:
    python cli_chat.py
"""

import sys
import os

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

from engine.dialogue_manager import DialogueManager
from engine.transliteration import to_devanagari, to_iast

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
    USE_RICH = True
    console = Console()
except ImportError:
    USE_RICH = False

BANNER = """
========================================================================
            वाग्देवी • VĀGDEVĪ - SANSKRIT AI CHATBOT
      संस्कृत-संभाषणम् • व्याकरणम् • सुभाषितानि • प्रश्नोत्तरी
========================================================================
Type in Devanagari (नमस्ते), English phonetics (katham asti), or English!
Commands:
  /quiz       - Start an interactive Sanskrit quiz question
  /shloka     - Recite a daily Subhashita / Gita verse with meaning
  /trans <t>  - Transliterate English phonetic text to Devanagari
  /help       - Show supported topics & grammar guides
  /exit       - Quit the application
========================================================================
"""

def print_banner():
    if USE_RICH:
        console.print(Panel.fit(
            "[bold gold1]वाग्देवी • VĀGDEVĪ - SANSKRIT AI COMPANION[/bold gold1]\n"
            "[italic cyan]संस्कृत-संभाषणम् • व्याकरणम् • सुभाषितानि • प्रश्नोत्तरी[/italic cyan]\n\n"
            "[yellow]Type in Devanagari (नमस्ते), English phonetics (katham asti), or English![/yellow]\n"
            "[green]Commands: /quiz, /shloka, /trans <text>, /help, /exit[/green]",
            border_style="dark_orange"
        ))
    else:
        print(BANNER)

def display_response(resp):
    sa_text = resp["text_sa"]
    iast_text = resp["text_iast"]
    en_text = resp["text_en"]
    follow_ups = resp.get("follow_ups", [])

    if USE_RICH:
        content = Text()
        content.append(f"\n🕉️ संस्कृतम्: {sa_text}\n", style="bold orange1")
        content.append(f"🔤 IAST:     {iast_text}\n\n", style="italic cyan")

        console.print(Panel(content, title="[bold]वाग्देवी (Vagdevi)[/bold]", border_style="gold1"))

        if en_text:
            console.print(Markdown(en_text))

        if follow_ups:
            sugg_str = " | ".join([f"[dim cyan]{s}[/dim cyan]" for s in follow_ups[:4]])
            console.print(f"[dim]💡 Suggestions: {sugg_str}[/dim]\n")
    else:
        print("\n" + "-"*50)
        print(f"🕉️ संस्कृतम्: {sa_text}")
        print(f"🔤 IAST:     {iast_text}")
        print(f"📖 English:   {en_text}")
        if follow_ups:
            print(f"💡 Suggestions: {' | '.join(follow_ups[:4])}")
        print("-" * 50 + "\n")

def main():
    print_banner()
    dm = DialogueManager()

    # Welcome greeting
    welcome = dm.process_message("namaste")
    display_response(welcome)

    while True:
        try:
            prompt_str = "भवान् (You) > "
            user_input = input(prompt_str).strip()
            if not user_input:
                continue

            if user_input.lower() in ["/exit", "exit", "quit", ":q"]:
                farewell = dm.process_message("punah milamah")
                display_response(farewell)
                break

            if user_input.lower() == "/quiz":
                resp = dm.process_message("start quiz")
                display_response(resp)
                continue

            if user_input.lower() == "/shloka":
                resp = dm.process_message("tell me a shloka")
                display_response(resp)
                continue

            if user_input.lower().startswith("/trans "):
                phrase = user_input[7:].strip()
                deva = to_devanagari(phrase)
                iast = to_iast(deva)
                if USE_RICH:
                    console.print(f"[bold gold1]Devanagari:[/bold gold1] {deva}  |  [cyan]IAST:[/cyan] {iast}\n")
                else:
                    print(f"Devanagari: {deva}  |  IAST: {iast}\n")
                continue

            if user_input.lower() in ["/help", "help"]:
                resp = dm.process_message("what can you do")
                display_response(resp)
                continue

            resp = dm.process_message(user_input)
            display_response(resp)

        except (KeyboardInterrupt, EOFError):
            print("\nपुनर्मिलामः! (See you again!)")
            break

if __name__ == "__main__":
    main()
