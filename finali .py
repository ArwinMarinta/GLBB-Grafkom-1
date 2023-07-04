import pygame, sys
from pygame import gfxdraw

# init
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Lensa cembung")
font = pygame.font.SysFont(("verdana"), 11)
mainClock = pygame.time.Clock()

# warna
fullscreen = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)

# Membuat class slider
class Slider():
    def __init__(self, name, val, max, min, posx, posy):
        self.val = val
        self.max = max
        self.min = min
        self.xpos = posx
        self.ypos = posy
        self.hit = False

        # membuat permukaan(surface) dan teks yang akan ditampilkan dalam surface
        self.surf = pygame.surface.Surface((100, 50))
        self.txt_surf = font.render(name, 1, BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))
        self.surf.fill(ORANGE)

        # Membuat element didalam surface
        self.surf.blit(self.txt_surf, self.txt_rect)
        self.button_rect = None
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(WHITE)
        self.button_surf.set_colorkey(WHITE)
        pygame.draw.circle(self.button_surf, BLACK, (10, 10), 5, 0)
        pygame.draw.rect(self.surf, GREY, [0, 0, 100, 50], 2)
        pygame.draw.rect(self.surf, WHITE, [10, 30, 80, 5], 0)

    # Mengambar slider di dalam surface yang telah dibuat
    def draw(self, surface):
        surf = self.surf.copy()
        pos = (10 + int((self.val - self.min) / (self.max - self.min) * 80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)
        surface.blit(surf, (self.xpos, self.ypos))

    # fungsi agar slider bisa di geser
    def move(self):
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.max - self.min) + self.min
        if self.val < self.min:
            self.val = abs(self.min)
        if self.val > self.max:
            self.val = abs(self.max)


# Membuat class input box
class input_Box:
    allInputBox = []

    def __init__(self, xy, wh, val):
        self.rect = pygame.Rect(xy, wh)
        self.val = val
        self.text = str(val)
        self.active = False
        self.change = False

    # Merender atau Membuat input box muncul di screen
    def render(self, surface):
        if self.active:
            text_obj = font.render(str(self.text), True, WHITE)
        else:
            self.text = str(self.val)
            text_obj = font.render(str(self.text), True, WHITE)
        surface.blit(text_obj, (self.rect.x, self.rect.y))


def ddaAlgortihm(xy1, xy2, color):
    x = xy1[0]
    y = xy1[1]
    dx = xy2[0] - xy1[0]
    dy = xy2[1] - xy1[1]
    maxValue = max(abs(dx), abs(dy))
    try:
        x_inc = dx / maxValue
        y_inc = dy / maxValue
    except ZeroDivisionError:
        return 0
    for i in range(maxValue):
        x += x_inc
        y += y_inc
        gfxdraw.pixel(screen, round(x), round(y), color)


def quadran(x, y):
    x = screen.get_width() // 2 + x * -1
    y = screen.get_height() // 2 + y * -1
    return x, y

def gradien(xy1, xy2):
    try:
        m = (xy2[1] - xy1[1]) / (xy2[0] - xy1[0])
    except ZeroDivisionError:
        m = 0
    return m

def LSV(xy1, xy2, length):
    m = gradien(xy1, xy2)
    y = xy2[1] + m * (length - xy2[0])
    return length, y

def teks (xy1, xy2, color, text):
    text_surface = font.render(text, color, WHITE)
    screen.blit(text_surface, (xy1, xy2))

# inisiasi
position = Slider(f"Jarak Benda", 0, screen.get_width() / 2 , -600, 1080, 20)
pen = Slider(f"Tinggi Benda", 0, screen.get_height() / 2 , -400, 1080, 80)
lensa = Slider(f"Titik Fokus", 0, screen.get_width() / 2, 0, 1080, 140)
slider = [pen, position, lensa]


def main():
    global LEFT, RIGHT, UP, DOWN, DOWNFOKUS, UPFOKUS
    # Input BOX
    jarak_benda_update = input_Box((0, 0), (100, 20), position.val)
    tinggi_benda_update = input_Box((0, 0), (100, 20), pen.val)
    titik_fokus_update = input_Box((0, 0), (100, 20), lensa.val)
    
    run = True
    while run:
        screen.fill(BLACK)
        events = pygame.event.get()

        # Handle Input TEXT
        if jarak_benda_update.change:
            position.val = jarak_benda_update.val
            jarak_benda_update.change = False
            jarak_benda_update.val = abs
        else:
            jarak_benda_update.val = abs(position.val)

        if tinggi_benda_update.change:
            pen.val = tinggi_benda_update.val
            tinggi_benda_update.change = False
            tinggi_benda_update.val = abs
        else:
            tinggi_benda_update.val = (pen.val)

        if titik_fokus_update.change:
            lensa.val = titik_fokus_update.val
            titik_fokus_update.change = False
        else:
            titik_fokus_update.val = lensa.val

        try:
            jarak_bayangan = ((lensa.val * position.val) / (position.val - lensa.val) * -1)
        except ZeroDivisionError:
            jarak_bayangan = 0
        try:
            tinggi_bayangan = (jarak_bayangan / position.val) * pen.val
        except ZeroDivisionError:
            tinggi_bayangan = 0

        # Membuat garis vertikal dan horizontal
        x1, y1 = 0, screen.get_height() // 2
        x2, y2 = screen.get_width(), screen.get_height() // 2
        ddaAlgortihm((x1, y1), (x2, y2), WHITE)

        x1, y1 = screen.get_width() // 2, 0
        x2, y2 = screen.get_width() // 2, screen.get_height()
        ddaAlgortihm((x1, y1), (x2, y2), WHITE)

        # LENSA
        r = pygame.Rect(585, 0, 30, 800)
        pygame.draw.ellipse(screen, ORANGE, r, 1)

        # titik fokus depan
        x1, y1 = quadran(round(lensa.val), 0)
        x2, y2 = quadran(round(lensa.val), 10)
        ddaAlgortihm((x1, y1), (x2, y2), RED)
        teks((x2,y1), (x2,y2), WHITE, "F")

        # titik fokus belakang
        x1, y1 = quadran(-1 * (round(lensa.val)), 0)
        x2, y2 = quadran(-1 * (round(lensa.val)), 10)
        ddaAlgortihm((x1, y1), (x2, y2), RED)
        teks((x1,y1), (x2,y2), WHITE, "F'")

        # titik kelengkungan depan
        x1, y1 = quadran(round(lensa.val) * 2, 0)
        x2, y2 = quadran(round(lensa.val) * 2, 10)
        ddaAlgortihm((x1, y1), (x2, y2), RED)
        teks((x1,y1), (x2,y2), WHITE, "2F")

        # titik kelengkungan belakang
        x1, y1 = quadran(-1 * (round(lensa.val) * 2), 0)
        x2, y2 = quadran(-1 * (round(lensa.val) * 2), 10)
        ddaAlgortihm((x1, y1), (x2, y2), RED)
        teks((x1,y1), (x2,y2), WHITE, "2F'")

        # Sinar istimewa 1 Sinar datang sejajar sumbu utama di depan lensa
        x1, y1 = quadran(round(position.val), round(pen.val))
        x2, y2 = quadran(0, round(pen.val))
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2))
        if round(position.val) < 0:
            pygame.draw.line(screen, RED, (x1, y1), (screen.get_width(), y2))
        else:
            pygame.draw.line(screen, RED, (x1, y1), (0, y2))

        # sinar bias 1 yang akan dibiaskan ke titik fokus yang ada di belakang lensa
        x1, y1 = quadran(0, round(pen.val))
        x2, y2 = quadran(jarak_bayangan, tinggi_bayangan)
        if jarak_bayangan < 0:
            x2, y2 = LSV((x1, y1), (x2, y2), screen.get_width())
        else:
            x2, y2 = LSV((x1, y1), (x2, y2), 0)
        pygame.draw.line(screen, MAGENTA, (x1, y1), (x2, y2), )

        # Sinar istimewa 2 Sinar datang menuju titik fokus 1 di depan lensa
        x1, y1 = quadran(0, tinggi_bayangan)
        x2, y2 = quadran(round(position.val), round(pen.val))
        if round(position.val) < 0:
            x2, y2 = LSV((x1, y1), (x2, y2), screen.get_width())
        else:
            x2, y2 = LSV((x1, y1), (x2, y2), 0)
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2))

        # Sinar bias 2 yang dibiaskan sejajar dengan sumbu utama
        x1, y1 = quadran(jarak_bayangan, tinggi_bayangan)
        x2, y2 = quadran(0, tinggi_bayangan)
        pygame.draw.line(screen, MAGENTA, (x1, y1), (x2, y2))
        if jarak_bayangan < 0:
            pygame.draw.line(screen, MAGENTA, (x1, y1), (screen.get_width(), y2))
        else:
            pygame.draw.line(screen, MAGENTA, (x1, y1), (0, y2))

        # Sinar istimewa 3 Sinar yang datang melewati pusat optik lensa
        x1, y1 = quadran(0, 0)
        x2, y2 = quadran(round(position.val), round(pen.val))
        if round(position.val) < 0:
            x2, y2 = LSV((x1, y1), (x2, y2), screen.get_width())
        else:
            x2, y2 = LSV((x1, y1), (x2, y2), 0)
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2))

        # Sinar istimewa 3 Sinar yang diteruskan dari pusat optik lensa
        x1, y1 = quadran(0, 0)
        x1, y1 = quadran(0, 0)
        x2, y2 = quadran(jarak_bayangan, tinggi_bayangan)
        if jarak_bayangan < 0:
            x2, y2 = LSV((x1, y1), (x2, y2), screen.get_width())
        else:
            x2, y2 = LSV((x1, y1), (x2, y2), 0)
        pygame.draw.line(screen, MAGENTA, (x1, y1), (x2, y2))

        # BENDA
        x1, y1 = quadran(position.val, 0)
        x2, y2 = quadran(position.val, pen.val)
        pygame.draw.aaline(screen, BLACK, (x1, y1), (x2, y2))

        pygame.draw.aaline(screen, ORANGE, quadran((position.val + (pen.val // 20)), pen.val//1.1), (x2, y2))
        pygame.draw.aaline(screen, ORANGE, quadran((position.val - (pen.val // 20)), pen.val // 1.1), (x2, y2))
        pygame.draw.aaline(screen, ORANGE, quadran((position.val + (pen.val // 30)), pen.val // 1.2), quadran((position.val + (pen.val // 20)), pen.val // 1.1))
        pygame.draw.aaline(screen, ORANGE, quadran((position.val - (pen.val // 30)), pen.val // 1.2), quadran((position.val - (pen.val // 20)), pen.val // 1.1))

        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 12)), pen.val // 1.2), quadran((position.val - (pen.val // 12)), pen.val // 1.2))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 12)), pen.val // 1.2), quadran((position.val + (pen.val // 12)), pen.val // 1.2))
        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 12)), pen.val // 1.25), quadran((position.val - (pen.val // 12)), pen.val // 1.25))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 12)), pen.val // 1.25), quadran((position.val + (pen.val // 12)), pen.val // 1.25))
        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 12)), pen.val // 1.25), quadran((position.val + (pen.val // 12)), pen.val // 1.2))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 12)), pen.val // 1.25), quadran((position.val - (pen.val // 12)), pen.val // 1.2))

        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 12)), pen.val // 5), quadran((position.val + (pen.val // 25)), pen.val // 1.25))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 12)), pen.val // 5), quadran((position.val - (pen.val // 25)), pen.val // 1.25))

        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 3)), pen.val // 5), quadran(position.val, pen.val // 5))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 3)), pen.val // 5), quadran(position.val, pen.val // 5))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 3)), pen.val // 6), quadran(position.val, pen.val // 6))
        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 3)), pen.val // 6), quadran(position.val, pen.val // 6))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 3)), pen.val // 5), quadran((position.val - (pen.val // 3)), pen.val // 6))
        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 3)), pen.val // 5), quadran((position.val + (pen.val // 3)), pen.val // 6))

        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 8)),  pen.val // 20), quadran((position.val + (pen.val // 3.2)), pen.val // 6))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 8)),  pen.val // 20), quadran((position.val - (pen.val // 3.2)), pen.val // 6))

        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 4)), pen.val // 20), quadran(position.val, pen.val //20))
        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 4)), pen.val // 20), quadran(position.val, pen.val // 20))
        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 4)), 0), quadran((position.val + (pen.val // 4)), pen.val // 20))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 4)), 0), quadran((position.val - (pen.val // 4)), pen.val // 20))
        pygame.draw.aaline(screen, GREEN, quadran((position.val + (pen.val // 4)), 0), quadran(position.val, 0))
        pygame.draw.aaline(screen, GREEN, quadran((position.val - (pen.val // 4)), 0), quadran(position.val, 0))


        #bayangan benda
        x1, y1 = quadran(jarak_bayangan, 0)
        x2, y2 = quadran(jarak_bayangan, tinggi_bayangan)
        pygame.draw.aaline(screen, BLACK, (x1, y1), (x2, y2))
        pygame.draw.aaline(screen, RED, quadran((jarak_bayangan - (tinggi_bayangan // 20)), tinggi_bayangan // 1.1), (x2, y2))
        pygame.draw.aaline(screen, RED, quadran((jarak_bayangan + (tinggi_bayangan // 20)), tinggi_bayangan // 1.1), (x2, y2))
        pygame.draw.aaline(screen, RED, quadran((jarak_bayangan + (tinggi_bayangan // 30)), tinggi_bayangan // 1.2), quadran((jarak_bayangan + (tinggi_bayangan // 20)), tinggi_bayangan // 1.1))
        pygame.draw.aaline(screen, RED, quadran((jarak_bayangan - (tinggi_bayangan // 30)), tinggi_bayangan // 1.2), quadran((jarak_bayangan - (tinggi_bayangan // 20)), tinggi_bayangan // 1.1))

        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 12)), tinggi_bayangan // 1.2), quadran((jarak_bayangan - (tinggi_bayangan // 12)), tinggi_bayangan // 1.2))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 12)), tinggi_bayangan // 1.2), quadran((jarak_bayangan + (tinggi_bayangan // 12)), tinggi_bayangan // 1.2))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 12)), tinggi_bayangan // 1.25), quadran((jarak_bayangan - (tinggi_bayangan // 12)), tinggi_bayangan // 1.25))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 12)), tinggi_bayangan // 1.25), quadran((jarak_bayangan + (tinggi_bayangan // 12)), tinggi_bayangan // 1.25))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 12)), tinggi_bayangan // 1.25), quadran((jarak_bayangan + (tinggi_bayangan // 12)), tinggi_bayangan // 1.2))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 12)), tinggi_bayangan // 1.25), quadran((jarak_bayangan - (tinggi_bayangan // 12)), tinggi_bayangan // 1.2))

        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 12)), tinggi_bayangan // 5), quadran((jarak_bayangan + (tinggi_bayangan // 25)), tinggi_bayangan // 1.25))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 12)), tinggi_bayangan // 5), quadran((jarak_bayangan - (tinggi_bayangan // 25)), tinggi_bayangan // 1.25))

        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 3)), tinggi_bayangan // 5), quadran(jarak_bayangan, tinggi_bayangan // 5))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 3)), tinggi_bayangan // 5), quadran(jarak_bayangan, tinggi_bayangan // 5))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 3)), tinggi_bayangan // 6), quadran(jarak_bayangan, tinggi_bayangan // 6))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 3)), tinggi_bayangan // 6), quadran(jarak_bayangan, tinggi_bayangan // 6))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 3)), tinggi_bayangan // 5), quadran((jarak_bayangan + (tinggi_bayangan // 3)), tinggi_bayangan // 6))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 3)), tinggi_bayangan // 5), quadran((jarak_bayangan - (tinggi_bayangan // 3)), tinggi_bayangan // 6))

        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 8)), tinggi_bayangan // 20),quadran((jarak_bayangan - (tinggi_bayangan // 3.2)), tinggi_bayangan // 6))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 8)), tinggi_bayangan // 20), quadran((jarak_bayangan + (tinggi_bayangan // 3.2)), tinggi_bayangan // 6))

        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 4)), tinggi_bayangan // 20), quadran(jarak_bayangan, tinggi_bayangan // 20))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 4)), tinggi_bayangan // 20), quadran(jarak_bayangan, tinggi_bayangan // 20))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 4)), 0), quadran((jarak_bayangan - (tinggi_bayangan // 4)), tinggi_bayangan // 20))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 4)), 0), quadran((jarak_bayangan + (tinggi_bayangan // 4)), tinggi_bayangan // 20))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan - (tinggi_bayangan // 4)), 0), quadran(jarak_bayangan, 0))
        pygame.draw.aaline(screen, YELLOW, quadran((jarak_bayangan + (tinggi_bayangan // 4)), 0), quadran(jarak_bayangan, 0))

        text = [
            f"Jarak benda= ",
            f"Tinggi benda = ",
            f"Fokus Lensa = ",
            f"Jarak Bayangan = ",
            f"Tinggi Bayangan = "
        ]
        value = [
            jarak_benda_update,
            tinggi_benda_update,
            titik_fokus_update,
            (int(jarak_bayangan) * -1),
            (int(tinggi_bayangan) * -1)
        ]
        x1 = 1150
        y1 = 200
        for k, val in zip(text, value):
            text_obj = font.render(k, False, WHITE)
            text_rect = text_obj.get_rect(topright=(x1, y1))
            screen.blit(text_obj, text_rect)
            if type(val) == int:
                val_obj = font.render(str(val), False, WHITE)
                screen.blit(val_obj, (x1, y1))
            else:
                val.rect.x = x1
                val.rect.y = y1
                val.render(screen)

            y1 += 15

        # Text Box and Input END
        # HANDLE SEMUA EVENT YANG TERJADI
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                UP = True
            else:
                UP = False
            if keys[pygame.K_DOWN]:
                DOWN = True
            else:
                DOWN = False
            if keys[pygame.K_LEFT]:
                LEFT = True
            else:
                LEFT = False
            if keys[pygame.K_RIGHT]:
                RIGHT = True
            else:
                RIGHT = False
            if keys[pygame.K_s]:
                DOWNFOKUS = True
            else:
                DOWNFOKUS = False
            if keys[pygame.K_w]:
                UPFOKUS = True
            else:
                UPFOKUS = False

            # HANDLES BUTTON PRESSES
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button_keys['left_arrow']:
                    LEFT = True
                if event.button == button_keys['right_arrow']:
                    RIGHT = True
                if event.button == button_keys['down_arrow']:
                    DOWN = True
                if event.button == button_keys['up_arrow']:
                    UP = True

            # HANDLES BUTTON RELEASES
            if event.type == pygame.JOYBUTTONUP:
                if event.button == button_keys['left_arrow']:
                    LEFT = False
                if event.button == button_keys['right_arrow']:
                    RIGHT = False
                if event.button == button_keys['down_arrow']:
                    DOWN = False
                if event.button == button_keys['up_arrow']:
                    UP = False

            # HANDLE SLIDER
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for s in slider:
                    if s.button_rect.collidepoint(pos):
                        s.hit = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for s in slider:
                    s.hit = False

            # HANDLES ANALOG INPUTS
            elif event.type == pygame.JOYAXISMOTION:
                analog_keys[event.axis] = event.value
                print(analog_keys)
                # Horizontal Analog
                if abs(analog_keys[0]) > .4:
                    if analog_keys[0] < -.7:
                        LEFT = True
                    else:
                        LEFT = False
                    if analog_keys[0] > .7:
                        RIGHT = True
                    else:
                        RIGHT = False

                # Vertical Analog
                if abs(analog_keys[1]) > .4:
                    if analog_keys[1] < -.7:
                        UP = True
                    else:
                        UP = False
                    if analog_keys[1] > .7:
                        DOWN = True
                    else:
                        DOWN = False
                if abs(analog_keys[2]) > .4:
                    if analog_keys[2] < -.7:
                        UPFOKUS = True
                    else:
                        UPFOKUS = False
                    if analog_keys[2] > .7:
                        DOWNFOKUS = True
                    else:
                        DOWNFOKUS = False

        # PERGERAKAN SLIDER DAN MEMUNCULKAN SLIDER
        for s in slider:
            if s.hit:
                s.move()
        for s in slider:
            s.draw(screen)
        # Handle Tinggi Benda + Jarak Benda + Fokus Benda
        if LEFT:
            if position.val < position.maxi:
                position.val += 1
            else:
                position.val += 0
        if RIGHT:
            if position.val > position.mini:
                position.val -= 1
            else:
                position.val = 0
                position.val -= 1
        if UP:
            if pen.val < pen.maxi:
                pen.val += 1
            else:
                pen.val += 0
        if DOWN:
            pen.val -= 1
            if DOWNFOKUS:
                if lensa.val > lensa.mini:
                    lensa.val -= 1
            if UPFOKUS:
                if lensa.val < lensa.maxi:
                    lensa.val += 1
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.QUIT()

