import unittest
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from unittest.mock import MagicMock, patch
from kivy.uix.screenmanager import Screen
from screens.adoption_screen import AdoptionScreen

class TestAdoptionScreen(unittest.TestCase):
    def setUp(self):
        self.adoption_screen = AdoptionScreen()

    def test_adoption_screen_initial_attributes(self):
        self.assertEqual(self.adoption_screen.pet_types, 5)
        self.assertIsInstance(self.adoption_screen.pet_animation, Image)
        self.assertIsInstance(self.adoption_screen.name_input, TextInput)
        self.assertIsInstance(self.adoption_screen.try_again_button, Button)
        self.assertIsInstance(self.adoption_screen.name_button, Button)

    def test_choose_random_pet_type(self):
        pet_type = self.adoption_screen.choose_random_pet_type()
        self.assertGreaterEqual(pet_type, 1)
        self.assertLessEqual(pet_type, 5)

    def test_try_again(self):
        self.adoption_screen.try_again_button.disabled = False
        layout = self.adoption_screen.children[0]
        self.adoption_screen.try_again(None)
        self.assertTrue(self.adoption_screen.try_again_button.disabled)

    def test_name_pet(self):
        self.adoption_screen.name_input.text = "Fluffy"
        self.adoption_screen.save_pet_data = MagicMock()
        screen_manager = MagicMock()
        pet_screen = Screen(name='pet_screen')
        screen_manager.add_widget = MagicMock(return_value=pet_screen)
        self.adoption_screen.manager = screen_manager

        self.adoption_screen.name_pet(None)

        self.adoption_screen.save_pet_data.assert_called_once()
        self.assertEqual(screen_manager.current,'pet_screen')

if __name__ == '__main__':
    unittest.main()
