import tkinter as tk
import pygame as pg
from pygame.locals import *

pg.init()
root=tk.Tk()

canvas=tk.Canvas(root,width=500,height=500)
canvas.pack()

screen = pg.display.set_mode((500,500))
background=pg.Surface((500,500))
background.fill((255,255,255))
canvas.create_image(0,0,image=tk.PhotoImage(screen))

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            root.quit()
    screen.blit(background,(0,0))
    pg.draw.circle(background,(255,0,0),(250,250),50)
    canvas.create_image(0,0,image=tk.PhotoImage(background))

    pg.display.update()
    root.update()