import pygame
import random
import os

# Define the SnakeGame class to encapsulate the game logic
class SnakeGame:
    # Initialize the game
    def __init__(self):
        pygame.init()
        # pygame.mixer.init()  # Initialize the mixer

        pygame.display.set_caption("Jogo da Cobrinha em Python")

        # Set screen dimensions
        self.largura, self.altura = 1000, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.relogio = pygame.time.Clock()

        # Define colors
        self.preta = (0, 0, 0)
        self.branca = (255, 255, 255)
        self.verde = (0, 255, 0)
        self.vermelha = (255, 0, 0)
        self.azul = (0, 0, 255)

        # Game parameters
        self.tamanho_quadrado = 10
        self.velocidade_jogo = 15

        # Fonts for text display
        self.fonte_pontuacao = pygame.font.SysFont("arial", 25)
        self.fonte_gameover = pygame.font.SysFont("arial", 50)
        self.fonte_instrucoes = pygame.font.SysFont("arial", 25)

        # Initialize game state variables
        self.x = self.largura / 2
        self.y = self.altura / 2
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.tamanho_cobrinha = 1
        self.pixel = []
        self.comida_x, self.comida_y = self.gerar_comida()
        self.pontuacao = 0
        self.perdeu = False
        self.pausado = False


    # Generate random position for food
    def gerar_comida(self):
        comida_x = round(random.randrange(0, self.largura - self.tamanho_quadrado) / 10.0) * 10.0
        comida_y = round(random.randrange(0, self.altura - self.tamanho_quadrado) / 10.0) * 10.0
        return comida_x, comida_y

    # Draw the food on the screen
    def desenhar_comida(self, tamanho, comida_x, comida_y):
        pygame.draw.rect(self.tela, self.verde, [comida_x, comida_y, tamanho, tamanho])

    # Draw the snake on the screen
    def desenhar_cobrinha(self, tamanho, pixel):
        for pix in pixel:
            pygame.draw.rect(self.tela, self.branca, [pix[0], pix[1], tamanho, tamanho])

    # Draw the score on the screen
    def desenhar_pontuacao(self, pontuacao):
        texto = self.fonte_pontuacao.render(f"Pontuação: {pontuacao}", True, self.azul)
        self.tela.blit(texto, [1, 1])

    # Display a message on the screen (e.g., Game Over, Paused)
    def exibir_mensagem(self, msg, cor):
        texto = self.fonte_gameover.render(msg, True, cor)
        self.tela.blit(texto, [self.largura / 6, self.altura / 3])

    # Display game over message with restart/quit instructions
    def exibir_game_over(self):
        mensagem_game_over = self.fonte_gameover.render("Game Over!", True, self.vermelha)
        mensagem_instrucoes = self.fonte_instrucoes.render("Pressione C para jogar novamente ou Q para sair", True, self.vermelha)

        # Calculate centered positions
        game_over_rect = mensagem_game_over.get_rect(center=(self.largura / 2, self.altura / 3))
        instrucoes_rect = mensagem_instrucoes.get_rect(center=(self.largura / 2, self.altura / 3 + 50)) # Adjust vertical spacing

        self.tela.blit(mensagem_game_over, game_over_rect)
        self.tela.blit(mensagem_instrucoes, instrucoes_rect)


    # Handle user input events
    def handle_events(self):
        for evento in pygame.event.get():
            # Quit event
            if evento.type == pygame.QUIT:
                return True
            # Key press events
            if evento.type == pygame.KEYDOWN:
                # Handle game over state input
                if self.perdeu:
                    if evento.key == pygame.K_c:
                        self.__init__() # Reset game state by re-initializing
                        self.rodar_jogo() # Start a new game loop after resetting
                        return True # Exit the current game over loop
                    if evento.key == pygame.K_q:
                        return True
                # Handle game play input
                else:
                    if evento.key == pygame.K_LEFT:
                        self.velocidade_x = -self.tamanho_quadrado
                        self.velocidade_y = 0
                    elif evento.key == pygame.K_RIGHT:
                        self.velocidade_x = self.tamanho_quadrado
                        self.velocidade_y = 0
                    elif evento.key == pygame.K_UP:
                        self.velocidade_y = -self.tamanho_quadrado
                        self.velocidade_x = 0
                    elif evento.key == pygame.K_DOWN:
                        self.velocidade_y = self.tamanho_quadrado
                        self.velocidade_x = 0
                    # Toggle pause state
                    elif evento.key == pygame.K_p:
                        self.pausado = not self.pausado
        return False

    # Update game state (snake position, collisions, food eating)
    def update_game_state(self):
        # Do not update if paused or game over
        if self.pausado or self.perdeu:
            return

        # Update snake position
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        # Check for collision with walls
        if self.x < 0 or self.x >= self.largura or self.y < 0 or self.y >= self.altura:
            self.perdeu = True
            # if self.game_over_sound:
            #     self.game_over_sound.play()


        # Update snake body pixels
        self.pixel.append([self.x, self.y])
        if len(self.pixel) > self.tamanho_cobrinha:
            del self.pixel[0]

        # Check for collision with itself
        for cada_pixel in self.pixel[:-1]:
            if cada_pixel == [self.x, self.y]:
                self.perdeu = True
                # if self.game_over_sound:
                #     self.game_over_sound.play()

        # Check for collision with food
        if self.x == self.comida_x and self.y == self.comida_y:
            self.comida_x, self.comida_y = self.gerar_comida()
            self.tamanho_cobrinha += 1
            self.pontuacao += 1
            # if self.eat_sound:
            #     self.eat_sound.play()

    # Draw all game elements on the screen
    def draw_game_elements(self):
        self.tela.fill(self.preta)
        self.desenhar_cobrinha(self.tamanho_quadrado, self.pixel)
        self.desenhar_comida(self.tamanho_quadrado, self.comida_x, self.comida_y)
        self.desenhar_pontuacao(self.pontuacao)

        # Display pause message
        if self.pausado:
             self.exibir_mensagem("Pausado", self.azul)

        # Display game over message
        if self.perdeu:
            self.exibir_game_over()

        # Update the full display Surface to the screen
        pygame.display.update()


    # Main game loop
    def rodar_jogo(self):
        fim_jogo = False
        while not fim_jogo:
            # Handle events, update game state, and draw elements
            fim_jogo = self.handle_events()
            self.update_game_state()
            self.draw_game_elements()
            # Control game speed
            self.relogio.tick(self.velocidade_jogo)

# Create a game instance and run the game
game = SnakeGame()
game.rodar_jogo()