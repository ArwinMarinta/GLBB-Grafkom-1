import pygame, math
import sys


pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("GERAK LURUS BERUBAH BERATURAN")
font_j = pygame.font.SysFont(("verdana"), 11)
font = pygame.font.Font(None, 40)
screen_w = screen.get_width()
screen_h = screen.get_height()

angle = 0
s = 0
g = 0.00098
hor_v = 0
ver_v = 0
vx = 0
vy = 0
dt = 0



ball_x = screen_w // 8
ball_y = screen_h // 1.3 - 49



rotation = False
fullscreen = False
grab = False
kiri = False
kanan = False
jatuh = False
fall = False

BLACK = (0, 0, 0)
BLACK_1 = (32, 32, 32)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ABU_ABU = (128, 128, 128)
ABU = (192, 192, 192)

clock = pygame.time.Clock()

# Input box
input_box = pygame.Rect(400, 700, 50, 32)
color_inactive = pygame.Color(WHITE)
color_active = pygame.Color(GREEN)
color = color_inactive
active = False
value_input = '0'
done = False


# Membuat button kanan, kiri, dan bawah(jatuh)
button_left = pygame.Rect(300, 700, 70, 32)
button_right = pygame.Rect(600, 700, 90, 32)
button_under = pygame.Rect(1000, 700, 90, 32)
button_left_surface = font.render("LEFT", True, WHITE)
button_right_surface = font.render("RIGHT", True, WHITE)
button_under_surface = font.render("DOWN", True, WHITE)

button_left_text_rect = button_left_surface.get_rect(center=button_left.center)
button_right_text_rect = button_right_surface.get_rect(center=button_right.center)
button_under_text_rect = button_under_surface.get_rect(center=button_under.center)

ball_radius = 50
ball = pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

background_image = pygame.image.load("Backgroundd.jpg")
background_image = pygame.transform.smoothscale(background_image, (screen_w, screen_h))

def get_line_angle(x, y):
    cos = math.cos(math.radians(angle) * -1)
    sin = math.sin(math.radians(angle) * -1)
    x_ya = (x * cos) - (y * sin)
    y_ya = (x * sin) + (y * cos)
    return x_ya, y_ya

def get_angle():
    global rotation, ball_x, new_ball_x, angle
    if rotation:
        if ball_x > new_ball_x:
                angle -= ((abs(new_ball_x - ball_x) * 360) / (3.14)) / 100
        if ball_x < new_ball_x:
                angle += ((abs(new_ball_x - ball_x) * 360) / (3.14)) / 100


def scale():
    global ball, ball_radius
    if ball.centery < screen_h // 1.3:
        ball_radius = 50 - ((screen_h // 1.3 - ball.centery) // 30)
        ball_radius = max(ball_radius, 0)

def menu():
    screen.blit((0, screen_h - 100))
    pygame.draw.rect(screen, BLACK, (0, screen_h - 5, screen_w, 5))
    pygame.draw.rect(screen, BLACK, (0, screen_h - 100, screen_w, 5))

def gerak_kiri():
    global hor_v, jatuh
    if value_input:
        hor_v = -int(value_input) / 90
        jatuh = False
        get_angle()
    else :
        hor_v = 0

def gerak_kanan():
    global hor_v, jatuh
    if value_input:
        hor_v = int(value_input) / 90
        jatuh = False
        get_angle()
    else :
        hor_v = 0

def gerak_jatuh():
    global fall, jatuh
    fall = True
    jatuh = True

def move(vx, vy):
    global ball_x, ball_y, hor_v, ver_v, new_ball_x, rotation, fall
    rotation = True
    if vx != 0:
        ball_x += vx * dt
        hor_v -= hor_v/300
        get_angle()
    if hor_v > -0.005 and hor_v < 0.005:
        hor_v = 0
    if ball_x <= ball_radius:
        ball_x = ball_radius
        hor_v = -hor_v / 1.2
    if ball_x >= screen_w - ball_radius:
        ball_x = screen_w - ball_radius
        hor_v = -hor_v / 1.2
    if vy != 0:
        if ball_y <= ball_radius:
            ball_y = ball_radius
        if ball_y >= screen_h//1.3 - ball_radius:
            ball_y = screen_h//1.3 - ball_radius

def gravity():
    global vy, ball_y, new_ball_y, fall, ball_x, jatuh, ball, angle, vx
    if fall and jatuh:
        vy += g * dt * 24
        new_ball_y = ball_y + vy
        if new_ball_y >= screen_h // 1.3 - ball_radius:
            new_ball_y = screen_h // 1.3 - ball_radius
            vy = -vy * 0.9 
            if abs(vy) < 0.1:  
                fall = False
                vy = 0

        ball_y = new_ball_y

run = True
while run:

    screen.blit(background_image, (0, 0))
    dt = clock.tick_busy_loop(120)

    pygame.draw.aaline(screen, WHITE, (0, screen_h // 1.3), (screen_w, screen_h // 1.3), 2)
    pygame.draw.circle(screen, RED, ball.center, ball_radius)

    xy1, xy2 = get_line_angle(-ball_radius, 0), get_line_angle(ball_radius, 0)
    L1_xy1, L1_xy2 = (ball.centerx + xy1[0], xy1[1] + ball.centery), (ball.centerx + xy2[0], xy2[1] + ball.centery)
    L2_xy1, L2_xy2 = (ball.centerx + xy1[1], xy2[0] + ball.centery), (ball.centerx + xy2[1], xy1[0] + ball.centery)
    L1 = pygame.draw.aaline(screen, BLUE, L1_xy1, L1_xy2, 2)
    L2 = pygame.draw.aaline(screen, GREEN, L2_xy1, L2_xy2, 2)

    txt_surface = font.render(value_input, True, color)
    width = max(150, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.draw.rect(screen, BLACK, button_left)
    screen.blit(button_left_surface, button_left_text_rect)
    pygame.draw.rect(screen, BLACK, button_right)
    screen.blit(button_right_surface, button_right_text_rect)
    pygame.draw.rect(screen, BLACK, button_under)
    screen.blit(button_under_surface, button_under_text_rect)

    new_ball_x = ball_x
    new_ball_y = ball_y

    ball.center = (ball_x, ball_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive

            if ball.collidepoint(event.pos):
                grab = True
                rotation = False
                fall = False
                scale()

            if button_left.collidepoint(event.pos):
                gerak_kiri()

            if button_right.collidepoint(event.pos):
                gerak_kanan()

            if button_under.collidepoint(event.pos):
                gerak_jatuh()

        if event.type == pygame.MOUSEBUTTONUP:
            grab = False

        if event.type == pygame.MOUSEMOTION and grab:

            ball.centerx = event.pos[0]
            ball.centery = event.pos[1]

            ball_x = ball.centerx
            ball_y = ball.centery

            if ball_x < new_ball_x:
                angle += ((abs(new_ball_x - ball_x) * 360) / (3.14)) / 100
            elif ball_x > new_ball_x:
                angle -= ((abs(new_ball_x - ball_x) * 360) / (3.14)) / 100
            else:
                angle += 0

            if ball_x < ball_radius:
                ball_x = ball_radius
            elif ball_x > screen_w - ball_radius:
                ball_x = screen_w - ball_radius

            if ball_y < ball_radius:
                ball_y = ball_radius
            elif ball_y > screen_h // 1.3 - ball_radius:
                ball_y = screen_h // 1.3 - ball_radius

            ball.center = (ball_x, ball_y)

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(value_input)
                    value_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    value_input = value_input[:-1]
                elif event.key == pygame.K_DELETE:
                    value_input = ''
                else:
                    value_input += event.unicode

    move(hor_v, ver_v)
    scale()
    gravity()
    pygame.display.update()