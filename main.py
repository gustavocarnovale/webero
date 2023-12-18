from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import webbrowser

class KivyApp(App):
    def build(self):
        webbrowser.open('http://127.0.0.1:5000/')
    #    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
#
    #    # Botón para abrir el navegador web con la URL del servidor Flask
    #    open_browser_button = Button(text='Abrir Navegador Web', size_hint=(1, 1))
    #    open_browser_button.bind(on_press=self.open_browser)
    #    layout.add_widget(open_browser_button)
#
    #    return layout
#
    #def open_browser(self, instance):
    #    # Abre el navegador web externo con la URL del servidor Flask
    #    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    KivyApp().run()
