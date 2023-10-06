# imports
import ibis
import marvin

import reflex as rx

# from ibis_birdbrain.bots.birdbrain import bot
from ibis_birdbrain.bots.tpch3000 import bot

# configure ibis and birdbrain
bot.interactive = False  # this is unintuitive


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = {
        "hello, birdbrain": [QA(question="hello,", answer="birdbrain")],
    }

    # The current chat name.
    current_chat = "hello, birdbrain"

    # The currrent question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    def create_chat(self):
        """Create a new chat."""
        # Insert a default question.
        self.chats[self.new_chat_name] = [QA(question="hello,", answer="birdbrain")]
        self.current_chat = self.new_chat_name

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = {"new chat": [QA(question="hello,", answer="birdbrain")]}
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Check if we have already asked the last question or if the question is empty
        self.question = form_data["question"]
        if (
            self.chats[self.current_chat][-1].question == self.question
            or self.question == ""
        ):
            return

        # Set the processing flag to true and yield.
        self.processing = True
        yield

        # Build the messages.
        messages = [{"role": "system", "content": "You are Ibis Birdbrain"}]

        for qa in self.chats[self.current_chat][1:]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        messages.append({"role": "user", "content": self.question})

        # Start a new session to answer the question.
        qa = QA(question=self.question, answer="")
        self.chats[self.current_chat].append(qa)

        # Stream the results, yielding after every word.
        response = "squawk"
        if self.question == "/debug" or self.question == "/audit":
            response = ""
            for m in bot.ai.history.messages:
                response += f"""
role: {m.role}<br>
timestamp: {m.timestamp}<br>
content: {m.content}<br>
<br>
"""
                if m.role.value == "FUNCTION_RESPONSE":
                    response += f"""
name: {m.name}<br>
data: {m.data}<br>
<br>
"""
                response += "---<br><br>"
            response = response.strip()

        else:
            response = bot(self.question)

        self.chats[self.current_chat][-1].answer = response
        yield

        # Toggle the processing flag.
        self.processing = False
