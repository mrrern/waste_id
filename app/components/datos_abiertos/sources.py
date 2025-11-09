import reflex as rx
from app.states.dashboard_state import DashboardState

class DatosAbiertosState(DashboardState):
    """State for the Datos Abiertos page."""
    
    @rx.var
    def sources_list(self) -> list[dict]:
        """List of data sources."""
        return [
            {
                "name": "Our World in Data - Electronic Waste",
                "description": "Datos y visualizaciones sobre tasas de reciclaje de residuos electrónicos y gestión de desechos a nivel global.",
                "url": "https://ourworldindata.org/search?q=Electronic+waste+recycling+rate&resultType=all",
                "icon": "database",
                "color": "cyan",
            },
            {
                "name": "Global E-waste Monitor",
                "description": "Monitoreo global de residuos electrónicos (e-waste) con estadísticas, datos y análisis sobre generación, recolección y reciclaje.",
                "url": "https://globalewaste.org",
                "icon": "globe",
                "color": "purple",
            },
            {
                "name": "Global E-waste Monitor - Map",
                "description": "Mapa interactivo que muestra la distribución geográfica de residuos electrónicos a nivel mundial.",
                "url": "https://globalewaste.org/map/",
                "icon": "map",
                "color": "teal",
            },
            {
                "name": "Our World in Data - Waste Management",
                "description": "Recursos completos sobre gestión de residuos, incluyendo datos sobre reciclaje, tratamiento y políticas de gestión de desechos.",
                "url": "https://ourworldindata.org/waste-management",
                "icon": "recycle",
                "color": "green",
            },
            {
                "name": "Overpass Turbo",
                "description": "Herramienta de consulta para datos geoespaciales de OpenStreetMap, útil para mapeo y análisis de ubicaciones relacionadas con gestión de residuos.",
                "url": "https://overpass-turbo.eu/",
                "icon": "map-pin",
                "color": "amber",
            },
        ]

def source_card(source_data: dict) -> rx.Component:
    """Card component for displaying a data source."""
    icon_name = str(source_data["icon"])
    color_name = str(source_data["color"])
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    str(source_data["name"]),
                    class_name="text-lg font-bold text-cyan-300 mb-2",
                ),
                rx.el.p(
                    str(source_data["description"]),
                    class_name="text-sm text-gray-400 mb-4",
                ),
                rx.el.a(
                    rx.el.div(
                        rx.icon(tag="external-link", class_name="mr-2 size-4"),
                        "Visitar sitio",
                        class_name="flex items-center text-cyan-400 hover:text-cyan-300 transition-colors duration-150",
                    ),
                    href=str(source_data["url"]),
                    target="_blank",
                    rel="noopener noreferrer",
                    class_name="inline-flex items-center",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.icon(tag=icon_name, class_name="size-8"),
                class_name=f"p-3 rounded-lg bg-gradient-to-br from-{color_name}-500 to-{color_name}-600 text-white shadow-lg",
            ),
            class_name="flex justify-between items-start gap-4",
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm hover:bg-gray-800/70 transition-colors duration-200 flex flex-col",
    )

def datos_abiertos_dashboard() -> rx.Component:
    """The main dashboard component for the datos abiertos page."""
    return rx.el.main(
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    rx.icon(tag="database", class_name="mr-2 text-cyan-400 hidden sm:inline-block"),
                    "Directorio de Fuentes de Datos",
                    class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    DatosAbiertosState.sources_list,
                    source_card,
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            rx.el.p(
                "Estas fuentes proporcionan datos abiertos y recursos sobre gestión de residuos electrónicos y desechos a nivel global.",
                class_name="text-xs text-gray-500 mt-4 text-center",
            ),
            class_name="mb-6",
        ),
        rx.el.section(
            rx.el.div(
                rx.el.h3(
                    "Sobre los Datos",
                    class_name="text-lg font-semibold text-gray-200 mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Los datos utilizados en esta plataforma provienen de fuentes confiables y verificadas, incluyendo:",
                        class_name="text-sm text-gray-400 mb-3",
                    ),
                    rx.el.ul(
                        rx.el.li(
                            rx.el.span("• ", class_name="text-cyan-400"),
                            "The Global E-waste Monitor 2020 (UNU/UNITAR)",
                            class_name="text-sm text-gray-400 mb-2",
                        ),
                        rx.el.li(
                            rx.el.span("• ", class_name="text-cyan-400"),
                            "Our World in Data - Datos abiertos sobre gestión de residuos",
                            class_name="text-sm text-gray-400 mb-2",
                        ),
                        rx.el.li(
                            rx.el.span("• ", class_name="text-cyan-400"),
                            "Global E-waste Monitor - Estadísticas y análisis globales",
                            class_name="text-sm text-gray-400 mb-2",
                        ),
                        rx.el.li(
                            rx.el.span("• ", class_name="text-cyan-400"),
                            "OpenStreetMap / Overpass Turbo - Datos geoespaciales",
                            class_name="text-sm text-gray-400",
                        ),
                        class_name="list-none space-y-1",
                    ),
                    class_name="space-y-2",
                ),
                class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mt-6",
            ),
        ),
        class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
    )

