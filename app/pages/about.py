import reflex as rx
from app.components.template import template
from app.components.about.team import about_dashboard

@rx.page(route="/about")
def about() -> rx.Component:
    """About page."""
    return template(page_content=about_dashboard())

