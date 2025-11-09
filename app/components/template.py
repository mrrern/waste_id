import reflex as rx
from app.components.sidebar import sidebar
from app.states.dashboard_state import DashboardState

def template(page_content: rx.Component) -> rx.Component:
    """The template for all pages."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            #ashboard_header(),
            rx.el.div(
                page_content,
                #right_sidebar(),
                class_name="flex flex-1 overflow-hidden",
            ),
            class_name="flex flex-col flex-1 overflow-hidden",
        ),
        rx.cond(
            DashboardState.mobile_sidebar_open,
            rx.el.div(
                on_click=DashboardState.toggle_mobile_sidebar,
                class_name="fixed inset-0 bg-black/50 z-30 md:hidden",
            ),
            None,
        ),
        class_name="flex h-screen bg-gray-950 text-gray-300 relative",
        on_mount=DashboardState.load_data,
    )
