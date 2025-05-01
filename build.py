import json
import os

with open("meta.json", "r", encoding="utf-8") as f:
    info = json.load(f)

cmd = [
    "nuitka",
    "--standalone",
    "--onefile",
    "--follow-imports",  # Garante que dependências sejam incluídas
    f'--output-filename={info["output_filename"]}',
    f'--windows-product-name="{info["product_name"]}"',
    f'--windows-file-description="{info["file_description"]}"',
    f'--windows-file-version={info["file_version"]}',
    f'--windows-product-version={info["product_version"]}',
    "main.py",
]

# Junte os argumentos e rode o comando
os.system(" ".join(cmd))
