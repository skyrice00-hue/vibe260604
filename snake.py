import sys
import random

try:
    import pygame
except Exception:
    print("pygame가 설치되어 있지 않습니다. 설치하려면: pip install pygame")
    raise


CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10


def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos


def draw_rect(screen, color, pos):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = random_food_position(snake)
    score = 0

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        direction = (1, 0)

        if not paused:
            # move snake
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # check wall collision
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
            ):
                break

            # check self collision
            if new_head in snake:
                break

            snake.insert(0, new_head)

            # check food
            if new_head == food:
                score += 1
                food = random_food_position(snake)
            else:
                snake.pop()

        # draw
        screen.fill((10, 10, 10))

        # draw food
        draw_rect(screen, (200, 50, 50), food)

        # draw snake
        for i, segment in enumerate(snake):
            color = (50, 200, 50) if i == 0 else (30, 160, 30)
            draw_rect(screen, color, segment)

        # draw grid optional (light)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (25, 25, 25), (0, y), (WIDTH, y))

        # score
        score_surf = font.render(f"Score: {score}", True, (200, 200, 200))
        screen.blit(score_surf, (10, 10))

        if paused:
            paused_surf = font.render("Paused - press P to resume", True, (200, 200, 200))
            screen.blit(paused_surf, (WIDTH // 2 - paused_surf.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

    # game over screen
    game_over_font = pygame.font.SysFont(None, 72)
    go_surf = game_over_font.render("Game Over", True, (240, 60, 60))
    info_surf = font.render("R: Restart  Q or ESC: Quit", True, (200, 200, 200))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, HEIGHT // 3))
        screen.blit(info_surf, (WIDTH // 2 - info_surf.get_width() // 2, HEIGHT // 2))
        score_final = font.render(f"Final Score: {score}", True, (200, 200, 200))
        screen.blit(score_final, (WIDTH // 2 - score_final.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main()


if __name__ == "__main__":
    main()
