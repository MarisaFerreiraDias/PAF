import pygame


WIDTH, HEIGHT = 1500, 800 #Coloquei logo os valores pois eles nao vao ser mudados.
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #WIN significa window. Nos aqui estamos a colocar a altura e largura do nosso jogo.
pygame.display.set_caption("Addams") #Esta linha de codigo esta a nomear o nosso jogo. 

#BG =pygame.transform.scale(pygame.image.load("Addams_Entrada.png"), (WIDTH, HEIGHT)) colocamos a imagem de fundo default e com a scale que eu quero, que neste caso cubra a screen toda

PLAYER_WIDTH = 40
PLAYER_HEIGTH = 60
PLAYER_VEL = 10

rooms = [   #aqui eu coloquei todas as imagens, ao seja 'rooms' que vao existir
    pygame.transform.scale(pygame.image.load("Addams_Entrada1.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Entrada.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Corredor1.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Corredor3.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Biblioteca.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Corredor2.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_SalaRandom.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_ParteDeFora.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_WineCellas.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("Addams_Cemiterio.png"), (WIDTH, HEIGHT))
]

room_connections = {
    0: {"up": 1},
    1: {"down": 0, "left": 5,"right": 2},
    2: {"left": 1, "right": 3,},
    3: {"left": 2, "up": 4},
    4: {"down": 3},
    5: {"right": 1, "left": 6},
    6: {"left": 7, "right": 5},
    7: {"right": 6, "down": 9, "up": 8},
    8: {"down": 7},
    9: {"up": 7},
}


current_room = 0 #o 'room' que o player vai começar vai ser o 0, ao seja o primeiro

def draw(player, bg):
    WIN.blit(bg, (0, 0)) #vai colocar a imagem que colocamos no background na coordenada

    pygame.draw.rect(WIN, "black", player) #aqui estou a dizer que o retangulo(rect) vai estar na window(WIN), vai ser preto e vai estar nas coordenadas player

    pygame.display.update() #vai dar update

def main():
    global current_room #estou a declarar o current_room como global para que depois de para modificar
    

    run = True  #criei a variavel run para fazer o loop para o jogo ficar a correr e nao fechar ate nos querermos

    player = pygame.Rect(725 , 700, PLAYER_WIDTH, PLAYER_HEIGTH)

    clock = pygame.time.Clock() #isto vai determinar a velocidade que o 'player' move (na verdade ele esta a determinar o quao rapido o loop vai ser, para que a velocidade seja 
    #sempre a mesma)

    while run: #enquanto a variavel for verdadeira:
        clock.tick(60) #aqui coloco 60 porque é o numero maximo de frames por segundo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break #se clicarmos no botao para sair, o run fica falso, ao seja o loop do jogo acaba

        keys = pygame.key.get_pressed() #aqui esta a movimentação do player
        if keys[pygame.K_LEFT]:    #se a key esquerda for clicada, ele move para a esquerda
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT]:    #se a key direita for clicada, ele move para a direita
            player.x += PLAYER_VEL
        if keys[pygame.K_UP]:    #se a key para cima for clicada, ele move para cima
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]:    #se a key para baixo for clicada, ele move para baixo
            player.y += PLAYER_VEL

        #movimento do player
        if player.left > WIDTH:  #se o player for para a esquerda 
            if "right" in room_connections[current_room]:
                current_room = room_connections[current_room]["right"]
                player.left = 0

    
        if player.right < 0:     #se o player for para a direita 
            if "left" in room_connections[current_room]:
                current_room = room_connections[current_room]["left"]
                player.right = WIDTH

        if player.top > HEIGHT:  # Move to the lower room
            if "down" in room_connections[current_room]:
                current_room = room_connections[current_room]["down"]
                player.bottom = 0

        if player.bottom < 0:  # Move to the upper room
            if "up" in room_connections[current_room]:
                current_room = room_connections[current_room]["up"]
                player.top = HEIGHT

    
        draw(player, rooms[current_room]) #vai tar a chamar a funçao do player ate o ciclo acabar. ela tambem desenha o bg
    
    pygame.quit() #a window fecha por nos
    


if __name__ == "__main__": #este codigo assegura que nos estejamos a correr o codigo do main e nao a importar-lo
    main()
