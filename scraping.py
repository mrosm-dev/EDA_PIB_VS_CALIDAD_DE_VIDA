import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup

BASE_URL = "https://www.idealista.com"
START_URL = f"{BASE_URL}/sala-de-prensa/informes-precio-vivienda/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}

CCAA_SLUGS = {
    "Andalucía": "andalucia",
    "Madrid": "madrid",
    # empieza con 2–3 para probar
}

MONTHS = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

def polite_sleep():
    time.sleep(random.uniform(3, 6))

def get_session():
    s = requests.Session()
    s.headers.update(HEADERS)

    # Paso 1: entrar como haría un usuario
    r = s.get(START_URL, timeout=30)
    r.raise_for_status()
    polite_sleep()

    return s

def fetch_ccaa(session, tipo, ccaa, slug):
    url = f"{BASE_URL}/sala-de-prensa/informes-precio-vivienda/{tipo}/{slug}/"
    print(f"→ {tipo.upper()} | {ccaa}")

    headers = {
        "Referer": START_URL
    }

    r = session.get(url, headers=headers, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find("table")
    if table is None:
        raise ValueError("No se encontró la tabla")

    df = pd.read_html(str(table))[0]
    df.columns = ["mes", "precio_m2", "v1", "v2", "v3"]
    df = df[["mes", "precio_m2"]]

    df["precio_m2"] = (
        df["precio_m2"]
        .str.replace("€/m2", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["mes"] = df["mes"].str.lower()
    df["anio"] = df["mes"].str.extract(r"(\d{4})").astype(int)
    df["mes_num"] = df["mes"].apply(
        lambda x: next(v for k, v in MONTHS.items() if k in x)
    )

    df["ccaa"] = ccaa
    df["tipo"] = tipo

    polite_sleep()
    return df[["anio", "mes_num", "ccaa", "tipo", "precio_m2"]]

def main():
    session = get_session()
    all_data = []

    for tipo in ["venta", "alquiler"]:
        for ccaa, slug in CCAA_SLUGS.items():
            try:
                df = fetch_ccaa(session, tipo, ccaa, slug)
                all_data.append(df)
            except Exception as e:
                print(f"✖ {ccaa} ({tipo}): {e}")

    if all_data:
        final = pd.concat(all_data)
        final.to_csv("idealista_test.csv", index=False)
        print("✔ Datos guardados")

if __name__ == "__main__":
    main()
