import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Login Screen")
font = pygame.font.Font(None, 32)

# Cores
white = (255, 255, 255)
blue = (0, 0, 128)
black = (0, 0, 0)

# Variáveis para armazenar inputs
input_box_user = pygame.Rect(100, 50, 140, 32)  # Tamanho ajustado para evitar redimensionamento
input_box_pass = pygame.Rect(100, 100, 140, 32)
button_box = pygame.Rect(150, 150, 100, 32)
user_text = ''
pass_text = ''
user_active = pass_active = False

def main():
    global user_text, pass_text, user_active, pass_active

    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Define a caixa ativa baseada na localização do clique
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

            if event.type == pygame.KEYDOWN:
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

        screen.fill(white)
        # Renderizar o texto
        txt_surface_user = font.render(user_text, True, black)
        txt_surface_pass = font.render('*' * len(pass_text), True, black)
        # Desenhar o texto
        screen.blit(txt_surface_user, (input_box_user.x+5, input_box_user.y+5))
        screen.blit(txt_surface_pass, (input_box_pass.x+5, input_box_pass.y+5))
        # Desenhar as caixas de texto
        pygame.draw.rect(screen, blue, input_box_user, 2)
        pygame.draw.rect(screen, blue, input_box_pass, 2)
        # Desenhar o botão
        pygame.draw.rect(screen, blue, button_box)
        btn_text = font.render('Login', True, white)
        screen.blit(btn_text, (button_box.x+15, button_box.y+5))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
