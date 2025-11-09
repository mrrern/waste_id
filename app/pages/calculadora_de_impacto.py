
import reflex as rx
from app.components.template import template

@rx.page(route="/calculadora-de-impacto")
def calculadora_de_impacto():
    content = rx.container(
        rx.heading("Calculadora de Impacto", size="5"),
        rx.text("Contenido de la página Calculadora de Impacto."),
    )
    return template(page_content=content)
