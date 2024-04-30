from datetime import datetime
import pygame
import sys
import os
from models import Bd_postgres  # Certifique-se de que o caminho de importação está correto

# Inicializa o Pygame
pygame.init()

# Importando a conexão com o banco de dados
bd = Bd_postgres()
bd.create_connection()

# Configurações da tela
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Carteira de Investimentos")

# Carregar e configurar a fonte
font_path = os.path.join('fonts', 'Poppins-Regular.ttf')
font_small = pygame.font.Font(font_path, 16)
font_medium = pygame.font.Font(font_path, 20)
font_large = pygame.font.Font(font_path, 40)

# Cores
purple = (123, 120, 255)
light_purple = (184, 146, 255)
white = (255, 255, 255)
blue = (0, 0, 128)
black = (0, 0, 0)
red = (255, 20, 59)
light_red = (255, 59, 59)
marine_blue = (35,35,142)
light_marine_blue = (60, 60, 180)

# Estado da aplicação
current_screen = "login"
selected_index = None 

# Variáveis de texto para inputs
user_text = ''
pass_text = ''
name_text = ''
email_text = ''
dob_text = ''
cpf_text = ''
asset_code_text = ''
quantity_text = ''
average_price_text = ''
account_number_text = ''
button_rects = []

# Ativação de inputs
input_user = {'user': False, 'pass': False, 'name': False, 'email': False, 'dob': False, 'cpf': False}
input_oper = {'ticker': False, 'quant': False, "p_medio": False}

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
    border_color = white if pygame.mouse.get_pressed()[0] and input_boxes['user'].collidepoint(pygame.mouse.get_pos()) else blue
    pygame.draw.rect(screen, border_color, input_boxes['user'], 2, border_radius=5)
    
    # Label e Input para Senha
    password_label = font_small.render("Senha:", True, white)
    screen.blit(password_label, (screen_width // 2 - 100, 295))  # Aumenta o espaço vertical
    input_boxes['pass'] = pygame.Rect(screen_width // 2 - 100, 320, 200, 40)
    txt_surface_pass = font_small.render(pass_text, True, white)
    screen.blit(txt_surface_pass, (input_boxes['pass'].x + 5, input_boxes['pass'].y + 5))
    border_color = white if pygame.mouse.get_pressed()[0] and input_boxes['pass'].collidepoint(pygame.mouse.get_pos()) else blue
    pygame.draw.rect(screen, border_color, input_boxes['pass'], 2, border_radius=5)
    
    # Botão de login
    login_button = font_small.render('Entrar', True, black)
    button_box = pygame.Rect(screen_width // 2 - 100, 470, 200, 40)  # Ajustado para mais espaço
    button_color = light_purple if button_box.collidepoint(pygame.mouse.get_pos()) else white
    pygame.draw.rect(screen, button_color, button_box, border_radius=15)
    screen.blit(login_button, (button_box.x + 75, button_box.y + 8))
    
    # Link de cadastro
    no_account_text = font_small.render("Não tem uma conta?", True, white)
    screen.blit(no_account_text, (screen_width // 2 - no_account_text.get_width() // 2, 390))
    register_text = font_small.render("Cadastre-se", True, black if register_text_box.collidepoint(pygame.mouse.get_pos()) else white)
    register_text_box.topleft = (screen_width // 2 - register_text.get_width() // 2, 410)
    register_text_box.size = (register_text.get_width(), 30)
    screen.blit(register_text, (register_text_box.x, register_text_box.y))
    pygame.draw.rect(screen, purple, register_text_box, 1)

    pygame.display.flip()

def draw_register_screen():
    global name_text, email_text, dob_text, cpf_text, pass_text
    screen.fill(purple)
    # Aumenta o espaço entre cada label e input para evitar sobreposição
    base_y = 130  # Posição inicial para o primeiro label
    vertical_spacing = 70  # Espaço vertical entre cada par de label e input
    
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
        
        input_boxes[key] = pygame.Rect(screen_width // 2 - 100, input_y, 200, 35)
        txt_surface = font_small.render(inputs[i], True, white)
        screen.blit(txt_surface, (input_boxes[key].x + 5, input_boxes[key].y + 5))
        border_color = white if pygame.mouse.get_pressed()[0] and input_boxes[key].collidepoint(pygame.mouse.get_pos()) else blue
        pygame.draw.rect(screen, border_color, input_boxes[key], 2, border_radius=5)
    
    # Botão de cadastro ajustado para estar abaixo do último input box
    button_y = base_y + len(labels) * vertical_spacing
    button_box = pygame.Rect(screen_width // 2 - 100, button_y, 200, 40)
    register_button = font_small.render('Cadastrar', True, black)
    button_color = light_purple if button_box.collidepoint(pygame.mouse.get_pos()) else white
    pygame.draw.rect(screen, button_color, button_box, border_radius=15)
    screen.blit(register_button, (button_box.x + 65, button_box.y + 8))

    pygame.display.flip()

def draw_main_screen(selected_index=None):
    global button_rects
    screen.fill(purple)
    # Divisão de tela
    menu_width = 300
    content_width = screen_width - menu_width

    # Área do menu à esquerda
    pygame.draw.rect(screen, marine_blue, [0, 0, menu_width, screen_height])

    # Área de conteúdo à direita
    pygame.draw.rect(screen, purple, [menu_width, 0, content_width, screen_height])

    # Renderiza o cabeçalho e o subcabeçalho centrados dentro da área do menu
    header_text = font_medium.render("Você está na sua Carteira", True, white)
    header2_text = font_small.render("O que você deseja fazer?", True, white)
    screen.blit(header_text, ((menu_width - header_text.get_width()) // 2, 50))
    screen.blit(header2_text, ((menu_width - header2_text.get_width()) // 2, 110))

    buttons_text = ["Realizar Compra", "Realizar Venda", "Histórico de Operações", "Carteira Resumida", "Mostrar Perfil", "Sair"]
    button_rects = []
    start_y = 150

    for index, text in enumerate(buttons_text):
        if index == 5:
            # Botão Sair é menor na largura e mais abaixo
            small_btn_width = 180  # Largura menor para o botão Sair
            btn_rect = pygame.Rect(menu_width / 2 - small_btn_width / 2, start_y + (index * 60 + 50), small_btn_width, 40)
            button_color = red if btn_rect.collidepoint(pygame.mouse.get_pos()) else light_red
            pygame.draw.rect(screen, button_color, btn_rect, border_radius=15)
        else:
            btn_rect = pygame.Rect(10, start_y + index * 60, menu_width - 20, 50)
            button_color = light_marine_blue if (index == selected_index or btn_rect.collidepoint(pygame.mouse.get_pos())) else black
            pygame.draw.rect(screen, button_color, btn_rect, border_radius=15)  # Usa a cor clara para o botão selecionado

        btn_text = font_small.render(text, True, white)
        screen.blit(btn_text, (btn_rect.x + (btn_rect.width - btn_text.get_width()) // 2, btn_rect.y + (btn_rect.height - btn_text.get_height()) // 2))
        button_rects.append(btn_rect)

    # Conteúdo à direita baseado no botão selecionado
    if selected_index is not None:
        if selected_index == 0:
            perform_purchase(menu_width, content_width)
        elif selected_index == 1:
            perform_sale(menu_width, content_width)
        elif selected_index == 2:
            show_transaction_history(menu_width, content_width)
        elif selected_index == 3:
            show_wallet_summary(menu_width, content_width)
        elif selected_index == 4:
            show_profile(menu_width, content_width)
        elif selected_index == 5:
            exit_application()

    pygame.display.flip()

def perform_purchase(menu_width, content_width):
    # Limpa a área de conteúdo
    pygame.draw.rect(screen, purple, [menu_width, 0, content_width, screen_height])

    # Cabeçalho para a compra de ativos
    header_text = font_large.render("Compra", True, white)
    header_x = menu_width + (content_width - header_text.get_width()) // 2  # Centraliza o cabeçalho
    screen.blit(header_text, (header_x, 70))

    # Labels e Inputs para a compra
    labels = ['Código do ativo:', 'Quantidade:', 'Preço Médio:']
    texts = [asset_code_text, quantity_text, average_price_text]
    y_offset = 150
    input_width = content_width - 240  # Diminui a largura das caixas de input
    input_x = menu_width + (content_width - input_width) // 2  # Centraliza as caixas de input
    for i, label in enumerate(labels):
        label_surf = font_small.render(label, True, white)
        input_rect = pygame.Rect(input_x, y_offset + 70 * i, input_width, 40)  # Altura da caixa ajustada para 40
        pygame.draw.rect(screen, white, input_rect, border_radius=5)
        text_surf = font_medium.render(texts[i], True, black)
        screen.blit(label_surf, (input_x, y_offset + 70 * i - 30))
        text_x = input_rect.x + 10  # Posiciona o texto um pouco para a direita dentro da caixa
        screen.blit(text_surf, (text_x, input_rect.y + (input_rect.height - text_surf.get_height()) // 2))

    # Botão para realizar a compra
    buy_button_rect = pygame.Rect(input_x, y_offset + 70 * len(labels) + 10, input_width, 50)
    pygame.draw.rect(screen, blue, buy_button_rect, border_radius=15)
    buy_button_text = font_medium.render("Registrar", True, white)
    buy_button_text_x = input_x + (input_width - buy_button_text.get_width()) // 2
    screen.blit(buy_button_text, (buy_button_text_x, buy_button_rect.y + (buy_button_rect.height - buy_button_text.get_height()) // 2))

    pygame.display.flip()

def perform_sale(menu_width, content_width):
    # Limpa a área de conteúdo
    pygame.draw.rect(screen, purple, [menu_width, 0, content_width, screen_height])

    # Cabeçalho para a venda de ativos
    header_text = font_large.render("Venda", True, white)
    header_x = menu_width + (content_width - header_text.get_width()) // 2  # Centraliza o cabeçalho
    screen.blit(header_text, (header_x, 70))

    # Labels e Inputs para a venda
    labels = ['Código do ativo:', 'Quantidade:', 'Preço Médio:']
    texts = [asset_code_text, quantity_text, average_price_text]
    y_offset = 150
    input_width = content_width - 240  # Diminui a largura das caixas de input
    input_x = menu_width + (content_width - input_width) // 2  # Centraliza as caixas de input
    for i, label in enumerate(labels):
        label_surf = font_small.render(label, True, white)
        input_rect = pygame.Rect(input_x, y_offset + 70 * i, input_width, 40)  # Altura da caixa ajustada para 40
        pygame.draw.rect(screen, white, input_rect, border_radius=5)
        text_surf = font_medium.render(texts[i], True, black)
        screen.blit(label_surf, (input_x, y_offset + 70 * i - 30))
        text_x = input_rect.x + 10  # Posiciona o texto um pouco para a direita dentro da caixa
        screen.blit(text_surf, (text_x, input_rect.y + (input_rect.height - text_surf.get_height()) // 2))

    # Botão para realizar a venda
    buy_button_rect = pygame.Rect(input_x, y_offset + 70 * len(labels) + 10, input_width, 50)
    pygame.draw.rect(screen, blue, buy_button_rect, border_radius=15)
    buy_button_text = font_medium.render("Registrar", True, white)
    buy_button_text_x = input_x + (input_width - buy_button_text.get_width()) // 2
    screen.blit(buy_button_text, (buy_button_text_x, buy_button_rect.y + (buy_button_rect.height - buy_button_text.get_height()) // 2))

    pygame.display.flip()

def show_transaction_history(menu_width, content_width):
    # Limpa a área de conteúdo
    pygame.draw.rect(screen, purple, [menu_width, 0, content_width, screen_height])

    # Cabeçalho para o histórico de operações
    header_text = font_large.render("Histórico de Operações", True, white)
    header_x = menu_width + (content_width - header_text.get_width()) // 2  # Centraliza o cabeçalho
    screen.blit(header_text, (header_x, 70))

    pygame.display.flip()

def show_wallet_summary(menu_width, content_width):
    # Limpa a área de conteúdo
    pygame.draw.rect(screen, purple, [menu_width, 0, content_width, screen_height])

    # Cabeçalho para a carteira resumida
    header_text = font_large.render("Carteira Resumida", True, white)
    header_x = menu_width + (content_width - header_text.get_width()) // 2  # Centraliza o cabeçalho
    screen.blit(header_text, (header_x, 70))

    pygame.display.flip()

def show_profile(menu_width, content_width):
    # Limpa a área de conteúdo
    pygame.draw.rect(screen, purple, [menu_width, 0, content_width, screen_height])

    # Cabeçalho para o perfil do usuário
    header_text = font_large.render("Perfil", True, white)
    header_x = menu_width + (content_width - header_text.get_width()) // 2  # Centraliza o cabeçalho
    screen.blit(header_text, (header_x, 70))

    # Labels e Inputs para a compra
    labels = ['Número da Conta:', 'Nome:', 'Email:', 'Data de Nascimento:']
    texts = [asset_code_text, name_text, email_text, dob_text]
    y_offset = 150
    input_width = content_width - 240  # Diminui a largura das caixas de input
    input_x = menu_width + (content_width - input_width) // 2  # Centraliza as caixas de input
    for i, label in enumerate(labels):
        label_surf = font_small.render(label, True, white)
        input_rect = pygame.Rect(input_x, y_offset + 70 * i, input_width, 40)  # Altura da caixa ajustada para 40
        pygame.draw.rect(screen, white, input_rect, border_radius=5)
        text_surf = font_medium.render(texts[i], True, black)
        screen.blit(label_surf, (input_x, y_offset + 70 * i - 30))
        text_x = input_rect.x + 10  # Posiciona o texto um pouco para a direita dentro da caixa
        screen.blit(text_surf, (text_x, input_rect.y + (input_rect.height - text_surf.get_height()) // 2))

    # Botão para atualizar o perfil
    buy_button_rect = pygame.Rect(input_x, y_offset + 70 * len(labels) + 10, input_width, 50)
    pygame.draw.rect(screen, blue, buy_button_rect, border_radius=15)
    buy_button_text = font_medium.render("Atualizar", True, white)
    buy_button_text_x = input_x + (input_width - buy_button_text.get_width()) // 2
    screen.blit(buy_button_text, (buy_button_text_x, buy_button_rect.y + (buy_button_rect.height - buy_button_text.get_height()) // 2))

    pygame.display.flip()

def exit_application():
    print("Exiting Application...")
    sys.exit()

def draw_popup(message):
    #Desenha um pop-up de erro na tela e espera o usuário fechar.#
    popup_width = 600
    popup_height = 200
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    
    # Desenha o fundo do pop-up
    pygame.draw.rect(screen, white, popup_rect)
    pygame.draw.rect(screen, black, popup_rect, 3)
    
    # Mensagem de erro
    error_text = font_medium.render(message, True, red)
    text_x = popup_x + (popup_width - error_text.get_width()) // 2
    text_y = popup_y + (popup_height - error_text.get_height()) // 2
    screen.blit(error_text, (text_x, text_y))

    # Botão Ok
    ok_button_text = font_small.render("Ok", True, white)
    ok_button_width = 100
    ok_button_height = 40
    ok_button_x = popup_x + (popup_width - ok_button_width) // 2
    ok_button_y = popup_y + popup_height - ok_button_height - 30
    ok_button_rect = pygame.Rect(ok_button_x, ok_button_y, ok_button_width, ok_button_height)
    pygame.draw.rect(screen, marine_blue, ok_button_rect)  # Botão azul
    screen.blit(ok_button_text, (ok_button_x + (ok_button_width - ok_button_text.get_width()) // 2,
                                 ok_button_y + (ok_button_height - ok_button_text.get_height()) // 2))

    pygame.display.flip()  # Atualiza a tela para mostrar o pop-up
    
    # Loop para manter o pop-up visível
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  # Fecha o pop-up se o mouse é clicado
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False  # Fecha o pop-up se ENTER é pressionado

    # Redesenha a tela onde o pop-up foi chamado para restaurar a vista anterior
    if current_screen == "register":
        draw_register_screen()
    elif current_screen == "login":
        draw_login_screen()
    elif current_screen == "main":
        draw_main_screen(selected_index)

def login_check(cpf, senha):
    # Verifica se o cpf e a senha correspondem a algum usuário no banco
    user_data = bd.select_where("clients", cpf=cpf, senha=senha)
    if user_data:
        print("Login Successful")
        return True
    else:
        draw_popup("CPF ou senha incorretos.")
        return False
    
def register_new_user(name, email, dob, cpf, senha):
    try:
        # Formata a data de nascimento
        dob_formatted = datetime.strptime(dob, "%d/%m/%Y").date()
        bd.inserir("clients", (name, email, dob_formatted, cpf, senha))
        print("Register Successful")
        return True
    except Exception as e:
        draw_popup(str(e))
        return False

def handle_mouse_input(event):
    global current_screen, selected_index
    if current_screen == "login":
        if input_boxes['user'].collidepoint(event.pos):
            input_user['user'] = True 
            reset_other_input_user('user')
        elif input_boxes['pass'].collidepoint(event.pos):
            input_user['pass'] = True
            reset_other_input_user('pass')
        elif button_box.collidepoint(event.pos):
            if not user_text or not pass_text:
                draw_popup("CPF e senha são obrigatórios.")
            elif login_check(user_text, pass_text):
                current_screen = "main"
        elif register_text_box.collidepoint(event.pos):
            current_screen = "register"
        else:
            input_user['user'] = input_user['pass'] = False
    if current_screen == "register":
        if button_box.collidepoint(event.pos):
            if all([name_text, email_text, dob_text, cpf_text, pass_text]):
                if register_new_user(name_text, email_text, dob_text, cpf_text, pass_text):
                    current_screen = "login"
            else:
                draw_popup("Todos os campos devem ser preenchidos.")

    elif current_screen == "main":
        for i, rect in enumerate(button_rects):
            if rect.collidepoint(event.pos):
                selected_index = i
                print(f"Button {i} clicked")  # Placeholder para ação de cada botão

def reset_other_input_user(active_key):
    global input_user
    for key in input_user:
        if key != active_key:
            input_user[key] = False

def reset_all_input_user():
    global input_user
    for key in input_user:
        input_user[key] = False

def handle_key_input(event):
    global user_text, pass_text, name_text, email_text, dob_text, cpf_text  

    if current_screen == "login":
        if input_user['user']:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
        elif input_user['pass']:
            if event.key == pygame.K_BACKSPACE:
                pass_text = pass_text[:-1]
            else:
                pass_text += event.unicode
    elif current_screen == "register":
        if input_user['name']:
            if event.key == pygame.K_BACKSPACE:
                name_text = name_text[:-1]
            else:
                name_text += event.unicode
        elif input_user['email']:
            if event.key == pygame.K_BACKSPACE:
                email_text = email_text[:-1]
            else:
                email_text += event.unicode
        elif input_user['dob']:
            if event.key == pygame.K_BACKSPACE:
                dob_text = dob_text[:-1]
            else:
                dob_text += event.unicode
        elif input_user['cpf']:
            if event.key is pygame.K_BACKSPACE:
                cpf_text = cpf_text[:-1]
            else:
                cpf_text += event.unicode
        elif input_user['pass']:
            if event.key == pygame.K_BACKSPACE:
                pass_text = pass_text[:-1]
            else:
                pass_text += event.unicode

def main():
    global current_screen, selected_index
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
        elif current_screen == "main":
            draw_main_screen(selected_index)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
