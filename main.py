from tkinter import *
import random
import time
WIDTH=1200
HEIGHT=700
CHARACTER_W=100
CHARACTER_H=120
PLATFORM_W=120
PLATFORM_H=24



""" def finish():
    root.destroy()
    print("окно закрылось")
    перехват закрытия окна """

root = Tk()  # создаем корневой объект - окно
root.title("doodle jump")  # устанавливаем заголовок окна
root.geometry(f"{WIDTH}x{HEIGHT}+0+0")  # устанавливаем размеры окна
root.resizable(False, False)
icon=PhotoImage(file="images\doodle.png")
hero=PhotoImage(file="images\doodle.png")
platform=PhotoImage(file="images\platform.png")
background=PhotoImage(file=".\images\\back.png")
root.iconphoto(False, icon)
score = 0
speed = 30
gravity_moved = 0
stamina = 30
hit = False
jump_platform = 0
landing_platform = 0


# label = Label(text="Hello METANIT.COM")  # создаем текстовую метку
# label.pack()  # размещаем метку в окне
# перехват закрытия окна root.protocol("WM_DELETE_WINDOW", finish)

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='black', bd=0, highlightthickness=0)
canvas.create_image(0, 0, image=background, anchor=NW)
character = canvas.create_image(0, 0, image=hero, anchor=NW)


canvas.pack()



class Platform:
    def __init__(self, x, y):
        self.platform = canvas.create_image(x, y, image=platform, anchor=NW)

    def move(self, amount):
        canvas.move(self.platform, 0, amount)

    def coords(self):
        coord_list_core = canvas.coords(self.platform)
        coord_list_core.append(coord_list_core[0] + PLATFORM_W)
        coord_list_core.append(coord_list_core[1] + PLATFORM_H)
        return coord_list_core


spawn2= Platform(150,50)
spawn3= Platform(1000,150)
spawn4= Platform(700,200)
spawn5= Platform(400,250)
spawn6= Platform(200, 300)
spawn7=Platform(600,350)
spawn8=Platform(1100, 400)
spawn9=Platform(150, 450)
spawn10=Platform(500,500)

platforms = [spawn2, spawn3, spawn4, spawn5, spawn6, spawn7, spawn8, spawn9, spawn10]

def spawn_platform():
    a=random.randint(0, 1200-PLATFORM_W)
    new_platform=Platform(a,50)
    platforms.append(new_platform)

# def platform_move():
#     global platforms
#     global score
#     while (canvas.coords(character)[1] + CHARACTER_H) < 580:
#         spawn_platform()
#         for platform in platforms:
#             plat_list = platform.coords()
#             platform.move(200)                                                    пробный метод(не работаетd)
#             root.update()
#             if plat_list[1] >=HEIGHT:
#                 canvas.delete(platform)
#                 try:
#                     platforms.remove(platform)
#                 except:
#                     pass
#                 score += 1
#         canvas.move(character, 0, 4.5)
def update_score(score):
    canvas.delete("score")
    canvas.create_text(0 ,0,  text=f"Score: {score}", anchor="nw", fill="white", tags="score", font=('Arial',10))
def gameover():
    root.unbind('<d>')
    root.unbind('<a>')
    canvas.delete('all')
    canvas.create_image(0, 0, image=background, anchor=NW)
    canvas.create_text(600,350 , text='G A M E  O V E R', fill='#d91919', font=('Arial',20))
    canvas.create_text(600, 400, text=f'SCORE = {score}', fill='#d91919', font=('Arial',20))
def platform_move(move, plat):
    global platforms
    global score
    moved = 0
    while (canvas.coords(character)[1] + CHARACTER_H) < 600:
        if moved >= 60:
            moved = 0
            spawn_platform()
        coords = Platform.coords(plat)
        if coords[1] >= 550:
            break
        for platform in platforms:
            plat_list = platform.coords()
            platform.move(4.5)
            root.update()
            if plat_list[1] >= HEIGHT:
                try:
                    canvas.delete(platform)
                    platforms.remove(platform)
                except:
                    pass
                score += 1
                update_score(score)
        moved += 4.5
def platform_hit():
    global hit
    global landing_platform
    for platform in platforms:
        coords_list = platform.coords()
        if coords_list[0] <= canvas.coords(character)[0] <= coords_list[2]:
            if (coords_list[1]) <= (canvas.coords(character)[1] + CHARACTER_H) <= (coords_list[3]):
                hit = True
                landing_platform = platform
                return platform
        if coords_list[0] <= (canvas.coords(character)[0] + CHARACTER_H) <= coords_list[2]:
            if (coords_list[1]) <= (canvas.coords(character)[1] + CHARACTER_H) <= (coords_list[3]):
                hit = True
                landing_platform = platform
                return platform

def gravity():
    global hit
    global gravity_moved
    global jump_platform
    platform = platform_hit()
    if ((canvas.coords(character)[1] + CHARACTER_H) + 2 + (gravity_moved / 1000)) < HEIGHT and hit is not True:
        canvas.move(character, 0, 2 + (gravity_moved / 10))
        if gravity_moved < 100:
            gravity_moved += 2
        root.after(9, gravity)
    elif hit:
        hit = False
        gravity_moved = 0
        jump()
        jump_platform = platform
        try:
            if canvas.coords(character)[1] <=600:
               move = -((canvas.coords(character)[1] + CHARACTER_H) - 700)
               platform_move(move, platform)

        except IndexError:
            pass
    else:
        canvas.move(character, 0, HEIGHT - (canvas.coords(character)[1] + CHARACTER_H))
        gravity_moved = 0
        gameover()

def jump():
    global stamina
    try:
        if canvas.coords(character)[1]-(2 + (stamina / 4)) > 0:
            if stamina >= 0 and canvas:
                canvas.move(character, 0, -(2 +(stamina / 4)))
                stamina -= 1
                root.after(15, jump)
            else:
                stamina = 30
                root.after(90, gravity)
        else:
            stamina = 30
            root.after(90, gravity)
    except IndexError:
        pass


def right(event): #метод для движения героя вправо
    if (canvas.coords(character)[0]+ CHARACTER_W + speed) <= WIDTH:
        canvas.move(character, speed, 0)
    if(canvas.coords(character)[0]+CHARACTER_W + speed) >= WIDTH:
        canvas.move(character, -WIDTH+CHARACTER_W, 0)

def left(event): #метод для движения героя влево
    if (canvas.coords(character)[0] - speed) >= 0:
        canvas.move(character, -speed, 0)
    if (canvas.coords(character)[0]-speed) <= 0:
        canvas.move(character, WIDTH-CHARACTER_W, 0)

root.bind('<d>', right)
root.bind('<a>', left)
gravity()
root.mainloop()