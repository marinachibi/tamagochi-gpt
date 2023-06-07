import json
import openai
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

class PetScreen(Screen):
    def __init__(self, pet, **kwargs):
        super().__init__(**kwargs)
        self.pet = pet
        self.status = self.pet.status  # Adiciona o atributo status
        self.layout = BoxLayout(orientation='vertical')
        self.build_layout()
        self.pet.update_pet_status()
        
    def build_layout(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')

        # Layout para o nome do pet
        pet_name_label = Label(text=self.pet.name, font_size=30, size_hint=(1, 0.1))
        main_layout.add_widget(pet_name_label)

        # Layout superior com imagem do pet
        top_layout = BoxLayout(size_hint=(1, 0.3))
        pet_image = Image(source=self.pet.pet_type.image, size=(150, 150))
        top_layout.add_widget(pet_image)

        main_layout.add_widget(top_layout)

        # Layout com informações do pet
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

        # Layout para ações do usuário
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

        # Layout para chat
        chat_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.7))
        self.chat_response_label = Label(text='', size_hint=(1, 0.5))
        chat_layout.add_widget(self.chat_response_label)

        self.chat_input = TextInput(multiline=False, size_hint=(1, 0.2), pos_hint={'center_x': 0.5})  # Tamanho aumentado
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
        # Aqui atualizamos o status do pet na tela
        self.hunger_label.text = 'Fome: {}'.format(self.pet.hunger)
        self.health_label.text = 'Saúde: {}'.format(self.pet.health)
        self.emotion_label.text = 'Emoção: {}'.format(self.pet.emotion)
        self.status_label.text = 'Status: {}'.format(self.pet.status)
    
    def feed_button_pressed(self, instance):
        self.pet.feed()
        self.update_pet_status()

    def injection_button_pressed(self, instance):
        self.pet.give_injection()
        self.update_pet_status()

    def play_button_pressed(self, instance):
        self.pet.play()
        self.update_pet_status()

    def show_chat_input(self, instance):
        self.chat_input.disabled = False
        self.chat_input.opacity = 1
        self.send_button.disabled = False
        self.send_button.opacity = 1
    
    def send_message(self, instance):
        user_input = self.chat_input.text

        # Verifica se a entrada do usuário está vazia
        if not user_input:
            return

        # Chama a API de chat GPT para obter a resposta
        openai.api_key = "API_KEY"
        prompt = self.pet.pet_type.prompt.format(self=self)
        prompt += f" Usuário: {user_input}\nPet:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=50,
            n=1,
            stop=None
        )

        # Obtém a resposta gerada pelo modelo
        chat_response = response.choices[0].text.strip()

        # Atualiza a interface do usuário com a resposta do pet
        self.chat_input.disabled = True
        self.chat_input.opacity = 0
        self.chat_input.text = ""  # Limpa a caixa de entrada
        self.send_button.disabled = True
        self.send_button.opacity = 0
        self.chat_response_label.text = f"\nUser: {user_input}\nPet: {chat_response}"
        self.update_pet_status()
