

import reflex as rx
from app.components.template import template
from app.states.maps_state import MapeoDeFlujosState
from app.components.mapeo_de_flujos.card_map import map_card

@rx.page(route="/mapeo-de-flujos")
def mapeo_de_flujos():
    return template(
        page_content=rx.container(
            rx.heading("Mapeo de Flujos de E-Waste en LATAM", size="5"),
            rx.el.select(
                        rx.foreach(
                            MapeoDeFlujosState.country_list,
                            lambda pais: rx.el.option(pais, value=pais),
                        ),
                        value=MapeoDeFlujosState.selected_country,
                        on_change=MapeoDeFlujosState.on_country_change,
                        class_name="bg-gray-800 border border-gray-700 text-gray-300 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block p-3 m-2",
                    ),
            map_card(
                title= MapeoDeFlujosState.selected_country,
                componente=rx.plotly(data=MapeoDeFlujosState.map_figure),
            ),
            on_mount=MapeoDeFlujosState.get_e_waste_data,
        )
    )

