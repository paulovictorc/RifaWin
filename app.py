from flask import Flask, render_template
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import GridLayout
from kivy.metrics import dp
import random
import pyperclip


Builder.load_string('''
<RootWidget>:
    orientation: 'vertical'
    padding: '10dp'

    MDLabel:
        text: "Bem vindo(a) ao RiffaWinner futuro(a) ganhador(a)!"
        font_size: 25
        size_hint_y: None
        height: self.texture_size[1] + dp(10)  # Adicionando um espaçamento
        padding: dp(10)

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)

        MDTextField:
            id: code_input
            hint_text: 'Cole um código'

        MDTextField:
            id: quantity_input
            hint_text: 'Quantidade de bilhetes comprado (máximo 50)'

        MDRaisedButton:
            text: 'Ver meus bilhetes'
            on_release: app.generate_numbers()

    ScrollView:
        GridLayout:
            id: output_grid
            cols: 5
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            row_default_height: dp(40)  # Altura fixa para cada rótulo de número
            height: self.minimum_height
            pos_hint: {'top': 1}  # Coloca a GridLayout no topo
''')

app = Flask(__name__)

class RootWidget(MDBoxLayout):
    pass

class RifaWinnerApp(MDApp):
    def build(self):
        return RootWidget()

    def generate_numbers(self):
        try:
            entered_code = self.root.ids.code_input.text.strip()
            quantity = int(self.root.ids.quantity_input.text)
            clipboard_content = pyperclip.paste()

            if entered_code == clipboard_content:
                if 0 < quantity <= 50:
                    seed = hash(entered_code) % ((2 ** 32) - 1)
                    random.seed(seed)

                    self.root.ids.output_grid.clear_widgets()
                    numbers = [str(random.randint(0, 999999)).zfill(6) for _ in range(quantity)]
                    for number in numbers:
                        number_label = MDLabel(text=number, font_size=20, size_hint_y=None, height=dp(40))
                        self.root.ids.output_grid.add_widget(number_label)
                else:
                    self.show_message("Insira uma quantidade válida (> 0 e <= 50)")
            else:
                self.show_message("Código incorreto. Cole o código correto para ver seus bilhetes")
        except ValueError:
            self.show_message("Insira um número válido")

    def show_message(self, text):
        message_label = MDLabel(text=text)
        self.root.ids.output_grid.clear_widgets()
        self.root.ids.output_grid.add_widget(message_label)

@app.route('/')
def index():
    return render_template('kivy_template.html')

if __name__ == '__main__':
    RifaWinnerApp().run()
