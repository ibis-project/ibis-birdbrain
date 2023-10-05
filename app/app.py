"""Ibis Birdbrain"""

# imports
import reflex as rx

from app import styles
from app.state import State
from app.components import chat, modal, navbar, sidebar


# pages
def index() -> rx.Component:
    """The main app."""
    return rx.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


# app
app = rx.App(state=State, style=styles.base_style)
app.add_page(index)
app.compile()
