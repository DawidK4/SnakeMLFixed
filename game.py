import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
DEFAULT_SPEED = 10
AI_SPEED = 40


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        self.background = pygame.image.load('Photos/tile.png')
        self.background = pygame.transform.scale(self.background, (self.w, self.h))
        self.apple = pygame.image.load('Photos/apple.png')
        self.apple = pygame.transform.scale(self.apple, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_head_right = pygame.image.load('Photos/Snake_Head/Head_Right.png')
        self.snake_head_left = pygame.image.load('Photos/Snake_Head/Head_Left.png')
        self.snake_head_up = pygame.image.load('Photos/Snake_Head/Head_Up.png')
        self.snake_head_down = pygame.image.load('Photos/Snake_Head/Head_Down.png')
        self.snake_head_right = pygame.transform.scale(self.snake_head_right, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_head_left = pygame.transform.scale(self.snake_head_left, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_head_up = pygame.transform.scale(self.snake_head_up, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_head_down = pygame.transform.scale(self.snake_head_down, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_body_vertical = pygame.image.load('Photos/Snake_Body/Body_Vertical.png')
        self.snake_body_horizontal = pygame.image.load('Photos/Snake_Body/Body_Horizontal.png')
        self.snake_body_vertical = pygame.transform.scale(self.snake_body_vertical, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_body_horizontal = pygame.transform.scale(self.snake_body_horizontal, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_tail_right = pygame.image.load('Photos/Snake_Tail/Tail_Right.png')
        self.snake_tail_left = pygame.image.load('Photos/Snake_Tail/Tail_Left.png')
        self.snake_tail_up = pygame.image.load('Photos/Snake_Tail/Tail_Up.png')
        self.snake_tail_down = pygame.image.load('Photos/Snake_Tail/Tail_Down.png')
        self.snake_tail_right = pygame.transform.scale(self.snake_tail_right, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_tail_left = pygame.transform.scale(self.snake_tail_left, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_tail_up = pygame.transform.scale(self.snake_tail_up, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_tail_down = pygame.transform.scale(self.snake_tail_down, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_body_bend_rd = pygame.image.load('Photos/Snake_Bend/Right_Down.png')
        self.snake_body_bend_ld = pygame.image.load('Photos/Snake_Bend/Left_Down.png')
        self.snake_body_bend_ru = pygame.image.load('Photos/Snake_Bend/Right_Up.png')
        self.snake_body_bend_lu = pygame.image.load('Photos/Snake_Bend/Left_Up.png')
        self.snake_body_bend_rd = pygame.transform.scale(self.snake_body_bend_rd, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_body_bend_ld = pygame.transform.scale(self.snake_body_bend_ld, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_body_bend_ru = pygame.transform.scale(self.snake_body_bend_ru, (BLOCK_SIZE, BLOCK_SIZE))
        self.snake_body_bend_lu = pygame.transform.scale(self.snake_body_bend_lu, (BLOCK_SIZE, BLOCK_SIZE))

    def reset(self):
        """
        This method simply resets the position of the snake in case of losing the game.
        """
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.speed = DEFAULT_SPEED

    def _place_food(self):
        """
        This method spawns an apple in a random place.
        """
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action=None, controlled_by_player=False):
        """
        Execute one step of the game.

        This method updates the game state by processing user input, moving the snake,
        checking for collisions, placing new food, updating the UI, and managing the game speed.
        It can operate in two modes: controlled by a player or an AI.

        Args:
            action (list or None): The action to be taken by the AI, typically a list of
            [turn_left, go_straight, turn_right].
                                   Ignored if controlled_by_player is True.
            controlled_by_player (bool): If True, the game is controlled by the player using keyboard input.
                                         If False, the game is controlled by the AI using the action parameter.

        Returns:
            tuple:
                reward (int): The reward obtained from this step. Positive if food is eaten, negative
                if collision occurs.
                game_over (bool): True if the game has ended, False otherwise.
                score (int): The current score of the game.

        Raises:
            pygame.error: If there is an issue with the Pygame library (e.g., during event handling).

        Examples:
            -reward, game_over, score = game.play_step([1, 0, 0], False)
            -reward, game_over, score = game.play_step(controlled_by_player=True)
        """
        self.frame_iteration += 1

        self.speed = DEFAULT_SPEED if controlled_by_player else AI_SPEED

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if controlled_by_player and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.speed += 10
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.speed -= 10

        # 2. move
        if not controlled_by_player:
            self._move(action)
        else:
            self._move([1, 0, 0])

        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.speed)

        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        """
        Check if a point collides with the boundaries of the game area or the snake itself.

        This method determines whether the given point (or the snake's head by default)
        collides with the boundaries of the game area or intersects with any part of the snake's body.

        Args:
            pt (Point, optional): The point to check for collision. If None, the method uses the snake's head.

        Returns:
            bool: True if the point collides with the boundary or the snake's body, False otherwise.

        Examples:
            -is_collision(Point(5, 5))
            False
            -is_collision()
            True if the snake's head is out of bounds or hits itself, False otherwise.
        """
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        """
        Update the game's user interface.

        This method renders the game's background, the snake with its head, body, and tail
        oriented correctly based on its current direction, the food, and the current score.
        It then updates the display to reflect these changes.

        Raises:
            pygame.error: If there is an issue with rendering using the Pygame library.

        """
        self.display.blit(self.background, (0, 0))

        for index, pt in enumerate(self.snake):
            if index == 0:  # render the snake's head
                if self.direction == Direction.RIGHT:
                    self.display.blit(self.snake_head_right, (pt.x, pt.y))
                elif self.direction == Direction.LEFT:
                    self.display.blit(self.snake_head_left, (pt.x, pt.y))
                elif self.direction == Direction.UP:
                    self.display.blit(self.snake_head_up, (pt.x, pt.y))
                elif self.direction == Direction.DOWN:
                    self.display.blit(self.snake_head_down, (pt.x, pt.y))
            else:  # render the snake's body and tail
                if index < len(self.snake) - 1:  # if not the tail
                    next_pt = self.snake[index + 1]
                    prev_pt = self.snake[index - 1]

                    if prev_pt.x < pt.x and next_pt.y > pt.y:  # bend right down
                        self.display.blit(self.snake_body_bend_rd, (pt.x, pt.y))
                    elif prev_pt.x > pt.x and next_pt.y > pt.y:  # bend left down
                        self.display.blit(self.snake_body_bend_lu, (pt.x, pt.y))
                    elif prev_pt.x < pt.x and next_pt.y < pt.y:  # bend right up
                        self.display.blit(self.snake_body_bend_rd, (pt.x, pt.y))
                    elif prev_pt.x > pt.x and next_pt.y < pt.y:  # bend left up
                        self.display.blit(self.snake_body_bend_ld, (pt.x, pt.y))
                    elif prev_pt.y < pt.y and next_pt.x > pt.x:  # bend down right
                        self.display.blit(self.snake_body_bend_ru, (pt.x, pt.y))
                    elif pt.x == next_pt.x:  # vertical
                        self.display.blit(self.snake_body_vertical, (pt.x, pt.y))
                    else:  # horizontal
                        self.display.blit(self.snake_body_horizontal, (pt.x, pt.y))
                else:
                    next_pt = self.snake[index - 1]
                    if pt.x > next_pt.x:
                        self.display.blit(self.snake_tail_right, (pt.x, pt.y))
                    elif pt.x < next_pt.x:
                        self.display.blit(self.snake_tail_left, (pt.x, pt.y))
                    elif pt.y > next_pt.y:
                        self.display.blit(self.snake_tail_down, (pt.x, pt.y))
                    elif pt.y < next_pt.y:
                        self.display.blit(self.snake_tail_up, (pt.x, pt.y))

        self.display.blit(self.apple, (self.food.x, self.food.y))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d
        self.direction = new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)


def save_score(score):
    """
    Save the score to a file.

    This method appends the given score to a file named "scores.txt".

    Args:
        score (int): The score to be saved.
    """
    with open("scores.txt", "a") as file:
        file.write(f"Score: {score}\n")


def display_prompt(screen, width, height, score):
    """
    Display the game over prompt and handle user input.

    This method fills the screen with a game over message and instructions for the player
    to either play again or quit. It waits for the player's input and returns a boolean
    indicating whether the player chose to play again.

    Args:
        screen (pygame.Surface): The Pygame screen surface to display the prompt.
        width (int): The width of the screen.
        height (int): The height of the screen.
        score (int): The player's score to be displayed.

    Returns:
        bool: True if the player chooses to play again, False if the player chooses to quit.

    Raises:
        pygame.error: If there is an issue with rendering or handling events using the Pygame library.
    """
    screen.fill(BLACK)
    text1 = font.render(f"Game Over! Your Score: {score}", True, WHITE)
    text2 = font.render("Press Y to Play Again or N to Quit", True, WHITE)
    screen.blit(text1, [width // 2 - 150, height // 2 - 50])
    screen.blit(text2, [width // 2 - 150, height // 2])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False


def play_game():
    """
    Start and run the main game loop.

    This method initializes the game, runs the main game loop, and handles game over conditions.
    It saves the player's score and displays a prompt for the player to either play again or quit.
    The game is controlled by the player.

    Raises:
        pygame.error: If there is an issue with the Pygame library during game execution.
    """
    game = SnakeGameAI()
    controlled_by_player = True
    while True:
        reward, game_over, score = game.play_step(controlled_by_player=controlled_by_player)
        if game_over:
            save_score(score)
            if display_prompt(game.display, game.w, game.h, score):
                game.reset()
            else:
                pygame.quit()
                quit()


if __name__ == "__main__":
    play_game()
