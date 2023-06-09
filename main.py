import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import NoTransition
from kivy.core.audio import SoundLoader
from screens.adoption_screen import AdoptionScreen
from screens.pet_screen import PetScreen
from models.pet import Pet


class PetGameApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())

       # self.load_background_music()

        pet = self.load_pet_from_save_file()
        if pet:
            self.sm.add_widget(PetScreen(name='pet_screen', pet=pet))
            self.sm.current = 'pet_screen'
        else:
            self.sm.add_widget(AdoptionScreen(name='adoption_screen'))
            self.sm.current = 'adoption_screen'

        return self.sm

    def load_background_music(self):
        music_file_path = "assets/music/background_music.mp3"

        if os.path.exists(music_file_path):
            self.background_music = SoundLoader.load(music_file_path)
            if self.background_music:
                self.background_music.loop = True
                self.background_music.play()

    def load_pet_from_save_file(self):
        save_file_path = "save_file.txt"

        if os.path.exists(save_file_path):
            with open(save_file_path, "r") as file:
                pet_data = json.load(file)

            pet_name = pet_data.get("name")
            pet_animal_type = pet_data.get("animal_type")
            pet_characteristics = pet_data.get("characteristics")
            pet_health = pet_data.get("health")
            pet_hunger = pet_data.get("hunger")
            pet_emotion = pet_data.get("emotion")
            pet_status = pet_data.get("status")
            pet_image = pet_data.get("image_number")
            pet_last_fed_time = pet_data.get("last_fed_time")
            pet_last_play_time = pet_data.get("last_play_time")
            last_chat_time = pet_data.get("last_chat_time")
            pet_chat_history = pet_data.get("chat_history", "")

            pet = Pet(pet_name, pet_health, pet_hunger, pet_emotion, chat_history=pet_chat_history, image_number=pet_image,last_fed_time=pet_last_fed_time,last_play_time=pet_last_play_time,last_chat_time=pet_last_play_time)
            pet.animal_type = pet_animal_type  # Atribuir o tipo de animal carregado
            pet.characteristics = pet_characteristics  # Atribuir as características carregadas

            return pet
        else:
            return None

if __name__ == '__main__':
    PetGameApp().run()
