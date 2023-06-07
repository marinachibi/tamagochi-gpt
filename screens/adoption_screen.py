import json
import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from screens.pet_screen import PetScreen
from models.pet import Pet

class AdoptionScreen(Screen):
    def __init__(self, **kwargs):
        super(AdoptionScreen, self).__init__(**kwargs)
        self.pet_types = 5  # Número total de tipos de pet

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        pet_type_id = self.choose_random_pet_type()
        pet_image_path = f"assets/pet_animations/pet_{pet_type_id}.png"
        self.pet_animation = Image(source=pet_image_path)
        layout.add_widget(self.pet_animation)

        self.name_input = TextInput(hint_text="Digite o nome do pet")
        layout.add_widget(self.name_input)

        self.try_again_button = Button(text="Tentar outro pet", on_release=self.try_again, disabled=False)
        layout.add_widget(self.try_again_button)

        self.name_button = Button(text="Nomear pet", on_release=self.name_pet)
        layout.add_widget(self.name_button)
        self.pet_type_id = pet_type_id

    def choose_random_pet_type(self):
        random_pet_type = random.randint(1, 5)
        return random_pet_type

    def try_again(self, instance):
        # Verifica se o botão "Tentar outro pet" ainda está habilitado
        if self.try_again_button.disabled:
            return

        self.try_again_button.disabled = True  # Desabilita o botão
        layout = self.children[0]
        layout.remove_widget(self.pet_animation)

        # Atualiza o tipo de pet aleatoriamente
        self.pet_type_id = self.choose_random_pet_type()
        pet_image_path = f"assets/pet_animations/pet_{self.pet_type_id}.png"

        # Cria uma nova instância do widget da animação do pet
        self.pet_animation = Image(source=pet_image_path)
        layout.add_widget(self.pet_animation,  index=len(layout.children))


    def name_pet(self, instance):
        pet_name = self.name_input.text

        # Verifica se o nome do pet foi digitado
        if not pet_name:
            return

        # Salva as informações do pet em um arquivo de salvamento (ou banco de dados)
        pet_type_id = self.pet_type_id
        pet_health = 100
        pet_hunger = 10
        pet_emotion = 'happy'

        pet_data = {
            "name": pet_name,
            "type_id": pet_type_id,
            "health": pet_health,
            "hunger": pet_hunger,
            "emotion": pet_emotion
        }
        self.save_pet_data(pet_data)

        # Navega para a tela do pet existente
        screen_manager = self.manager
        pet_type_id = pet_type_id
        pet_screen = PetScreen(name='pet_screen', pet=Pet(pet_data['name'], pet_type_id, pet_data['health'], pet_data['hunger'], pet_data['emotion']))
        screen_manager.add_widget(pet_screen)
        screen_manager.current = 'pet_screen'

    def save_pet_data(self, pet_data):
        save_file_path = "save_file.txt"  # Caminho do arquivo de salvamento

        with open(save_file_path, "w") as file:
            json.dump(pet_data, file)