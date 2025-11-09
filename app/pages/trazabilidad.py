
import reflex as rx
from app.components.template import template

@rx.page(route="/trazabilidad")
def trazabilidad() -> rx.Component:
    content = rx.container(
        rx.heading("Trazabilidad", size="5"),
        rx.text("Contenido de la página Trazabilidad."),
    )
    return template(page_content=content)

