from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text='Kivy 테스트 - 이 텍스트가 보이면 정상입니다!')

if __name__ == '__main__':
    TestApp().run()
