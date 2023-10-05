import reflex as rx

from app import styles
from app.state import State


def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon(
                    tag="hamburger",
                    mr=4,
                    on_click=State.toggle_drawer,
                    cursor="pointer",
                ),
                rx.link(
                    rx.box(
                        rx.image(src="favicon.ico", width=30, height="auto"),
                        p="1",
                        border_radius="2",
                        bg="#800080",
                        mr="1",
                    ),
                    href="/",
                ),
                rx.breadcrumb(
                    rx.breadcrumb_item(
                        rx.text("Ibis Birdbrain", size="lg", font_weight="bold"),
                    ),
                    rx.breadcrumb_item(
                        rx.text(State.current_chat, size="lg", font_weight="normal"),
                    ),
                ),
            ),
            rx.hstack(
                rx.button(
                    "+ New chat",
                    bg=styles.accent_color,
                    px="4",
                    py="3",
                    h="auto",
                    on_click=State.toggle_modal,
                ),
                rx.menu(
                    rx.menu_button(
                        rx.avatar(name="Eddie Cambaras", size="md"),
                        rx.box(),
                    ),
                    rx.menu_list(
                        rx.menu_item("Help"),
                        rx.menu_divider(),
                        rx.menu_item("Settings"),
                    ),
                ),
                spacing="8",
            ),
            justify="space-between",
        ),
        bg=styles.bg_dark_color,
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="4",
        border_bottom=f"1px solid {styles.border_color}",
        position="sticky",
        top="0",
        z_index="100",
    )
