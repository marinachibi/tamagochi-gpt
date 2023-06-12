from kivy.uix.image import Image
from kivy.clock import Clock

class AnimatedImage(Image):
    def __init__(self, atlas, **kwargs):
        super().__init__(**kwargs)
        self.atlas = atlas
        self.index = 1
        self.max_index = len(self.atlas.textures)
        Clock.schedule_interval(self.update_image, 0.1)

    def update_image(self, dt):
        self.texture = self.atlas['frame' + str(self.index)]
        self.index += 1
        if self.index > self.max_index:
            self.index = 1