import json
import cv2
import random
import config
import openai
import os
import requests
from PIL import Image
from io import BytesIO
import numpy as np

class Pet:
    def __init__(self, name, health, hunger, emotion, chat_history="", image_number=None):
        self.name = name
        self.health = health
        self.hunger = hunger
        self.emotion = emotion
        self.status = ""
        self.chat_history = chat_history
        self.animal_type, self.characteristics = self.get_animal_and_characteristics()
        self.image = image_number if image_number is not None else self.generate_image()
        self.prompt = self.generate_prompt()

    def get_animal_and_characteristics(self):
        with open('utils/data/animal_types.json', encoding='utf-8') as f:
            animals = json.load(f)['Portuguese']
        with open('utils/data/personality_traits.json', encoding='utf-8') as f:
            characteristics = json.load(f)['Portuguese']

        animal_type = random.choice(animals)
        char_1, char_2, char_3 = random.sample(characteristics, 3)
        
        return animal_type, [char_1, char_2, char_3]

    def generate_image(self):
        openai.api_key = config.API_KEY
        response = openai.Image.create(
            prompt=f"a 8 bit sprite-sheet like a tamagochi of a {self.animal_type} face with 6 frames and black background",
            n=1,
            size="1024x1024"
        )

        image_url = response['data'][0]['url']

        # Faz o download da imagem
        image_data = requests.get(image_url).content

        # Salva a imagem na pasta pet_animations
        image = Image.open(BytesIO(image_data))
        next_file_number = self.get_pet_number("assets/pet_animations")
        image.save(f"assets/pet_animations/pet_{next_file_number}.png")
        
        self.generate_atlas_file(next_file_number)

        return next_file_number
    
    def generate_atlas_file(self, image_number: int):
        image_path = os.path.abspath(f"assets/pet_animations/pet_{image_number}.png")

        # Carrega a imagem
        img = cv2.imread(image_path)

        # Assume que a imagem contém uma grade de 3x3 frames
        grid_size = 3

        # Calcula a altura e a largura do frame
        frame_height = img.shape[0] // grid_size
        frame_width = img.shape[1] // grid_size

        # Cria um dicionário para armazenar os retângulos de contorno
        data_dict = {image_path: {}}

        # Gera retângulos para cada frame
        for i in range(grid_size):
            for j in range(grid_size):
                x = j * frame_width
                y = i * frame_height
                data_dict[image_path][f"frame{i * grid_size + j + 1}"] = [x, y, frame_width, frame_height]

        # Gera o caminho do arquivo de saída
        output_file = "utils/data/animation_mapping.atlas"

        # Escreve o dicionário como um arquivo JSON
        with open(output_file, 'w') as f:
            json.dump(data_dict, f, indent=4)
        
    def get_pet_number(self, directory_path):
        files = os.listdir(directory_path)
        max_number = 0
        for file in files:
            if file.startswith("pet_"):
                number = int(file.replace("pet_", "").replace(".png", ""))
                max_number = max(max_number, number)
        return max_number + 1
    
    def generate_prompt(self):
        return (f"O usuário está conversando com seu pet {self.name}. "
                f"Que é um {self.animal_type} virtual como um tamagochi e o usuário tem a responsabilidade de cuidar. "
                f"Suas características são {self.characteristics[0]}, {self.characteristics[1]} e também é um pouco {self.characteristics[2]}. "
                f"Atue de acordo com essas características.")

    def update_pet_status(self):
        if self.hunger > 11:
            self.status = 'Faminto'
        elif self.health < 50:
            self.status = 'Doente'
        else:
            self.status = 'Feliz'

    def feed(self):
        self.hunger = max(0, self.hunger - 10)
        self.update_pet_status()
        self.save_info()

    def give_injection(self):
        self.health = min(100, self.health + 10)
        self.update_pet_status()
        self.save_info()

    def play(self):
        self.emotion = 'Feliz'
        self.status = 'Feliz'
        self.update_pet_status()
        self.save_info()

    def save_info(self, chat_history=None):
        if chat_history is None:
            chat_history = self.chat_history
        pet_info = {
            'name': self.name,
            'animal_type': self.animal_type,
            'characteristics': self.characteristics,
            'health': self.health,
            'hunger': self.hunger,
            'emotion': self.emotion,
            'status': self.status,
            'image_number': self.image,  # Salvamos o número da imagem aqui
            "chat_history": chat_history
        }
        with open('save_file.txt', 'w') as file:
            json.dump(pet_info, file)

    def get_image_path(self):
        return f'assets/pet_animations/pet_{self.image}.png'

    def get_prompt(self):
        return self.prompt
