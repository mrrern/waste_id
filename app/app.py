import reflex as rx
from app.components.main_content import main_content
from app.components.template import template
from app.states.dashboard_state import DashboardState
from app.pages import mapeo_de_flujos, trazabilidad, calculadora_de_impacto, datos_abiertos

@rx.page(route="/", title="Waste ID")
def index() -> rx.Component:
    return template(page_content=main_content())


app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="green"),
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.29.0/feather.min.js"
    ],
)
app.add_page(index, route="/", title="WastedID")
app.add_page(mapeo_de_flujos, route="/mapeo-de-flujos")
app.add_page(trazabilidad, route="/trazabilidad")
app.add_page(calculadora_de_impacto, route="/calculadora-de-impacto")
app.add_page(datos_abiertos, route="/datos-abiertos")