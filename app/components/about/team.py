import reflex as rx
from app.states.dashboard_state import DashboardState

class AboutState(DashboardState):
    """State for the About page."""
    
    @rx.var
    def team_members(self) -> list[dict]:
        """List of team members."""
        return [
            {
                "name": "Richard Brito",
                "role": "Estudiante de Física",
                "institution": "Universidad de los Andes (ULA), Venezuela",
                "bio": "Estudiante de física de la Universidad de los Andes(ULA) VE. Apasionado de la investigación en inteligencia artificial y tecnologías adyacentes, promotor del pensamiento critico hacia las tecnologías y el buen uso racional de las mismas, amante del Voleibol y el Taekwondo. Amante del reciclaje para la construcción de cosas nuevas. Entusiasta de la divulgación y enseñanza de la ciencia y la programación en la vida cotidiana",
                "icon": "user",
                "color": "cyan",
            },
            {
                "name": "Roman Duarte",
                "role": "Estudiante de Tecnología",
                "institution": "Instituto Tecnológico Metropolitano (ITM), Medellín",
                "bio": "Me llamo Roman Duarte Parra, estudio en el Instituto Tecnológico Metropolitano de Medellín (ITM), he dedicado gran parte de mi vida a la producción musical profesional y al diseño y desarrollo frontend. Mantengo una rutina de estudio y actualización constante diaria para siempre estar al tanto de las tecnologías modernas y poder siempre estar al día con el mundo del desarrollo y de la IA, ademas, mantengo mis proyectos personales y el promuevo el aprendizaje libre para los principiantes en el mundo tecnológico.",
                "icon": "music",
                "color": "purple",
            },
            {
                "name": "Andrés Flores",
                "role": "Físico",
                "institution": "Universidad de Los Andes, Venezuela",
                "bio": "Soy Andrés Flores, Físico egresado de la Universidad de Los Andes, Venezuela. Mi pasión por la ciencia converge en el campo de la Física Médica y se complementa con un firme compromiso por impulsar tecnologías que mitiguen los efectos del cambio climático. Como parte de este compromiso con el impacto social, participo activamente en Rotaract (una ONG), donde canalizo mi vocación de servicio ayudando a otros, y me dedico a la divulgación científica, convencido de que acercar el conocimiento a la sociedad es fundamental para inspirar hacia un futuro sostenible al alcance de todos.",
                "icon": "atom",
                "color": "teal",
            },
            {
                "name": "Reinaldo Díaz",
                "role": "Estudiante de Física",
                "institution": "Universidad Central de Venezuela (UCV)",
                "bio": "Mi nombre es Reinaldo Kevin Díaz Parra, soy estudiante de Física en la Universidad Central de Venezuela (UCV), apasionado por el conocimiento científico y su aplicación en la vida cotidiana. Además de mi interés académico, disfruto del béisbol como espacio de deporte y comunidad. Comprometido con el cuidado del medio ambiente, participo en iniciativas que promueven el reciclaje y la sostenibilidad, buscando generar un impacto positivo tanto en el entorno universitario como en la sociedad.",
                "icon": "globe",
                "color": "green",
            },
            {
                "name": "Laura Rodriguez",
                "role": "Ingeniera Industrial e Ingeniera de Sistemas",
                "institution": "Universidad Nacional del Callao / Universidad Nacional Mayor de San Marcos",
                "bio": "Soy Ingeniera Industrial en la Universidad Nacional del Callao e Ingeniera de Sistemas en la Universidad Nacional Mayor de San Marcos, con una sólida formación en ambos campos y una gran pasión por el aprendizaje continuo y el desarrollo profesional. A lo largo de mi formación académica, he demostrado un fuerte compromiso con el voluntariado, participando en diversas iniciativas comunitarias y programas de ayuda. Mi participación en hackathones me ha permitido desarrollar habilidades en resolución de problemas y trabajo bajo presión, además de fomentar la innovación y la creatividad en entornos competitivos. La investigación es otra de mis grandes pasiones, donde he tenido la oportunidad de colaborar en proyectos interdisciplinarios que buscan soluciones prácticas y eficientes a problemas reales.",
                "icon": "briefcase",
                "color": "amber",
            },
        ]

def team_member_card(name: str, role: str, institution: str, bio: str, icon: str, color: str) -> rx.Component:
    """Card component for displaying a team member."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.image(icon, class_name="size-12 rounded-full h-auto "),
                        class_name=f"p-4 rounded-full bg-gradient-to-br from-{color}-500 to-{color}-600 text-white shadow-lg mx-auto mb-4 w-fit",
                    ),
                    rx.el.h3(
                        name,
                        class_name="text-xl font-bold text-cyan-300 mb-2 text-center",
                    ),
                    rx.el.p(
                        role,
                        class_name="text-sm font-medium text-gray-400 mb-1 text-center",
                    ),
                    rx.el.p(
                        institution,
                        class_name="text-xs text-gray-500 mb-4 text-center",
                    ),
                    rx.el.p(
                        bio,
                        class_name="text-sm text-gray-400 leading-relaxed",
                    ),
                    class_name="flex flex-col items-center",
                ),
                class_name="flex-1",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-6 shadow-md backdrop-blur-sm hover:bg-gray-800/70 transition-colors duration-200 flex flex-col h-full",
    )

def about_dashboard() -> rx.Component:
    """The main dashboard component for the about page."""
    return rx.el.main(
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    rx.icon(tag="users", class_name="mr-2 text-cyan-400 hidden sm:inline-block"),
                    "Los Tensores de CR7",
                    class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Conoce al equipo detrás de WasteIT, un grupo multidisciplinario comprometido con la sostenibilidad y la gestión responsable de residuos electrónicos.",
                    class_name="text-sm text-gray-400 mb-6 text-center max-w-3xl mx-auto",
                ),
                rx.el.div(
                    rx.el.h3(
                        rx.image("/WasteID.png", class_name="w-fit h-auto mx-auto mb-6 "),
                        class_name="w-20 text-center font-semibold text-gray-200 mb-4 mr-auto ml-auto ",
                    ),
                ),
                rx.el.div(
                    team_member_card(
                        "Richard Brito",
                        "Estudiante de Física",
                        "Universidad de los Andes (ULA), Venezuela",
                        "Estudiante de física de la Universidad de los Andes(ULA) VE. Apasionado de la investigación en inteligencia artificial y tecnologías adyacentes, promotor del pensamiento critico hacia las tecnologías y el buen uso racional de las mismas, amante del Voleibol y el Taekwondo. Amante del reciclaje para la construcción de cosas nuevas. Entusiasta de la divulgación y enseñanza de la ciencia y la programación en la vida cotidiana",
                        "/richard.jpg",
                        "cyan",
                    ),
                    team_member_card(
                        "Roman Duarte",
                        "Estudiante de Tecnología",
                        "Instituto Tecnológico Metropolitano (ITM), Medellín",
                        "Me llamo Roman Duarte Parra, estudio en el Instituto Tecnológico Metropolitano de Medellín (ITM), he dedicado gran parte de mi vida a la producción musical profesional y al diseño y desarrollo frontend. Mantengo una rutina de estudio y actualización constante diaria para siempre estar al tanto de las tecnologías modernas y poder siempre estar al día con el mundo del desarrollo y de la IA, ademas, mantengo mis proyectos personales y el promuevo el aprendizaje libre para los principiantes en el mundo tecnológico.",
                        "/roman.jpg",
                        "purple",
                    ),
                    team_member_card(
                        "Andrés Flores",
                        "Físico",
                        "Universidad de Los Andes, Venezuela",
                        "Soy Andrés Flores, Físico egresado de la Universidad de Los Andes, Venezuela. Mi pasión por la ciencia converge en el campo de la Física Médica y se complementa con un firme compromiso por impulsar tecnologías que mitiguen los efectos del cambio climático. Como parte de este compromiso con el impacto social, participo activamente en Rotaract (una ONG), donde canalizo mi vocación de servicio ayudando a otros, y me dedico a la divulgación científica, convencido de que acercar el conocimiento a la sociedad es fundamental para inspirar hacia un futuro sostenible al alcance de todos.",
                        "/andres.jpg",
                        "teal",
                    ),
                    team_member_card(
                        "Reinaldo Díaz",
                        "Estudiante de Física",
                        "Universidad Central de Venezuela (UCV)",
                        "Mi nombre es Reinaldo Kevin Díaz Parra, soy estudiante de Física en la Universidad Central de Venezuela (UCV), apasionado por el conocimiento científico y su aplicación en la vida cotidiana. Además de mi interés académico, disfruto del béisbol como espacio de deporte y comunidad. Comprometido con el cuidado del medio ambiente, participo en iniciativas que promueven el reciclaje y la sostenibilidad, buscando generar un impacto positivo tanto en el entorno universitario como en la sociedad.",
                        "/reinaldo.jpg",
                        "green",
                    ),
                    team_member_card(
                        "Laura Rodriguez",
                        "Ingeniera Industrial e Ingeniera de Sistemas",
                        "Universidad Nacional del Callao / Universidad Nacional Mayor de San Marcos",
                        "Soy Ingeniera Industrial en la Universidad Nacional del Callao e Ingeniera de Sistemas en la Universidad Nacional Mayor de San Marcos, con una sólida formación en ambos campos y una gran pasión por el aprendizaje continuo y el desarrollo profesional. A lo largo de mi formación académica, he demostrado un fuerte compromiso con el voluntariado, participando en diversas iniciativas comunitarias y programas de ayuda. Mi participación en hackathones me ha permitido desarrollar habilidades en resolución de problemas y trabajo bajo presión, además de fomentar la innovación y la creatividad en entornos competitivos. La investigación es otra de mis grandes pasiones, donde he tenido la oportunidad de colaborar en proyectos interdisciplinarios que buscan soluciones prácticas y eficientes a problemas reales.",
                        "/laura.jpg",
                        "amber",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="mb-6",
            ),
            class_name="mb-6",
        ),
        rx.el.section(
            rx.el.div(
                rx.el.h3(
                    "Sobre el Proyecto",
                    class_name="text-lg font-semibold text-gray-200 mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "WasteIT es una plataforma desarrollada por 'Los Tensores de CR7' con el objetivo de proporcionar herramientas y visualizaciones para comprender mejor el impacto de los residuos electrónicos (e-waste) en Latinoamérica.",
                        class_name="text-sm text-gray-400 mb-3",
                    ),
                    rx.el.p(
                        "Nuestro equipo multidisciplinario combina conocimientos en física, ingeniería, tecnología y ciencias ambientales para crear soluciones innovadoras que promuevan la sostenibilidad y el manejo responsable de los residuos electrónicos.",
                        class_name="text-sm text-gray-400",
                    ),
                    class_name="space-y-2",
                ),
                class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mt-6",
            ),
        ),
        class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
    )

