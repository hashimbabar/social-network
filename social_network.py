import pygame
import numpy as np
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (50, 150, 50)
PURPLE = (130, 0, 130)
GREY = (230, 230, 230)
YELLOW = (190, 175, 50)

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600

# Create a class to represent users in the social network
class User(pygame.sprite.Sprite):
    def __init__(self, x, y, social_network):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.friends = []
        self.status = "Idle"
        self.update_countdown = 0
        self.influence = random.uniform(0.1, 0.9)
        self.opinion = random.uniform(-1, 1)
        self.interests = [random.choice(['Music', 'Sports', 'Movies', 'Books', 'Travel'])]
        self.message_queue = []

    def update(self):
        if self.status == "Idle":
            if random.random() < 0.01:
                self.status = "Updating"
                self.update_countdown = random.randint(30, 120)
                self.opinion += random.uniform(-0.1, 0.1)
                if random.random() < 0.1:
                    self.post_message("I'm feeling great today!")
        elif self.status == "Updating":
            if self.update_countdown <= 0:
                self.status = "Idle"
            else:
                self.update_countdown -= 1
                if random.random() < self.influence * 0.02:
                    for friend in self.friends:
                        friend.opinion += self.influence * random.uniform(-0.05, 0.05)
                        friend.opinion = max(-1, min(1, friend.opinion))
        elif self.status == "Interacting":
            if self.update_countdown <= 0:
                self.status = "Idle"
            else:
                self.update_countdown -= 1
                if random.random() < self.influence * 0.05:
                    for friend in self.friends:
                        friend.opinion += self.influence * random.uniform(-0.1, 0.1)
                        friend.opinion = max(-1, min(1, friend.opinion))

    def make_friend(self, other_user):
        if other_user not in self.friends and len(self.friends) < 5:
            self.friends.append(other_user)
            other_user.friends.append(self)

    def post_message(self, message):
        self.message_queue.append(message)
        if random.random() < self.influence * 0.1:
            for friend in self.friends:
                friend.receive_message(message)

    def receive_message(self, message):
        if random.random() < self.influence * 0.2:
            self.post_message("I agree with your last message!")

# Create a class for the social network simulation
class SocialNetwork:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Social Network Influence Simulation")
        self.all_users = pygame.sprite.Group()

    def create_user(self, x, y):
        user = User(x, y, self)
        self.all_users.add(user)
        return user

    def connect_users(self, user1, user2):
        user1.make_friend(user2)

    def simulate(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.all_users.update()

            self.screen.fill(WHITE)

            for user in self.all_users:
                for friend in user.friends:
                    pygame.draw.line(self.screen, GREY, user.rect.center, friend.rect.center, 2)

                if user.message_queue:
                    message = user.message_queue.pop(0)
                    font = pygame.font.Font(None, 25)
                    text = font.render(message, True, BLACK)
                    text_rect = text.get_rect(center=(user.rect.centerx, user.rect.centery - 25))
                    self.screen.blit(text, text_rect)

            self.all_users.draw(self.screen)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    social_network = SocialNetwork()
    
    # Create users and connect them (example connections)
    users = []
    for _ in range(50):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        user = social_network.create_user(x, y)
        users.append(user)

    for user in users:
        friends = random.sample(users, random.randint(5, 20))
        for friend in friends:
            if friend != user:
                social_network.connect_users(user, friend)

    social_network.simulate()
