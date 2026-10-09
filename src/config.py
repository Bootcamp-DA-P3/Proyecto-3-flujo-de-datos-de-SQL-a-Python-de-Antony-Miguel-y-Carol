import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=False)

# La raíz del proyecto es la carpeta que contiene a src/.
RAIZ = Path(__file__).resolve().parent.parent

load_dotenv(RAIZ / ".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_NAME = os.getenv("DB_NAME", "olist")


_faltan = [
    nombre
    for nombre, valor in (
        ("DB_USER", DB_USER),
        ("DB_PASSWORD", DB_PASSWORD),
        ("DB_HOST", DB_HOST),
        ("DB_PORT", DB_PORT),
        ("DB_NAME", DB_NAME),
    )
    if not valor
]

if _faltan:
    raise RuntimeError(
        f"Faltan variables en el .env: {', '.join(_faltan)}.\n"
        "Copia .env_example a .env y rellena tus credenciales."
    )

# Carpetas de trabajo
CARPETA_QUERIES = RAIZ / "sql"
CARPETA_OUTPUT = RAIZ / os.getenv("DATA_FOLDER", "data")

# Excel. El ETL no disena el dashboard: solo crea el libro si no existe,
# apunta a las fuentes y lo abre.
EXCEL_FILE = RAIZ / os.getenv("EXCEL_FILE", "dashboard/Olist_Dashboard.xlsx")
AUTO_OPEN_EXCEL = os.getenv("AUTO_OPEN_EXCEL", "true").lower() == "true"