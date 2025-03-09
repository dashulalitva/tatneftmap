import pygame
from pygame.locals import *
import tkinter as tk
from PIL import ImageTk, Image
import os

pygame.init()
#параметры окна:
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("республика Татарстан")


class Game(pygame.sprite.Sprite):
    # Класс для игрового объекта (маркера)
    def __init__(self, image_path, x, y, scale=(50, 50)):
        super().__init__()
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            self.scaled_image = pygame.transform.scale(self.original_image, scale)
            self.image = self.scaled_image
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            self.image = pygame.Surface((scale[0], scale[1]))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = "" 


    def render(self, surface):#отображение маркера
        surface.blit(self.image, self.rect)

    def set_text(self, text):#установка текста, связанного с маркером.
        self.text = text

    def get_text(self):#получение текста, связанного с маркером.
        return self.text


def load_background(filename):#загрузка фонового изображения.
    
    background_image = pygame.image.load(filename).convert()
    background_rect = background_image.get_rect()
    background_rect.center = (screen_width // 2, screen_height // 2)
    return background_image, background_rect



def open_tk_window(image_path, label_text_content):# Открытие окна tkinter с информацией о местах отмеченных маркером
    root = tk.Tk()
    root.title("информация")

    def on_closing():#закрытие главного окна tkinter
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    tk_photo = None

    if os.path.exists(image_path):
        photo = Image.open(image_path)
        photo_resized = photo.resize((300, 200), Image.LANCZOS)
        tk_photo = ImageTk.PhotoImage(photo_resized)
        label_photo = tk.Label(root, image=tk_photo)
        label_photo.image = tk_photo
        label_photo.pack()


    label_text = tk.Label(root, text=label_text_content)
    label_text.pack()
    root.mainloop()


def open_editor_window(game_object=None): #окно редактора, где пользователи могут вводить или редактировать текст. 
    global editor_text, placing_marker
    editor_text = ""  

    root = tk.Tk()
    root.title("Редактор")

    text_content = tk.Text(root, height=10, width=40)

    if game_object:
        text_content.insert(tk.END, game_object.get_text())
    text_content.pack()

    def save_data():#сохранение
        global editor_text, placing_marker 
        editor_text = text_content.get("1.0", tk.END)
        print("Текст:", editor_text)

        if game_object:
            game_object.set_text(editor_text)  
            root.destroy()
        else:
            placing_marker = True
            root.destroy()

    save_button = tk.Button(root, text="Сохранить", command=save_data)
    save_button.pack()

    root.mainloop()


def draw_button(surface, rect, color, text, text_color=(0, 0, 0)):#отрисовка кнопки с заданными параметрами
    pygame.draw.rect(surface, color, rect)
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def draw_text(surface, text, x, y, color=(255, 255, 255)):#отрисовка текста с заданными параметрами
    font = pygame.font.Font(None, 30)  
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)



background_image, background_rect = load_background('tatmap.jpg')#фон
# Создаём игровые объекты с разными позициями:
game1 = Game("marker.png", 550, 400)
game2 = Game("marker.png", 510, 360)
game3 = Game("marker.png", 500, 215)
game4 = Game("marker.png", 300, 270)
game5 = Game("marker.png", 120, 175)
game6 = Game("marker.png", 600, 300)
game7 = Game("marker.png", 650, 515)
game8 = Game("marker.png", 550, 400)
game9 = Game("marker.png", 650, 515)

edit_button_rect = pygame.Rect(10, 10, 100, 30)  
#тексты:
text1 = """Город Альметьевск сыграл важную роль в годы Великой Отечественной войны.
 Он был крупным центром нефтедобычи, что имело стратегическое значение для обеспечения
топливом военной техники и промышленности. Нефть, добываемая в Альметьевске,
использовалась для производства топлива и смазочных материалов, необходимых для работы танков, 
самолетов и других видов военной техники. Кроме того, в городе находились важные промышленные 
предприятия, которые производили военную продукцию. Все эти факторы делали Альметьевск важным 
стратегическим объектом в годы войны."""

text2 = """Ромашкинское нефтяное месторождение стало ключевым фактором в развитии нефтяной промышленности СССР во время Великой Отечественной войны.
    В условиях угрозы захвата северокавказских нефтяных промыслов, открытие новых месторождений стало жизненно важным для страны.
    В 1941 году начались разведочные работы, и 25 июля 1943 года в Татарстане,
у села Шугурово, из скважины №1 был получен первый промышленный приток нефти
с дебитом 15 тонн в сутки. Это событие ознаменовало вступление Татарстана в число
нефтедобывающих регионов страны. Открытие Ромашкинского месторождения 25 июля 1948 года
стало началом создания в Татарстане новой нефтяной базы СССР — «Второго Баку». Благодаря самоотверженному труду нефтяников, Красная Армия на всех этапах
войны была обеспечена горюче-смазочными материалами."""

text3="""ТАНЕКО (Татарско-Американская Нефтяная Компания)
- Нефтехимический комплекс в Нижнекамске, один из самых современных в России.
Занимается переработкой нефти и производством нефтепродуктов высокого качества."""
text4="""Чистополь
- Центр эвакуации. Чистополь стал местом размещения многих эвакуированных жителей
и предприятий из западных регионов СССР. Здесь также действовали госпитали и производственные мощности."""
text5="""Казань.   
В Казань были эвакуированы десятки заводов, включая Московский авиационный завод №22 
(ныне КАПО имени Горбунова), Московский подшипниковый завод и другие.
Эти предприятия сыграли ключевую роль в производстве военной техники и боеприпасов.
   - Производство вооружений. Казанские заводы выпускали самолеты, боеприпасы, минометы и другое вооружение.
   - Госпитали. В Казани было развернуто большое количество госпиталей для лечения раненых солдат."""
text6="""Джалильнефть. Добыча нефти в Азнакаево началась в 1950-х годах, когда здесь были открыты первые крупные месторождения. 
Именно тогда началось активное освоение района, и «Джалильнефть» стала одним из ключевых игроков в этой отрасли. 
Название подразделения связано с именем Героя Советского Союза Мусы Джалиля, известного татарского поэта и общественного деятеля."""
text7="""Научно-технический центр «ТатНИПИнефть» является важным элементом инфраструктуры нефтяной промышленности Татарстана и России
в целом. Его деятельность направлена на повышение эффективности и устойчивости нефтедобычи, улучшение экологической ситуации 
и подготовку высококвалифицированных кадров для отрасли."""
text8="""Учебный центр подготовки кадров «Татнефть» — это профессиональное образовательное учреждение, которое специализируется
на подготовке квалифицированных специалистов для работы в нефтегазовой отрасли. Центр расположен в Альметьевске, Республика Татарстан,
и играет важную роль в обеспечении кадрового потенциала ПАО «Татнефть» и других предприятий отрасли."""

text9="""Бугульма. Бугульма была очень важным транспортным узлом и базой для авиации, поддерживавшей боевые действия на фронте."""
# пустые значения для редактора и списка маркеров:
editor_text = ""  
placing_marker = False  
markers = []

clock = pygame.time.Clock()#таймер
#основной цикл:
running = True

while running:
    clock.tick(60)
# Обработка событий:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if game1.rect.collidepoint(event.pos):
                open_tk_window('image.jpg', text1)
            if game2.rect.collidepoint(event.pos):
                open_tk_window('romashkinsk.jpeg', text2)
            if game3.rect.collidepoint(event.pos):
                open_tk_window('taneko.jpg', text3)
            if game4.rect.collidepoint(event.pos):
                open_tk_window('chistopol.jpg', text4)
            if game5.rect.collidepoint(event.pos):
                open_tk_window('kazan.png', text5)
            if game6.rect.collidepoint(event.pos):
                open_tk_window('djadilneft.jpg', text6)
            if game7.rect.collidepoint(event.pos):
                open_tk_window('tatnil.jpg', text7)
            if game8.rect.collidepoint(event.pos):
                open_tk_window('kadrs.jpg', text8)
            if game9.rect.collidepoint(event.pos):
                open_tk_window('bugulma.jpeg', text9)
                
            if edit_button_rect.collidepoint(event.pos):
                open_editor_window()

            elif placing_marker:  

                new_marker = Game("marker.png", event.pos[0] - 25, event.pos[1] - 25)  
                new_marker.set_text(editor_text)
                markers.append(new_marker)
                placing_marker = False 
            else:

                for marker in markers:
                    if marker.rect.collidepoint(event.pos):
                        open_editor_window(marker) 
                        break
# Отрисовка фона и игровых объектов:
    if background_image:
        screen.blit(background_image, background_rect)
    game1.render(screen)
    game2.render(screen)
    game3.render(screen)
    game4.render(screen)
    game5.render(screen)
    game6.render(screen)
    game7.render(screen)
    game8.render(screen)
    game9.render(screen)

    draw_button(screen, edit_button_rect, (213, 48, 50), "Редактор") #отрисовка кнопки редактора


    if placing_marker:
        draw_text(screen, "Выберите место маркера щелкнув мышью по экрану", 100, 100, color=(0,0,0))#мини инструкция
    for marker in markers:
        marker.render(screen)

    pygame.display.flip()

pygame.quit()

