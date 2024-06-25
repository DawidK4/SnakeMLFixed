import pygame
import sys
import agent
import game

class Button:
    def __init__(self, color, x, y, text='', path=''):
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.width = 150
        self.height = 30
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Scale image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


class ScoreBoard:
    def __init__(self, screen):
        self.scores = []
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 30)
        self.exit_button = Button((0, 255, 0), 700, 50, 'Exit', 'Photos/Buttons/ExitButton.png')
        self.working = True
        self.scroll = 0
        self.image = pygame.image.load('Photos/scoreBoardImage.jpg')
        self.image = pygame.transform.scale(self.image, (800, 800))
        self.load_scores_from_file()  # Load scores from file on initialization

    def load_scores_from_file(self):
        try:
            with open("scores.txt", "r") as file:
                for line in file:
                    if line.startswith("Score: "):
                        score = int(line.split(": ")[1])
                        self.scores.append(score)
        except FileNotFoundError:
            print("scores.txt not found. No scores loaded.")

    def add_score(self, score):
        self.scores.append(score)

    def display(self):
        self.working = True
        self.screen.blit(self.image, (0, 0))
        for i, score in enumerate(self.scores):
            color = (255, 0, 0) if i < 3 else (255, 255, 255)  # Highlight top 3 scores in red
            text = self.font.render(f'Score {i + 1}: {score}', True, color)
            textHS = self.font.render(f'Generation: {len(self.scores)}', True, (255, 255, 255))
            self.screen.blit(textHS, (700, 20))
            self.screen.blit(text, (50, 50 + i * 20 - self.scroll))
        self.exit_button.draw(self.screen)
        pygame.display.flip()
        self.scoreboard()

    def scoreboard(self):
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
        pygame.display.set_caption('Snake AI')
        self.screen = pygame.display.set_mode((800, 800))
        self.working = True
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load('Photos/menuImage.jpg')
        self.image = pygame.transform.scale(self.image, (800, 800))

        button_width = 150
        screen_width = 800

        x_centered = (screen_width - button_width) // 2

        start_button_y = 600
        exit_button_y = 650
        scoreboard_button_y = 700
        snakeml_button_y = 750

        self.start_button = Button((255, 5, 5), x_centered, start_button_y, 'Start', 'Photos/Buttons/StartButton.png')
        self.exit_button = Button((0, 255, 0), x_centered, exit_button_y, 'Exit', 'Photos/Buttons/ExitButton.png')
        self.scoreboard_button = Button((0, 255, 0), x_centered, scoreboard_button_y, 'Score Board',
                                        'Photos/Buttons/ScoreBoardButton.png')
        self.snakeml_button = Button((0, 255, 0), x_centered, snakeml_button_y, 'Snake Ml',
                                     'Photos/Buttons/StartButton.png')
        self.scoreboard = ScoreBoard(self.screen)

    def menu(self):
        while self.working:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.working = False
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
