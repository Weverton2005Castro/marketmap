"""Funções de I/O simples: salvar JSON e HTML."""
import json
from pathlib import Path
from typing import Iterable

# Salva uma lista de itens em JSON no diretório e arquivo especificados.
def save_json(items: Iterable, out_dir: str | Path, filename: str):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    file_path = out_dir / filename
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(list(items), f, ensure_ascii=False, indent=2)
    return file_path

# Salva texto HTML em um arquivo no diretório especificado.
def save_html(text: str, out_dir: str | Path, filename: str = "gruposdewhats.html"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    file_path = out_dir / filename
    file_path.write_text(text, encoding="utf-8")
    return file_path
