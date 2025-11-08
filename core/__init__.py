"""Pacote `core` — atalhos de importação para funções e utilitários principais.

Importação sugerida:
  from core import extrair_html, extrair_link_invite

Também é possível acessar o subpacote `core.utils` para funções mais específicas:
  from core.utils import extractor, http, io
"""

from .group import extrair_html
from .linkwpp import extrair_link_invite
from .url import gerar_urls, verificar_urls

# expor o subpacote utils
from . import utils

__all__ = [
    "extrair_html",
    "extrair_link_invite",
    "gerar_urls",
    "verificar_urls",
    "utils",
]
