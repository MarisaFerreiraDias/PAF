import pygame
import sys


WIDTH, HEIGHT = 1500, 800 #Coloquei logo os valores pois eles nao vao ser mudados.
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #WIN significa window. Nos aqui estamos a colocar a altura e largura do nosso jogo.
pygame.display.set_caption("Addams") #Esta linha de codigo esta a nomear o nosso jogo. 


PLAYER_WIDTH = 200
PLAYER_HEIGHT = 200
PLAYER_VEL = 8

background_image = pygame.image.load("startscreen_Addams_background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.font.init()
FONT = pygame.font.SysFont("timesnewroman", 70)

player_image = pygame.transform.scale(pygame.image.load("Wedn_Addams_Player1.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)) #imagem do player

rooms = [   #aqui eu coloquei todas as imagens, ao seja 'rooms' que vao existir
    pygame.transform.scale(pygame.image.load("Addams_Entrada1.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Entrada.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Corredor1.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Corredor3.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Biblioteca.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Corredor2.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_SalaRandom.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_WineCellas.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_ParteDeFora.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Cemiterio.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Entrada_Cemiterio.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Basement.png"), (WIDTH, HEIGHT))
]

room_connections = { #aqui eu coloquei quais sao os possiveis caminhos que podem ir, ao seja, no primeiro quarto, so pode sair de la se for para cima, onde entra no segundo quarto
    0: {"up": 1},
    1: {"down": 0, "left": 5,"right": 2},
    2: {"left": 1, "right": 3,},
    3: {"left": 2, "up": 4, "down":10},
    4: {"down": 3},
    5: {"right": 1, "left": 6},
    6: {"left": 8, "right": 5},
    7: {"down": 8},
    8: {"right": 6, "down": 9, "up": 7},
    9: {"up": 8},
    10: {"up": 3, "down": 11},
    11: {"up": 10}
}
current_room = 0 #o 'room' que o player vai começar vai ser o 0, ao seja o primeiro


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def start_screen():
    run = True
    while run:
        WIN.blit(background_image, (0, 0))
        draw_text("Addams Game", FONT, WHITE, WIN, WIDTH//2, HEIGHT//2 - 50)
        draw_text("Press any key to start", pygame.font.SysFont("timesnewroman", 40), WHITE, WIN, WIDTH//2, HEIGHT//2 + 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Any key press will start the game
                run = False

def draw(player, bg):
    WIN.blit(bg, (0, 0)) #vai colocar a imagem que colocamos no background na coordenada

    WIN.blit(player_image, (player.x, player.y)) #aqui estou a desenhar o player com a imagem

    pygame.display.update() #vai dar update

def main():
    global current_room #estou a declarar o current_room como global para que depois de para modificar
    

    run = True  #criei a variavel run para fazer o loop para o jogo ficar a correr e nao fechar ate nos querermos

    player = pygame.Rect(625 , 600, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock() #isto vai determinar a velocidade que o 'player' move (na verdade ele esta a determinar o quao rapido o loop vai ser, para que a velocidade seja 
    #sempre a mesma)

    while run: #enquanto a variavel for verdadeira:
        clock.tick(60) #aqui coloco 60 porque é o numero maximo de frames por segundo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break #se clicarmos no botao para sair, o run fica falso, ao seja o loop do jogo acaba

        #movimento do player
        keys = pygame.key.get_pressed() #aqui esta a movimentação do player
        if keys[pygame.K_LEFT]:    #se a key esquerda for clicada, ele move para a esquerda
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT]:    #se a key direita for clicada, ele move para a direita
            player.x += PLAYER_VEL
        if keys[pygame.K_UP]:    #se a key para cima for clicada, ele move para cima
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]:    #se a key para baixo for clicada, ele move para baixo
            player.y += PLAYER_VEL


        if player.left > WIDTH:  #se o player for para a esquerda 
            if "right" in room_connections[current_room]:
                current_room = room_connections[current_room]["right"]
                player.left = 0
            
    
        if player.right < 0:     #se o player for para a direita 
            if "left" in room_connections[current_room]:
                current_room = room_connections[current_room]["left"]
                player.right = WIDTH
            else:
                player.x = 0

        if player.top > HEIGHT:  # Se o player está além da parte inferior da tela
            if "down" in room_connections[current_room]:
                current_room = room_connections[current_room]["down"]  # Transição para a sala de baixo
                player.bottom = 0  # Reaparece na parte superior da nova sala
                player.y = 600  # Ajusta a posição do player para o limite inferior
            else:
                # Boundary para impedir que o jogador vá além de um certo ponto (ex: limite inferior da tela)
                player.y = HEIGHT - player.height  # Limita o player no limite da parte inferior da tela
            

        if player.bottom < 700:  # se o player está acima de 600 (parte superior da tela)
            if "up" in room_connections[current_room]:
                current_room = room_connections[current_room]["up"]  # Transição para a sala de cima
                player.top = HEIGHT  # Aparece no fundo da nova sala
                player.y = 710  # Ajuste da posição para aparecer um pouco acima do fundo
            else:
                # Aqui você cria um boundary para evitar que o player vá para cima se não for para mudar de sala
                player.y = 700 - player.height  # Limita o player na posição 700
                

    
        draw(player, rooms[current_room]) #vai tar a chamar a funçao do player ate o ciclo acabar. ela tambem desenha o bg
    
    pygame.quit() #a window fecha por nos
    


if __name__ == "__main__": #este codigo assegura que nos estejamos a correr o codigo do main e nao a importar-lo
    start_screen()
    main()
