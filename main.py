import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import NoTransition
from screens.adoption_screen import AdoptionScreen
from screens.pet_screen import PetScreen
from models.pet import Pet


class PetGameApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(AdoptionScreen(name='adoption_screen'))

        pet = self.load_pet_from_save_file()
        if pet:
            self.sm.add_widget(PetScreen(name='pet_screen', pet=pet))
            self.sm.current = 'pet_screen'
        else:
            self.sm.current = 'adoption_screen'

        return self.sm

    def load_pet_from_save_file(self):
        save_file_path = "save_file.txt"

        if os.path.exists(save_file_path):
            with open(save_file_path, "r") as file:
                pet_data = json.load(file)

            pet_name = pet_data.get("name")
            pet_type_id = pet_data.get("type_id")
            pet_health = pet_data.get("health")
            pet_hunger = pet_data.get("hunger")
            pet_emotion = pet_data.get("emotion")
            pet_status = pet_data.get("status")

            return Pet(pet_name, pet_type_id, pet_health, pet_hunger, pet_emotion)
        else:
            return None


if __name__ == '__main__':
    PetGameApp().run()
