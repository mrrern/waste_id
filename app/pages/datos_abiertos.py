
import reflex as rx
from app.components.template import template

@rx.page(route="/datos-abiertos")
def datos_abiertos():
    content = rx.container(
        rx.heading("Datos Abiertos", size="5"),
        rx.text("Contenido de la página Datos Abiertos."),
    )
    return template(page_content=content)
