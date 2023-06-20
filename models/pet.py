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
        height, width, _ = img.shape

        # Cria uma cópia da imagem para desenhar os retângulos de contorno (para fins de debug)
        img_debug = img.copy()

        # Aplica pré-processamento para melhorar a detecção de contornos
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)


        # Realiza detecção de contornos
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        # Define critérios de filtragem de contornos
        min_contour_area = 25000  # Área mínima para considerar um contorno
        max_contour_area = 230000 # Área máxima para considerar um contorno

        # Cria um dicionário para armazenar os retângulos de contorno
        data_dict = {image_path: {}}

        # Gera retângulos para cada contorno filtrado
        frame_index = 1
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_contour_area < area < max_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                y = height - (y + h)  # Transforma a coordenada y para o sistema de referência do canto inferior esquerdo
                data_dict[image_path][f"frame{frame_index}"] = [x, y, w, h]
                frame_index += 1

                # Desenha o retângulo na imagem de debug
                cv2.rectangle(img_debug, (x, y), (x + w, y + h), (0, 255, 0), 2)
                

        # Gera o caminho do arquivo de saída
        output_file = "utils/data/animation_mapping.atlas"

        # Escreve o dicionário como um arquivo JSON
        with open(output_file, 'w') as f:
            json.dump(data_dict, f, indent=4)

        # Mostra a imagem de debug com os retângulos desenhados
        cv2.imshow("Debug Image", img_debug)

  
    def get_pet_number(self, directory_path):
        files = os.listdir(directory_path)
        max_number = 0
        for file in files:
            if file.startswith("pet_"):
                number = int(file.replace("pet_", "").replace(".png", ""))
                max_number = max(max_number, number)
        return max_number + 1
    
    def generate_prompt(self):
        return (f"Você é um pet virtual como um tamagochi seu nome é {self.name}. "
                f"Você é do tipo {self.animal_type} eu tenho a responsabilidade de cuidar de você. "
                f"Suas características são {self.characteristics[0]}, {self.characteristics[1]} e também bastante {self.characteristics[2]}. "
                f"Atue com um pet virtual de acordo com essas características.")

    def update_pet_status(self):
        if self.hunger > 11:
            self.status = 'Faminto'
        elif self.health > 70:
             self.status = 'Saudavel'
        elif self.hunger == 0:                                 
            self.status = 'Nao querendo comer'
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
    
    def generate_reaction(self,action):
        reacton_prompt= f"Como um {self.animal_type},Quando voce esta {self.status} Diga uma frase para quando o meu dono {action}. Respoda de forma {self.characteristics[0]}"
        openai.api_key = config.API_KEY
        response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=reacton_prompt,
                temperature=0.7,
                max_tokens=40,
                n=1,
                stop=None
        )

        rection = response.choices[0].text.strip()
        return rection


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
