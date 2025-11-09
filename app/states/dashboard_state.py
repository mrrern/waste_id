import asyncio
import datetime
import logging
from typing import TypedDict
import reflex as rx
import pandas as pd
from app.states.data import (
    paises_latam,
    performance_chart_data,
    quick_actions_data,
    resource_allocation_data,
)


class StatCardData(TypedDict):
    title: str
    value: str
    sub_detail: str
    icon: str
    color: str
    chart_data: list[dict[str, int]]
    description: str


class RecyclingData(TypedDict):
    region: str
    rate: float
    color: str


class ResourceAllocationData(TypedDict):
    name: str
    value: int
    color: str


class QuickActionData(TypedDict):
    name: str
    icon: str


class PerformanceChartData(TypedDict):
    time: str
    CPU: int
    Memory: int
    Network: int


def _create_stat_cards(
    data_source: pd.Series | pd.DataFrame, is_total: bool
) -> list[StatCardData]:
    if is_total:
        generated_kt = data_source["raee_generado_2019_kt"].sum()
        collected_rate = data_source["tasa_recoleccion_%"].mean()
        unmanaged_kt = data_source["raee_no_gestionado_kt"].sum()
        unmanaged_percent = unmanaged_kt / generated_kt * 100 if generated_kt > 0 else 0
        value_potential = data_source["valor_materiales_millones_usd"].sum()
        value_lost = data_source["valor_perdido_millones_usd"].sum()
        pob_total = data_source["poblacion_2019_millones"].sum()
        avg_kg_hab = (
            generated_kt * 1000 / (pob_total * 1000000) * 1000 if pob_total > 0 else 0
        )
    else:
        generated_kt = data_source["raee_generado_2019_kt"]
        collected_rate = data_source["tasa_recoleccion_%"]
        unmanaged_kt = data_source["raee_no_gestionado_kt"]
        unmanaged_percent = unmanaged_kt / generated_kt * 100 if generated_kt > 0 else 0
        value_potential = data_source["valor_materiales_millones_usd"]
        value_lost = data_source["valor_perdido_millones_usd"]
        avg_kg_hab = data_source["raee_kg_hab"]
    return [
        {
            "title": "E-Waste Generado (2019)",
            "value": f"{generated_kt:,.0f} kt",
            "sub_detail": f"Promedio: {avg_kg_hab:.1f} kg/hab",
            "icon": "trash-2",
            "color": "cyan",
            "chart_data": [
                {"v": v}
                for v in range(
                    int(generated_kt / 100), int(generated_kt), int(generated_kt / 10)
                )
            ]
            if generated_kt > 10
            else [{"v": 1}] * 10,
            "description": "Total de residuos de aparatos eléctricos y electrónicos (RAEE) generados en kilotoneladas. Incluye desde electrodomésticos hasta celulares.",
        },
        {
            "title": "Tasa de Recolección Formal",
            "value": f"{collected_rate:.1f}%",
            "sub_detail": f"{unmanaged_kt:,.0f} kt no gestionado ({unmanaged_percent:.1f}%)",
            "icon": "recycle",
            "color": "purple",
            "chart_data": [{"v": int(collected_rate)}] * 10,
            "description": "Porcentaje del E-Waste que se recolecta a través de canales oficiales y seguros, garantizando un tratamiento ambientalmente adecuado.",
        },
        {
            "title": "Valor Económico Potencial",
            "value": f"${value_potential:,.0f} M",
            "sub_detail": f"${value_lost:,.0f} M perdidos anualmente",
            "icon": "dollar-sign",
            "color": "teal",
            "chart_data": [
                {"v": v}
                for v in range(
                    int(value_potential / 10),
                    int(value_potential),
                    int(value_potential / 10),
                )
            ]
            if value_potential > 10
            else [{"v": 1}] * 10,
            "description": "Valor estimado (en millones de USD) de los materiales crudos secundarios (oro, cobre, etc.) que podrían recuperarse del E-Waste.",
        },
        {
            "title": "Trazabilidad de Cadena de Valor",
            "value": "15 empleos/ton",
            "sub_detail": "$1200 valor agregado",
            "icon": "git-branch",
            "color": "amber",
            "chart_data": [
                {"v": 10},
                {"v": 20},
                {"v": 15},
                {"v": 40},
                {"v": 35},
                {"v": 60},
                {"v": 55},
                {"v": 80},
                {"v": 75},
                {"v": 100},
            ],
            "description": "Impacto socioeconómico de la gestión formal. Cada tonelada reciclada puede generar empleos y añadir valor a la economía local.",
        },
    ]


class DashboardState(rx.State):
    """Holds the state for the dashboard."""

    _df_raee: pd.DataFrame = pd.DataFrame()
    current_time: str = ""
    current_date: str = ""
    uptime: str = "14d 06:42:18"
    time_zone: str = "UTC-08:00"
    active_nav: str = "Visión 360°"
    active_performance_tab: str = "Resumen Estadístico"
    mobile_sidebar_open: bool = False
    stat_cards: list[StatCardData] = []
    paises: list[str] = paises_latam
    selected_pais: str = "Toda Latinoamérica"
    recycling_data: list[RecyclingData] = [
        {"region": "Latam & Caribbean", "rate": 2.75, "color": "red"},
        {"region": "Europe", "rate": 42.77, "color": "blue"},
        {"region": "North America", "rate": 52.13, "color": "green"},
        {"region": "World", "rate": 22.3, "color": "yellow"},
    ]
    resource_allocation: list[ResourceAllocationData] = resource_allocation_data
    quick_actions: list[QuickActionData] = quick_actions_data
    performance_chart_data: list[PerformanceChartData] = performance_chart_data
    system_load: int = 35

    @rx.event(background=True)
    async def load_data(self):
        async with self:
            if self._df_raee.empty:
                try:
                    self._df_raee = pd.read_csv(
                        "assets/dataset_raee_latam_completo.csv"
                    )
                    self._df_raee["pais"] = self._df_raee["pais"].replace(
                        {
                            "Bolivia (Plurinational State of)": "Bolivia",
                            "Venezuela (Bolivarian Republic of)": "Venezuela",
                        }
                    )
                except FileNotFoundError as e:
                    logging.exception(f"Error: {e}")
            self.current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.current_date = datetime.datetime.now().strftime("%b %d, %Y")
        yield DashboardState.set_selected_pais(self.selected_pais)
        yield DashboardState.update_time

    @rx.event(background=True)
    async def update_time(self):
        if not self._df_raee.empty:
            while True:
                async with self:
                    self.current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    self.current_date = datetime.datetime.now().strftime("%b %d, %Y")
                await asyncio.sleep(1)

    @rx.event
    def set_active_nav(self, nav_item: str):
        self.active_nav = nav_item
        if self.mobile_sidebar_open:
            self.mobile_sidebar_open = False

    @rx.event
    def set_active_performance_tab(self, tab_name: str):
        self.active_performance_tab = tab_name

    @rx.event
    def set_selected_pais(self, pais: str):
        self.selected_pais = pais
        if self._df_raee.empty:
            try:
                self._df_raee = pd.read_csv("assets/dataset_raee_latam_completo.csv")
                self._df_raee["pais"] = self._df_raee["pais"].replace(
                    {
                        "Bolivia (Plurinational State of)": "Bolivia",
                        "Venezuela (Bolivarian Republic of)": "Venezuela",
                    }
                )
            except FileNotFoundError as e:
                logging.exception(f"Error: {e}")
                return
        if pais == "Toda Latinoamérica":
            self.stat_cards = _create_stat_cards(self._df_raee, is_total=True)
        else:
            country_data = self._df_raee[self._df_raee["pais"] == pais]
            if not country_data.empty:
                self.stat_cards = _create_stat_cards(
                    country_data.iloc[0], is_total=False
                )
            else:
                self.stat_cards = _create_stat_cards(self._df_raee, is_total=True)

    @rx.event
    def toggle_mobile_sidebar(self):
        self.mobile_sidebar_open = not self.mobile_sidebar_open

    @rx.var
    def nav_items(self) -> list[dict[str, str]]:
        return [
            {"name": "Visión 360°", "icon": "layout-dashboard"},
            {"name": "Mapeo de flujos", "icon": "map"},
            {"name": "Trazabilidad", "icon": "package"},
            {"name": "Calculadora de Impacto", "icon": "calculator"},
            {"name": "Datos Abiertos", "icon": "database"},
        ]