import flet as ft
import time
import g4f


# the styling properties for the main content area class
def main_style():
    return {
        "width": 420,
        "height": 500,
        "bgcolor": "#141518",
        "border_radius": 10,
        "padding": 15,
    }


def prompt_style():
    return {
        "width": 420,
        "height": 40,
        "border_color": "white",
        "content_padding": 10,
        "cursor_color": "white",
    }


# main content area class
class MainContentArea(ft.Container):
    def __init__(self):
        super().__init__(**main_style())
        self.chat = ft.ListView(
            expand=True,
            height=200,
            spacing=15,
            auto_scroll=True,
        )

        self.content = self.chat


class CreateMessage(ft.Column):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message
        self.text = ft.Text(self.message)
        super().__init__(spacing=4)
        self.controls = [ft.Text(self.name, opacity=0.6), self.text]


# user input class
class Prompt(ft.TextField):
    messages = []

    def __init__(self, chat: ft.ListView):
        super().__init__(**prompt_style(), on_submit=self.run_prompt)
        self.chat = chat

    def animate_text_output(self, name: str, prompt: str):
        word_list = []
        msg = CreateMessage(name, "")
        self.chat.controls.append(msg)

        for word in list(prompt):
            word_list.append(word)
            msg.text.value = "".join(word_list)
            self.chat.update()
            time.sleep(0.008)

    def user_output(self, prompt):
        self.animate_text_output(name="Me", prompt=prompt)

    def gpt_output(self, prompt):
        self.messages.append({"role": "user", "content": prompt})


        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo_16k,
            messages=self.messages)


        self.animate_text_output(name="ChatGPT", prompt=response)

        self.messages.append({"role": "assistant", "content": response})

    # method: run all methods when started
    def run_prompt(self, event):
        text = event.control.value
        self.value = ""
        self.update()

        # first, we output the user prompt
        self.user_output(prompt=text)

        # second, we display GPT output
        self.gpt_output(prompt=text)


def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"
    page.window_width = 600
    page.window_height = 800

    def clear(e):
        prompt.chat.controls.clear()
        prompt.messages = []
        page.update()

    main = MainContentArea()
    prompt = Prompt(chat=main.chat)
    clearButton = ft.IconButton(icon="delete", on_click=clear)

    page.add(
        ft.Text("ChatGPT App", size=28, weight=ft.FontWeight.W_800),
        clearButton,
        main,
        ft.Divider(height=6, color="transparent"),
        prompt,
        # clearButton,
    )

    page.update()


ft.app(target=main)

