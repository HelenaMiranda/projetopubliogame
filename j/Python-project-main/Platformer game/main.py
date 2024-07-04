import pygame
from pygame.locals import *# importando 
from pygame import mixer# importando 
import pickle# importando 
from os import path # da biblioteca os, importe path

# inicia o pygame
pygame.mixer.pre_init(44100, -16, 2, 512)# inicia o mixer
mixer.init() # inicia o mixer
mixer.init()# inicia o pygame
pygame.init()

#define o tempo
clock = pygame.time.Clock() # define o tempo
fps = 60# define o tempo

#define a tela
screen_width = 800 # define a largura da tela
screen_height = 800 # define a altura da tela

screen = pygame.display.set_mode((screen_width, screen_height)) # define a tela
pygame.display.set_caption('Platformer') # define o titulo da tela


#define font
font = pygame.font.SysFont('Bauhaus 93', 70)#define a  fonte
font_score = pygame.font.SysFont('Bauhaus 93', 30)#define a  fonte


#define as variáveis do jogo 
tile_size = 40 # define o tamanho das casas
game_over = 0 # define o estado do jogo
main_menu = True # define o estado do menu
level = 7 # define o nivel
max_levels = 7 # define o maximo de niveis
score = 0 # define a sua pontuação


#define as cores que serão usadas 
white = (255, 255, 255) # define a cor branca
blue = (0, 0, 255)# define a cor azul

# carrega imagens
sun_img = pygame.image.load('img/sun.png') # carrega a imagem do sol
bg_img = pygame.image.load('img/sky.png')# carrega a imagem do fundo
restart_img = pygame.image.load('img/restart_btn.png')# carrega a imagem do botao de reiniciar
start_img = pygame.image.load('img/start_btn.png')# carrega a imagem do botao de iniciar
exit_img = pygame.image.load('img/exit_btn.png')# carrega a imagem do botao de sair

#carrega sons 
pygame.mixer.music.load('img/music.wav')# carrega a musica
pygame.mixer.music.play(-1, 0.0, 5000)# toca a musica
coin_fx = pygame.mixer.Sound('img/coin.wav')# carrega o som da moeda
coin_fx.set_volume(0.5)#define o volume do som 
jump_fx = pygame.mixer.Sound('img/jump.wav') # carrega o som do pulo
jump_fx.set_volume(0.5) # define o volume do som
game_over_fx = pygame.mixer.Sound('img/game_over.wav')  # carrega o som do game over
game_over_fx.set_volume(0.5) # define o volume do som

# Define uma função para imprimir texto 
def draw_text(text, font, text_col, x, y): # define a função para imprimir texto para o menu
	img = font.render(text, True, text_col) # define a imagem do texto no tamanho e cor definidos
	screen.blit(img, (x, y))  # imprime o texto na tela 

# Função para resetar o level
def reset_level(level): # define a função para resetar o level
	player.reset(100, screen_height - 130) # define a posicao do jogador
	blob_group.empty() # limpa o grupo de blobs
	platform_group.empty()  # limpa o grupo de plataformas
	coin_group.empty() # limpa o grupo de moedas
	lava_group.empty() # limpa o grupo de lava
	exit_group.empty() # limpa o grupo de saida

	# Carrega os dados de cada level e cria um novo 'mundo'
	if path.exists(f'level{level}_data'): # verifica se existe um arquivo com o nome do nivel
		pickle_in = open(f'level{level}_data', 'rb') # abre o arquivo de dados do nivel
		world_data = pickle.load(pickle_in) # carrega os dados do nivel
	world = World(world_data) # cria um novo 'mundo' a partir dos dados do arquivo
	#criando uma pontuação 
	score_coin = Coin(tile_size // 2, tile_size // 2) # cria uma moeda para a pontuacao
	coin_group.add(score_coin) # adiciona a moeda ao grupo de moedas
	return world # retorna o novo 'mundo'

# Classe para criar botões
class Button(): # define a classe para criar botões
	def __init__(self, x, y, image): # define o construtor da classe para criar botões
		self.image = image # define a imagem do botao
		self.rect = self.image.get_rect() # define o retangulo do botao
		self.rect.x = x # define a posicao x do botao
		self.rect.y = y # define a posicao y do botao
		self.clicked = False  # define se o botao foi clicado e a partir disso se ele deve ser desenhado ou não


# Cria uma função para desenhar os botões
	def draw(self): # define a função para desenhar o botao
		action = False # define se o botao deve ser desenhado ou nao

		#atribui a posição do mouse 
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos): # verifica se o mouse está sobre o botão
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # verifica se o mouse está sobre o botão e se o botão foi clicado, caso sim, o botão deve ser desenhado
				action = True  # define se o botao deve ser desenhado 
				self.clicked = True # define se o botao foi clicado


		if pygame.mouse.get_pressed()[0] == 0: # verifica se o mouse esta sobre o botao e se o botao foi clicado, caso sim, o botao deve ser desenhado
			self.clicked = False # define se o botao foi clicado

		#desenha botão
		screen.blit(self.image, self.rect)

		return action # retorna se o botao deve ser desenhado


class Player():# define a classe para criar o jogador
	def __init__(self, x, y):# define o construtor da classe para criar o jogador
		self.reset(x, y) # define a posição do jogador

	def update(self, game_over): # define a função para atualizar o jogador
		dx = 0 # define a variavel dx para o movimento horizontal
		dy = 0  # define a variavel dy para o movimento vertical
		walk_cooldown = 5 # define o tempo de espera entre as imagens de movimento do jogador
		col_thresh = 20 # define o limite de colisão do jogador


		if game_over == 0: # verifica se o jogo está rodando
			# verifica as teclas pressionadas
			key = pygame.key.get_pressed()  # verifica se a tecla espaço foi pressionada e se o jogador não está no chão
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:# toca o som do pulo
				jump_fx.play() # toca o som do pulo 
				self.vel_y = -15# define a velocidade do pulo 
				self.jumped = True # define se o jogador ja pulou
			if key[pygame.K_SPACE] == False: # verifica se a tecla espaço foi pressionada
				self.jumped = False # define se o jogador ja pulou
			if key[pygame.K_LEFT]:  # verifica se a tecla esquerda foi pressionada
				dx -= 6.5 # define o movimento horizontal para a esquerda
				self.counter += 1  #define o contador para o movimento horizontal
				self.direction = -1# define a direção do movimento horizontal para a esquerda
			if key[pygame.K_RIGHT]: # verifica se a tecla direita foi pressionada
				dx += 5 # define o movimento horizontal para a direita
				self.counter += 1 #define o contador para o movimento horizontal
				self.direction = 1 # define a direcao do movimento horizontal para a direita
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:  # verifica se nenhuma tecla foi pressionada
				self.counter = 0  # define o contador para o movimento horizontal
				self.index = 0 # define o indice para o movimento horizontal para o padrao
				if self.direction == 1: # verifica se a direção do movimento horizontal é para a direita ou para a esquerda
					self.image = self.images_right[self.index] # define a imagem do movimento horizontal para o padrão
				if self.direction == -1: # verifica se a direção do movimento horizontal é para a direita ou para a esquerda
					self.image = self.images_left[self.index]# define a imagem do movimento horizontal para o padrão


			if self.counter > walk_cooldown:# verifica se o contador é maior que o tempo de espera entre as imagens de movimento do jogador
				self.counter = 0 # define o contador para o movimento horizontal para o padrao
				self.index += 1 # define o indice para o movimento horizontal para o proximo
				if self.index >= len(self.images_right):# verifica se o indice é maior ou igual ao tamanho da lista de imagens do movimento horizontal para o padrão
					self.index = 0 # define o índice para o movimento horizontal para o padrão 
				if self.direction == 1: # verifica se a direção do movimento horizontal é para a direita ou para a esquerda
					self.image = self.images_right[self.index] # define a imagem do movimento horizontal para o próximo
				if self.direction == -1: # verifica se a direção do movimento horizontal é para a direita ou para a esquerda
					self.image = self.images_left[self.index] # define a imagem do movimento horizontal para o próximo


			#define a gravidade do jogador 
			self.vel_y += 1 # define a velocidade do movimento vertical para baixo
			if self.vel_y > 10: # verifica se a velocidade do movimento vertical é maior que 10
				self.vel_y = 10 # define a velocidade do movimento vertical para 10
			dy += self.vel_y # define a velocidade do movimento vertical para baixo para o jogador


			# define a colisão do jogador com as plataformas
			self.in_air = True # define se o jogador está no chão
			for tile in world.tile_list: # percorre a lista de tiles do 'mundo' para verificar se o jogador está no chão
				#  verifica se o jogador está no chão
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): # verifica se o jogador está no chão no eixo x e se a colisão do jogador com a plataforma está dentro do retângulo do jogo
					dx = 0# define o movimento horizontal para o padrão
				## verifica se o jogador esta no chao no eixo y e se a colisao do jogador com a plataforma esta dentro do retangulo do jogo
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):# verifica se o jogador está no chão
					# verifica se o jogador está no chão
					if self.vel_y < 0: # verifica se a velocidade do movimento vertical é menor que 0 
						dy = tile[1].bottom - self.rect.top # define a velocidade do movimento vertical para o topo do tile 
						self.vel_y = 0  # define a velocidade do movimento vertical para o padrao
					#check if above the ground i.e. falling
					elif self.vel_y >= 0: # verifica se a velocidade do movimento vertical é maior ou igual a 0 
						dy = tile[1].top - self.rect.bottom # define a velocidade do movimento vertical para o topo do tile 
						self.vel_y = 0 # define a velocidade do movimento vertical para o padrao
						self.in_air = False# define se o jogador está no chão


			 # se o sprite de colisão for a moeda, a moeda é adicionada ao grupo de moedas
			if pygame.sprite.spritecollide(self, blob_group, False):# verifica se o jogador esta colidindo com o grupo de blobs
				game_over = -1# caso sim, define o estado do jogo para -1 (game over) para o jogador perder o jogo
				game_over_fx.play() # toca o som de 'game over' 

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):  # verifica se o jogador esta colidindo com o grupo de lava
				game_over = -1 # caso sim, o estado do jogo é definido para -1 (game over) para o jogador perder o jogo 
				game_over_fx.play()  # toca o som do 'game over' 
 
			#verifica a colisão com a saída 
			if pygame.sprite.spritecollide(self, exit_group, False): # verifica se o jogador esta no chao
				game_over = 1 # define o estado do jogo para 1 e o jogador ganha o jogo



			#para a colisão do jogador com a plataforma 
			for platform in platform_group:# percorre a lista de plataformas do 'mundo' para ver se o jogador esta no chao
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):  # verifica se a plataforma está colidindo com o jogador no eixo x e se a colisão da plataforma com o jogador está dentro do retângulo do jogo
					dx = 0 #movimento horizontal é o padrão 
				#colisão no eixo y 
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):  # verifica se a plataforma esta colidindo com o jogador no eixo y e se a colisao da plataforma com o jogador esta dentro do retangulo do jogo
					
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:# checa se o jogador esta abaixo da plataforma
						self.vel_y = 0 # define a velocidade do movimento vertical para o padrao para baixo
						dy = platform.rect.bottom - self.rect.top# define a velocidade do movimento vertical para o topo da plataforma
					
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh: #verifica se está acima plataforma
						self.rect.bottom = platform.rect.top - 1 # define a posicao do jogador para abaixo da plataforma
						self.in_air = False # define se o jogador esta no chao 
						dy = 0 # define a velocidade do movimento vertical para o padrao para cima
          
					#move  para o lado com as plataformas 
					if platform.move_x != 0:
						self.rect.x += platform.move_direction # atualiza a posicao do jogador para cima ou para baixo com as plataformas 


			#atualiza as coordenadas do jogador 
			self.rect.x += dx # atualiza a posicao do jogador para a direita ou para a esquerda com as plataformas 
			self.rect.y += dy # atualiza a posicao do jogador para cima ou para baixo com as plataformas 


		elif game_over == -1: # verifica se o jogo está rodando  
			self.image = self.dead_image # define a imagem do jogador para o estado de morte 
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2) # desenha o texto 'game over' na tela
			if self.rect.y > 200:  # verifica se a posicao y do jogador é maior que 200
				self.rect.y -= 5 # define a posicao y do jogador para cima com as plataformas

		#draw player onto screen
		screen.blit(self.image, self.rect) # checa se o jogador esta abaixo da plataforma

		return game_over # retorna o estado do jogo



	def reset(self, x, y):  # define a função para resetar o jogador
		self.images_right = [] # define a lista de imagens para o movimento horizontal para a direita 
		self.images_left = [] # define a lista de imagens para o movimento horizontal para a esquerda
		self.index = 0 # define o índice para o movimento horizontal para o padrão
		self.counter = 0 # define o contador para o movimento horizontal para o padrão
		for num in range(1, 5): # percorre os numeros de 1 a 4 para criar as imagens do movimento horizontal para a direita
			img_right = pygame.image.load(f'img/guy{num}.png')  # carrega a imagem do movimento horizontal para a direita
			img_right = pygame.transform.scale(img_right, (35, 70)) # define o tamanho da imagem do movimento horizontal para a direita
			img_left = pygame.transform.flip(img_right, True, False) # define a imagem do movimento horizontal para a esquerda como a imagem do movimento horizontal para a direita
			self.images_right.append(img_right) # adiciona a imagem do movimento horizontal para a direita na lista de imagens
			self.images_left.append(img_left) # adiciona a imagem do movimento horizontal para a esquerda na lista de imagens
		self.dead_image = pygame.image.load('img/ghost.png') # carrega a imagem do jogador para o estado de morte
		self.image = self.images_right[self.index] # define a imagem do jogador para o padrao
		self.rect = self.image.get_rect() # define o retângulo do jogador 
		self.rect.x = x # define a posição x do jogador
		self.rect.y = y # define a posição y do jogador
		self.width = self.image.get_width() # define o largura do jogador
		self.height = self.image.get_height() # define a altura do jogador 
		self.vel_y = 0 # define a velocidade do movimento vertical para o padrão
		self.jumped = False # define se o jogador está saltando
		self.direction = 0 # define a direção do movimento horizontal para o padrão
		self.in_air = True # define se o jogador está no chão




class World(): # define a classe World para criar o 'mundo' do jogo
	def __init__(self, data): # define o construtor da classe World
		self.tile_list = [] # define a lista de tiles do 'mundo'

		#carregar 
		dirt_img = pygame.image.load('img/dirt.png')  # define o construtor da classe World
		grass_img = pygame.image.load('img/grass.png') # define a lista de tiles do 'mundo'

		row_count = 0 # define o contador de linhas
		for row in data: # percorre as linhas do 'mundo' para criar os tiles
			col_count = 0 # define o contador de colunas para cada linha
			for tile in row: # percorre as colunas do 'mundo' para criar os tiles
				if tile == 1: # verifica se o tile é 1 (plataforma)
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size)) # define a imagem do tile como a imagem de 'dirt'
					img_rect = img.get_rect()# define o retângulo do tile
					img_rect.x = col_count * tile_size # define a posição x do tile
					img_rect.y = row_count * tile_size # define a posição y do tile
					tile = (img, img_rect) # define o tile como uma tupla com a imagem e o retangulo do tile
					self.tile_list.append(tile) # adiciona o tile na lista de tiles do 'mundo'
				if tile == 2: # verifica se o tile é 2 (moeda)
					img = pygame.transform.scale(grass_img, (tile_size, tile_size)) # define a imagem do tile como a imagem de 'grass'
					img_rect = img.get_rect() # define o retângulo do tile
					img_rect.x = col_count * tile_size # define a posição x do tile
					img_rect.y = row_count * tile_size # define a posição y do tile
					tile = (img, img_rect)  # define o tile como uma tupla com a imagem e o retângulo do tile
					self.tile_list.append(tile) # adiciona o tile na lista de tiles do 'mundo
				if tile == 3: # verifica se o tile é 3 (plataforma)
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15) # define a plataforma como um objeto da classe Platform
					blob_group.add(blob)  # adiciona a plataforma ao grupo de plataformas
				if tile == 4: # verifica se o tile é 4 (plataforma)
					platform = Platform(col_count * tile_size , row_count * tile_size, 1, 0) # define a plataforma como um objeto da classe Platform
					platform_group.add(platform) # adiciona a plataforma ao grupo de plataformas
				if tile == 5: # verifica se o tile é 5 (plataforma)
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)  # define a plataforma como um objeto da classe Platform
					platform_group.add(platform) # adiciona a plataforma ao grupo de plataformas
				if tile == 6: # verifica se o tile é 6 (plataforma)
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2)) # define a lava como um objeto da classe Lava
					lava_group.add(lava) # adiciona a lava ao grupo de lava
				if tile == 7: # verifica se o tile é 7 (plataforma)
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2)) # define a moeda como um objeto da classe Coin
					coin_group.add(coin) # adiciona a moeda ao grupo de moedas
				if tile == 8:  # verifica se o tile é 8 (plataforma)
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2)) # define a saida como um objeto da classe Exit
					exit_group.add(exit)  # adiciona a saida ao grupo de saidas para o jogador sair do 'mundo'
				col_count += 1 # incrementa o contador de colunas p/ cada linha
			row_count += 1 # incrementa o contador de linhas p/ cada linha


	def draw(self): # define a função para desenhar o 'mundo' do jogo
		for tile in self.tile_list:  # percorre a lista de tiles do 'mundo' para desenhar cada tile 
			screen.blit(tile[0], tile[1]) # desenha o tile na tela 
 


class Enemy(pygame.sprite.Sprite): # define a classe Enemy para criar os inimigos do jogo
	def __init__(self, x, y): # define o construtor da classe Enemy em que o x e o y sao as posições do inimigo
		pygame.sprite.Sprite.__init__(self) # inicializa a classe Sprite do Pygame
		self.image = pygame.image.load('img/blob.png') # carrega a imagem do inimigo
		self.rect = self.image.get_rect() # define o retângulo do inimigo para o tamanho da imagem
		self.rect.x = x # define a posição x do inimigo
		self.rect.y = y # define a posição y do inimigo
		self.move_direction = 1 # define a direção do movimento horizontal do inimigo
		self.move_counter = 0 # define o contador do movimento horizontal do inimigo

	def update(self): # define a função para atualizar o inimigo do jogo
		self.rect.x += self.move_direction # atualiza a posicao x do inimigo para a direita ou para a esquerda
		self.move_counter += 1 # incrementa o contador do movimento horizontal do inimigo
		if abs(self.move_counter) > 50: # verifica se o contador do movimento horizontal do inimigo é  maior que 50
			self.move_direction *= -1 # inverte a direcao do movimento horizontal do inimigo
			self.move_counter *= -1 # inverte o contador do movimento horizontal do inimigo


class Platform(pygame.sprite.Sprite): # define a classe Platform para criar as plataformas do jogo e definir as suas propriedades
	def __init__(self, x, y, move_x, move_y):  # define o construtor da classe Platform em que o x e o y sao as posicoes da plataform
		pygame.sprite.Sprite.__init__(self) # inicializa a classe Sprite do Pygame
		img = pygame.image.load('img/platform.png') # carrega a imagem da plataforma
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2)) # define o tamanho da imagem da plataforma
		self.rect = self.image.get_rect() # define o retângulo da plataforma para o tamanho da imagem
		self.rect.x = x # define a posição x da plataforma
		self.rect.y = y # define a posição y da plataforma
		self.move_counter = 0 # define o contador do movimento horizontal da plataforma
		self.move_direction = 1 # define a direção do movimento horizontal da plataforma
		self.move_x = move_x # define o movimento horizontal da plataforma
		self.move_y = move_y # define o movimento vertical da plataforma


	def update(self):  # define a função para atualizar a plataforma do jogo
		self.rect.x += self.move_direction * self.move_x # atualiza a posição x da plataforma para a direita ou para a esquerda
		self.rect.y += self.move_direction * self.move_y # atualiza a posição y da plataforma para cima ou para baixo
		self.move_counter += 1# incrementa o contador do movimento horizontal da plataforma
		if abs(self.move_counter) > 50: # verifica se o contador do movimento horizontal da plataforma é maior que 50
			self.move_direction *= -1 # inverte a direcao do movimento horizontal da plataforma
			self.move_counter *= -1# inverte o contador do movimento horizontal da plataforma





class Lava(pygame.sprite.Sprite):# define a classe Lava para criar as lavas do jogo
	def __init__(self, x, y): # define o construtor da classe Lava em que o x e o y são das posições 
		pygame.sprite.Sprite.__init__(self)# inicializa a classe Sprite do Pygame
		img = pygame.image.load('img/lava.png')# carrega a imagem da lava
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))# define o tamanho da imagem da lava
		self.rect = self.image.get_rect()# define o retângulo da lava para o tamanho da imagem
		self.rect.x = x # define a posição x da lava
		self.rect.y = y # define a posição y da lava


class Coin(pygame.sprite.Sprite): # define a classe Coin para criar as moedas do jogo
	def __init__(self, x, y): # define o construtor da classe Coin em que o x e o y sao as posições da moeda
		pygame.sprite.Sprite.__init__(self) # inicializa a classe Sprite do Pygame
		img = pygame.image.load('img/coin.png') # carrega a imagem da moeda
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))  # define o tamanho da imagem da moeda
		self.rect = self.image.get_rect() # define o retângulo da moeda para o tamanho da imagem
		self.rect.center = (x, y) # define a posição central da moeda para as posições x e y


class Exit(pygame.sprite.Sprite):  # define a classe Exit para criar as saidas do jogo
	def __init__(self, x, y): # define o construtor da classe Exit em que o x e o y são as posições da saida
		pygame.sprite.Sprite.__init__(self) # inicializa a classe Sprite do Pygame
		img = pygame.image.load('img/exit.png') # carrega a imagem da saída
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5))) # define o tamanho da imagem da saida
		self.rect = self.image.get_rect() # define o retângulo da saida para o tamanho da imagem
		self.rect.x = x # define a posição x da saída
		self.rect.y = y # define a posição y da saida

#Matriz para criar o nível com os obstáculos, objetos , inimigos e espaços vazios 
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



player = Player(100, screen_height - 130) # define o jogador como um objeto da classe Player

blob_group = pygame.sprite.Group()  # define o grupo de blobs como um objeto do Pygame
platform_group = pygame.sprite.Group()  # define o grupo de plataformas como um objeto do Pygame
lava_group = pygame.sprite.Group() # define o grupo de lavas como um objeto do Pygame
coin_group = pygame.sprite.Group()# define o grupo de moedas como um objeto do Pygame
exit_group = pygame.sprite.Group() # define o grupo de saidas como um objeto do Pygame

#cria moeda fictícia para a pontuação
score_coin = Coin(tile_size // 2, tile_size // 2) # define a moeda como um objeto da classe Coin
coin_group.add(score_coin)  # adiciona a moeda ao grupo de moedas

# carregar dados de nível e criar mundo
if path.exists(f'level{level}_data'): # verifica se o arquivo de nível existe
	pickle_in = open(f'level{level}_data', 'rb')  #Abre o arquivo de nível em modo de leitura binária
	world_data = pickle.load(pickle_in)# carrega os dados do arquivo de nível em um objeto do Pygame
world = World(world_data)# define o 'mundo' como um objeto da classe World


#cria botões 
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img) # define o botão de reiniciar como um objeto da classe Button
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)# define o botão de iniciar como um objeto da classe Button
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)# define o botao de sair como um objeto da classe Button


# define a fonte para o texto do jogo
run = True # define a variavel run como True
while run:# enquanto run for True

	clock.tick(fps) # define a taxa de quadros do jogo

	screen.blit(bg_img, (0, 0)) # desenha a imagem de fundo na tela
	screen.blit(sun_img, (100, 100))  # desenha a imagem do sol na tela

	if main_menu == True: # se main_menu for True
		if exit_button.draw(): # se o botão de sair for clicado
			run = False # define run como False para sair do jogo
		if start_button.draw(): # se o botão de iniciar for clicado
			main_menu = False # define main_menu como False para entrar no loop do jogo
	else: # se main_menu nao for True
		world.draw() # desenha o 'mundo' do jogo

		if game_over == 0:  # se game_over for 0
			blob_group.update() # atualiza os blobs do jogo
			platform_group.update() # atualiza as plataformas do jogo
			#atualiza a pontuação
			#verifica se a moesda foi coletada 
			if pygame.sprite.spritecollide(player, coin_group, True): # verifique se uma moeda foi coletada
				score += 1 # incrementa a pontuação do jogador
				coin_fx.play() # toca o som de coletar moeda
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10) # desenha a pontuação do jogador na tela
		
		blob_group.draw(screen) # desenha os blobs do jogo na tela
		platform_group.draw(screen) # desenha as plataformas do jogo na tela
		lava_group.draw(screen) # desenha as lavas do jogo na tela
		coin_group.draw(screen) # desenha as moedas do jogo na tela
		exit_group.draw(screen) # desenha as saidas do jogo na tela
 
		game_over = player.update(game_over)  # atualiza o jogo do jogador e retorna o estado do jogo

		#se o jogador morreu 
		if game_over == -1:
			if restart_button.draw(): # se o botao de reiniciar for clicado
				world_data = [] # define o nivel como um objeto do Pygame 
				world = reset_level(level) # define o 'mundo' como um objeto da classe World
				game_over = 0 # define game_over como 0 para reiniciar o jogo
				score = 0 # reinicia a pontuação do jogador como 0

		#se o jogador tiver completado o próximo nível 
		if game_over == 1:
			#reseta  o jogo e passa pro próximo nível
			level += 1# reinicia o nivel como 1
			if level <= max_levels:
				#reseta nível
				world_data = []# define o nivel como um objeto do Pygame
				world = reset_level(level)# define o 'mundo' como um objeto da classe World
				game_over = 0# define game_over como 0 para reiniciar o jogo
			else:
				draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)# desenha a mensagem de vitória na tela
				if restart_button.draw():# se o botão de reiniciar for clicado
					level = 1# reinicia o nivel como 1
					#reseta o nível
					world_data = []# define o nivel como um objeto do Pygame
					world = reset_level(level)# define o 'mundo' como um objeto da classe World
					game_over = 0# define game_over como 0 para reiniciar o jogo
					score = 0# reinicia a pontuação do jogador como 0

	for event in pygame.event.get(): # percorre a lista de eventos do jogo para verificar se algum evento ocorreu
		if event.type == pygame.QUIT: # se o evento for de fechar a janela
			run = False # define run como False para sair do jogo
 
	pygame.display.update() # atualiza a tela do jogo

pygame.quit() # encerra o Pygame