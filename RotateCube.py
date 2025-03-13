import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 480, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cube Simulation")

# Font for FPS display
font = pygame.font.Font(None, 20)

# Linked list node for cube storage
class CubeNode:
    def __init__(self, cube_id, position, angles, scale):
        self.id = cube_id
        self.position = np.array(position, dtype=float)
        self.angles = np.array(angles, dtype=float)
        self.scale = float(scale)
        self.next = None

class CubeList:
    def __init__(self):
        self.head = None
    
    #Create a new cube to the linked list
    def add_cube(self, cube_id, position, angles, scale):
        new_cube = CubeNode(cube_id, position, angles, scale)
        new_cube.next = self.head
        self.head = new_cube

    #Remove a cube from the list
    def remove_cube(self, cube_id):
        prev, current = None, self.head
        while current:
            if current.id == cube_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return
            prev, current = current, current.next
    
    #Delete all cubes
    def clear_all(self):
        self.head = None
    
    #Move a cube by updating its position.
    def move_cube(self, cube_id, dx=10, dy=10, dz=10):
        current = self.head
        while current:
            if current.id == cube_id:
                current.position += [dx, dy, dz]
                return
            current = current.next
    
    #Rotate a cube by updating its angles
    def rotate_cube(self, cube_id, angles):
        current = self.head
        while current:
            if current.id == cube_id:
                current.angles += angles
                return
            current = current.next
    
    #Scale a cube by updating its scale
    def scale_cube(self, cube_id, scale_factor):
        current = self.head
        while current:
            if current.id == cube_id:
                current.scale *= scale_factor
                return
            current = current.next
    
    #Generate 10 Random Cubes
    def generate_random_cubes(self, count=10):
        for _ in range(count):
            cube_id = random.randint(1000, 9999)
            position = [random.uniform(-1, 1) for _ in range(3)]
            angles = [random.uniform(0, 360) for _ in range(3)]
            scale = random.uniform(0.5, 2)
            self.add_cube(cube_id, position, angles, scale)

# Read commands from a text file and execute them
def process_commands(filename, cube_list):
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            
            command = parts[0]
            if command == "C":
                cube_list.add_cube(int(parts[1]), list(map(float, parts[2:5])), list(map(float, parts[5:8])), float(parts[8]))
            elif command == "D":
                if parts[1] == "A":
                    cube_list.clear_all()
                else:
                    cube_list.remove_cube(int(parts[1]))
            elif command == "M":
                cube_list.move_cube(int(parts[1]))
            elif command == "R":
                cube_list.rotate_cube(int(parts[1]), list(map(float, parts[2:5])))
            elif command == "S":
                cube_list.scale_cube(int(parts[1]), float(parts[2]))
            elif command == "N":
                cube_list.generate_random_cubes()

# Main program loop
def main():
    cube_list = CubeList()
    process_commands("commands.txt", cube_list)  # Read commands from a file
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Display FPS
        fps = pygame.time.Clock().get_fps()
        fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
