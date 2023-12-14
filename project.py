import pygame
import sys

class Ball:
    """Класс задает внешний вид и поведение шаров: расчитывет их энергию и обновляет положение"""
    def __init__(self, index, num_balls, radius, color, string_length):
        self.index = index
        self.num_balls = num_balls
        self.radius = radius
        self.color = color
        self.string_length = string_length
        self.angle = 0
        self.angular_velocity = 0
        self.gravity = 0.005
        self.terminal_velocity = 5.0
        self.x = 0

    def update(self):
        self.angular_velocity += self.gravity * pygame.time.get_ticks() / 1000.0
        self.angle += self.angular_velocity

        angle_offset = 2 * pygame.math.Vector2(0, 1).rotate(self.angle).as_polar()[1] * self.index / self.num_balls
        y_offset = self.string_length * pygame.math.Vector2(0, 1).rotate(self.angle + angle_offset).y
        x_center = self.string_length // 2
        self.x = x_center + y_offset

        if abs(self.angular_velocity) > self.terminal_velocity:
            self.angular_velocity = self.terminal_velocity * (self.angular_velocity / abs(self.angular_velocity))

    def kinetic_energy(self):
        return 0.5 * self.angular_velocity**2

    def total_energy(self):
        return self.kinetic_energy()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.string_length)), self.radius)

class NewtonsCradle:
    """Класс объединяет шары в как бы один объект, проверяет коллизию объектов"""
    def __init__(self, num_balls, ball_radius, string_length, width, height):
        self.width = width
        self.height = height
        self.ball_radius = ball_radius
        self.string_length = string_length
        self.balls = [
            Ball(i, num_balls, ball_radius, (0, 0, 255), self.string_length)
            for i in range(num_balls)
        ]

    def update(self):
        for i in range(len(self.balls)):
            self.balls[i].update()
            self.check_collision(i)

    def check_collision(self, current_index):
        for i in range(current_index + 1, len(self.balls)):
            ball1 = self.balls[current_index]
            ball2 = self.balls[i]

            distance = abs(ball1.x - ball2.x)
            if distance < (ball1.radius + ball2.radius):
                ball1.angular_velocity, ball2.angular_velocity = ball2.angular_velocity, ball1.angular_velocity

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for ball in self.balls:
            ball.draw(screen)

class NewtonsCradleApp:
    """Класс, в котором указаны функции запуска симуляции и указываются некоторые характеристики, которые используются в модели"""
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Newton's Cradle Simulation")

        self.newtons_cradle = NewtonsCradle(num_balls=5, ball_radius=20, string_length=150, width=self.width, height=self.height)
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

            self.newtons_cradle.update()
            self.newtons_cradle.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = NewtonsCradleApp()
    app.run_simulation()
