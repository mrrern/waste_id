import reflex as rx
from app.states.dashboard_state import DashboardState, RecyclingData


def navigation_item(item: dict[str, str]) -> rx.Component:
    return rx.el.button(
        rx.icon(tag=item["icon"], class_name="mr-3 size-5"),
        rx.el.span(item["name"]),
        on_click=lambda: DashboardState.set_active_nav(item["name"]),
        class_name=rx.cond(
            DashboardState.active_nav == item["name"],
            "w-full flex items-center px-4 py-3 text-sm font-medium rounded-lg bg-cyan-600/20 text-cyan-300 border border-cyan-600/30",
            "w-full flex items-center px-4 py-3 text-sm font-medium rounded-lg text-gray-400 hover:bg-gray-800 hover:text-gray-200 transition-colors duration-150",
        ),
    )


def recycling_data_item(item: RecyclingData) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(item["region"], class_name="text-xs font-medium text-gray-400"),
            rx.el.span(
                item["rate"].to_string() + "%",
                class_name="text-xs font-semibold text-gray-200",
            ),
            class_name="flex justify-between mb-1",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": item["rate"].to_string() + "%"},
                class_name=rx.cond(
                    item["color"] == "red",
                    "h-1 rounded-full bg-gradient-to-r from-red-500 to-red-400",
                    rx.cond(
                        item["color"] == "blue",
                        "h-1 rounded-full bg-gradient-to-r from-blue-500 to-blue-400",
                        rx.cond(
                            item["color"] == "green",
                            "h-1 rounded-full bg-gradient-to-r from-green-500 to-green-400",
                            "h-1 rounded-full bg-gradient-to-r from-yellow-500 to-yellow-400",
                        ),
                    ),
                ),
            ),
            class_name="w-full bg-gray-700 rounded-full h-1",
        ),
        class_name="mb-3",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.image(src="/WasteID.png", class_name="h-8 w-auto mr-3"),
                rx.el.h1(
                    "WasteID",
                    class_name="text-xl font-bold text-gray-100 tracking-wider",
                ),
                rx.el.button(
                    rx.icon(tag="x", class_name="size-5"),
                    on_click=DashboardState.toggle_mobile_sidebar,
                    class_name="ml-auto md:hidden p-2 text-gray-400 hover:text-gray-200",
                ),
                class_name="flex items-center p-4 mb-6 border-b border-gray-700/50 md:border-b-0",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.foreach(DashboardState.nav_items, navigation_item),
                    class_name="space-y-2",
                ),
                class_name="px-4 mb-auto flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.h3(
                    "TASAS DE RECICLAJE E-WASTE",
                    class_name="px-4 mb-3 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                ),
                rx.el.div(
                    rx.foreach(DashboardState.recycling_data, recycling_data_item),
                    class_name="px-4",
                ),
                rx.el.p(
                    "Fuente: Our World in Data (2022)",
                    class_name="px-4 mt-2 text-[10px] text-gray-500",
                ),
                class_name="mt-auto pt-6 border-t border-gray-700/50 hidden md:block",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=rx.cond(
            DashboardState.mobile_sidebar_open,
            "fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 text-gray-300 flex flex-col border-r border-gray-700/50 transform transition-transform duration-300 ease-in-out md:translate-x-0",
            "fixed inset-y-0 left-0 z-40 w-64 bg-gray-900 text-gray-300 flex-col border-r border-gray-700/50 transform -translate-x-full transition-transform duration-300 ease-in-out md:flex md:translate-x-0 md:static md:z-auto",
        ),
    )