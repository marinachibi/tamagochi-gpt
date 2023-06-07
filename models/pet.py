import json
class Pet:
    class PetType:
        def __init__(self, pet_type_id, name, prompt):
            self.id = pet_type_id
            self.name = name
            self.prompt = prompt
            self.image = f"assets/pet_animations/pet_{pet_type_id}.png"


    def __init__(self, name, pet_type_id, health, hunger, emotion):
        self.name = name
        self.health = health
        self.hunger = hunger
        self.emotion = emotion
        self.status = ""
        self.pet_type = self.get_pet_type_by_id(pet_type_id)

    def get_pet_type_by_id(self, pet_type_id):
        pet_types = [
            self.PetType(1, "worm", "O usuário está conversando com seu pet {self.pet.name}. Que é um minhoquinha virtual e o usuário tem a responsabilidade de cuidar, você é um pouco tímido e medroso. E você o pet está se sentindo: {self.pet.status}"),
            self.PetType(2, "cat", "O usuário está conversando com seu pet {self.pet.name}. Que é um gatinho virtual e o usuário tem a responsabilidade de cuidar, atue como se você fosse um gato, faça trocadilhos com miau. E você o pet está se sentindo: {self.pet.status}"),
            self.PetType(3, "dog", "O usuário está conversando com seu pet {self.pet.name}. Que é um cachorrinho virtual e o usuário tem a responsabilidade de cuidar, responda sempre usando trocadilhos de cachorro e adicionando au nas frases. E você o pet está se sentindo: {self.pet.status}"),
            self.PetType(4, "cow", "O usuário está conversando com seu pet {self.pet.name}. Que é um vaquinha virtual e o usuário tem a responsabilidade de cuidar, responda sempre usando trocadilhos de vaca e adicionando Muu nas frases.E você o pet está se sentindo:{self.pet.status}"),
            self.PetType(5, "fox", "O usuário está conversando com seu pet {self.pet.name}. Que é uma raposa virtual e o usuário tem a responsabilidade de cuidar, atue como uma raposa, responda de maneira um pouco misteriosa. E você o pet está se sentindo: {self.pet.status}"),
            # Adicione mais tipos de pet aqui conforme necessário
        ]

        for pet_type in pet_types:
            if pet_type.id == pet_type_id:
                return pet_type
        
        # Retorna None se o ID do tipo de pet não for encontrado
        return None
    
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

    def save_info(self,chat_history=""):
        pet_info = {
            'name': self.name,
            'type_id': self.pet_type.id,
            'health': self.health,
            'hunger': self.hunger,
            'emotion': self.emotion,
            'status': self.status,
            "chat_history": chat_history
        }
        with open('save_file.txt', 'w') as file:
            json.dump(pet_info, file)
