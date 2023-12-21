import pygame
import sys
import math

initial_characteristics = [0, 0]


class Ball:
    """Класс задает внешний вид шаров, проверяет столкновение с другими шарами"""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.angular_velocity = initial_characteristics[1]
        self.angular_acceleration = 0
        self.angle = 0

    def hittest(self, obj):
        """Проверяет, столкнулись ли два шара"""
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2) <= (self.radius + obj.radius)**2:
            return True
        else:
            return False


class NewtonsCradle:
    """Класс создает сам объект, рисует и обновляет общую картину, в нем прописано поведение шаров как системы"""
    def __init__(self, num_balls, ball_radius, string_length, beam_height, gravity, width, height):
        self.width = width
        self.height = height
        self.ball_radius = ball_radius
        self.string_length = string_length
        self.beam_height = beam_height
        self.gravity = gravity
        self.balls = [Ball(0, 0, ball_radius, (0, 100, 155)) for _ in range(num_balls)]

        for i, ball in enumerate(self.balls):
            # Первое число задает x первого шарика, последнее число в скобках задает расстояние между шарами
            ball.x = 325 + i * (2 * self.ball_radius + 0)
            ball.y = 100 - self.beam_height + self.string_length
            if i <= 0:
                ball.angle = -initial_characteristics[0]
                # Здесь выставляется начальный угол левого шарика в радианах

        self.initial_positions_string = [(ball.x, ball.y - self.string_length+9) for ball in self.balls]
        self.initial_positions = [(ball.x, ball.y) for ball in self.balls]

    def update(self, elapsed_time):
        """Считается угловое ускорение, обновляется угловая скорость и угол в радианах"""
        for i, ball in enumerate(self.balls):
            # Затухания нет
            ball.angular_acceleration = -math.sin(ball.angle) * self.gravity / self.string_length
            ball.angular_velocity += ball.angular_acceleration * elapsed_time
            ball.angle += ball.angular_velocity * elapsed_time
            ball.x = self.initial_positions_string[i][0] + self.string_length * math.sin(ball.angle)
            ball.y = self.initial_positions_string[i][1] + self.string_length * math.cos(ball.angle)

    def hit(self):
        """Обновляются угловые скорости при столкновении двух соседних,
        включается звук столкновения"""
        for i in range(4):
            ball1 = self.balls[i]
            ball2 = self.balls[i+1]
            if ball1.hittest(ball2) and (ball1.angular_velocity - ball2.angular_velocity >= 0):
                if ball1.angular_velocity - ball2.angular_velocity >= 0.0005:
                    pygame.mixer.music.load("be_metal_plate_surface_15801.mp3")
                    pygame.mixer.music.play(1)
                #Законы сохранения энергии и импульса
                #Вспомогательные переменные:
                v1 = ball1.angular_velocity
                v2 = ball2.angular_velocity
                ball1.angular_velocity = v1 - (v1 - v2) * (math.cos(ball1.angle)) ** 2
                ball2.angular_velocity = v2 - (v2 - v1) * (math.cos(ball2.angle)) ** 2

    def draw(self, screen):
        screen.fill((255, 255, 255))
        ball_image = pygame.image.load("liquid-architecture.jpg").convert_alpha()
        new_ball_image = pygame.transform.scale(ball_image, (50, 50))
        new_ball_image.set_colorkey((255, 255, 255))
        # Нити, соединяющие шары и балку
        for i, ball in enumerate(self.balls):
            line_start = (ball.x, ball.y)
            line_end = (self.initial_positions_string[i][0], self.initial_positions_string[i][1])
            pygame.draw.line(screen, (0, 0, 0), line_start, line_end, 2)

        # Рисуются сами шары
        for ball in self.balls:
            screen.blit(new_ball_image, (ball.x-24, ball.y-19))
            # ball.draw(screen)

        # Рисуется балка
        pygame.draw.rect(screen, (0, 0, 0), (150, 100 - self.beam_height, 500, self.beam_height))


class NewtonsCradleApp:
    """Класс, в котором указаны функции запуска симуляции и
    указываются некоторые характеристики, использующиеся в модели"""
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Newton's Cradle Simulation")
        self.gravity = 0.002
        self.newtons_cradle = NewtonsCradle(num_balls=5, ball_radius=20, string_length=250, beam_height=10,
                                            gravity=self.gravity, width=self.width, height=self.height)
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

            elapsed_time = self.clock.tick(FPS)
            self.newtons_cradle.hit()
            self.newtons_cradle.update(elapsed_time)
            self.newtons_cradle.draw(self.screen)

            pygame.display.flip()

    def interface(self):
        screen = self.screen
        font = pygame.font.Font(None, 32)
        button_font = pygame.font.SysFont('Arial', 28)
        input_box_angle = pygame.Rect(300, 400, 140, 32)
        input_box_velocity = pygame.Rect(330, 300, 140, 32)
        input_box_button = pygame.Rect(325, 100, 160, 100)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color_angle = color_inactive
        color_velocity = color_inactive
        button_text = button_font.render('Start simulation', True, color_inactive)
        #Характерные параметры: угловая скорость 0.001, угол 1 радиан
        active_angle = False
        active_velocity = False
        text_angle = ''
        text_velocity = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Если пользователь нажал на текстовое поле
                    if input_box_angle.collidepoint(event.pos):
                        # Делает поле активным.
                        active_angle = not active_angle
                    else:
                        active_angle = False

                    if input_box_velocity.collidepoint(event.pos):
                        # Аналогично углу
                        active_velocity = not active_velocity
                    else:
                        active_velocity = False

                    # Меняется цвет текстового поля
                    color_angle = color_active if active_angle else color_inactive
                    color_velocity = color_active if active_velocity else color_inactive

                    if input_box_button.collidepoint(event.pos):
                        NewtonsCradleApp().run_simulation()

                if event.type == pygame.KEYDOWN:
                    if active_angle:
                        if event.key == pygame.K_RETURN:
                            initial_characteristics[0] = (float(text_angle))
                            text_angle = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text_angle = text_angle[:-1]
                        else:
                            text_angle += event.unicode
                    if active_velocity:
                        if event.key == pygame.K_RETURN:
                            initial_characteristics[1] = (float(text_velocity))
                            text_velocity = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text_velocity = text_velocity[:-1]
                        else:
                            text_velocity += event.unicode

            screen.fill((30, 30, 30))
            # Рендерится введеный текст
            txt_surface_angle = font.render(text_angle, True, color_angle)
            txt_surface_velocity = font.render(text_velocity, True, color_velocity)
            # Изменяет размер поля ввода, если текст больше
            width = max(200, txt_surface_angle.get_width() + 10)
            input_box_angle.w = width
            # Отрисовка текста
            screen.blit(txt_surface_angle, (input_box_angle.x + 5, input_box_angle.y + 5))
            screen.blit(txt_surface_velocity, (input_box_velocity.x + 5, input_box_velocity.y + 5))
            screen.blit(button_text, input_box_button)
            # Отрисовка полей ввода и кнопки
            pygame.draw.rect(screen, color_angle, input_box_angle, 2)
            pygame.draw.rect(screen, color_velocity, input_box_velocity, 2)
            pygame.draw.rect(screen, color_inactive, input_box_button, 2)

            pygame.display.flip()
            self.clock.tick(FPS)


# Запуск симуляции
FPS = 360
NewtonsCradleApp().interface()
