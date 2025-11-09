import reflex as rx
import pandas as pd
from app.states.dashboard_state import DashboardState, StatCardData
from app.components.main_content import stat_card
from app.components.charts import TOOLTIP_PROPS, RECHART_WRAPPER_CLASS

# Load data
trazabilidad_data = pd.read_csv("assets/trazabilidad_cadena_valor.csv")
proyecciones_data = pd.read_csv("assets/proyecciones_raee_2020_2030.csv")

class TrazabilidadState(DashboardState):
    """State for the Trazabilidad page."""
    
    _trazabilidad_df: pd.DataFrame = trazabilidad_data
    _proyecciones_df: pd.DataFrame = proyecciones_data
    active_trazabilidad_tab: str = "Eficiencia por Etapa"

    @rx.var
    def eficiencia_card_data(self) -> StatCardData:
        avg_eficiencia = self._trazabilidad_df["eficiencia_promedio_%"].mean()
        return {
            "title": "Eficiencia Promedio",
            "value": f"{avg_eficiencia:.2f}%",
            "sub_detail": "En toda la cadena",
            "icon": "bar-chart-2",
            "color": "cyan",
            "chart_data": [{"v": val} for val in self._trazabilidad_df["eficiencia_promedio_%"].tolist()]
        }

    @rx.var
    def valor_agregado_card_data(self) -> StatCardData:
        total_valor = self._trazabilidad_df["valor_agregado_usd_ton"].sum()
        return {
            "title": "Valor Agregado Total",
            "value": f"${total_valor:,.0f}/ton",
            "sub_detail": "Suma de todas las etapas",
            "icon": "dollar-sign",
            "color": "purple",
            "chart_data": [{"v": val} for val in self._trazabilidad_df["valor_agregado_usd_ton"].tolist()]
        }

    @rx.var
    def empleos_card_data(self) -> StatCardData:
        total_empleos = self._trazabilidad_df["empleos_por_etapa"].sum()
        return {
            "title": "Empleos Generados",
            "value": f"{total_empleos}",
            "sub_detail": "Por cada 1000 toneladas",
            "icon": "users",
            "color": "teal",
            "chart_data": [{"v": val} for val in self._trazabilidad_df["empleos_por_etapa"].tolist()]
        }

    @rx.var
    def proyecciones_card_data(self) -> StatCardData:
        brecha_2030 = self._proyecciones_df[self._proyecciones_df["año"] == 2030]["brecha_proyectada_kt"].iloc[0]
        return {
            "title": "Brecha Proyectada (2030)",
            "value": f"{brecha_2030:,.0f} kt",
            "sub_detail": "RAEE no recolectado",
            "icon": "trending-up",
            "color": "amber",
            "chart_data": [{"v": val} for val in self._proyecciones_df["brecha_proyectada_kt"].tolist()]
        }

    @rx.var
    def trazabilidad_stat_cards(self) -> list[StatCardData]:
        return [
            self.eficiencia_card_data,
            self.valor_agregado_card_data,
            self.empleos_card_data,
            self.proyecciones_card_data,
        ]

    @rx.var
    def eficiencia_por_etapa_data(self) -> list[dict]:
        """Data for efficiency by stage chart."""
        return [
            {
                "etapa": row["etapa"],
                "eficiencia": row["eficiencia_promedio_%"]
            }
            for _, row in self._trazabilidad_df.iterrows()
        ]

    @rx.var
    def valor_agregado_por_etapa_data(self) -> list[dict]:
        """Data for value added by stage chart."""
        return [
            {
                "etapa": row["etapa"],
                "valor": row["valor_agregado_usd_ton"]
            }
            for _, row in self._trazabilidad_df.iterrows()
        ]

    @rx.var
    def empleos_por_etapa_data(self) -> list[dict]:
        """Data for jobs by stage chart."""
        return [
            {
                "etapa": row["etapa"],
                "empleos": row["empleos_por_etapa"]
            }
            for _, row in self._trazabilidad_df.iterrows()
        ]

    @rx.var
    def proyecciones_temporal_data(self) -> list[dict]:
        """Data for temporal projections chart."""
        # Aggregate by year across all countries
        proyecciones_agrupadas = self._proyecciones_df.groupby("año").agg({
            "raee_proyectado_kt": "sum",
            "recoleccion_proyectada_kt": "sum",
            "brecha_proyectada_kt": "sum"
        }).reset_index()
        
        return [
            {
                "año": int(row["año"]),
                "raee_proyectado": row["raee_proyectado_kt"],
                "recoleccion_proyectada": row["recoleccion_proyectada_kt"],
                "brecha_proyectada": row["brecha_proyectada_kt"]
            }
            for _, row in proyecciones_agrupadas.iterrows()
        ]

    @rx.event
    def set_active_trazabilidad_tab(self, tab_name: str):
        self.active_trazabilidad_tab = tab_name

def trazabilidad_cards() -> rx.Component:
    """Display the stat cards for the trazabilidad page."""
    return rx.el.div(
        rx.foreach(TrazabilidadState.trazabilidad_stat_cards, stat_card),
        class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4",
    )

def eficiencia_chart() -> rx.Component:
    """Chart showing efficiency by stage."""
    return rx.el.div(
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#374151", vertical=False
            ),
            rx.recharts.tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="etapa",
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
                angle=-45,
                text_anchor="end",
                height=80,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
            ),
            rx.recharts.bar(
                data_key="eficiencia",
                fill="#22d3ee",
                radius=[4, 4, 0, 0],
            ),
            data=TrazabilidadState.eficiencia_por_etapa_data,
            width="100%",
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 80},
        ),
        rx.el.p(
            "Eficiencia promedio (%) por etapa de la cadena de valor",
            class_name="text-xs text-gray-400 mt-4 text-center",
        ),
        class_name=RECHART_WRAPPER_CLASS,
    )


def valor_agregado_chart() -> rx.Component:
    """Chart showing value added by stage."""
    return rx.el.div(
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#374151", vertical=False
            ),
            rx.recharts.tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="etapa",
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
                angle=-45,
                text_anchor="end",
                height=80,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
            ),
            rx.recharts.bar(
                data_key="valor",
                fill="#a855f7",
                radius=[4, 4, 0, 0],
            ),
            data=TrazabilidadState.valor_agregado_por_etapa_data,
            width="100%",
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 80},
        ),
        rx.el.p(
            "Valor agregado (USD/ton) por etapa de la cadena de valor",
            class_name="text-xs text-gray-400 mt-4 text-center",
        ),
        class_name=RECHART_WRAPPER_CLASS,
    )


def empleos_chart() -> rx.Component:
    """Chart showing jobs by stage."""
    return rx.el.div(
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#374151", vertical=False
            ),
            rx.recharts.tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="etapa",
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
                angle=-45,
                text_anchor="end",
                height=80,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
            ),
            rx.recharts.bar(
                data_key="empleos",
                fill="#2dd4bf",
                radius=[4, 4, 0, 0],
            ),
            data=TrazabilidadState.empleos_por_etapa_data,
            width="100%",
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 80},
        ),
        rx.el.p(
            "Empleos generados por cada 1000 toneladas por etapa",
            class_name="text-xs text-gray-400 mt-4 text-center",
        ),
        class_name=RECHART_WRAPPER_CLASS,
    )


def proyecciones_chart() -> rx.Component:
    """Chart showing temporal projections."""
    return rx.el.div(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#374151", vertical=False
            ),
            rx.recharts.tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="año",
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
            ),
            rx.recharts.y_axis(
                y_axis_id="left",
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                orientation="left",
                style={"fontSize": "12px"},
            ),
            rx.recharts.y_axis(
                y_axis_id="right",
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                orientation="right",
                style={"fontSize": "12px"},
            ),
            rx.recharts.line(
                data_key="raee_proyectado",
                y_axis_id="left",
                type_="monotone",
                stroke="#22d3ee",
                stroke_width=2,
                dot=False,
                name="RAEE Proyectado (kt)",
            ),
            rx.recharts.line(
                data_key="recoleccion_proyectada",
                y_axis_id="left",
                type_="monotone",
                stroke="#2dd4bf",
                stroke_width=2,
                dot=False,
                name="Recolección Proyectada (kt)",
            ),
            rx.recharts.line(
                data_key="brecha_proyectada",
                y_axis_id="right",
                type_="monotone",
                stroke="#f59e0b",
                stroke_width=2,
                dot=False,
                name="Brecha Proyectada (kt)",
            ),
            data=TrazabilidadState.proyecciones_temporal_data,
            width="100%",
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 5},
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="w-3 h-3 rounded-full bg-cyan-400"),
                rx.el.span("RAEE Proyectado", class_name="text-xs text-gray-300 ml-2"),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.div(class_name="w-3 h-3 rounded-full bg-teal-500"),
                rx.el.span("Recolección Proyectada", class_name="text-xs text-gray-300 ml-2"),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.div(class_name="w-3 h-3 rounded-full bg-amber-500"),
                rx.el.span("Brecha Proyectada", class_name="text-xs text-gray-300 ml-2"),
                class_name="flex items-center",
            ),
            class_name="flex flex-col sm:flex-row justify-center items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-6 pt-4",
        ),
        rx.el.p(
            "Proyecciones de RAEE, recolección y brecha proyectada (2020-2030)",
            class_name="text-xs text-gray-400 mt-4 text-center",
        ),
        class_name=RECHART_WRAPPER_CLASS,
    )


def trazabilidad_performance_section() -> rx.Component:
    """Display the performance section for the trazabilidad page with tabs."""
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                "Eficiencia por Etapa",
                on_click=lambda: TrazabilidadState.set_active_trazabilidad_tab(
                    "Eficiencia por Etapa"
                ),
                class_name=rx.cond(
                    TrazabilidadState.active_trazabilidad_tab == "Eficiencia por Etapa",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            rx.el.button(
                "Valor Agregado",
                on_click=lambda: TrazabilidadState.set_active_trazabilidad_tab(
                    "Valor Agregado"
                ),
                class_name=rx.cond(
                    TrazabilidadState.active_trazabilidad_tab == "Valor Agregado",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            rx.el.button(
                "Empleos por Etapa",
                on_click=lambda: TrazabilidadState.set_active_trazabilidad_tab(
                    "Empleos por Etapa"
                ),
                class_name=rx.cond(
                    TrazabilidadState.active_trazabilidad_tab == "Empleos por Etapa",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            rx.el.button(
                "Proyecciones Temporales",
                on_click=lambda: TrazabilidadState.set_active_trazabilidad_tab(
                    "Proyecciones Temporales"
                ),
                class_name=rx.cond(
                    TrazabilidadState.active_trazabilidad_tab == "Proyecciones Temporales",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            class_name="flex space-x-1 border-b border-gray-700/50 mb-4 pb-2 overflow-x-auto",
        ),
        rx.el.div(
            rx.cond(
                TrazabilidadState.active_trazabilidad_tab == "Eficiencia por Etapa",
                eficiencia_chart(),
                rx.cond(
                    TrazabilidadState.active_trazabilidad_tab == "Valor Agregado",
                    valor_agregado_chart(),
                    rx.cond(
                        TrazabilidadState.active_trazabilidad_tab == "Empleos por Etapa",
                        empleos_chart(),
                        rx.cond(
                            TrazabilidadState.active_trazabilidad_tab == "Proyecciones Temporales",
                            proyecciones_chart(),
                            rx.el.div(
                                rx.el.p(
                                    "Datos para "
                                    + TrazabilidadState.active_trazabilidad_tab
                                    + " próximamente.",
                                    class_name="text-gray-400 p-10 text-center",
                                )
                            ),
                        ),
                    ),
                ),
            )
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mt-6",
    )

def trazabilidad_dashboard() -> rx.Component:
    """The main dashboard component for the trazabilidad page."""
    return rx.el.main(
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    rx.icon(tag="package", class_name="mr-2 text-cyan-400 hidden sm:inline-block"),
                    "Análisis de Trazabilidad",
                    class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            trazabilidad_cards(),
            rx.el.p(
                "Datos basados en la cadena de valor y proyecciones para LATAM.",
                class_name="text-xs text-gray-500 mt-4 text-center",
            ),
            class_name="mb-6",
        ),
        rx.el.section(trazabilidad_performance_section()),
        class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
    )