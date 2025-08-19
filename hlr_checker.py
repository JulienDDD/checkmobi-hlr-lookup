import requests, json, os, datetime
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)
console = Console()

# === CONFIGURATION ===
with open("config.json") as f:
    config = json.load(f)

API_KEY = config["api_key"]
HEADERS = {
    "Authorization": API_KEY
}

DATE_DIR = datetime.datetime.now().strftime("results/%Y-%m-%d")
os.makedirs(DATE_DIR, exist_ok=True)

stats = {
    "total": 0,
    "actifs": 0,
    "inactifs": 0,
    "erreurs": 0,
    "timeouts": 0
}

results_table = Table(title="Résultats en direct", expand=True)
results_table.add_column("Numéro", style="bold")
results_table.add_column("Statut", style="bold")
results_table.add_column("Opérateur", style="bold")

# === UI DYNAMIQUE ===
def render_ui():
    table = Table.grid()
    table.add_row(Text("GOTHAM HLR LOOKUP", style="bold cyan"))
    table.add_row("")
    table.add_row(f"📤 Total checkés : {stats['total']}")
    table.add_row(f"✅ Actifs       : [green]{stats['actifs']}[/green]")
    table.add_row(f"❌ Inactifs     : [yellow]{stats['inactifs']}[/yellow]")
    table.add_row(f"⚠️  Erreurs      : [red]{stats['erreurs']}[/red]")
    table.add_row(f"⏱️  Timeouts     : [magenta]{stats['timeouts']}[/magenta]")
    return Panel(Group(table, results_table), title="CheckMobi HLR Tool")

# === CHECK HLR ===
def check_number(number, live):
    url = f"https://api.checkmobi.com/v1/lookup/hlr/{number.replace('+', '')}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        stats["total"] += 1

        if r.status_code != 200:
            stats["erreurs"] += 1
            results_table.add_row(number, "[red]ERREUR[/red]", "-")
            live.update(render_ui())
            return

        reachable = data.get("reachable")
        status = data.get("processing_status")
        operateur = data.get("current_network", {}).get("network_name", "Unknown").replace(" ", "_")

        if reachable == "connected" and status == "completed":
            stats["actifs"] += 1
            filename = os.path.join(DATE_DIR, f"{operateur}.txt")
            with open(filename, "a") as f:
                f.write(number + "\n")
            results_table.add_row(number, "[green]ACTIF[/green]", operateur)
        else:
            stats["inactifs"] += 1
            results_table.add_row(number, "[yellow]INACTIF[/yellow]", operateur)

    except Exception as e:
        stats["timeouts"] += 1
        results_table.add_row(number, "[magenta]TIMEOUT[/magenta]", "-")

    live.update(render_ui())

def main():
    with open("numbers.txt") as f:
        numbers = [line.strip() for line in f if line.strip()]

    with Live(render_ui(), refresh_per_second=5, console=console, screen=False) as live:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for number in numbers:
                executor.submit(check_number, number, live)

    console.print(Panel(f"[bold green]✔️ Terminé. Résultats dans : {DATE_DIR}[/bold green]"))

if __name__ == "__main__":
    main()
