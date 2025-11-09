import reflex as rx
import pandas as pd
from app.states.dashboard_state import DashboardState, StatCardData
from app.components.main_content import stat_card
from app.components.charts import TOOLTIP_PROPS, RECHART_WRAPPER_CLASS

# Load data
dataset_raee = pd.read_csv("assets/dataset_raee_latam_completo.csv")

class CalculadoraState(DashboardState):
    """State for the Calculadora de Impacto page."""
    
    _dataset_df: pd.DataFrame = dataset_raee
    selected_personas: int = 1
    promedio_raee_kg_hab: float = dataset_raee["raee_kg_hab"].mean()
    
    @rx.var
    def raee_calculado_kg(self) -> float:
        """Calculate RAEE in kg for selected number of people."""
        return self.selected_personas * self.promedio_raee_kg_hab
    
    @rx.var
    def raee_calculado_ton(self) -> float:
        """Calculate RAEE in tons for selected number of people."""
        return self.raee_calculado_kg / 1000.0
    
    @rx.var
    def valor_potencial_usd(self) -> float:
        """Calculate potential value in USD."""
        # Average value per ton from dataset
        # valor_materiales_millones_usd is in millions USD
        # raee_generado_2019_kt is in kilotons (kt = 1000 tons)
        total_valor_usd = self._dataset_df["valor_materiales_millones_usd"].sum() * 1_000_000
        total_raee_tons = self._dataset_df["raee_generado_2019_kt"].sum() * 1000  # Convert kt to tons
        avg_valor_por_ton = total_valor_usd / total_raee_tons if total_raee_tons > 0 else 0
        return self.raee_calculado_ton * avg_valor_por_ton
    
    @rx.var
    def empleos_potenciales(self) -> float:
        """Calculate potential jobs created."""
        # Average jobs per ton from dataset
        # empleos_formales is total jobs
        # raee_generado_2019_kt is in kilotons (kt = 1000 tons)
        total_empleos = self._dataset_df["empleos_formales"].sum()
        total_raee_tons = self._dataset_df["raee_generado_2019_kt"].sum() * 1000  # Convert kt to tons
        empleos_por_ton = total_empleos / total_raee_tons if total_raee_tons > 0 else 0
        return self.raee_calculado_ton * empleos_por_ton
    
    @rx.var
    def calculadora_stat_cards(self) -> list[StatCardData]:
        """Generate stat cards for calculator results."""
        return [
            {
                "title": "RAEE Generado",
                "value": f"{self.raee_calculado_kg:.2f} kg",
                "sub_detail": f"{self.raee_calculado_ton:.4f} toneladas",
                "icon": "trash-2",
                "color": "cyan",
                "chart_data": [{"v": self.raee_calculado_kg}] * 10,
            },
            {
                "title": "Valor Potencial",
                "value": f"${self.valor_potencial_usd:,.2f}",
                "sub_detail": "En materiales recuperables",
                "icon": "dollar-sign",
                "color": "purple",
                "chart_data": [{"v": self.valor_potencial_usd / 1000}] * 10,
            },
            {
                "title": "Empleos Potenciales",
                "value": f"{self.empleos_potenciales:.1f}",
                "sub_detail": "Empleos formales generados",
                "icon": "users",
                "color": "teal",
                "chart_data": [{"v": self.empleos_potenciales}] * 10,
            },
            {
                "title": "Personas",
                "value": f"{self.selected_personas:,}",
                "sub_detail": f"Promedio: {self.promedio_raee_kg_hab:.2f} kg/persona/año",
                "icon": "users",
                "color": "amber",
                "chart_data": [{"v": self.selected_personas}] * 10,
            },
        ]
    
    @rx.event
    def set_personas(self, num_personas: int):
        """Set the number of people for calculation."""
        self.selected_personas = num_personas

def calculadora_cards() -> rx.Component:
    """Display the stat cards for the calculadora page."""
    return rx.el.div(
        rx.foreach(CalculadoraState.calculadora_stat_cards, stat_card),
        class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4",
    )

def calculadora_buttons() -> rx.Component:
    """Display buttons to select number of people."""
    return rx.el.div(
        rx.el.button(
            rx.icon(tag="user", class_name="mr-2 size-4"),
            "1 Persona",
            on_click=CalculadoraState.set_personas(1),
            class_name=rx.cond(
                CalculadoraState.selected_personas == 1,
                "px-4 py-3 text-sm font-medium text-white bg-cyan-600 rounded-lg focus:outline-none hover:bg-cyan-700 transition-colors duration-150 flex items-center",
                "px-4 py-3 text-sm font-medium text-gray-300 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none hover:bg-gray-700 hover:border-gray-600 transition-colors duration-150 flex items-center",
            ),
        ),
        rx.el.button(
            rx.icon(tag="users", class_name="mr-2 size-4"),
            "100 Personas",
            on_click=CalculadoraState.set_personas(100),
            class_name=rx.cond(
                CalculadoraState.selected_personas == 100,
                "px-4 py-3 text-sm font-medium text-white bg-cyan-600 rounded-lg focus:outline-none hover:bg-cyan-700 transition-colors duration-150 flex items-center",
                "px-4 py-3 text-sm font-medium text-gray-300 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none hover:bg-gray-700 hover:border-gray-600 transition-colors duration-150 flex items-center",
            ),
        ),
        rx.el.button(
            rx.icon(tag="users", class_name="mr-2 size-4"),
            "500 Personas",
            on_click=CalculadoraState.set_personas(500),
            class_name=rx.cond(
                CalculadoraState.selected_personas == 500,
                "px-4 py-3 text-sm font-medium text-white bg-cyan-600 rounded-lg focus:outline-none hover:bg-cyan-700 transition-colors duration-150 flex items-center",
                "px-4 py-3 text-sm font-medium text-gray-300 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none hover:bg-gray-700 hover:border-gray-600 transition-colors duration-150 flex items-center",
            ),
        ),
        rx.el.button(
            rx.icon(tag="users", class_name="mr-2 size-4"),
            "1000 Personas",
            on_click=CalculadoraState.set_personas(1000),
            class_name=rx.cond(
                CalculadoraState.selected_personas == 1000,
                "px-4 py-3 text-sm font-medium text-white bg-cyan-600 rounded-lg focus:outline-none hover:bg-cyan-700 transition-colors duration-150 flex items-center",
                "px-4 py-3 text-sm font-medium text-gray-300 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none hover:bg-gray-700 hover:border-gray-600 transition-colors duration-150 flex items-center",
            ),
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
    )

def calculadora_info_section() -> rx.Component:
    """Display information section about the calculator."""
    return rx.el.div(
        rx.el.h3(
            "Información sobre el Cálculo",
            class_name="text-lg font-semibold text-gray-200 mb-4",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span("Promedio de RAEE por persona: ", class_name="text-gray-400"),
                rx.el.span(
                    f"{CalculadoraState.promedio_raee_kg_hab:.2f} kg/persona/año",
                    class_name="text-cyan-400 font-semibold",
                ),
                class_name="mb-2",
            ),
            rx.el.p(
                "Este cálculo se basa en el promedio de generación de residuos de aparatos eléctricos y electrónicos (RAEE) por habitante en Latinoamérica, según datos del Global E-waste Monitor 2020.",
                class_name="text-sm text-gray-400 mb-2",
            ),
            rx.el.p(
                "Los valores de potencial económico y empleos se calculan basándose en las tasas promedio de recuperación de materiales y generación de empleo formal en la región.",
                class_name="text-sm text-gray-400",
            ),
            class_name="space-y-2",
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mt-6",
    )

def calculadora_dashboard() -> rx.Component:
    """The main dashboard component for the calculadora page."""
    return rx.el.main(
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    rx.icon(tag="calculator", class_name="mr-2 text-cyan-400 hidden sm:inline-block"),
                    "Calculadora de Impacto",
                    class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            calculadora_buttons(),
            calculadora_cards(),
            rx.el.p(
                "Selecciona el número de personas para calcular el impacto de generación de RAEE.",
                class_name="text-xs text-gray-500 mt-4 text-center",
            ),
            class_name="mb-6",
        ),
        rx.el.section(calculadora_info_section()),
        class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
    )

