import reflex as rx


def map_card(title: str, componente: rx.Component) -> rx.Component:
    """Card to display detail for a single critical material."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                title,
                class_name="text-lg font-bold text-cyan-300",
            ),
        ),
        rx.el.div(
            componente,
            class_name="mb-2 w-full h-full p-2 m-2",

        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm hover:bg-gray-800/70 transition-colors duration-200 flex flex-col",
    )
