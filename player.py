import numpy as np

class Player():
    def __init__(self, position, angle):
        self.position = np.array(position, dtype=float)
        self.angle = angle

    def move(self, delta):
        unit_delta = np.array(np.cos(self.angle), np.sin(self.angle))
        self.position += delta * unit_delta
    
    def rotate(self, delta):
        self.angle += delta
        self.angle %= 2 * np.pi
