import reflex as rx
from app.components.charts import performance_line_chart, stat_card_chart
from app.states.dashboard_state import DashboardState, StatCardData


def stat_card(card_data: StatCardData) -> rx.Component:
    color = card_data["color"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    card_data["title"], class_name="text-sm font-medium text-gray-400"
                ),
                rx.el.p(
                    card_data["value"],
                    class_name="text-2xl font-bold text-gray-100 mt-1",
                ),
                rx.el.p(
                    card_data["sub_detail"], class_name="text-xs text-gray-500 mt-1"
                ),
            ),
            rx.el.div(
                rx.icon(tag=card_data["icon"], class_name="size-6"),
                class_name=f"p-3 rounded-lg bg-gradient-to-br from-{color}-500 to-{color}-600 text-white shadow-lg",
            ),
            class_name="flex justify-between items-start",
        ),
        
        stat_card_chart(card_data["chart_data"], card_data["color"]),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm hover:bg-gray-800/70 transition-colors duration-200 flex flex-col",
    )


def material_card(metal_data: dict) -> rx.Component:
    """Card to display detail for a single critical material."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                metal_data["metal"],
                class_name="text-lg font-bold text-cyan-300",
            ),
            rx.el.span(
                "Criticidad: ",
                rx.el.span(
                    metal_data["criticidad"],
                ),
                class_name=rx.cond(
                    metal_data["criticidad"] == "Alta",
                    "text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-300 border border-red-500/30",
                    rx.cond(
                        metal_data["criticidad"] == "Media",
                        "text-xs px-2 py-1 rounded-full bg-yellow-500/20 text-yellow-300 border border-yellow-500/30",
                        rx.cond(
                            metal_data["criticidad"] == "Baja",
                            "text-xs px-2 py-1 rounded-full bg-green-500/20 text-green-300 border border-green-500/30",
                            "text-xs px-2 py-1 rounded-full bg-gray-700 text-gray-300",
                        ),
                    ),
                ),
            ),
            class_name="flex justify-between items-center mb-3",
        ),
        rx.el.div(
            rx.el.p(
                "Recuperado:",
                class_name="text-sm font-medium text-gray-400",
            ),
            rx.el.p(
                f"{metal_data['recovered_t']:.4f} ton",
                class_name="text-xl font-bold text-white",
            ),
            class_name="mb-2",
        ),
        rx.el.div(
            rx.el.p(
                "Valor:",
                class_name="text-sm font-medium text-gray-400",
            ),
            rx.el.p(
                f"${metal_data['recovered_value_usd']:,.2f} USD",
                class_name="text-xl font-bold text-teal-300",
            ),
            class_name="mb-3",
        ),
        rx.el.div(
            rx.el.p(
                f"Concentración: {metal_data['concentracion_ppm']} ppm",
                class_name="text-xs text-gray-500",
            ),
            rx.el.p(
                f"Precio: ${metal_data['valor_usd_kg']}/kg",
                class_name="text-xs text-gray-500",
            ),
            class_name="flex justify-between text-xs text-gray-500",
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm hover:bg-gray-800/70 transition-colors duration-200 flex flex-col",
    )


def material_details_section() -> rx.Component:
    """Section to display the grid of critical material details."""
    return rx.el.div(
        rx.el.h3(
            "Detalle de Materiales Críticos Recuperados",
            class_name="text-lg font-semibold text-gray-200 mb-4",
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.critical_metals_detail,
                material_card,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4",
        ),
        rx.el.p(
            f"Estimaciones para {DashboardState.selected_pais} basadas en la tasa de recolección y reciclaje actual.",
            class_name="text-xs text-gray-500 mt-4 text-center",
        ),
        class_name="mt-6",
    )



def performance_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                "Resumen Estadístico",
                on_click=lambda: DashboardState.set_active_performance_tab(
                    "Resumen Estadístico"
                ),
                class_name=rx.cond(
                    DashboardState.active_performance_tab == "Resumen Estadístico",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            rx.el.button(
                "Detalle por Material",
                on_click=lambda: DashboardState.set_active_performance_tab(
                    "Detalle por Material"
                ),
                class_name=rx.cond(
                    DashboardState.active_performance_tab == "Detalle por Material",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            rx.el.button(
                "Impacto Económico",
                on_click=lambda: DashboardState.set_active_performance_tab(
                    "Impacto Económico"
                ),
                class_name=rx.cond(
                    DashboardState.active_performance_tab == "Impacto Económico",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            class_name="flex space-x-1 border-b border-gray-700/50 mb-4 pb-2 overflow-x-auto",
        ),
        rx.el.div(
            rx.cond(
                DashboardState.active_performance_tab == "Resumen Estadístico",
                rx.el.div(
                    performance_line_chart(DashboardState.performance_chart_data),
                    # DEBUG: show raw series values to help diagnose rendering issues
                    
                    rx.el.div(
                        rx.el.p(
                            f"{DashboardState.selected_pais}", class_name="text-xs text-gray-400"
                        ),
                       
                        class_name="absolute top-5 right-5 bg-gray-800/70 p-2 rounded-md text-center border border-gray-700/50 backdrop-blur-sm",
                    ),
                    class_name="relative",
                ),
                rx.cond(
                    DashboardState.active_performance_tab == "Detalle por Material",
                    material_details_section(),
                    rx.el.div(
                        rx.el.p(
                            "Datos para "
                            + DashboardState.active_performance_tab
                            + " próximamente.",
                            class_name="text-gray-400 p-10 text-center",
                        )
                    ),
                ),
            )
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mt-6",
    )


def main_content() -> rx.Component:
    return rx.el.main(
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    rx.icon(
                        tag="bar-chart-2",
                        class_name="mr-2 text-cyan-400 hidden sm:inline-block",
                    ),
                    "Panorama E-WASTE en LATAM",
                    class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            DashboardState.paises,
                            lambda pais: rx.el.option(pais, value=pais),
                        ),
                        value=DashboardState.selected_pais,
                        on_change=DashboardState.set_selected_pais,
                        class_name="bg-gray-800 border border-gray-700 text-gray-300 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-full p-2.5",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(DashboardState.stat_cards, stat_card),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4",
            ),
            rx.el.p(
                "Fuente: The Global E-waste Monitor 2020 y cálculos propios basados en datos de UNU/UNITAR.",
                class_name="text-xs text-gray-500 mt-4 text-center",
            ),
            class_name="mb-6",
        ),
        rx.el.section(performance_section()),
        class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
    )