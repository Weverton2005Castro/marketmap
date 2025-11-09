# gerar o db

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from pathlib import Path
from core.group import extrair_html
from core.linkwpp import extrair_link_invite

try:
    from colorama import Fore, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        BLUE = ""

def load_config():
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_db(namedb="quick_extracao.json", out="data"):
    """Gera o banco de dados extraindo links de grupos do WhatsApp e seus invites de múltiplas fontes."""
    try:
        fontes = [
            "https://gruposdewhats.com.br/",
            "https://whatsgrouplink.com/",
            "https://gruposwhats.app/"
        ]

        resultados_totais = []
        print(f"{Fore.YELLOW}Iniciando extração de múltiplas fontes...\n")

        for fonte in fontes:
            print(f"{Fore.CYAN}Extraindo da fonte: {fonte}")
            try:
                resultados = extrair_html(fonte, namedb=namedb, out_path=out)
                resultados_totais.extend(resultados)
                print(f"{Fore.GREEN}→ {len(resultados)} links encontrados em {fonte}")
            except Exception as e:
                print(f"{Fore.RED}Falha ao extrair de {fonte}: {e}")

        # Remover duplicados
        unique_results = {r["href"]: r for r in resultados_totais if "href" in r}.values()
        all_results = list(unique_results)

        out_dir = Path(out)
        out_dir.mkdir(parents=True, exist_ok=True)
        combined_json_path = out_dir / namedb

        with combined_json_path.open("w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"{Fore.GREEN}\nTotal combinado: {len(all_results)} grupos salvos em {combined_json_path}")

        # Extrair links de convite (invites)
        invites_db = []
        total_urls = len(all_results)
        for i, group_data in enumerate(all_results, 1):
            group_url = group_data.get("href")
            if not group_url:
                continue

            print(f"{Fore.BLUE}[{i}/{total_urls}] Extraindo invites de: {group_url}")
            try:
                invites = extrair_link_invite(group_url, out, "invites.json")
                invites_db.extend(invites)
            except Exception as e:
                print(f"{Fore.RED}Erro ao extrair de {group_url}: {e}")
                continue

        # Salvar invites únicos
        config = load_config()
        invites_file = config.get("invites_file", "data/invites.json")
        unique_invites = list(set(invites_db))
        invites_json_path = Path(invites_file)
        invites_json_path.parent.mkdir(parents=True, exist_ok=True)

        with invites_json_path.open("w", encoding="utf-8") as f:
            json.dump(unique_invites, f, ensure_ascii=False, indent=2)

        print(f"{Fore.GREEN}\nInvites extraídos: {len(unique_invites)} itens salvos em {invites_json_path}")

        return all_results, unique_invites

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Processo interrompido pelo usuário. Salvando progresso...")
        if 'invites_db' in locals():
            config = load_config()
            invites_file = config.get("invites_file", "data/invites.json")
            unique_invites = list(set(invites_db))
            invites_json_path = Path(invites_file)
            invites_json_path.parent.mkdir(parents=True, exist_ok=True)
            with invites_json_path.open("w", encoding="utf-8") as f:
                json.dump(unique_invites, f, ensure_ascii=False, indent=2)
            print(f"{Fore.GREEN}Progresso salvo: {len(unique_invites)} invites em {invites_json_path}")
        print(f"{Fore.RED}Saindo...")
        return [], []

if __name__ == "__main__":
    generate_db()
