import pygame
import math
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0) # Black
FPS = 60
SPAWN_INTERVAL = 2000  # Time in milliseconds between enemy missile spawns
PLAYER_MISSILE_SPEED = 5  # Speed for player missiles
ENEMY_MISSILE_SPEED = 3  # Speed for enemy missiles

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Having a BLAST/Missile Command by Pranit Singh")
clock = pygame.time.Clock()

# Classes
class MissileCommand:
    def __init__(self): # Initilize game state
        self.level = 1
        self.score = 0

    def click(self, x, y):
        # Create a new player missile targeting the click position
        if silos:
            # Choose the closest silo to launch the missile
            closest_silo = min(silos, key=lambda silo: abs(silo.rect.centerx - x))
            # Create and launch a missile from the closest silo
            player_missile = Missile((255, 255, 255), closest_silo.rect.centerx, closest_silo.rect.centery, PLAYER_MISSILE_SPEED)
            player_missile.set_target(x, y)  # Set the target for the missile
            all_sprites.add(player_missile)  # Add the missile to the list of all sprites
            player_missiles.add(player_missile)  # Add the missile to the list of player missiles

class City(pygame.sprite.Sprite):# Creating the city sprite and fucntions
    def __init__(self, x, y):
        # Initialize city sprite
        super().__init__()
        self.image = pygame.Surface((50, 50)) # City size
        self.image.fill((0, 255, 0)) # City color: green
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = "alive"

    def destroy(self):
        # Destroy city
        self.state = "destroyed"
        self.kill() # Remove the city sprite

class Silo(pygame.sprite.Sprite): # Creating the silo sprite and fucntions
    def __init__(self, x, y):
        # Initialize silo sprite
        super().__init__()
        self.image = pygame.Surface((50, 50)) # Silo size
        self.image.fill((0, 0, 255)) # Silo color: blue
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = "alive"

    def destroy(self):
        # Destroy silo
        self.state = "destroyed"
        self.kill() # Remove the silo sprite

class Missile(pygame.sprite.Sprite): # Creating the missile sprite and fucntions
    def __init__(self, color, x, y, speed):
        super().__init__() # initialize the sprite
        self.image = pygame.Surface((10, 10)) # set missile size
        self.image.fill(color) # Set missile color
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.state = "ready"
        self.target_x = 0
        self.target_y = 0
        self.dx = 0
        self.dy = 0
        self.frame = 0.0

    def set_target(self, target_x, target_y):
        # Set missile taget coordinates and calculate movement vectors
        if self.state == "ready":
            self.target_x = target_x
            self.target_y = target_y
            self.dx = self.target_x - self.rect.centerx
            self.dy = self.target_y - self.rect.centery
            distance = math.sqrt(self.dx**2 + self.dy**2) # Calculate distance between missile and target
            self.dx = (self.dx / distance) * self.speed # Normalize dy - missile moves at constant speed towards it target regardless of distance
            self.dy = (self.dy / distance) * self.speed # Normalize dx - missile moves at constant speed towards it target regardless of distance
            self.state = "launched" # Change state to launched

    def explode(self):
        # Handle missile explosion animation
        self.frame += 1.0
        if self.frame < 30.0:
            size = int(self.frame * 0.2 * 10)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (size // 2, size // 2), size // 2)
            self.rect = self.image.get_rect(center=self.rect.center)
        elif self.frame < 55.0:
            size = int((60 - self.frame) * 0.2 * 10)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (size // 2, size // 2), size // 2)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.destroy() # Destroy the missile after explosion

    def update(self):
        # Update missile position and handle state changes
        if self.state == "launched":
            self.rect.x += self.dx
            self.rect.y += self.dy
            distance = math.sqrt((self.target_x - self.rect.centerx)**2 + (self.target_y - self.rect.centery)**2)
            if distance < 10:
                self.state = "explode"
        elif self.state == "explode": # Change state to explode when reaching target
            self.explode() # Handle explosion

    def destroy(self):
        # Destroy missile
        self.state = "ready"
        self.kill() # Remove the missile sprite

# Functions
def spawn_enemy_missiles(enemy_missiles, num_missiles):
    # Spawn enemy missiles at random positions with random targets
    for _ in range(num_missiles):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(-400, -100)
        enemy_missile = Missile((255, 0, 0), x, y, ENEMY_MISSILE_SPEED) # Create enemy missile
        target = random.choice(cities.sprites() + silos.sprites()) # Randomly choose target (city or silo)
        enemy_missile.set_target(target.rect.centerx, target.rect.centery) # Set target for enemy missile
        all_sprites.add(enemy_missile) # Add enemy missile to all sprites
        enemy_missiles.add(enemy_missile) # Add enemy missile to enemy missiles
        print(f"Spawned enemy missile at ({x}, {y}) targeting ({target.rect.centerx}, {target.rect.centery})")  # Debugging statement

def main():
    # Main game function
    global all_sprites, player_missiles, cities, silos, enemy_missiles
    game = MissileCommand()

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    player_missiles = pygame.sprite.Group()
    cities = pygame.sprite.Group()
    silos = pygame.sprite.Group()
    enemy_missiles = pygame.sprite.Group()

    # Create cities and silos
    for i in range(6):
        city = City(-250 + (i * 100) + SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        all_sprites.add(city)
        cities.add(city)

    for i in range(3):
        silo = Silo(-350 + (i * 350) + SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75)
        all_sprites.add(silo)
        silos.add(silo)

    # Spawn initial enemy missiles
    spawn_enemy_missiles(enemy_missiles, game.level)

    # Set up enemy missile spawn timer
    pygame.time.set_timer(pygame.USEREVENT, SPAWN_INTERVAL)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Launch player missile on mouse click
                x, y = event.pos
                game.click(x, y)
            elif event.type == pygame.USEREVENT:
                # Spawn enemy missile at interval
                spawn_enemy_missiles(enemy_missiles, 1)

        # Update game
        all_sprites.update()

        # Check for collisions and handle game logic
        for player_missile in player_missiles:
            if player_missile.state == "explode":
                for enemy_missile in enemy_missiles:
                    if pygame.sprite.collide_circle(player_missile, enemy_missile):
                        enemy_missile.destroy()
                        game.score += 10

        for enemy_missile in enemy_missiles:
            if enemy_missile.state == "explode":
                for city in cities:
                    if pygame.sprite.collide_rect(enemy_missile, city):
                        city.destroy()
                for silo in silos:
                    if pygame.sprite.collide_rect(enemy_missile, silo):
                        silo.destroy()

        # Check for game over condition
        if not cities and not silos:
            print("Game Over")
            running = False # End the game

        # Render game
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
