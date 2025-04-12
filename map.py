from PIL import Image
import numpy as np

DARK_GREY = np.array([50, 50, 50])
GREY = np.array([40, 40, 40])
class Map():
    def __init__(self, map_file, player):
        self.map_file = map_file
        self.player = player
        
        image = Image.open(self.map_file).convert("RGB")

        player.world_width, player.world_height = image.size
        self.color_map = np.array(image)

        # add world borders
        self.color_map[0, :]  = DARK_GREY
        self.color_map[-1, :] = DARK_GREY
        self.color_map[:, 0]  = DARK_GREY
        self.color_map[:, -1] = DARK_GREY

        # whatever is not white is a wall
        WHITE = np.array([255, 255, 255]).reshape(1, 1, 3)

        self.hit_map = ~(np.all(self.color_map==WHITE, axis=2))
    
    def emit_ray(self, angle):
        # ray casting algorithm
        current_x, current_y = self.player.position
      
        ray_angle = (angle + self.player.angle) % (2 * np.pi)

        ray_is_vertical = np.pi*1/4 < ray_angle < np.pi*3/4 or np.pi*5/4 < ray_angle < np.pi*7/4
        if not ray_is_vertical:
            slope = np.tan(ray_angle)
            movement_sign = -1 if np.pi*1/2 < ray_angle < np.pi * 3/2 else 1
            while not self.hit_map[round(current_y), round(current_x)]:
                current_x += movement_sign
                current_y += movement_sign * slope
        else:
            slope = 1 / np.tan(ray_angle)
            movement_sign = -1 if ray_angle > np.pi else 1

            while not self.hit_map[round(current_y), round(current_x)]:
                current_x += movement_sign * slope
                current_y += movement_sign

        relative_position = np.array([current_x, current_y]) - self.player.position
        depth = np.cos(angle) * np.linalg.norm(relative_position)

        color = self.color_map[round(current_y), round(current_x)]
        ratio = min(1, 0.2 +  25 / depth)
        mixed = color * ratio + GREY*(1-ratio)
        return depth, mixed
    
    def emit_rays(self, angles):      
        ray_angles = (angles + self.player.angle) % (2 * np.pi)
        is_ray_vertical =  ((np.pi*1/4 < ray_angles) & (ray_angles< np.pi*3/4)) | ((np.pi*5/4 < ray_angles) & (ray_angles < np.pi*7/4))

        slopes = np.tan(ray_angles)
        slopes[is_ray_vertical] = 1 / slopes[is_ray_vertical]

        movement_signs = np.zeros_like(ray_angles)
        movement_signs[is_ray_vertical]  = (ray_angles[is_ray_vertical] < np.pi) * 2 - 1
        movement_signs[~is_ray_vertical] = 1 - 2 * ((np.pi*1/2 < ray_angles[~is_ray_vertical]) & (ray_angles[~is_ray_vertical] < np.pi * 3/2))
        
        movement_step = np.zeros((len(ray_angles), 2))

        movement_step[is_ray_vertical,  0] = movement_signs[is_ray_vertical] * slopes[is_ray_vertical]
        movement_step[is_ray_vertical,  1] = movement_signs[is_ray_vertical]

        movement_step[~is_ray_vertical, 0] = movement_signs[~is_ray_vertical]
        movement_step[~is_ray_vertical, 1] = movement_signs[~is_ray_vertical] * slopes[~is_ray_vertical]

        current_position = np.zeros_like(movement_step) + self.player.position
        is_ray_going = np.arange(len(angles))

        while len(is_ray_going) > 0:
            current_position[is_ray_going] += movement_step[is_ray_going]
            is_ray_going = np.delete(
                is_ray_going,
                self.hit_map[np.round(current_position[is_ray_going, 1]).astype(int),
                             np.round(current_position[is_ray_going, 0]).astype(int)]
            )

        relative_positions = current_position - self.player.position
        depths = np.cos(angles) * np.linalg.norm(relative_positions, axis=1)
        colors = self.color_map[np.round(current_position[:, 1]).astype(int),
                                np.round(current_position[:, 0]).astype(int)]

        ratio = np.clip(0.2 +  25 / depths, 0, 1)[:, np.newaxis]
        mixed = colors * ratio + GREY*(1-ratio)

        return depths, mixed