import pygame
import random
import sys

# Ekran ayarları
screen_width = 1280
screen_height = 720
max_blocks_x = 20
max_blocks_y = 15

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Grid hesaplamaları
def calculate_grid_size(screen_width, screen_height, max_blocks_x, max_blocks_y):
    block_size_x = screen_width // max_blocks_x
    block_size_y = screen_height // max_blocks_y
    block_size = min(block_size_x, block_size_y)
    cols = screen_width // block_size
    rows = screen_height // block_size
    return rows, cols, block_size

rows, cols, block_size = calculate_grid_size(screen_width, screen_height, max_blocks_x, max_blocks_y)

# Dünya oluşturma
def create_world(rows, cols, default_value=0):
    return [[default_value for _ in range(cols)] for _ in range(rows)]

def generate_terrain(rows, cols, min_height=3, max_height=6, grass_type=1, dirt_type=2):
    world = create_world(rows, cols)
    for x in range(cols):
        height = random.randint(min_height, max_height)
        for y in range(rows - height, rows):
            world[y][x] = dirt_type if y < rows - 1 else grass_type
    return world

world = generate_terrain(rows, cols, min_height=3, max_height=6)

# Karakter sınıfı
class Character:
    def __init__(self, grid_x, grid_y, block_size):
        self.grid_x = grid_x  # Karakterin grid üzerindeki x pozisyonu
        self.grid_y = grid_y  # Karakterin grid üzerindeki y pozisyonu
        self.block_size = block_size
        self.direction = "right"  # Sağ veya sol bakış
        self.color = (255, 255, 0)  # Karakterin rengi (sarı)
        self.gravity_enabled = True  # Yerçekimi kontrolü

    def draw(self, screen):
        # Karakteri çiz (2 blok yüksekliğinde)
        x = self.grid_x * self.block_size
        y = self.grid_y * self.block_size
        pygame.draw.rect(screen, self.color, (x, y, self.block_size, self.block_size * 2))

    def can_move(self, world, new_x, new_y):
        # Hareket edilecek konumu kontrol et
        if new_x < 0 or new_x >= cols or new_y < 0 or new_y + 1 >= rows:
            return False  # Dünya sınırlarının dışına çıkmaya çalışıyorsa engelle
        # Hareket edilecek yer veya altındaki blok doluysa engelle
        if world[new_y][new_x] != 0 or world[new_y + 1][new_x] != 0:
            return False
        return True

    def apply_gravity(self, world):
        # Altındaki blokları kontrol et
        if self.grid_y + 2 < rows and world[self.grid_y + 2][self.grid_x] == 0:
            delay = 100  # Yerçekimi hızı
            self.grid_y += 1  # Yerçekimiyle bir blok aşağı düş
        else:
            self.gravity_enabled = False  # Yerçekimi artık etkili değil

    def move(self, keys, world):
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            if self.can_move(world, self.grid_x - 1, self.grid_y):
                self.grid_x -= 1  # 1 blok sola hareket et
        elif keys[pygame.K_RIGHT]:
            self.direction = "right"
            if self.can_move(world, self.grid_x + 1, self.grid_y):
                self.grid_x += 1  # 1 blok sağa hareket et
        elif keys[pygame.K_UP]:
            if self.can_move(world, self.grid_x, self.grid_y - 1):
                self.grid_y -= 1  # 1 blok yukarı hareket et

    def break_block(self, world):
        # Karakterin baktığı yöne bağlı olarak blok kırma
        target_x, target_y = self.grid_x, self.grid_y

        if self.direction == "right" and target_x + 1 < cols:
            target_x += 1
        elif self.direction == "left" and target_x - 1 >= 0:
            target_x -= 1

        # Blok kırma işlemi
        if world[target_y][target_x] != 0:
            world[target_y][target_x] = 0  # Blok yok edilir

# Karakter oluştur
player = Character(grid_x=5, grid_y=rows - 6, block_size=block_size)

# Dünyayı çizme fonksiyonu
def draw_world(world):
    for y, row in enumerate(world):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            if tile == 1:  # Grass
                pygame.draw.rect(screen, (107, 142, 35), rect)
            elif tile == 2:  # Dirt
                pygame.draw.rect(screen, (139, 69, 19), rect)

# Ana döngü
def main():
    global world
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space tuşuna basınca blok kır
                    player.break_block(world)

        keys = pygame.key.get_pressed()
        player.move(keys, world)

        # Yerçekimi
        if player.gravity_enabled:
            player.apply_gravity(world)
        else:
            # Altında blok yoksa tekrar yerçekimini etkinleştir
            if player.grid_y + 2 < rows and world[player.grid_y + 2][player.grid_x] == 0:
                player.gravity_enabled = True

        screen.fill((0, 0, 0))  # Ekranı temizle
        draw_world(world)  # Dünyayı çiz
        player.draw(screen)  # Karakteri çiz
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
