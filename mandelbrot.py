import pygame as game
import time as t

game.init()

WIDTH = 500
HEIGHT = 500

screen = game.display.set_mode((WIDTH, HEIGHT))

game.display.set_caption("Mandelbrot Set")

generated_points = False 
points = [[(0, 0, 0) for _ in range(WIDTH)] for __ in range(HEIGHT)]

scroll = 2
scroll_speed = 0.2
speed = 30
x_offset = 0
y_offset = -10
last_frame = 0

def _map(val, r1, r2, nr1, nr2):
    return ((val - r1) / (r2 - r1) ) * (nr2 - nr1) + nr1

def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def num_to_hex(num):
    return hex(int(num))[2:]

def num_to_rgb(num):
    return hex_to_rgb(num_to_hex(num))


def calc_colour(point):
    if abs(point) > 2:
        return (255, 255, 255)

    def next_z(zn, c):
        return zn**2 + c
    
    z = 0
    z_count = 0
    for x in range(20):
        try:
            z = next_z(z, point)
            z_count += 1
            if abs(z) > 2:
                col = _map(z_count, 0, 49, 0, 16777215)
                return num_to_rgb(col)
        except OverflowError:
            col = _map(z_count, 0, 49, 0, 16777215)
            return num_to_rgb(col)

    return (0, 0, 0)
    

last_frame = t.time()
a = 0
running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
        elif event.type == game.KEYDOWN:
            if event.key == game.K_w:
                y_offset += speed
                generated_points = False
            elif event.key == game.K_s:
                y_offset -= speed
                generated_points = False
            elif event.key == game.K_a:
                x_offset += speed
                generated_points = False
            elif event.key == game.K_d:
                x_offset -= speed
                generated_points = False
            elif event.key == game.K_q:
                scroll += scroll_speed
                generated_points = False
            elif event.key == game.K_r:
                scroll -= scroll_speed
                generated_points = False
            
    screen.fill((255, 255, 255))

    if not generated_points:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                mapped_x = _map(x, x_offset, WIDTH+x_offset, -scroll, scroll)
                mapped_y = _map(y, y_offset, HEIGHT+y_offset, -scroll, scroll)

                colour = calc_colour(complex(mapped_x, mapped_y))
                points[x][y] = colour

                screen.set_at((x, y), colour)

        generated_points = True
    else:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                screen.set_at((x, y), points[x][y])

    if not a%10:
        print(1/(t.time()-last_frame))
        
    last_frame = t.time()
    a += 1
    game.display.update()