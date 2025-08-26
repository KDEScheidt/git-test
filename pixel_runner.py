import pygame, sys, random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/poim.ogg')

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 300:
            pygame.mixer.Sound.play(self.jump_sound)
            self.gravity = -18

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6.5
        self.destroy()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(midtop=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def collision_sprite(sound):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        pygame.mixer.Sound.play(sound)
        return 2
    else:
        return 1

#Inicia o módulo pygame
pygame.init()

#Cria a tela e armazena ela em uma variável
screen = pygame.display.set_mode((800, 400))
#Define o nome da janela
pygame.display.set_caption('Tumbalacatumba')
#Define o framerate do jogo
clock = pygame.time.Clock()
game_active = 0
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#Cria um evento customizado para usar como quiser
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

#Cria uma fonte pra usar onde quiser
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#Importa imagem e armazena em variável (superfície)
sky_surface = pygame.image.load('graphics/assets/Sky.png').convert()
ground_surface = pygame.image.load('graphics/assets/ground.png').convert()

#Obstáculos

#Cria um retângulo ao redor das superfícies para facilitar a usabilidade.
sky_rect = sky_surface.get_rect(topleft = (0, 0))
ground_rect = ground_surface.get_rect(topleft = (0, 300))

#Cria um elemento de texto pra ser colocado na tela
defeat_surface = test_font.render('YOU DIED', False, 'Red')
defeat_rect = defeat_surface.get_rect(midtop = (400, 200))
defeat_surface2 = test_font.render('PRESS ENTER TO RESTART, NUB', False, 'Red')
defeat_surface2_rect = defeat_surface2.get_rect(midtop = (400, 250))
start_surface = test_font.render('PRESS ENTER TO START GAME, NUB', False, 'White')
start_rect = start_surface.get_rect(midtop = (400, 150))
logo_surface = test_font.render('Developed by Pirulim Corp.', False, 'White')
logo_rect = logo_surface.get_rect(midtop = (400, 200))

#Sons
death_sound = pygame.mixer.Sound('audio/ouch.ogg')

#Loop do jogo
while True:

    #Verifica se o player clicou em fechar o jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Pula o boneco, fecha o game ou reseta, dependendo do input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                game_active = 1
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active == 1:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly', 'snail'])))

    if game_active == 1:
        #Coloca um objeto na tela (uma superfície sobre a outra)
        screen.blit(sky_surface, sky_rect)
        screen.blit(ground_surface, ground_rect)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        score = display_score()

        game_active = collision_sprite(death_sound)

    elif game_active == 2:
        screen.fill('Yellow')
        screen.blit(defeat_surface, defeat_rect)
        screen.blit(defeat_surface2, defeat_surface2_rect)
        final_score = test_font.render(f'Tempo que correste: {score} secundos', False, 'Red')
        final_score_rect = final_score.get_rect(midtop=(400, 150))
        screen.blit(final_score, final_score_rect)

    else:
        screen.fill('Black')
        screen.blit(start_surface, start_rect)
        screen.blit(logo_surface, logo_rect)

    #Atualiza a tela
    pygame.display.update()
    #Limitador de FPS
    clock.tick(60)