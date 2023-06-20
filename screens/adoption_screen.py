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
from models.animatedImage import AnimatedImage
from kivy.core.image import Atlas

class AdoptionScreen(Screen):
    def __init__(self, **kwargs):
        super(AdoptionScreen, self).__init__(**kwargs)

        self.pet = Pet(name='unnamed', health=100, hunger=10, emotion='happy')
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)
        self.pet_animation = Image(source=self.pet.get_image_path())
        atlas = Atlas("utils/data/animation_mapping.atlas")
        self.pet_animation = AnimatedImage(atlas, size=(150, 150))
        layout.add_widget(self.pet_animation)

        self.name_input = TextInput(hint_text="Digite o nome do pet")
        layout.add_widget(self.name_input)

        self.try_again_button = Button(text="Tentar outro pet", on_release=self.try_again, disabled=False)
        layout.add_widget(self.try_again_button)

        self.name_button = Button(text="Nomear pet", on_release=self.name_pet)
        layout.add_widget(self.name_button)

    def try_again(self, instance):
        if self.try_again_button.disabled:
            return

        self.try_again_button.disabled = True  
        layout = self.children[0]
        layout.remove_widget(self.pet_animation)

        self.pet = Pet(name='unnamed', health=100, hunger=10, emotion='happy')
        atlas = Atlas("utils/data/animation_mapping.atlas")
        self.pet_animation = AnimatedImage(atlas, size=(150, 150))
        layout.add_widget(self.pet_animation,  index=len(layout.children))

    def name_pet(self, instance):
        pet_name = self.name_input.text.strip()
        if not pet_name:
            return

        if self.pet.name == 'unnamed':
            self.pet.name = pet_name
            self.pet.save_info()

        screen_manager = self.manager
        pet_screen = PetScreen(name='pet_screen', pet=self.pet)
        screen_manager.add_widget(pet_screen)
        screen_manager.current = 'pet_screen'