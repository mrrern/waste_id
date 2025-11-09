import reflex as rx
from app.components.template import template
from app.components.calculadora.calculator import calculadora_dashboard

@rx.page(route="/calculadora-de-impacto")
def calculadora_de_impacto() -> rx.Component:
    """Calculadora de Impacto page."""
    return template(page_content=calculadora_dashboard())
