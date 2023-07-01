from io import BytesIO
import requests
import config
import openai
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from PIL import Image as PILImage


class GameOverScreen(Screen):
    def __init__(self, pet, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text=f"GAME OVER {pet.name} Morreu!",font_size=30))
        self.layout.add_widget(Image(source=self.generate_dead_image(pet), size=(150,150)))
        retry_button = Button(text="Tente Novamente")
        retry_button.bind(on_press=self.go_to_adoption_screen)
        self.layout.add_widget(retry_button)
        self.add_widget(self.layout)
    
    def generate_dead_image(self, pet):
        openai.api_key = config.API_KEY
        response = openai.Image.create(
            prompt=f"a 16 bit pixel art of dead a {pet.animal_type} like a tamagotchi on a black background",
            n=1,
            size="1024x1024"
        )

        image_url = response['data'][0]['url']

        # Faz o download da imagem
        image_data = requests.get(image_url).content

        # Salva a imagem na pasta pet_animations
        image = PILImage.open(BytesIO(image_data))
        img_path = ("assets/pet_animations/pet_dead.png")
        image.save(f"assets/pet_animations/pet_dead.png")

        return img_path

    def go_to_adoption_screen(self, instance):
        from screens.adoption_screen import AdoptionScreen
        manager = self.manager
        manager.add_widget(AdoptionScreen(name='adoption_screen'))  # adiciona AdoptionScreen
        manager.remove_widget(self)  # remove GameOverScreen
        manager.current = 'adoption_screen'

    

    





