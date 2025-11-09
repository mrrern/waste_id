import reflex as rx
from app.states.dashboard_state import PerformanceChartData

TOOLTIP_PROPS = {
    "cursor": {"fill": "rgba(200, 200, 200, 0.1)"},
    "content_style": {
        "backgroundColor": "rgba(30, 41, 59, 0.9)",
        "borderColor": "rgba(51, 65, 85, 0.5)",
        "borderRadius": "8px",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.2)",
        "padding": "8px 12px",
    },
    "label_style": {"color": "#cbd5e1", "fontSize": "12px", "fontWeight": "bold"},
    "item_style": {"color": "#94a3b8", "fontSize": "12px"},
}
RECHART_WRAPPER_CLASS = "[&_.recharts-tooltip-cursor]:fill-zinc-500/10 [&_.recharts-tooltip-item]:!text-gray-300 [&_.recharts-tooltip-item-name]:!text-gray-400 [&_.recharts-tooltip-item-separator]:!text-gray-400 [&_.recharts-label]:!fill-gray-400 [&_.recharts-cartesian-axis-tick-value]:!fill-gray-400 [&_.recharts-legend-item-text]:!text-gray-300"


def stat_card_chart(
    data: rx.Var[list[dict[str, int]]], color: rx.Var[str]
) -> rx.Component:
    return rx.recharts.area_chart(
        rx.recharts.area(
            data_key="v",
            type_="natural",
            fill=rx.match(
                color,
                ("cyan", "url(#cyanGradient)"),
                ("purple", "url(#purpleGradient)"),
                ("teal", "url(#tealGradient)"),
                "url(#defaultGradient)",
            ),
            stroke=rx.match(
                color,
                ("cyan", "#22d3ee"),
                ("purple", "#a855f7"),
                ("teal", "#2dd4bf"),
                "#8884d8",
            ),
            stroke_width=2,
            dot=False,
            fill_opacity=0.3,
        ),
        rx.el.defs(
            rx.el.linear_gradient(
                rx.el.stop(offset="5%", stop_color="#22d3ee", stop_opacity=0.8),
                rx.el.stop(offset="95%", stop_color="#22d3ee", stop_opacity=0),
                id="cyanGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
            rx.el.linear_gradient(
                rx.el.stop(offset="5%", stop_color="#a855f7", stop_opacity=0.8),
                rx.el.stop(offset="95%", stop_color="#a855f7", stop_opacity=0),
                id="purpleGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
            rx.el.linear_gradient(
                rx.el.stop(offset="5%", stop_color="#2dd4bf", stop_opacity=0.8),
                rx.el.stop(offset="95%", stop_color="#2dd4bf", stop_opacity=0),
                id="tealGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
            rx.el.linear_gradient(
                rx.el.stop(offset="5%", stop_color="#8884d8", stop_opacity=0.8),
                rx.el.stop(offset="95%", stop_color="#8884d8", stop_opacity=0),
                id="defaultGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
        ),
        data=data,
        width="100%",
        height=50,
        margin={"top": 5, "right": 0, "left": 0, "bottom": 0},
    )


def html_legend() -> rx.Component:
    legend_items = [
        ("Generado", "bg-cyan-400", "Volumen total de E-Waste (kt)"),
        ("Reciclado", "bg-purple-500", "Tasa de recolección formal (%)"),
        ("Valor", "bg-teal-500", "Valor potencial de materiales (M USD)"),
    ]
    return rx.el.div(
        rx.foreach(
            legend_items,
            lambda item: rx.el.div(
                rx.el.div(class_name=f"w-3 h-3 rounded-full {item[1]}"),
                rx.el.div(
                    rx.el.span(item[0], class_name="text-sm font-medium text-gray-200"),
                    rx.el.span(item[2], class_name="text-xs text-gray-400"),
                    class_name="ml-2 flex flex-col",
                ),
                class_name="flex items-center",
            ),
        ),
        class_name="flex flex-col sm:flex-row justify-center items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-6 pt-4",
    )


def performance_line_chart(data: rx.Var[list[PerformanceChartData]]) -> rx.Component:
    return rx.el.div(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#374151", vertical=False
            ),
            rx.recharts.tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="time",
                axis_line=False,
                tick_line=False,
                tick_margin=10,
                style={"fontSize": "12px"},
            ),
                    # Left axis: volume (kt)
                    rx.recharts.y_axis(
                        y_axis_id="left",
                        axis_line=False,
                        tick_line=False,
                        tick_margin=10,
                        orientation="left",
                        style={"fontSize": "12px"},
                    ),
                    # Right axis: economic value (M USD)
                    rx.recharts.y_axis(
                        y_axis_id="right",
                        axis_line=False,
                        tick_line=False,
                        tick_margin=10,
                        orientation="right",
                        style={"fontSize": "12px"},
                    ),
                    # Secondary axis for percentage (0-100)
                    rx.recharts.y_axis(
                        y_axis_id="pct",
                        axis_line=False,
                        tick_line=False,
                        tick_margin=10,
                        domain=[0, 100],
                        orientation="right",
                        style={"fontSize": "12px", "color": "#a855f7"},
                    ),

                    rx.recharts.line(
                        data_key="raee_kt",
                        y_axis_id="left",
                        type_="monotone",
                        stroke="#22d3ee",
                        stroke_width=2,
                        dot=False,
                        name="Generado (kt)",
                    ),
                    rx.recharts.line(
                        data_key="recoleccion_pct",
                        y_axis_id="pct",
                        type_="monotone",
                        stroke="#a855f7",
                        stroke_width=2,
                        dot=False,
                        name="Tasa de recolección (%)",
                    ),
                    rx.recharts.line(
                        data_key="valor_musd",
                        y_axis_id="right",
                        type_="monotone",
                        stroke="#14b8a6",
                        stroke_width=2,
                        dot=False,
                        name="Valor (M USD)",
                    ),
            data=data,
            width="100%",
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 5},
        ),
        html_legend(),
        class_name=RECHART_WRAPPER_CLASS,
    )


def material_line_chart(data: rx.Var[list[dict]]) -> rx.Component:
    """Line chart for critical metals detail.

    Expects items with keys: 'metal', 'recovered_t' (tons) and 'recovered_value_usd'.
    """
    return rx.el.div(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#374151", vertical=False),
            rx.recharts.tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(data_key="metal", axis_line=False, tick_line=False, tick_margin=10, style={"fontSize": "12px"}),
            # Left axis: tons recovered
            rx.recharts.y_axis(y_axis_id="left", axis_line=False, tick_line=False, tick_margin=10, orientation="left", style={"fontSize": "12px"}),
            # Right axis: USD value
            rx.recharts.y_axis(y_axis_id="right", axis_line=False, tick_line=False, tick_margin=10, orientation="right", style={"fontSize": "12px"}),
            rx.recharts.line(data_key="recovered_t", y_axis_id="left", type_="monotone", stroke="#22d3ee", stroke_width=2, dot=False, name="Toneladas recuperadas"),
            rx.recharts.line(data_key="recovered_value_usd", y_axis_id="right", type_="monotone", stroke="#14b8a6", stroke_width=2, dot=False, name="Valor recuperado (USD)"),
            data=data,
            width="100%",
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 5},
        ),
        # small legend
        rx.el.div(
            rx.el.span("Toneladas recuperadas", class_name="text-xs text-gray-300 mr-4"),
            rx.el.span("Valor recuperado (USD)", class_name="text-xs text-gray-300"),
            class_name="pt-4",
        ),
        class_name=RECHART_WRAPPER_CLASS,
    )