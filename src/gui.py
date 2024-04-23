import pygame
import sys
import os

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Login e Cadastro")

# Carregar e configurar a fonte
font_path = os.path.join('fonts', 'Poppins-Regular.ttf')
font_small = pygame.font.Font(font_path, 16)
font_medium = pygame.font.Font(font_path, 20)
font_large = pygame.font.Font(font_path, 40)

# Cores
purple = (123, 120, 255)
white = (255, 255, 255)
blue = (0, 0, 128)
black = (0, 0, 0)

# Estado da aplicação
current_screen = "login"

# Variáveis de texto para inputs
user_text = ''
pass_text = ''
name_text = ''
email_text = ''
dob_text = ''
cpf_text = ''

# Ativação de inputs
input_active = {'user': False, 'pass': False, 'name': False, 'email': False, 'dob': False, 'cpf': False}

# Definições dos retângulos de input e botão
label_spacing = 25  # Espaço entre o label e o input box
input_boxes = {
    'user': pygame.Rect(screen_width // 2 - 100, 250, 200, 40),
    'pass': pygame.Rect(screen_width // 2 - 100, 320, 200, 40),
    'name': pygame.Rect(screen_width // 2 - 100, 195 + label_spacing, 200, 40),
    'email': pygame.Rect(screen_width // 2 - 100, 245 + label_spacing, 200, 40),
    'dob': pygame.Rect(screen_width // 2 - 100, 295 + label_spacing, 200, 40),
    'cpf': pygame.Rect(screen_width // 2 - 100, 345 + label_spacing, 200, 40),
    'pass': pygame.Rect(screen_width // 2 - 100, 395 + label_spacing, 200, 40)
}
button_box = pygame.Rect(screen_width // 2 - 100, 445 + label_spacing, 200, 40)
register_text_box = pygame.Rect(screen_width // 2 - 100, 430, 300, 30)

def draw_login_screen():
    global user_text, pass_text
    screen.fill(purple)
    
    # Headers
    welcome_text = font_large.render("Bem-vindo!", True, white)
    login_text = font_medium.render("Faça login para acessar sua Carteira", True, white)
    screen.blit(welcome_text, (screen_width // 2 - welcome_text.get_width() // 2, 80))
    screen.blit(login_text, (screen_width // 2 - login_text.get_width() // 2, 130))
    
    # Label e Input para CPF
    cpf_label = font_small.render("CPF:", True, white)
    screen.blit(cpf_label, (screen_width // 2 - 100, 210))
    input_boxes['user'] = pygame.Rect(screen_width // 2 - 100, 235, 200, 40)
    txt_surface_user = font_small.render(user_text, True, white)
    screen.blit(txt_surface_user, (input_boxes['user'].x + 5, input_boxes['user'].y + 5))
    pygame.draw.rect(screen, blue, input_boxes['user'], 2)
    
    # Label e Input para Senha
    password_label = font_small.render("Senha:", True, white)
    screen.blit(password_label, (screen_width // 2 - 100, 295))  # Aumenta o espaço vertical
    input_boxes['pass'] = pygame.Rect(screen_width // 2 - 100, 320, 200, 40)
    txt_surface_pass = font_small.render(pass_text, True, white)
    screen.blit(txt_surface_pass, (input_boxes['pass'].x + 5, input_boxes['pass'].y + 5))
    pygame.draw.rect(screen, blue, input_boxes['pass'], 2)
    
    # Botão de login
    login_button = font_small.render('Entrar', True, black)
    button_box = pygame.Rect(screen_width // 2 - 100, 450, 200, 40)  # Ajustado para mais espaço
    pygame.draw.rect(screen, white, button_box)
    screen.blit(login_button, (button_box.x + 75, button_box.y + 8))
    
    # Link de cadastro
    no_account_text = font_small.render("Não tem uma conta?", True, white)
    screen.blit(no_account_text, (screen_width // 2 - no_account_text.get_width() // 2, 390))
    register_text = font_small.render("Cadastre-se", True, black if register_text_box.collidepoint(pygame.mouse.get_pos()) else white)
    register_text_box.topleft = (screen_width // 2 - register_text.get_width() // 2, 410)
    register_text_box.size = (register_text.get_width(), 30)
    screen.blit(register_text, (register_text_box.x, register_text_box.y))
    pygame.draw.rect(screen, purple, register_text_box, 1)  # Opcional

    pygame.display.flip()


def draw_register_screen():
    global name_text, email_text, dob_text, cpf_text, pass_text
    screen.fill(purple)
    # Aumenta o espaço entre cada label e input para evitar sobreposição
    base_y = 130  # Posição inicial para o primeiro label
    vertical_spacing = 75  # Espaço vertical entre cada par de label e input
    
    # Headers
    header_text = font_large.render("Cadastro", True, white)
    subheader_text = font_small.render("Crie sua conta", True, white)
    screen.blit(header_text, (screen_width // 2 - header_text.get_width() // 2, 40))
    screen.blit(subheader_text, (screen_width // 2 - subheader_text.get_width() // 2, 90))
    
    # Labels e inputs
    labels = ["Nome:", "Email:", "Data de Nascimento:", "CPF:", "Senha:"]
    inputs = [name_text, email_text, dob_text, cpf_text, pass_text]
    keys = ['name', 'email', 'dob', 'cpf', 'pass']
    
    # Ajusta as posições dos input boxes para espaçamento adequado
    for i, (label, key) in enumerate(zip(labels, keys)):
        label_y = base_y + i * vertical_spacing
        input_y = label_y + 25  # Posiciona o input box 25 pixels abaixo do label

        label_surf = font_small.render(label, True, white)
        screen.blit(label_surf, (screen_width // 2 - 100, label_y))
        
        input_boxes[key] = pygame.Rect(screen_width // 2 - 100, input_y, 200, 40)
        txt_surface = font_small.render(inputs[i], True, white)
        screen.blit(txt_surface, (input_boxes[key].x + 5, input_boxes[key].y + 5))
        pygame.draw.rect(screen, blue, input_boxes[key], 2)
    
    # Botão de cadastro ajustado para estar abaixo do último input box
    button_y = base_y + len(labels) * vertical_spacing
    button_box = pygame.Rect(screen_width // 2 - 100, button_y, 200, 40)
    register_button = font_small.render('Cadastrar', True, black)
    pygame.draw.rect(screen, white, button_box)
    screen.blit(register_button, (button_box.x + 65, button_box.y + 8))

    pygame.display.flip()

def main():
    global user_text, pass_text, name_text, email_text, dob_text, cpf_text, current_screen
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_input(event)
            elif event.type == pygame.KEYDOWN:
                handle_key_input(event)

        if current_screen == "login":
            draw_login_screen()
        elif current_screen == "register":
            draw_register_screen()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

def handle_mouse_input(event):
    global current_screen
    if current_screen == "login":
        if input_boxes['user'].collidepoint(event.pos):
            input_active['user'] = True
            input_active['pass'] = False
        elif input_boxes['pass'].collidepoint(event.pos):
            input_active['user'] = False
            input_active['pass'] = True
        elif button_box.collidepoint(event.pos):
            if user_text == 'admin' and pass_text == '123':
                print("Login Successful")
            else:
                print("Login Failed")
        elif register_text_box.collidepoint(event.pos):
            current_screen = "register"
        else:
            input_active['user'] = input_active['pass'] = False
    elif current_screen == "register":
        if input_boxes['name'].collidepoint(event.pos):
            input_active['name'] = True
            input_active['email'] = input_active['dob'] = False
        elif input_boxes['email'].collidepoint(event.pos):
            input_active['name'] = False
            input_active['email'] = True
            input_active['dob'] = False
        elif input_boxes['dob'].collidepoint(event.pos):
            input_active['name'] = False
            input_active['email'] = False
            input_active['dob'] = True
        elif button_box.collidepoint(event.pos):
            print("Register Successful")
        else:
            input_active['name'] = input_active['email'] = input_active['dob'] = False

def handle_key_input(event):
    global user_text, pass_text, name_text, email_text, dob_text
    if current_screen == "login":
        if input_active['user']:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
        elif input_active['pass']:
            if event.key == pygame.K_BACKSPACE:
                pass_text = pass_text[:-1]
            else:
                pass_text += event.unicode
    elif current_screen == "register":
        if input_active['name']:
            if event.key == pygame.K_BACKSPACE:
                name_text = name_text[:-1]
            else:
                name_text += event.unicode
        elif input_active['email']:
            if event.key == pygame.K_BACKSPACE:
                email_text = email_text[:-1]
            else:
                email_text += event.unicode
        elif input_active['dob']:
            if event.key == pygame.K_BACKSPACE:
                dob_text = dob_text[:-1]
            else:
                dob_text += event.unicode
        elif input_active['cpf']:
            if event.key == pygame.K_BACKSPACE:
                cpf_text = cpf_text[:-1]
            else:
                cpf_text += event.unicode
        elif input_active['pass']:
            if event.key == pygame.K_BACKSPACE:
                pass_text = pass_text[:-1]
            else:
                pass_text += event.unicode

if __name__ == '__main__':
    main()
