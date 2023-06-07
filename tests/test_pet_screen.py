import unittest
from unittest.mock import MagicMock
from screens.pet_screen import PetScreen
from models.pet import Pet

class TestPetScreen(unittest.TestCase):
    def setUp(self):
        pet = Pet("Fluffy", 2, 100, 50, "happy")
        self.pet_screen = PetScreen(pet)

    def test_pet_screen_initial_attributes(self):
        self.assertEqual(self.pet_screen.pet.name, "Fluffy")
        self.assertEqual(self.pet_screen.pet.hunger, 50)
        self.assertEqual(self.pet_screen.pet.health, 100)
        self.assertEqual(self.pet_screen.pet.emotion, "happy")
        self.assertEqual(self.pet_screen.pet.status, "Faminto")
        self.assertEqual(self.pet_screen.status, "")

    def test_update_pet_status(self):
        self.pet_screen.pet.update_pet_status()
        self.assertEqual(self.pet_screen.pet.status, "Faminto")

    def test_feed_button_pressed(self):
        self.pet_screen.pet.feed = MagicMock()
        self.pet_screen.update_pet_status = MagicMock()

        self.pet_screen.feed_button_pressed(None)

        self.pet_screen.pet.feed.assert_called_once()
        self.pet_screen.update_pet_status.assert_called_once()

    def test_injection_button_pressed(self):
        self.pet_screen.pet.give_injection = MagicMock()
        self.pet_screen.update_pet_status = MagicMock()

        self.pet_screen.injection_button_pressed(None)

        self.pet_screen.pet.give_injection.assert_called_once()
        self.pet_screen.update_pet_status.assert_called_once()

    def test_play_button_pressed(self):
        self.pet_screen.pet.play = MagicMock()
        self.pet_screen.update_pet_status = MagicMock()

        self.pet_screen.play_button_pressed(None)

        self.pet_screen.pet.play.assert_called_once()
        self.pet_screen.update_pet_status.assert_called_once()

    def test_show_chat_input(self):
        self.pet_screen.chat_input.disabled = True
        self.pet_screen.chat_input.opacity = 0
        self.pet_screen.send_button.disabled = True
        self.pet_screen.send_button.opacity = 0

        self.pet_screen.show_chat_input(None)

        self.assertFalse(self.pet_screen.chat_input.disabled)
        self.assertEqual(self.pet_screen.chat_input.opacity, 1)
        self.assertFalse(self.pet_screen.send_button.disabled)
        self.assertEqual(self.pet_screen.send_button.opacity, 1)

if __name__ == '__main__':
    unittest.main()
