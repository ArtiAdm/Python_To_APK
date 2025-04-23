import os
import shutil
import pygame
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

MUSIC_FOLDER = "music_files"
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)

pygame.mixer.init()

class MusicApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Кнопки
        upload_button = Button(text="Загрузить музыку", size_hint_y=None, height=50)
        upload_button.bind(on_press=self.upload_music)

        download_button = Button(text="Скачать музыку", size_hint_y=None, height=50)
        download_button.bind(on_press=self.download_music)

        self.layout.add_widget(upload_button)
        self.layout.add_widget(download_button)

        # Список музыки
        scroll = ScrollView()
        self.music_list_content = BoxLayout(orientation='vertical', size_hint_y=None)
        self.music_list_content.bind(minimum_height=self.music_list_content.setter('height'))
        scroll.add_widget(self.music_list_content)

        self.layout.add_widget(scroll)
        self.update_music_list()

        return self.layout

    def update_music_list(self):
        self.music_list_content.clear_widgets()
        for filename in os.listdir(MUSIC_FOLDER):
            if filename.endswith(".mp3"):
                btn = Button(text=filename, size_hint_y=None, height=40)
                btn.bind(on_press=lambda btn, filename=filename: self.play_music(filename))
                self.music_list_content.add_widget(btn)

    def upload_music(self, instance):
        box = BoxLayout(orientation='vertical')
        chooser = FileChooserListView()
        confirm_btn = Button(text="Загрузить выбранный файл", size_hint_y=None, height=50)

        def confirm_upload(_):
            if chooser.selection:
                src = chooser.selection[0]
                if src.endswith(".mp3"):
                    dest = os.path.join(MUSIC_FOLDER, os.path.basename(src))
                    try:
                        shutil.copy(src, dest)
                        print(f"Файл загружен: {dest}")
                        self.update_music_list()
                        popup.dismiss()
                    except Exception as e:
                        print(f"Ошибка копирования: {e}")
                else:
                    print("Выберите .mp3 файл.")
            else:
                print("Файл не выбран.")

        confirm_btn.bind(on_press=confirm_upload)
        box.add_widget(chooser)
        box.add_widget(confirm_btn)

        popup = Popup(title="Выбор файла", content=box, size_hint=(0.9, 0.9))
        popup.open()

    def download_music(self, instance):
        url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join(MUSIC_FOLDER, "downloaded_music.mp3")
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                self.update_music_list()
                print("Музыка скачана!")
            else:
                print("Ошибка при скачивании.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def play_music(self, filename):
        try:
            path = os.path.join(MUSIC_FOLDER, filename)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            print(f"Играет: {filename}")
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")

if __name__ == '__main__':
    MusicApp().run()
