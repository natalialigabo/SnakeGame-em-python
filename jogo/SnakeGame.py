import pygame
import random
import os 
import time

# Define the SnakeGame class to encapsulate the game logic
class SnakeGame:
    
    # Initialize the game
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Jogo da Cobrinha em Python")

        # Set screen dimensions
        self.largura, self.altura = 1000, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.relogio = pygame.time.Clock()

        # Cores Fixas
        self.preta = (0, 0, 0)
        self.branca = (255, 255, 255)
        self.vermelha = (255, 0, 0)
        self.azul = (0, 0, 255)
        self.cinza_obstaculo = (150, 150, 150) # Cor para os obstáculos
        
        # Cores para Power-ups (Novas Cores)
        self.amarelo_power = (255, 255, 0)
        self.ciano_power = (0, 255, 255)
        
        # Game parameters
        self.tamanho_quadrado = 10
        
        # --- Estrutura de Fases com OBSTÁCULOS ---
        self.fases = [
            # Fase 1: Sem Obstáculos
            {'pontos_necessarios': 0, 'velocidade': 15, 'cor_fundo': (0, 0, 0), 'cor_cobrinha': (0, 255, 0), 'cor_comida': (255, 255, 0), 'obstaculos': []},       
            
            # Fase 2: Parede Central Vertical
            {'pontos_necessarios': 5, 'velocidade': 20, 'cor_fundo': (50, 50, 50), 'cor_cobrinha': (0, 200, 255), 'cor_comida': (255, 0, 100), 
             'obstaculos': self.gerar_obstaculo_vertical(x=500, y_inicio=100, altura=600)},   
             
            # Fase 3: Obstáculos de Canto
            {'pontos_necessarios': 10, 'velocidade': 25, 'cor_fundo': (20, 0, 0), 'cor_cobrinha': (255, 150, 0), 'cor_comida': (0, 255, 100), 
             'obstaculos': self.gerar_obstaculo_quadrado(x_canto=100, y_canto=100, tamanho_lado=5) +
                           self.gerar_obstaculo_quadrado(x_canto=850, y_canto=650, tamanho_lado=5)},   
                           
            # Fase 4: Borda Interna (Túnel)
            {'pontos_necessarios': 15, 'velocidade': 30, 'cor_fundo': (0, 0, 0), 'cor_cobrinha': (255, 255, 255), 'cor_comida': (255, 0, 0),     
             'obstaculos': self.gerar_obstaculo_borda(margem=100, abertura_x=500, abertura_y=400)},
        ]
        
        self.fase_atual_indice = 0 
        self.velocidade_jogo = self.fases[self.fase_atual_indice]['velocidade']

        # --- Variáveis do Power-up ---
        self.power_up_ativo = False
        self.tipo_power_up = None 
        self.power_up_tempo_fim = 0 
        self.tempo_duracao_power_up = 5000 # 5 segundos em milissegundos
        self.velocidade_original = self.velocidade_jogo 
        self.power_up_x, self.power_up_y = None, None 
        self.chance_spawn_power_up = 3 # Chance de 1 em 3 de spawnar um power-up


        # Fonts for text display
        self.fonte_pontuacao = pygame.font.SysFont("arial", 25)
        self.fonte_gameover = pygame.font.SysFont("arial", 50)
        self.fonte_instrucoes = pygame.font.SysFont("arial", 25)
        self.fonte_fase = pygame.font.SysFont("arial", 25)

        # Initialize game state variables
        self.x = self.largura // 2
        self.y = self.altura // 2
        self.velocidade_x = self.tamanho_quadrado
        self.velocidade_y = 0
        self.tamanho_cobrinha = 1
        self.pixel = []
        self.pontuacao = 0
        self.perdeu = False
        self.pausado = False
        self.recorde_salvo = False 

        # Sistema de Recorde
        self.arquivo_recorde = "recorde.txt"
        self.recorde = self._carregar_recorde() 
        
        # Inicializa a comida 
        self.comida_x, self.comida_y = self.gerar_comida()


    # --- Funções Auxiliares para Geração de Obstáculos ---

    def gerar_obstaculo_vertical(self, x, y_inicio, altura):
        obstaculos = []
        x = (x // self.tamanho_quadrado) * self.tamanho_quadrado
        for y in range(y_inicio, y_inicio + altura, self.tamanho_quadrado):
            obstaculos.append([x, y])
        return obstaculos

    def gerar_obstaculo_quadrado(self, x_canto, y_canto, tamanho_lado):
        obstaculos = []
        x_canto = (x_canto // self.tamanho_quadrado) * self.tamanho_quadrado
        y_canto = (y_canto // self.tamanho_quadrado) * self.tamanho_quadrado
        
        for i in range(tamanho_lado):
            for j in range(tamanho_lado):
                obstaculos.append([x_canto + i * self.tamanho_quadrado, y_canto + j * self.tamanho_quadrado])
        return obstaculos

    def gerar_obstaculo_borda(self, margem, abertura_x, abertura_y):
        obstaculos = []
        t = self.tamanho_quadrado
        
        x_min, x_max = margem, self.largura - margem
        y_min, y_max = margem, self.altura - margem
        
        for x in range(x_min, x_max + t, t):
            if abs(x - abertura_x) > 5 * t: 
                 obstaculos.append([x, y_min])
            if abs(x - abertura_x) > 5 * t:
                obstaculos.append([x, y_max - t])
                
        for y in range(y_min, y_max + t, t):
            if abs(y - abertura_y) > 5 * t: 
                obstaculos.append([x_min, y])
            if abs(y - abertura_y) > 5 * t:
                obstaculos.append([x_max - t, y])

        return obstaculos


    # --- Funções de I/O do Recorde ---

    def _carregar_recorde(self):
        try:
            with open(self.arquivo_recorde, "r") as arquivo:
                return int(arquivo.read())
        except (FileNotFoundError, ValueError):
            return 0

    def _salvar_recorde(self):
        with open(self.arquivo_recorde, "w") as arquivo:
            arquivo.write(str(self.recorde))


    # --- Funções de Desenho e Lógica ---

    # Generate random position for food 
    def gerar_comida(self):
        obstaculos_atuais = self.fases[self.fase_atual_indice]['obstaculos']
        
        while True:
            comida_x = random.randrange(0, self.largura - self.tamanho_quadrado, self.tamanho_quadrado)
            comida_y = random.randrange(0, self.altura - self.tamanho_quadrado, self.tamanho_quadrado)
            
            nova_posicao = [comida_x, comida_y]
            
            # Garante que a comida não apareça em cima de um obstáculo, power-up ou da cobrinha
            if nova_posicao not in obstaculos_atuais and nova_posicao not in self.pixel and \
               (self.power_up_x, self.power_up_y) != (comida_x, comida_y):
                return comida_x, comida_y

    # Draw the food on the screen
    def desenhar_comida(self, tamanho, comida_x, comida_y):
        cor_comida = self.fases[self.fase_atual_indice]['cor_comida']
        pygame.draw.rect(self.tela, cor_comida, [comida_x, comida_y, tamanho, tamanho])

    # Draw the snake on the screen
    def desenhar_cobrinha(self, tamanho, pixel):
        cor_cobrinha = self.fases[self.fase_atual_indice]['cor_cobrinha']
        for pix in pixel:
            pygame.draw.rect(self.tela, cor_cobrinha, [pix[0], pix[1], tamanho, tamanho])
            
    # Desenha os obstáculos da fase atual
    def desenhar_obstaculos(self):
        obstaculos_atuais = self.fases[self.fase_atual_indice]['obstaculos']
        for obs in obstaculos_atuais:
            pygame.draw.rect(self.tela, self.cinza_obstaculo, [obs[0], obs[1], self.tamanho_quadrado, self.tamanho_quadrado])

    # Tenta gerar um Power-up em uma posição aleatória
    def gerar_power_up(self):
        if self.power_up_x is not None:
            return
            
        if random.randint(1, self.chance_spawn_power_up) != 1:
            return

        obstaculos_atuais = self.fases[self.fase_atual_indice]['obstaculos']
        
        while True:
            pu_x = random.randrange(0, self.largura - self.tamanho_quadrado, self.tamanho_quadrado)
            pu_y = random.randrange(0, self.altura - self.tamanho_quadrado, self.tamanho_quadrado)
            
            nova_posicao = [pu_x, pu_y]
            
            if nova_posicao not in obstaculos_atuais and \
               nova_posicao != [self.comida_x, self.comida_y] and \
               nova_posicao not in self.pixel:
                
                self.power_up_x, self.power_up_y = pu_x, pu_y
                self.tipo_power_up = random.choice(['slow', 'score'])
                return
    
    # Desenha o Power-up na tela
    def desenhar_power_up(self):
        if self.power_up_x is not None:
            if self.tipo_power_up == 'slow':
                cor = self.ciano_power
                texto = "S"
            else: # 'score'
                cor = self.amarelo_power
                texto = "+"
                
            pygame.draw.rect(self.tela, cor, [self.power_up_x, self.power_up_y, self.tamanho_quadrado, self.tamanho_quadrado])
            
            fonte_pu = pygame.font.SysFont("arial", 15, bold=True)
            texto_pu = fonte_pu.render(texto, True, self.preta)
            self.tela.blit(texto_pu, [self.power_up_x + 1, self.power_up_y - 2])

    # Aplica o efeito do Power-up
    def ativar_power_up(self):
        self.power_up_x, self.power_up_y = None, None 

        if self.tipo_power_up == 'slow':
            self.power_up_ativo = True
            self.velocidade_original = self.fases[self.fase_atual_indice]['velocidade']
            self.velocidade_jogo = max(10, self.velocidade_jogo - 10) 
            self.power_up_tempo_fim = pygame.time.get_ticks() + self.tempo_duracao_power_up
            
        elif self.tipo_power_up == 'score':
            self.pontuacao += 5 
    
    # Desativa o efeito do Power-up se o tempo acabar
    def verificar_e_desativar_power_up(self):
        if self.power_up_ativo:
            if pygame.time.get_ticks() > self.power_up_tempo_fim:
                self.velocidade_jogo = self.fases[self.fase_atual_indice]['velocidade']
                self.power_up_ativo = False

    # Draw the score, high score, and phase on the screen
    def desenhar_info_jogo(self):
        # 1. Pontuação
        texto_pontuacao = self.fonte_pontuacao.render(f"Pontuação: {self.pontuacao}", True, self.azul)
        self.tela.blit(texto_pontuacao, [1, 1])
        
        # 2. Recorde 
        texto_recorde = self.fonte_pontuacao.render(f"Recorde: {self.recorde}", True, self.azul)
        self.tela.blit(texto_recorde, [1, 30]) 

        # 3. Fase
        texto_fase = self.fonte_fase.render(f"Fase: {self.fase_atual_indice + 1}", True, self.azul)
        self.tela.blit(texto_fase, [self.largura - texto_fase.get_width() - 5, 1])

        # 4. Timer do Power-up
        if self.power_up_ativo:
            tempo_restante = max(0, (self.power_up_tempo_fim - pygame.time.get_ticks()) / 1000)
            cor = self.ciano_power
            texto_timer = self.fonte_fase.render(f"SLOW: {tempo_restante:.1f}s", True, cor)
            self.tela.blit(texto_timer, [self.largura - texto_timer.get_width() - 5, 30])
            
    # Display a message on the screen
    def exibir_mensagem(self, msg, cor):
        texto = self.fonte_gameover.render(msg, True, cor)
        self.tela.blit(texto, [self.largura / 6, self.altura / 3])

    # Display game over message with restart/quit instructions
    def exibir_game_over(self):
        mensagem_game_over = self.fonte_gameover.render("Game Over!", True, self.vermelha)
        mensagem_instrucoes = self.fonte_instrucoes.render("Pressione C para jogar novamente ou Q para sair", True, self.vermelha)

        game_over_rect = mensagem_game_over.get_rect(center=(self.largura / 2, self.altura / 3))
        instrucoes_rect = mensagem_instrucoes.get_rect(center=(self.largura / 2, self.altura / 3 + 50)) 

        self.tela.blit(mensagem_game_over, game_over_rect)
        self.tela.blit(mensagem_instrucoes, instrucoes_rect)
            
    
    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return True
            if evento.type == pygame.KEYDOWN:
                if self.perdeu:
                    if evento.key == pygame.K_c:
                        self.restart_requested = True
                        return True
                    if evento.key == pygame.K_q:
                        return True
                else:
                    # Impede a cobrinha de reverter 180 graus imediatamente
                    if evento.key == pygame.K_LEFT and self.velocidade_x == 0:
                        self.velocidade_x = -self.tamanho_quadrado
                        self.velocidade_y = 0
                    elif evento.key == pygame.K_RIGHT and self.velocidade_x == 0:
                        self.velocidade_x = self.tamanho_quadrado
                        self.velocidade_y = 0
                    elif evento.key == pygame.K_UP and self.velocidade_y == 0:
                        self.velocidade_y = -self.tamanho_quadrado
                        self.velocidade_x = 0
                    elif evento.key == pygame.K_DOWN and self.velocidade_y == 0:
                        self.velocidade_y = self.tamanho_quadrado
                        self.velocidade_x = 0
                    elif evento.key == pygame.K_p:
                        self.pausado = not self.pausado
        return False
    # --- FIM DO MÉTODO handle_events RESTAURADO ---


    # Update game state (snake position, collisions, food eating)
    def update_game_state(self):
        if self.pausado or self.perdeu:
            return

        # Update snake position
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        cabeca_cobrinha = [self.x, self.y]

        # 1. Colisão com as paredes
        if self.x < 0 or self.x >= self.largura or self.y < 0 or self.y >= self.altura:
            self.perdeu = True
            return

        # Update snake body pixels
        self.pixel.append(cabeca_cobrinha)
        if len(self.pixel) > self.tamanho_cobrinha:
            del self.pixel[0]

        # 2. Colisão com ela mesma
        for cada_pixel in self.pixel[:-1]:
            if cada_pixel == cabeca_cobrinha:
                self.perdeu = True
                return

        # 3. Colisão com Obstáculos
        obstaculos_atuais = self.fases[self.fase_atual_indice]['obstaculos']
        if cabeca_cobrinha in obstaculos_atuais:
            self.perdeu = True
            return

        # 4. Colisão com Power-up
        if self.power_up_x is not None and self.x == self.power_up_x and self.y == self.power_up_y:
            self.ativar_power_up()

        # 5. Colisão com a Comida
        if self.x == self.comida_x and self.y == self.comida_y:
            self.comida_x, self.comida_y = self.gerar_comida() 
            self.tamanho_cobrinha += 1
            self.pontuacao += 1
            
            self.verificar_mudanca_fase()
            self.gerar_power_up() # Tenta spawnar um power-up após comer a comida

    # Verifica e Aplica a Mudança de Fase
    def verificar_mudanca_fase(self):
        proxima_fase_indice = self.fase_atual_indice + 1
        
        if proxima_fase_indice < len(self.fases):
            pontos_proxima_fase = self.fases[proxima_fase_indice]['pontos_necessarios']
            
            if self.pontuacao >= pontos_proxima_fase:
                self.fase_atual_indice = proxima_fase_indice
                nova_velocidade = self.fases[self.fase_atual_indice]['velocidade']
                
                # Reseta a velocidade base, mesmo se o power-up estiver ativo
                self.velocidade_original = nova_velocidade
                if not self.power_up_ativo:
                    self.velocidade_jogo = nova_velocidade
                
                self.comida_x, self.comida_y = self.gerar_comida() 
                
    # Draw all game elements on the screen
    def draw_game_elements(self):
        cor_fundo = self.fases[self.fase_atual_indice]['cor_fundo']
        self.tela.fill(cor_fundo)
        
        self.desenhar_obstaculos()
        self.desenhar_power_up()
        self.desenhar_cobrinha(self.tamanho_quadrado, self.pixel)
        self.desenhar_comida(self.tamanho_quadrado, self.comida_x, self.comida_y)
        self.desenhar_info_jogo()

        if self.pausado:
             self.exibir_mensagem("Pausado", self.azul)

        if self.perdeu:
            self.exibir_game_over()

        pygame.display.update()

    # Main game loop
    def rodar_jogo(self):
        self.restart_requested = False
        fim_jogo = False
        while not fim_jogo:
            fim_jogo = self.handle_events() # Chamada que estava dando erro
            
            self.verificar_e_desativar_power_up()
            self.update_game_state()
            
            # Checagem e Salvamento do Recorde
            if self.perdeu and not self.recorde_salvo:
                if self.pontuacao > self.recorde:
                    self.recorde = self.pontuacao
                    self._salvar_recorde()
                self.recorde_salvo = True

            self.draw_game_elements()
            self.relogio.tick(self.velocidade_jogo)

# Create a game instance and run the game
while True:
    game = SnakeGame()
    game.rodar_jogo()
    if not getattr(game, 'restart_requested', False):
        break