import math
from PIL import Image
import os
import sys
import colour_map
import numpy as np
from threading import Thread

WIDTH = 256
HEIGHT = 256
FRAMES = 60

fp_in = "./mandelbrot/mandelbrot_img*.png"
fp_out = "output.gif"

frames = []
threads = []
remaining = [i for i in range(FRAMES)]
progress = {}
displaying = False

generated_points = False 
written_to_file = False
points = [[(0, 0, 0) for _ in range(WIDTH)] for __ in range(HEIGHT)]

scroll = 1.8
scroll_speed = 0.9
x_offset = -1.74999841099374081749002483162428393452822172335808534616943930976364725846655540417646727085571962736578151132907961927190726789896685696750162524460775546580822744596887978637416593715319388030232414667046419863755743802804780843375
y_offset = -0.00000000000000165712469295418692325810961981279189026504290127375760405334498110850956047368308707050735960323397389547038231194872482690340369921750514146922400928554011996123112902000856666847088788158433995358406779259404221904755

iterations = 1000

def _map(val, r1, r2, nr1, nr2):
    return ((val - r1) / (r2 - r1) ) * (nr2 - nr1) + nr1

def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def num_to_hex(num):
    return hex(int(num))[2:]

def num_to_rgb(num):
    h = num_to_hex(num)
    return hex_to_rgb("0"*(6-len(h))+h)

def colour_maths(_z, _z_count):
    smoothed = np.log2(np.log2(_z.real**2 + _z.imag**2) / 2)
    colourI = int(np.sqrt(_z_count + 10 - smoothed) * 256) % len(colour_map.red)
    colour = (int(colour_map.red[colourI]), int(colour_map.green[colourI]), int(colour_map.blue[colourI]))
    return colour

def calc_colour(point):
    if point.imag**2 + point.real**2 > 4:
        return (2, 3, 0)

    def next_z(zn, c):
        return zn**2 + c
    
    z = 0
    z_count = 0
    for x in range(iterations):
        try:
            z = next_z(z, point)
            z_count += 1
            if z.real**2 + z.imag**2 > 4:
                return colour_maths(z, z_count)
        except OverflowError:
            return colour_maths(z, z_count)
    
    return (0, 0, 0)

def calculate_indices():
    scrollarray = []
    s = scroll
    for i in range(FRAMES):
        s*=scroll_speed
        scrollarray.append((i, s))
    return scrollarray

def calculate_remaining(n):
    global remaining
    remaining.remove(n)
    return len(remaining)

def printProgressBar(value,label):
    n_bar = 100
    max = 100
    j= value/max
    sys.stdout.write('\r')
    bar = '█' * int(n_bar * j)
    bar = bar + '-' * int(n_bar * (1-j))

    sys.stdout.write(f"{label} | [{bar:{n_bar}s}] {int(100 * j)}% ")
    sys.stdout.flush()

def update_progress(frame, pct, done = True):
    global displaying
    progress[frame] = pct
    if not displaying:
        displaying = True
        clear = lambda: os.system('cls')
        clear()
        ps = dict(sorted(progress.items()))
        for i in list(ps):
            printProgressBar(math.ceil(progress[i]*100), i)
            print()
        displaying = False

def task(n, s):
    mandelbrot = Image.new("RGB", (WIDTH, HEIGHT))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            mapped_x = _map(x, 0, WIDTH, -s*(WIDTH/HEIGHT)+x_offset, s*(WIDTH/HEIGHT)+x_offset)
            mapped_y = _map(y, 0, HEIGHT, -s+y_offset, s+y_offset)
            colour = calc_colour(complex(mapped_x, mapped_y))
            mandelbrot.putpixel((x, y), colour)
        update_progress(n, x/WIDTH, False)
    r = calculate_remaining(n)
    frames.append((n, mandelbrot))

def save_frames():
    for i in frames:
        i[1].save(f"./mandelbrot/mandelbrot_img{i[0]}.png")

def create_threads():
    r = calculate_indices()
    for i in range(FRAMES):
        t = Thread(target=task, args=(r[i][0],r[i][1]))
        threads.append(t)

def start_threads():
    for i in range(len(threads)):
        threads[i].start()

def join_threads():
    for t in threads:
        t.join()
    print('Done')

def make_gif():
    global frames
    frames = sorted(frames, key=lambda tup: tup[0])
    imgs = [f[1] for f in frames]
    img = imgs[0]
    img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=FRAMES, loop=0)

if __name__ == '__main__':
    create_threads()
    start_threads()
    join_threads()
    save_frames()
    make_gif()
