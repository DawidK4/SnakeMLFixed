import os
import pygame
import sys
import agent
import game

class Button:
    def __init__(self, color, x, y, text='', path=''):
        """
        Initialize a Button object.

        Args:
            color (tuple): RGB color tuple for the button.
            x (int): The x-coordinate of the button's top-left corner.
            y (int): The y-coordinate of the button's top-left corner.
            text (str, optional): The text displayed on the button.
            path (str, optional): The file path to the button's image.

        """
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.width = 200
        self.height = 50
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        """
        Draw the button on the screen.

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw the button on.

        """
        screen.blit(self.image, (self.x, self.y))

    def is_over(self, pos):
        """
        Check if a given position is over the button.

        Args:
            pos (tuple): A tuple containing the x and y coordinates of the position to check.

        Returns:
            bool: True if the position is over the button, False otherwise.

        """
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


class ScoreBoard:
    def __init__(self, screen):
        """
        Initialize a ScoreBoard object.

        Args:
            screen (pygame.Surface): The Pygame screen surface to display the scoreboard on.

        """
        self.scores = []
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 30)
        self.exit_button = Button((0, 255, 0), 800, 50, 'Exit', 'Photos/Buttons/ExitButton.png')
        self.working = True
        self.scroll = 0
        self.image = pygame.image.load('Photos/scoreBoardImage.jpg')
        self.image = pygame.transform.scale(self.image, (1024, 1024))
        self.load_scores_from_file()

    def load_scores_from_file(self):
        """
        Load scores from the scores.txt file.

        This method reads scores from a file named "scores.txt" and appends them to the scores list.
        If the file is not found, it prints an error message.

        """
        try:
            with open("scores.txt", "r") as file:
                for line in file:
                    if line.startswith("Score: "):
                        score = int(line.split(": ")[1])
                        self.scores.append(score)
        except FileNotFoundError:
            print("scores.txt not found. No scores loaded.")

    def add_score(self, score):
        """
        Add a new score to the scoreboard.

        Args:
            score (int): The score to add to the scoreboard.

        """
        self.scores.append(score)

    def display(self):
        """
        Display the scoreboard.

        This method renders the scoreboard background, scores, and the exit button on the screen.
        It then calls the scoreboard method to handle events.

        """
        self.working = True
        self.screen.blit(self.image, (0, 0))
        for i, score in enumerate(self.scores):
            color = (255, 0, 0) if i < 3 else (255, 255, 255)  # Highlight top 3 scores in red
            text = self.font.render(f'Score {i + 1}: {score}', True, color)
            textHS = self.font.render(f'Generation: {len(self.scores)}', True, (255, 255, 255))
            self.screen.blit(textHS, (800, 20))
            self.screen.blit(text, (50, 50 + i * 20 - self.scroll))
        self.exit_button.draw(self.screen)
        pygame.display.flip()
        self.scoreboard()

    def scoreboard(self):
        """
        Handle the scoreboard's event loop.

        This method processes events such as quitting the game, clicking the exit button,
        and scrolling through the scores. It updates the display accordingly.

        """
        while self.working:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.working = False
                    Menu().display()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.is_over(pos):
                        print('clicked the exit button')
                        self.working = False
                        Menu().display()
                if event.type == pygame.MOUSEWHEEL:
                    self.scroll += event.y * 20
                    self.display()
            pygame.display.update()


class Menu:
    def __init__(self):
        """
        Initialize a Menu object.

        This method sets up the Pygame display, buttons, and other attributes required for the menu.

        """
        pygame.display.set_caption('Snake AI')
        self.screen = pygame.display.set_mode((1024, 1024))
        self.working = True
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load('Photos/menuImage.jpg')
        self.image = pygame.transform.scale(self.image, (1024, 1024))

        button_width = 200
        screen_width = 1024

        x_centered = (screen_width - button_width) // 2
        y_main = 950

        self.start_button = Button((255, 5, 5), x_centered-400, y_main, 'Start', 'Photos/Buttons/StartButton.png')
        self.exit_button = Button((0, 255, 0), x_centered+400, y_main, 'Exit', 'Photos/Buttons/ExitButton.png')
        self.scoreboard_button = Button((0, 255, 0), x_centered+150, y_main, 'Score Board',
                                        'Photos/Buttons/ScoreBoardButton.png')
        self.snakeml_button = Button((0, 255, 0), x_centered-150, y_main, 'Snake Ml',
                                     'Photos/Buttons/AIButton.png')
        self.scoreboard = ScoreBoard(self.screen)

    def menu(self):
        """
        Display the menu and handle user interactions.

        This method runs the main menu loop, processing events such as button clicks to start the game,
        display the scoreboard, or exit the application.

        Returns:
            bool: False if the menu loop exits, indicating that the application should terminate.

        """
        while self.working:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.working = False
                    try:
                        pygame.quit()
                        sys.exit()
                    except SystemExit:
                        pygame.quit()
                        os._exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_over(pos):
                        game.play_game()
                    if self.exit_button.is_over(pos):
                        print('clicked the exit button')
                        pygame.quit()
                        sys.exit()
                    if self.scoreboard_button.is_over(pos):
                        self.scoreboard.add_score(100)
                        self.scoreboard.add_score(200)
                        self.scoreboard.add_score(300)
                        print('clicked the scoreboard button')
                        self.scoreboard.display()
                    if self.snakeml_button.is_over(pos):
                        print('clicked the snakeml button')
                        self.working = False  # Stop the menu loop
                        agent.train()  # Start the agent training
                        return False  # Exit the menu method

            self.display()
            pygame.display.update()
        return False

    def display(self):
        """
        Render the menu screen.

        This method draws the background image and all buttons on the screen, and updates the display.

        """
        self.screen.blit(self.image, (0, 0))
        self.start_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        self.snakeml_button.draw(self.screen)
        self.scoreboard_button.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    menu = Menu()
    while True:
        if menu.menu():
            break
