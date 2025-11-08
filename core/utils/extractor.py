import re
from urllib.parse import urlparse

# Extrai links relevantes de um HTML fornecido.
def extract_links(html: str):
    pattern = re.compile(
        r'<a\s+[^>]*href="(?P<href>[^"]+)"[^>]*title="(?P<title>[^"]+)"[^>]*>(?:\s*<h2>(?P<h2>.*?)</h2>)?',
        re.IGNORECASE | re.DOTALL,
    )
    matches = pattern.finditer(html)

    resultados = []
    vistos_endpoints = set()
    # Lista de palavras e caminhos irrelevantes
    blacklist = ("blog", "minha conta", "contato", "sobre", "termos", "privacidade")
    blacklist_paths = ("/minha-conta", "/category/")

    for m in matches:
        href = (m.group('href') or '').strip()
        title = (m.group('title') or '').strip()
        h2 = (m.group('h2') or '').strip()
        text = h2 if h2 else title

        if not href:
            continue
        low = href.lower()
        if low.startswith('#') or low.startswith('mailto:') or low.startswith('tel:') or low.startswith('javascript:'):
            continue

        parsed = urlparse(href)
        endpoint_key = (parsed.netloc + parsed.path) if parsed.netloc else parsed.path
        endpoint_key = endpoint_key.lower()

        if any(bp in endpoint_key for bp in blacklist_paths):
            continue
        if any(b in low for b in blacklist):
            continue

        if endpoint_key in vistos_endpoints:
            continue
        vistos_endpoints.add(endpoint_key)

        resultados.append({"href": href, "title": title, "text": text})

    return resultados
