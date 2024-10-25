import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20  # размер одного сегмента змейки

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Настройка экрана и часов
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Шрифт для отображения текста
font = pygame.font.SysFont("Arial", 24)

# Функция для отрисовки текста
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Функция для генерации случайной позиции для пищи
def get_random_food_position():
    x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return x, y

# Основная функция игры
def game():
    # Начальные параметры змейки
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = 'RIGHT'
    score = 0
    high_score = 0  # Рекордный счет
    speed = 5  # Начальная скорость

    # Лист для позиций пищи и таймер обновления пищи
    food_positions = [get_random_food_position()]
    food_timer = 0  # таймер для обновления пищи

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # Обновление позиции змейки
        head_x, head_y = snake[0]
        if direction == 'UP':
            head_y -= BLOCK_SIZE
        elif direction == 'DOWN':
            head_y += BLOCK_SIZE
        elif direction == 'LEFT':
            head_x -= BLOCK_SIZE
        elif direction == 'RIGHT':
            head_x += BLOCK_SIZE
        new_head = (head_x, head_y)

        # Проверка столкновений со стенами или с собой
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in snake:
            # Вывод сообщения и сброс игры
            if score > high_score:
                high_score = score  # обновляем рекордный счет
            draw_text("Игра окончена. Нажмите любую клавишу для рестарта.", RED, WIDTH // 2 - 200, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(2000)  # задержка перед рестартом
            score = 0
            speed = 5
            snake = [(100, 100), (80, 100), (60, 100)]
            direction = 'RIGHT'
            food_positions = [get_random_food_position()]
            food_timer = 0
            continue

        # Добавление новой головы змейки
        snake.insert(0, new_head)

        # Проверка на поедание пищи
        if new_head in food_positions:
            score += 1
            food_positions.remove(new_head)  # удаляем съеденную еду
            new_food_position = get_random_food_position()
            while new_food_position in snake:
                new_food_position = get_random_food_position()
            food_positions.append(new_food_position) # добавляем новую еду
            food_timer = 0
            # Увеличение скорости каждые 10 очков
            if score % 10 == 0:
                speed += 1
        else:
            snake.pop()  # удаляем последний сегмент, если пища не съедена

        # Обновление позиции пищи по таймеру
        food_timer += 1
        if food_timer > 25:  # каждые 25 кадров обновляем пищу
            food_positions.append(get_random_food_position())
            if len(food_positions) > 5:  # если еды больше 5, удаляем самую старую
                food_positions.pop(0)
            food_timer = 0

        # Отрисовка экрана
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))
        for food in food_positions:
            pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))

        # Отображение счета и рекорда
        draw_text(f"Счет: {score}", WHITE, 10, 10)
        draw_text(f"Рекорд: {high_score}", WHITE, 10, 40)

        # Обновление экрана и контроль FPS
        pygame.display.flip()
        clock.tick(speed)  # динамическая скорость

# Запуск игры
game()
