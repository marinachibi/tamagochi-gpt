import unittest
from models.pet import Pet

class TestPet(unittest.TestCase):
    
    def setUp(self):
        self.pet = Pet('Fluffy', 1, 100, 0, 'happy')
        self.pet2 = Pet('Nonexistent', 10, 100, 0, 'happy')  # tipo de pet não existente

    def test_init(self):
        self.assertEqual(self.pet.name, 'Fluffy')
        self.assertEqual(self.pet.health, 100)
        self.assertEqual(self.pet.hunger, 0)
        self.assertEqual(self.pet.emotion, 'happy')
        self.assertEqual(self.pet.pet_type.name, 'worm')

    def test_get_pet_type_by_id(self):
        pet = Pet("Fluffy", 2, 100, 10, "Feliz")
        
        self.assertEqual(pet.get_pet_type_by_id(2).name, "cat")

    def test_pet_initial_attributes(self):
        pet = Pet("Rex", 3, 80, 50, "sad")
        
        self.assertEqual(pet.name, "Rex")
        self.assertEqual(pet.health, 80)
        self.assertEqual(pet.hunger, 50)
        self.assertEqual(pet.emotion, "sad")
        self.assertEqual(pet.status, "")

    def test_update_pet_status(self):
        pet = Pet("Buddy", 1, 60, 20, "happy")
        
        pet.update_pet_status()
        
        self.assertEqual(pet.status, "Faminto")

    def test_feed_pet(self):
        pet = Pet("Fido", 4, 70, 30, "hungry")
        
        pet.feed()
        
        self.assertEqual(pet.hunger, 20)

    def test_play_with_pet(self):
        pet = Pet("Charlie", 5, 90, 40, "bored")
        
        pet.play()
        
        self.assertEqual(pet.emotion, "Feliz")

if __name__ == '__main__':
    unittest.main()