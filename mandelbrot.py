import pygame as game
import numpy as np
from PIL import Image

game.init()

WIDTH = 900
HEIGHT = 900

screen = game.display.set_mode((WIDTH, HEIGHT))

game.display.set_caption("Mandelbrot Set")

generated_points = False 
written_to_file = False
points = [[(0, 0, 0) for _ in range(WIDTH)] for __ in range(HEIGHT)]

scroll = 2
scroll_speed = 0.78
speed = 30
x_offset = 0
y_offset = 0
last_frame = 0

iterations = 5000

def _map(val, r1, r2, nr1, nr2):
    return ((val - r1) / (r2 - r1) ) * (nr2 - nr1) + nr1

def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def num_to_hex(num):
    return hex(int(num))[2:]

def num_to_rgb(num):
    h = num_to_hex(num)
    return hex_to_rgb("0"*(6-len(h))+h)


def calc_colour(point):
    if point.imag**2 + point.real**2 > 4:
        return (255, 255, 255)

    def next_z(zn, c):
        return zn**2 + c
    
    z = 0
    z_count = 0
    for x in range(iterations):
        try:
            z = next_z(z, point)
            z_count += 1
            if z.real**2 + z.imag**2 > 4:
                col = _map(z_count, 0, iterations-1, 0, 16777215)
                return num_to_rgb(col)
        except OverflowError:
            col = _map(z_count, 0, iterations-1, 0, 16777215)
            return num_to_rgb(col)
    
    return (0, 0, 0)
    

running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
            
    screen.fill((255, 255, 255))

    if not generated_points:
        mandelbrot = Image.new("RGB", (WIDTH, HEIGHT))
        for x in range(WIDTH):
            for y in range(HEIGHT):
                mapped_x = _map(x, x_offset, WIDTH+x_offset, -scroll*(WIDTH/HEIGHT), scroll*(WIDTH/HEIGHT))
                mapped_y = _map(y, y_offset, HEIGHT+y_offset, -scroll, scroll)

                colour = calc_colour(complex(mapped_x, mapped_y))
                points[y][x] = colour

                mandelbrot.putpixel((x, y), colour)

                screen.set_at((x, y), colour)
            print(f"{(x*HEIGHT)+y+1}/{WIDTH*HEIGHT}")

        mandelbrot.save(f"mandelbrot_img.png")
        generated_points = True
    else:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                screen.set_at((x, y), points[y][x])

    game.display.update()
