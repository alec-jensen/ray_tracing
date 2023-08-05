import math
import numpy as np
from vector import Vector3
from ray import Ray

class Camera:
    def __init__(self, x: int, y: int, z: int, pitch: int, yaw: int, roll: int, fov: int, resolution: tuple[int, int] = (1920, 1080)):
        self.x: int = x
        self.y: int = y
        self.z: int = z
        self.pitch: int = pitch
        self.yaw: int = yaw
        self.roll: int = roll
        self.fov: int = fov
        self.resolution: tuple[int, int] = resolution
    
    def get_ray(self, pixel_x: int, pixel_y: int) -> Ray:
        aspect_ratio = self.resolution[0] / self.resolution[1]
        half_width = math.tan(math.radians(self.fov / 2))
        half_height = half_width / aspect_ratio

        # Map pixel coordinates to normalized device coordinates
        ndc_x = (pixel_x + 0.5) / self.resolution[0]
        ndc_y = (pixel_y + 0.5) / self.resolution[1]

        # Map NDC to camera space
        camera_x = (2 * ndc_x - 1) * half_width
        camera_y = (1 - 2 * ndc_y) * half_height

        # Apply camera transformations (pitch, yaw, roll)
        rotation_matrix = self.get_rotation_matrix()
        direction = np.dot(rotation_matrix, np.array([camera_x, camera_y, -1]))

        origin = Vector3(self.x, self.y, self.z)
        direction = Vector3(direction[0], direction[1], direction[2]).normalized()

        return Ray(origin, direction)

    def get_rotation_matrix(self):
        # Convert pitch, yaw, roll to radians
        pitch_rad = math.radians(self.pitch)
        yaw_rad = math.radians(self.yaw)
        roll_rad = math.radians(self.roll)

        # Calculate individual rotation matrices for pitch, yaw, and roll
        rotation_pitch = np.array([
            [1, 0, 0],
            [0, math.cos(pitch_rad), -math.sin(pitch_rad)],
            [0, math.sin(pitch_rad), math.cos(pitch_rad)]
        ])

        rotation_yaw = np.array([
            [math.cos(yaw_rad), 0, math.sin(yaw_rad)],
            [0, 1, 0],
            [-math.sin(yaw_rad), 0, math.cos(yaw_rad)]
        ])

        rotation_roll = np.array([
            [math.cos(roll_rad), -math.sin(roll_rad), 0],
            [math.sin(roll_rad), math.cos(roll_rad), 0],
            [0, 0, 1]
        ])

        # Combine rotation matrices
        rotation_matrix = np.dot(rotation_yaw, np.dot(rotation_pitch, rotation_roll))
        return rotation_matrix