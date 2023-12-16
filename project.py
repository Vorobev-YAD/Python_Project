import pygame
import sys
import math

class Ball:
    """Класс задает внешний вид и поведение шаров, обновляет положение"""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self, gravity, elapsed_time):
        # Update velocity and position based on gravity
        self.velocity_y += gravity * elapsed_time
        self.y += self.velocity_y * elapsed_time

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class NewtonsCradle:
    """Класс создает сам объект, обновляет общую картину, в нем прописано поведение как шаров как системы"""
    def __init__(self, num_balls, ball_radius, string_length, beam_height, gravity, width, height):
        self.width = width
        self.height = height
        self.ball_radius = ball_radius
        self.string_length = string_length
        self.beam_height = beam_height
        self.gravity = gravity
        self.balls = [Ball(0, 0, ball_radius, (0, 0, 255)) for _ in range(num_balls)]
        self.initial_positions = [(ball.x, ball.y) for ball in self.balls]

        for i, ball in enumerate(self.balls):
            # Первое число задает x первого шарика, последнее число в скобках задает расстояние между шарами
            ball.x = 300 + i * (2 * self.ball_radius + 10)
            ball.y = 100 - self.beam_height + self.string_length

    def update(self, elapsed_time):

        #По идее как-то так, но я не знаю как это правильно записать
        for ball, initial_position in zip(self.balls, self.initial_positions):
            ball.x += ball.velocity_x
            ball.y += ball.velocity_y
            angle = math.atan((ball.x - self.initial_positions[0])/(ball.y - self.initial_positions[1] + self.string_length))
            ball.velocity_x -= (((ball.velocity_x)**2+(ball.velocity_y)**2)/self.string_length + self.gravity*math.cos(angle))*math.sin(angle)
            ball.velocity_y += self.gravity*(1-math.cos(angle)) - ((ball.velocity_x)**2+(ball.velocity_y)**2)/self.string_length

        for ball in self.balls:
            ball.update(self.gravity, elapsed_time)
        # Симуляция натяжения в нитях, пока недоделано, неправильно работает
        for ball, initial_position in zip(self.balls, self.initial_positions):
            distance = math.sqrt(
                (ball.x - self.width // 2) ** 2 + (ball.y - (self.height // 2 - self.beam_height // 2)) ** 2)

            scale_factor = self.string_length / distance
            ball.x = self.width // 2 + (ball.x - self.width // 2) * scale_factor
            ball.y = (self.height // 2 - self.beam_height // 2) + (
                        ball.y - (self.height // 2 - self.beam_height // 2)) * scale_factor

    def draw(self, screen):
        screen.fill((255, 255, 255))

        # Нити, соединяющте шары и балку
        for i, ball in enumerate(self.balls):
            line_start = (ball.x, ball.y)
            line_end = (ball.x, 100 - self.beam_height  )
            pygame.draw.line(screen, (0, 0, 0), line_start, line_end, 2)

        # Рисуются сами шары
        for ball in self.balls:
            ball.draw(screen)

        # Рисуется балка
        pygame.draw.rect(screen, (0, 0, 0), (150, 100 - self.beam_height, 500, self.beam_height))


class NewtonsCradleApp:
    """Класс, в котором указаны функции запуска симуляции и указываются некоторые характеристики, которые используются в модели"""
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Newton's Cradle Simulation")

        self.gravity = 100
        self.newtons_cradle = NewtonsCradle(num_balls=5, ball_radius=20, string_length=250, beam_height=10, gravity=self.gravity, width=self.width, height=self.height)
        self.clock = pygame.time.Clock()

        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run_simulation(self):
        self.running = True
        while self.running:
            self.handle_events()

            elapsed_time = self.clock.tick(60)

            self.newtons_cradle.update(elapsed_time)
            self.newtons_cradle.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = NewtonsCradleApp()
    app.run_simulation()
