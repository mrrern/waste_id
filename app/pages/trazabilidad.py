
import reflex as rx
from app.components.template import template
from app.components.trazabilidad.charts import trazabilidad_dashboard

@rx.page(route="/trazabilidad")
def trazabilidad() -> rx.Component:
    """Trazabilidad page."""
    return template(page_content=trazabilidad_dashboard())

