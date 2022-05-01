import pygame as game
import numpy as np
import os
from PIL import Image

game.init()

WIDTH = 500
HEIGHT = 500

screen = game.display.set_mode((WIDTH, HEIGHT))

game.display.set_caption("Mandelbrot Set")

generated_points = False 
written_to_file = False
points = [[(0, 0, 0) for _ in range(WIDTH)] for __ in range(HEIGHT)]

scroll = 2
scroll_speed = 0.9
speed = 30
x_offset = -1.74999841099374081749002483162428393452822172335808534616943930976364725846655540417646727085571962736578151132907961927190726789896685696750162524460775546580822744596887978637416593715319388030232414667046419863755743802804780843375
y_offset = -0.00000000000000165712469295418692325810961981279189026504290127375760405334498110850956047368308707050735960323397389547038231194872482690340369921750514146922400928554011996123112902000856666847088788158433995358406779259404221904755

last_frame = 0

iterations = 500

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

a = 0
num = 0
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
                mapped_x = _map(x, 0, WIDTH, -scroll*(WIDTH/HEIGHT)+x_offset, scroll*(WIDTH/HEIGHT)+x_offset)
                mapped_y = _map(y, 0, HEIGHT, -scroll+y_offset, scroll+y_offset)

                colour = calc_colour(complex(mapped_x, mapped_y))
                points[y][x] = colour

                mandelbrot.putpixel((x, y), colour)

                screen.set_at((x, y), colour)
            if a%10 == 0: print(f"{(x*HEIGHT)+y+1}/{WIDTH*HEIGHT}")
            a += 1

        mandelbrot.save(f"mandelbrot/mandelbrot_img{num}.png")
        # generated_points = True
        print(f"done {num}")
        num += 1
        scroll *= scroll_speed
        # os.system("shutdown -s -t 10")
        
    else:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                screen.set_at((x, y), points[y][x])

    game.display.update()
