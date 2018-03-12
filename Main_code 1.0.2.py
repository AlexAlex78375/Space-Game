import pygame
import random
import sys
import os

ufo_x_coord = 1
ufo_y_coord = 400
ufo_x_speed = 0
ufo_y_speed = 0
ufo_life = 100

main_run = False

asteroid_change_direction = 0
go1 = 0 #
go2 = 0
go3 = 0

class Sky_object(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = cX
        self.rect.y = cY
class Ufo(Sky_object):
    def __init__(self, cX, cY):
        Sky_object.__init__(self, "ufo.gif", cX, cY)
class Asteroid(Sky_object):
    def __init__(self, cX, cY):
        Sky_object.__init__(self, "asteroid.gif", cX, cY)
class Medicine(Sky_object):
    def __init__(self, cX, cY):
        Sky_object.__init__(self, "medicine.gif", cX, cY)

class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = (162, 162, 208)
        self.font_color = (83, 55, 122)
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)
class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)
class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        # при создании кнопка не нажата
        self.pressed = False

    def render(self, surface):
        super().render(surface)
        if self.pressed:
            pygame.draw.rect(surface, pygame.Color('white'), self.rect, 1)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False

def init_window():
    pygame.init()
    pygame.display.set_mode((800, 800))
    music()
    pygame.display.set_caption('Space game by Alex') # устанавливаем заголовок окна
    start_page()

def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    #image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image, image.get_rect()
def background():
    back, back_rect = load_image("background.png")
    screen = pygame.display.get_surface()
    screen.blit(back, (0, 0))
    pygame.display.flip()
    return back

def get_events(events):
    global ufo_x_coord, ufo_y_coord, ufo_x_speed, ufo_y_speed, ufo_life
    global main_run
    for event in events:
        if event.type == pygame.QUIT:
            main_run = False
            print(1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ufo_x_speed = -10
            if event.key == pygame.K_RIGHT:
                ufo_x_speed = 10
            if event.key == pygame.K_UP:
                ufo_y_speed = -10
            if event.key == pygame.K_DOWN:
                ufo_y_speed = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ufo_x_speed = 0
            if event.key == pygame.K_RIGHT:
                ufo_x_speed = 0
            if event.key == pygame.K_UP:
                ufo_y_speed = 0
            if event.key == pygame.K_DOWN:
                ufo_y_speed = 0
    ufo_x_coord = ufo_x_coord + ufo_x_speed
    ufo_y_coord = ufo_y_coord + ufo_y_speed
    if ufo_x_coord < 0:
        ufo_x_coord = 0
    if ufo_x_coord > 800:
        ufo_x_coord = 800
    if ufo_y_coord < 0:
        ufo_y_coord = 0
    if ufo_y_coord > 800:
        ufo_y_coord = 800

class Gameover(pygame.sprite.Sprite):
    image = load_image("game_over.gif")
    def __init__(self, group):
        super().__init__(group)
        self.image , self.rect = Gameover.image
        self.rect = self.image.get_rect()
        self.rect.x = -800
        self.rect.y = 0

    def update(self):
        if self.rect.x < 0:
           self.rect = self.rect.move(20, 0)
        else:
           pass

def action(bk):
    global ufo_x_coord, ufo_y_coord,ufo_life, asteroid_change_direction, go1, go2, go3
    global main_run
    screen = pygame.display.get_surface()
    ufo = Ufo(20, 200)
    medicine = Medicine(400,400)
    ast1 = Asteroid(500, 100)
    ast2 = Asteroid(800, 200)
    ast3 = Asteroid(200, 350)
    asterow = []
    asterow.append(ast1)
    asterow.append(ast2)
    asterow.append(ast3)
    medicines = []
    med1 = Medicine(200, 200)
    med2 = Medicine(600, 200)
    med3 = Medicine(750, 400)
    medicines.append(med1)
    medicines.append(med2)
    medicines.append(med3)
    air = []
    air.append(ufo)
    asteroids = pygame.sprite.RenderPlain(asterow)
    ufos = pygame.sprite.RenderPlain(air)
    meds = pygame.sprite.RenderPlain(medicines)
    timer = pygame.time.Clock()
    main_run = True
    while main_run:
        timer.tick(700)
        get_events(pygame.event.get())
        hitten_asteroids = pygame.sprite.spritecollide(ufo, asteroids, False)
        medicines_got = pygame.sprite.spritecollide(ufo, medicines, False)# проверка на столкновение с аптечкой
        if len(hitten_asteroids) > 0:
            ufo_life -= len(hitten_asteroids)
            asteroids.draw(screen)
            ufos.draw(screen)
        if len(medicines_got) > 0:
            ufo_life += len(medicines_got) #10 очков жизни за каждую аптечку
            if ufo_life > 100:
                ufo_life = 100
            meds.draw(screen)
            ufos.draw(screen)
        if main_run and ufo_life < 1:
            clock = pygame.time.Clock()
            abc = pygame.sprite.Group()
            gm = Gameover(abc)
            try_again_button = Button((100, 60, 175, 80), "Try again!")
            exit_button = Button((400, 60, 175, 80), "Exit")
            gui1 = GUI()
            gui1.add_element(try_again_button)
            gui1.add_element(exit_button)
            fps = 20
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        main_run = False
                    if try_again_button.pressed:
                        ufo_life = 100
                        running = False
                    if exit_button.pressed:
                        running = False
                        main_run = False
                        pygame.display.flip()

                    gui1.get_event(event)

                gui1.update()


                abc.update()
                abc.draw(screen)
                gui1.render(screen)
                pygame.display.flip()
                clock.tick(fps)



        meds.draw(screen)
        ufo.rect.x = ufo_x_coord
        ufo.rect.y = ufo_y_coord
        ast1.rect.x = ast1.rect.x-1# меняем положение астероидов
        ast2.rect.x = ast2.rect.x-1
        ast3.rect.x = ast3.rect.x-1
        if ast1.rect.x < 0 :
            ast1.rect.x = 800
            ast1.rect.y = 0
        if ast2.rect.x < 0:
            ast2.rect.x = 800
            ast2.rect.y = 200
        if ast3.rect.x < 0:
            ast3.rect.x = 800
            ast3.rect.y = 350
        if asteroid_change_direction > 100:
            asteroid_change_direction = 0
            go1 = random.randint(-1, 1)
            go2 = random.randint(-1, 1)
            go3 = random.randint(-1, 1)
        ast1.rect.y += go1
        ast2.rect.y += go2
        ast3.rect.y += go3
        asteroid_change_direction += 1
        screen.blit(bk, (0, 0))
        font = pygame.font.Font(None, 25)
        color = (25,2,53)
        text = font.render( " Life : " + str(ufo_life), True, color)
        screen.blit(text, [10, 10])
        asteroids.update()
        ufos.update()
        asteroids.draw(screen)
        ufos.draw(screen)
        meds.draw(screen)
        pygame.display.flip()


def music():
    pygame.mixer.music.load("soundtrack.mp3")
    pygame.mixer.music.play()
    pass


def start_page():
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    image = pygame.image.load("data/start.png")
    screen.blit(image, (0, 0))
    start_button = Button((100, 60, 175, 80), "START")
    exit_button = Button((500, 60, 175, 80), "EXIT")
    gui.add_element(start_button)
    gui.add_element(exit_button)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # передаем события пользователя GUI-элементам
            gui.get_event(event)
        # обновляеем все GUI-элементы
        gui.update()
        # отрисовываем все GUI-элементы
        gui.render(screen)
        pygame.display.flip()
        if start_button.pressed:
            bk = background()
            action(bk)
        if exit_button.pressed:
            running = False
        pygame.display.flip()
    pygame.quit()
def game():
    init_window()

gui = GUI()
game()






