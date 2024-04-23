import pygame
import sys
import os

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen_width = 800  # Nova largura
screen_height = 600  # Nova altura
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Login")

# Carregar e configurar a fonte
font_path = os.path.join('fonts', 'Poppins-Regular.ttf')  # Substitua pelo caminho correto
font_small = pygame.font.Font(font_path, 16)
font_medium = pygame.font.Font(font_path, 20)
font_large = pygame.font.Font(font_path, 32)

# Cores
purple = (123, 120, 255, 1)
white = (255, 255, 255, 1)
blue = (0, 0, 128)
black = (0, 0, 0)

# Variáveis para armazenar inputs
input_box_user = pygame.Rect(screen_width // 2 - 100, 300, 200, 40)
input_box_pass = pygame.Rect(screen_width // 2 - 100, 360, 200, 40)
button_box = pygame.Rect(screen_width // 2 - 50, 420, 100, 40)
user_text = ''
pass_text = ''
user_active = pass_active = False

def draw_login_screen():
    global user_text, pass_text
    screen.fill(purple)
    
    # Header centralizado
    welcome_text = font_large.render("Bem-vindo", True, white)
    screen.blit(welcome_text, (screen_width // 2 - welcome_text.get_width() // 2, 100))
    
    # Sub-header centralizado
    login_text = font_medium.render("Faça login para acessar sua Carteira", True, white)
    screen.blit(login_text, (screen_width // 2 - login_text.get_width() // 2, 200))
    
    # Labels para os campos
    cpf_label = font_small.render("CPF:", True, white)
    screen.blit(cpf_label, (screen_width // 2 - 100, 275))
    password_label = font_small.render("Senha:", True, white)
    screen.blit(password_label, (screen_width // 2 - 100, 340))
    
    # Renderiza o texto nas caixas
    txt_surface_user = font_small.render(user_text, True, white)
    txt_surface_pass = font_small.render(pass_text, True, white)
    screen.blit(txt_surface_user, (input_box_user.x + 5, input_box_user.y + 5))
    screen.blit(txt_surface_pass, (input_box_pass.x + 5, input_box_pass.y + 5))
    
    # Desenha as caixas de texto
    pygame.draw.rect(screen, blue, input_box_user, 2)
    pygame.draw.rect(screen, blue, input_box_pass, 2)
    
    # Desenha o botão
    login_button = font_small.render('Login', True, white)
    pygame.draw.rect(screen, blue, button_box)
    screen.blit(login_button, (button_box.x + 30, button_box.y + 8))

def main():
    global user_text, pass_text, user_active, pass_active
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_user.collidepoint(event.pos):
                    user_active = True
                    pass_active = False
                elif input_box_pass.collidepoint(event.pos):
                    pass_active = True
                    user_active = False
                else:
                    user_active = pass_active = False
                if button_box.collidepoint(event.pos):
                    if user_text == 'admin' and pass_text == '123':
                        print("Login Successful")
                    else:
                        print("Login Failed")
            elif event.type == pygame.KEYDOWN:
                if user_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                elif pass_active:
                    if event.key == pygame.K_BACKSPACE:
                        pass_text = pass_text[:-1]
                    else:
                        pass_text += event.unicode

        draw_login_screen()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
