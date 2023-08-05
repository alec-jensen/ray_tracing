# Raytracing in Python
# Author: Alec Jensen

import numpy as np
from PIL import Image
import tqdm
import time

start = time.perf_counter_ns()

from camera import Camera
from vector import Vector2, Vector3
from geometry import _3DObject, Sphere, Box, Plane
from light import Light
from rgb import rgb
from material import Material
from ray import Ray

RAY_DEPTH = 5

class Scene:
    def __init__(self):
        self.objects: list[_3DObject] = []
        self.lights: list[Light] = []

    def register(self, obj: _3DObject | Light):
        if isinstance(obj, _3DObject):
            self.objects.append(obj)
        elif isinstance(obj, Light):
            self.lights.append(obj)

class Renderer:
    def __init__(self, scene: Scene, camera: Camera):
        self.scene: Scene = scene
        self.camera: Camera = camera

    def cast_ray(self, ray: Ray, depth: int = 0):
        closest_hit_point = None
        closest_normal = None
        closest_distance = float('inf')
        closest_material = None
        closest_color = rgb(0, 0, 0)

        for obj in self.scene.objects:
            hit_point, normal = obj.intersect(ray)
            if hit_point is not None:
                distance = (hit_point - ray.origin).magnitude()
                if distance < closest_distance:
                    closest_distance = distance
                    closest_hit_point = hit_point
                    closest_normal = normal  # Store the normal here
                    closest_material = obj.material
                    closest_color = obj.material.color

        if closest_hit_point is not None:
            lighting_color = self.calculate_lighting(closest_hit_point, closest_normal, closest_material, ray)
            color = closest_color * lighting_color
            if depth < RAY_DEPTH:
                # Cast a reflection ray with roughness
                reflection_direction = ray.direction - 2 * ray.direction.dot(closest_normal) * closest_normal
                reflection_direction = self.apply_roughness(reflection_direction, closest_material.roughness)
                reflection_ray = Ray(closest_hit_point + reflection_direction * 1e-4, reflection_direction)
                reflected_color = self.cast_ray(reflection_ray, depth + 1)
                color += reflected_color

            return color
        else:
            return rgb(0, 0, 0)  # Black if no intersection found
    
    def apply_roughness(self, direction: Vector3, roughness: float) -> Vector3:
        # Generate random perturbation within a cone based on roughness
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.arccos(1 - np.random.uniform(0, 1) * (1 - np.cos(np.radians(roughness * 90))))
        
        perturbation = Vector3(
            np.sin(phi) * np.cos(theta),
            np.sin(phi) * np.sin(theta),
            np.cos(phi)
        )
        
        # Combine the perturbation with the reflection direction
        perturbed_direction = direction + perturbation
        
        return perturbed_direction.normalized()

    def calculate_lighting(self, hit_point: Vector3, normal: Vector3, material: Material, ray: Ray):
        lighting_color = rgb(0, 0, 0)

        for light in self.scene.lights:
            light_direction = (light.position - hit_point).normalized()

            # Calculate ambient, diffuse, and specular components
            ambient = material.ambient * light.color * light.intensity
            diffuse = material.diffuse * max(normal.dot(light_direction), 0) * light.color * light.intensity

            # Calculate reflection direction
            reflection_direction = ray.direction - 2 * ray.direction.dot(normal) * normal

            # Calculate specular component
            specular = material.specular * max(reflection_direction.dot(light_direction), 0) ** material.shininess * light.color * light.intensity

            lighting_color += ambient + diffuse + specular

        lighting_color.clamp()
        return lighting_color

    def render(self):
        frame = np.zeros((self.camera.resolution[1], self.camera.resolution[0], 3), dtype=np.uint8)

        for y in tqdm.tqdm(range(self.camera.resolution[1])):
            for x in range(self.camera.resolution[0]):
                ray = self.camera.get_ray(x, y)
                color = self.cast_ray(ray)
                color.clamp()
                frame[y, x] = color.as_tuple()

        Image.fromarray(frame, 'RGB').show()

def main():
    scene = Scene()

    light = Light(Vector3(0, 100, 0), rgb(255, 255, 255), 0.05)
    scene.register(light)

    backWall = Plane(Vector3(0, 0, -200), Vector3(0, 0, 1), Vector2(1000, 1000), Material(rgb(255, 255, 255), 0.1, 0.9, 0.9, 100, 0.0))
    scene.register(backWall)

    leftWall = Plane(Vector3(-200, 0, 0), Vector3(1, 0, 0), Vector2(1000, 1000), Material(rgb(255, 0, 0), 0.1, 0.9, 0.9, 100, 0.0))
    scene.register(leftWall)

    rightWall = Plane(Vector3(200, 0, 0), Vector3(-1, 0, 0), Vector2(1000, 1000), Material(rgb(0, 255, 0), 0.1, 0.9, 0.9, 100, 0.0))
    scene.register(rightWall)

    floor = Plane(Vector3(-100, -100, -100), Vector3(0, 1, 0), Vector2(1000, 1000), Material(rgb(255, 255, 255), 0.1, 0.9, 0.9, 100, 0.1))
    scene.register(floor)

    sphere = Sphere(Vector3(0, 50, 0), 100, Material(rgb(138, 138, 138), 0.1, 0.9, 0.9, 100, 0.0))
    scene.register(sphere)

    sphere2 = Sphere(Vector3(300, 50, 0), 100, sphere.material)
    scene.register(sphere2)

    camera = Camera(150, 150, 300, 0, 0, 0, 100, (640, 480))
    renderer = Renderer(scene, camera)
    renderer.render()

    end = time.perf_counter_ns()
    print(f'Time elapsed: {(end - start) / 1e9} seconds')

if __name__ == '__main__':
    main()

