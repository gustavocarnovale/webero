from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import requests

class KivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        button = Button(text='Make Request to Flask')
        button.bind(on_press=self.make_request_to_flask)
        layout.add_widget(button)
        return layout

    def make_request_to_flask(self, instance):
        url = 'http://127.0.0.1:5000'  # Cambia esta URL según tu configuración de Flask
        data = {'barcode': '123', 'category': 'example', 'quantity': '5', 'price': '10.99'}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            print('Solicitud exitosa:', response.text)
        else:
            print('Error en la solicitud:', response.status_code)

if __name__ == '__main__':
    KivyApp().run()
