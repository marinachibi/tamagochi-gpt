import unittest
from unittest.mock import patch, MagicMock
from models.pet import Pet

class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet(name='Test Pet', health=100, hunger=10, emotion='happy', chat_history='Test chat history',image_number=1)

    def test_get_animal_and_characteristics(self):
        animal_type, characteristics = self.pet.get_animal_and_characteristics()
        self.assertIsNotNone(animal_type)
        self.assertIsNotNone(characteristics)
        self.assertIsInstance(animal_type, str)
        self.assertIsInstance(characteristics, list)
        self.assertEqual(len(characteristics), 3)

    def test_get_pet_number(self):
        mock_os = MagicMock()
        mock_os.listdir.return_value = ['pet_1.png', 'pet_3.png', 'not_a_pet.png', 'pet_2.png']
        with patch('models.pet.os', mock_os):
            pet_number = self.pet.get_pet_number('assets/pet_animations')
            self.assertEqual(pet_number, 4)

    def test_update_pet_status(self):
        self.pet.update_pet_status()
        self.assertEqual(self.pet.status, 'Feliz')

        self.pet.hunger = 12
        self.pet.update_pet_status()
        self.assertEqual(self.pet.status, 'Faminto')

        self.pet.hunger = 10
        self.pet.health = 49
        self.pet.update_pet_status()
        self.assertEqual(self.pet.status, 'Doente')

    def test_feed(self):
        self.pet.feed()
        self.assertEqual(self.pet.hunger, 0)
        self.assertEqual(self.pet.status, 'Feliz')

    def test_give_injection(self):
        self.pet.give_injection()
        self.assertEqual(self.pet.health, 100)
        self.assertEqual(self.pet.status, 'Feliz')

    def test_play(self):
        self.pet.play()
        self.assertEqual(self.pet.emotion, 'Feliz')
        self.assertEqual(self.pet.status, 'Feliz')

    def test_save_info(self):
        with patch('models.pet.json') as mock_json, \
             patch('models.pet.open') as mock_open:
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file
            self.pet.save_info(chat_history='New chat history')

            mock_open.assert_called_with('save_file.txt', 'w')
            mock_json.dump.assert_called_with({
                'name': 'Test Pet',
                'animal_type': self.pet.animal_type,
                'characteristics': self.pet.characteristics,
                'health': 100,
                'hunger': 10,
                'emotion': 'happy',
                'status': '',
                'image_number': self.pet.image,
                'chat_history': 'New chat history'
            }, mock_file)

    def test_get_image_path(self):
        self.pet.image = 1
        image_path = self.pet.get_image_path()
        self.assertEqual(image_path, 'assets/pet_animations/pet_1.png')

    def test_get_prompt(self):
        prompt = self.pet.get_prompt()
        self.assertIsInstance(prompt, str)
        self.assertNotEqual(prompt, '')

if __name__ == '__main__':
    unittest.main()
