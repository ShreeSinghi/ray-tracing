import numpy as np

GRAVITY = 2.5
JUMP_SPEED = 5
class Player():
    def __init__(self, position, angle):
        self.position = np.array(position, dtype=float)
        self.angle = angle
        self.z = 0
        self.z_vel = 0

    def move(self, delta):
        unit_delta = np.array((np.cos(self.angle), np.sin(self.angle)))
        self.position += delta * unit_delta
    
    def rotate(self, delta):
        self.angle += delta
        self.angle %= 2 * np.pi

    def jump(self):
        if self.z == 0:
            self.z_vel = JUMP_SPEED

    def gravity_update(self):
        if self.z > 0:
            self.z_vel -= GRAVITY
        self.z += self.z_vel
        self.z = max(0, self.z)        