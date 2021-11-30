import pygame
from pygame.locals import *
import time
import random

WIDTH = 1000
HEIGHT = 800
SIZE = 50
BACKGROUND_COLOR = (187, 221, 228)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("static/apple.bmp").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(0, WIDTH // SIZE - 1) * SIZE
        self.y = random.randint(0, HEIGHT // SIZE - 1) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def generate_position():
        x = random.randint(0, WIDTH // SIZE - 1) * SIZE
        y = random.randint(0, HEIGHT // SIZE - 1) * SIZE
        return x, y


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("static/block.bmp").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(0)
        self.y.append(0)

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def moving(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= 50
        if self.direction == 'right':
            self.x[0] += 50
        if self.direction == 'up':
            self.y[0] -= 50
        if self.direction == 'down':
            self.y[0] += 50

        self.draw()


class GameSnake:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    @staticmethod
    def is_overlapped(x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    @staticmethod
    def play_sound(sound_type):
        sound = pygame.mixer.Sound(f'static/{sound_type}.mp3')
        pygame.mixer.Sound.play(sound)

    @staticmethod
    def play_background_music():
        pygame.mixer.music.load('static/background_music.mp3')
        pygame.mixer.music.play()

    def play(self):
        self.snake.moving()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Встреча с яблоком
        if self.is_overlapped(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('hit_apple')
            # Установка яблока не в змейку
            ok = True
            while ok:
                x, y = self.apple.generate_position()
                for i in range(0, self.snake.length):
                    if self.is_overlapped(x, y, self.snake.x[i], self.snake.y[i]):
                        ok = False
                if ok:
                    self.apple.move(x, y)
                    ok = False
            self.snake.increase_length()

        # Проверка на пересечение с телом змейки
        for i in range(1, self.snake.length):
            if self.is_overlapped(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('game_over')
                raise 'Game over'

        # Проверка на края поля
        if not (0 <= self.snake.x[0] < WIDTH) or not (0 <= self.snake.y[0] < HEIGHT):
            self.play_sound('game_over')
            raise 'Game over'

    def display_score(self):
        font = pygame.font.SysFont('Courier New', 25)
        score = font.render(f"Points: {self.snake.length}", True, (4, 108, 228))
        self.surface.blit(score, (800, 15))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('Courier New', 30)
        message1 = font.render('Game over!', True, (4, 108, 228))
        score = font.render(f"Your points: {self.snake.length}.", True, (4, 108, 228))
        message2 = font.render('Press Enter to try again, Esc to exit.', True, (4, 108, 228))
        self.surface.blit(message1, (380, 300))
        self.surface.blit(score, (330, 400))
        self.surface.blit(message2, (100, 500))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                time.sleep(0.5)
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == '__main__':
    game = GameSnake()
    game.run()
