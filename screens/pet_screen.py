import config
import openai
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from models.animatedImage import AnimatedImage
from kivy.core.image import Atlas

class PetScreen(Screen):
    def __init__(self, pet, **kwargs):
        super().__init__(**kwargs)
        self.pet = pet
        self.status = self.pet.status  # Adiciona o atributo status
        self.layout = BoxLayout(orientation='vertical')
        self.build_layout()
        self.pet.update_pet_status()
        self.chat_history = ""

    def build_layout(self):
        # Main Layout
        main_layout = BoxLayout(orientation='vertical')

        # Pet name layout
        pet_name_label = Label(text=self.pet.name, font_size=30, size_hint=(1, 0.1))
        main_layout.add_widget(pet_name_label)

        # Top layout with pet image
        top_layout = BoxLayout(size_hint=(1, 0.3))
        atlas = Atlas("utils/data/animation_mapping.atlas")
        pet_image = AnimatedImage(atlas, size=(150, 150))
        top_layout.add_widget(pet_image)
        main_layout.add_widget(top_layout)

        # Layout with pet info
        pet_info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        status_layout = BoxLayout(orientation='horizontal')
        self.hunger_label = Label(text='Fome: {}'.format(self.pet.hunger))
        self.health_label = Label(text='Saúde: {}'.format(self.pet.health))
        self.emotion_label = Label(text='Emoção: {}'.format(self.pet.emotion))
        self.status_label = Label(text='Status: {}'.format(self.pet.status))
        status_layout.add_widget(self.hunger_label)
        status_layout.add_widget(self.health_label)
        status_layout.add_widget(self.emotion_label)
        status_layout.add_widget(self.status_label)
        pet_info_layout.add_widget(status_layout)

        main_layout.add_widget(pet_info_layout)

        # Layout for user actions
        user_actions_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        actions_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
        feed_button = Button(text='Alimentar')
        feed_button.bind(on_press=self.feed_button_pressed)
        injection_button = Button(text='Dar Injeção')
        injection_button.bind(on_press=self.injection_button_pressed)
        play_button = Button(text='Brincar')
        play_button.bind(on_press=self.play_button_pressed)
        actions_layout.add_widget(feed_button)
        actions_layout.add_widget(injection_button)
        actions_layout.add_widget(play_button)
        user_actions_layout.add_widget(actions_layout)

        # Layout for chat
        chat_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.7))
        self.chat_response_label = Label(text='', size_hint=(1, 0.5))
        chat_layout.add_widget(self.chat_response_label)

        self.chat_input = TextInput(multiline=False, size_hint=(1, 0.2), pos_hint={'center_x': 0.5})  
        self.chat_input.disabled = True
        self.chat_input.opacity = 0
        self.send_button = Button(text='Enviar', size_hint=(1, 0.1))
        self.send_button.disabled = True
        self.send_button.opacity = 0
        self.send_button.bind(on_press=self.send_message)
        chat_layout.add_widget(self.chat_input)
        chat_layout.add_widget(self.send_button)

        chat_button = Button(text='Conversar', size_hint=(1, 0.1))
        chat_button.bind(on_press=self.show_chat_input)
        chat_layout.add_widget(chat_button)
        user_actions_layout.add_widget(chat_layout)
        main_layout.add_widget(user_actions_layout)

        self.add_widget(main_layout)

    def update_pet_status(self):
        # Here we update the pet status on the screen
        self.hunger_label.text = 'Fome: {}'.format(self.pet.hunger)
        self.health_label.text = 'Saúde: {}'.format(self.pet.health)
        self.emotion_label.text = 'Emoção: {}'.format(self.pet.emotion)
        self.status_label.text = 'Status: {}'.format(self.pet.status)
    
    def feed_button_pressed(self, instance):
        self.pet.feed()
        self.update_pet_status()
        self.update_chat_history(self.pet.generate_reaction("te alimenta"))
        
    def injection_button_pressed(self, instance):
        self.pet.give_injection()
        self.update_pet_status()
        self.update_chat_history(self.pet.generate_reaction("te da uma injecao"))

    def play_button_pressed(self, instance):
        self.pet.play()
        self.update_pet_status()
        self.update_chat_history(self.pet.generate_reaction("brinca com voce"))

    def update_chat_history(self, pet_reaction):
        self.chat_history += f"\nPet:{pet_reaction}"
        self.chat_response_label.text = self.chat_history
        self.pet.save_info(self.chat_history)

    def show_chat_input(self, instance):
        self.chat_input.disabled = False
        self.chat_input.opacity = 1
        self.send_button.disabled = False
        self.send_button.opacity = 1

    def send_message(self, instance):
        try:
            user_input = self.chat_input.text
            if not user_input:
                return
            if not self.chat_history.strip():
                prompt = self.pet.generate_prompt()
                self.chat_history += prompt
            else:
                prompt = ""
            
            self.chat_history += f"{user_input}\n"
            openai.api_key = config.API_KEY
            prompt += self.chat_history
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=40,
                n=1,
                stop=None
            )
            chat_response = response.choices[0].text.strip()
            self.chat_history += f"{chat_response}\n"
            self.chat_input.disabled = True
            self.chat_input.opacity = 0
            self.chat_input.text = ""
            self.send_button.disabled = True
            self.send_button.opacity = 0
            self.chat_response_label.text = f"\nVoce: {user_input}\nPet: {chat_response}"
            self.update_pet_status()
            self.pet.save_info(self.chat_history)
        except Exception as e:
            print("Erro ao enviar mensagem:", e)
