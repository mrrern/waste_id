from pathlib import Path
import pandas as pd


resource_allocation_data = [
    {"name": "Recuperación de Materiales", "value": 42, "color": "cyan"},
    {"name": "Componentes Reutilizados", "value": 68, "color": "pink"},
    {"name": "Baterías Recicladas", "value": 35, "color": "blue"},
]
quick_actions_data = [
    {"name": "Security Scan", "icon": "shield-check"},
    {"name": "Sync Data", "icon": "refresh-cw"},
    {"name": "Backup", "icon": "database"},
    {"name": "Console", "icon": "terminal"},
]

# Build a performance series where x is years (2019..2025) and y are meaningful aggregated metrics
# Assumptions:
# - We have a base year in the CSV (2019: 'raee_generado_2019_kt') and a projection for 2025
#   ('proyeccion_raee_2025_kt'). We'll create a linear interpolation for the intermediate years.
# - For the second metric we'll use the collection rate (mean 'tasa_recoleccion_%' in 2019
#   and the mean target 'meta_recoleccion_2025_%' for 2025).
# - For the third metric we'll use the aggregated value of recoverable materials
#   ('valor_materiales_millones_usd' for 2019 and 'oportunidad_economica_millones_usd' for 2025 when present).


def _build_performance_series() -> list[dict]:
    assets_dir = Path(__file__).resolve().parents[2] / "assets"
    csv_path = assets_dir / "dataset_raee_latam_completo.csv"
    years = list(range(2019, 2026))  # 2019..2025 inclusive

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        # fallback: return a small static series (keeps previous shape but with years)
        return [
            {"time": str(y), "CPU": v * 10, "Memory": 30 + i, "Network": 15 + i * 2}
            for i, (y, v) in enumerate(zip(years, range(28, 28 + len(years))))
        ]

    # aggregate 2019 values
    total_2019 = int(df.get("raee_generado_2019_kt", pd.Series([0] * len(df))).sum())
    collection_2019 = float(df.get("tasa_recoleccion_%", pd.Series([0.0] * len(df))).mean())
    value_2019 = float(df.get("valor_materiales_millones_usd", pd.Series([0.0] * len(df))).sum())

    # aggregate 2025 projections/targets
    total_2025 = int(df.get("proyeccion_raee_2025_kt", pd.Series([total_2019] * len(df))).sum())
    collection_2025 = float(df.get("meta_recoleccion_2025_%", pd.Series([collection_2019] * len(df))).mean())
    # opportunitiy_economic column exists in dataset as 'oportunidad_economica_millones_usd'
    value_2025 = float(df.get("oportunidad_economica_millones_usd", pd.Series([value_2019] * len(df))).sum())

    series = []
    steps = len(years) - 1
    for i, y in enumerate(years):
        t = i / steps if steps > 0 else 0
        raee = int(round(total_2019 + (total_2025 - total_2019) * t))
        collection = round(collection_2019 + (collection_2025 - collection_2019) * t, 2)
        value = int(round(value_2019 + (value_2025 - value_2019) * t))
        # Use semantic field names for chart consumption:
        # time -> year, raee_kt -> RAEE generated (kt), recoleccion_pct -> collection rate (%), valor_musd -> material value (M USD)
        series.append(
            {
                "time": str(y),
                "raee_kt": raee,
                "recoleccion_pct": int(round(collection)),
                "valor_musd": value,
            }
        )

    return series


paises_latam = [
    "Toda Latinoamérica",
    "Argentina",
    "Bolivia",
    "Chile",
    "Costa Rica",
    "Cuba",
    "Ecuador",
    "El Salvador",
    "Guatemala",
    "Honduras",
    "Nicaragua",
    "Panamá",
    "Paraguay",
    "Perú",
    "República Dominicana",
    "Uruguay",
    "Venezuela",
]


performance_chart_data = _build_performance_series()


def _build_critical_metals_data() -> list[dict]:
    """Compute recovered critical metals from recycled material.

    Method:
    - Estimate total recycled mass (kg) = sum(raee_recolectado_kt * tasa_reciclaje_% / 100) * 1e6
    - For each metal in `metales_criticos_raee.csv`, compute recovered kg = recycled_kg * (concentracion_ppm / 1e6)
    - Compute value = recovered_kg * valor_usd_kg
    """
    assets_dir = Path(__file__).resolve().parents[2] / "assets"
    ds_path = assets_dir / "dataset_raee_latam_completo.csv"
    metals_path = assets_dir / "metales_criticos_raee.csv"

    try:
        df = pd.read_csv(ds_path)
    except Exception:
        return []

    # Safely get columns, defaulting to zeros when missing
    recolectado = df.get("raee_recolectado_kt", pd.Series([0.0] * len(df))).fillna(0.0).astype(float)
    tasa_reciclaje = df.get("tasa_reciclaje_%", pd.Series([0.0] * len(df))).fillna(0.0).astype(float)

    # total recycled kiloton -> convert to kg (1 kt = 1e6 kg)
    total_recycled_kt = (recolectado * (tasa_reciclaje / 100.0)).sum()
    total_recycled_kg = total_recycled_kt * 1_000_000.0

    metals_list: list[dict] = []
    try:
        mdf = pd.read_csv(metals_path)
    except Exception:
        mdf = pd.DataFrame()

    if mdf.empty:
        return []

    for _, row in mdf.iterrows():
        metal = str(row.get("metal", "unknown"))
        conc_ppm = float(row.get("concentracion_ppm", 0.0))
        valor_usd_kg = float(row.get("valor_usd_kg", 0.0))
        criticidad = str(row.get("criticidad", "Desconocida"))

        recovered_kg = total_recycled_kg * (conc_ppm / 1_000_000.0)
        recovered_value = recovered_kg * valor_usd_kg

        metals_list.append(
            {
                "metal": metal,
                "concentracion_ppm": conc_ppm,
                "recovered_kg": round(recovered_kg, 3),
                "recovered_t": round(recovered_kg / 1000.0, 6),
                "recovered_value_usd": round(recovered_value, 2),
                "valor_usd_kg": valor_usd_kg,
                "criticidad": criticidad,
            }
        )

    # sort by recovered value desc so top-value metals appear first in "Detalles por material"
    metals_list.sort(key=lambda x: x["recovered_value_usd"], reverse=True)
    return metals_list


critical_metals_data = _build_critical_metals_data()

