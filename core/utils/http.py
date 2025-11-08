"""Funções HTTP simples (usa requests)."""
from typing import Tuple
import requests


def fetch_text(url: str, timeout: float = 10.0) -> Tuple[int, str]:
    #Faz GET na URL e retorna (status_code, text).
    # Não lança exceções de requests; propaga se necessário.
    
    resp = requests.get(url, timeout=timeout)
    return resp.status_code, resp.text
