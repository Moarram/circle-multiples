import pygame
import colorsys
import time
from math import *

# This program requires the pygame module.
# To install it run "pip3 install pygame" or "pip install pygame" from the command line

STEPS = 640 # number of steps between whole numbers
POINTS = 10 # modifiable by keyboard input

FRAMERATE = 144
RADIUS = 500 # modifiable by keyboard input
BORDER = 100 # modifiable by keyboard input
FONTSIZE = 20

pygame.init()
pygame.display.set_caption("circle.py")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", FONTSIZE)
screen = pygame.display.set_mode((RADIUS*2 + BORDER*2, RADIUS*2 + BORDER*2 + FONTSIZE*4))
s = pygame.Surface((RADIUS*2 + BORDER*2, RADIUS*2 + BORDER*2 + FONTSIZE*2), pygame.SRCALPHA)   # per-pixel alpha

def validate(count, wrap=STEPS):
    if count >= STEPS*POINTS:
        return count%(STEPS*POINTS)
    if count < 0:
        return STEPS*POINTS - wrap
    return count

def draw_header(string_1, string_2, string_3, string_4):
    text = font.render(string_1, True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, RADIUS*2 + BORDER*2, FONTSIZE))
    screen.blit(text, (0, 0))

    text = font.render(string_2, True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, FONTSIZE, RADIUS*2 + BORDER*2, FONTSIZE))
    screen.blit(text, (0, FONTSIZE))

    text = font.render(string_3, True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, RADIUS*2 + BORDER*2 + FONTSIZE*2, RADIUS*2 + BORDER*2, FONTSIZE))
    screen.blit(text, (0, RADIUS*2 + BORDER*2 + FONTSIZE*2))

    text = font.render(string_4, True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, RADIUS*2 + BORDER*2 + FONTSIZE*3, RADIUS*2 + BORDER*2, FONTSIZE))
    screen.blit(text, (0, RADIUS*2 + BORDER*2 + FONTSIZE*3))

def message(x, y, text):
    buffer = 5
    color = (255, 255, 255)
    message = font.render(text, True, color) # create message for pygame
    pygame.draw.rect(screen, (0, 0, 0),  pygame.Rect(x, y - message.get_height() - buffer * 2, message.get_width() + buffer * 2, message.get_height() + buffer * 2))
    screen.blit(message, (x + buffer, y - message.get_height() - buffer))

def cartesian(a):
    radians = ((POINTS - a)/POINTS)*(2*pi)
    x = RADIUS*cos(radians)
    y = RADIUS*sin(radians)
    return x, y

def connect(a, b, highlightIntegers=False, onlyIntegers=False, width=3, extend=0):
    a_x, a_y = cartesian(a)
    b_x, b_y = cartesian(b)

    distance = sqrt((a_x - b_x)**2 + (a_y - b_y)**2)
    hue = (distance/(RADIUS*2.35))**2
    rgb = colorsys.hsv_to_rgb(hue, 1, 1)
    color = (rgb[0]*255, rgb[1]*255, rgb[2]*255)

    if b%1 > 0.99999999 or b%1 < 0.00000001: # whole number (within 8 decimals of accuracy)
        if highlightIntegers:
            color = (255, 255, 255)
            width = width*2 - 1
    else:
        if onlyIntegers:
            return

    c_x = a_x + (a_x - b_x)*extend
    d_x = b_x + (b_x - a_x)*extend
    c_y = a_y + (a_y - b_y)*extend
    d_y = b_y + (b_y - a_y)*extend
    pygame.draw.line(screen, color, (c_x + RADIUS + BORDER, c_y + RADIUS + BORDER + FONTSIZE*2), (d_x + RADIUS + BORDER, d_y + RADIUS + BORDER + FONTSIZE*2), width)

def point(a):
    a_x, a_y = cartesian(a)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(a_x - 2 + RADIUS + BORDER, a_y - 2 + RADIUS + BORDER + FONTSIZE*2, 4, 4))

wait = -1
mod_1 = 1
mod_2 = 1
extend = 0
reverse = False
beautify = False
showLabels = False
highlightIntegers = False
onlyIntegers = False
doBlur = False
width = 1

count = 0
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # clicking X on window or ctrl+C in cmd will exit loop
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

            if event.key == pygame.K_LSHIFT:
                mod_1 = STEPS//8
                mod_2 = POINTS//8
            if event.key == pygame.K_1:
                showLabels = not showLabels
            if event.key == pygame.K_2:
                onlyIntegers = not onlyIntegers
            if event.key == pygame.K_3:
                highlightIntegers = not highlightIntegers
            if event.key == pygame.K_4:
                doBlur = not doBlur
            if event.key == pygame.K_5:
                beautify = not beautify
            if event.key == pygame.K_6:
                if extend == 0:
                    extend = 2
                    RADIUS = 100
                    BORDER = 500
                else:
                    extend = 0
                    RADIUS = 500
                    BORDER = 100    
            if event.key == pygame.K_7:
                reverse = not reverse  
            if event.key == pygame.K_RIGHTBRACKET:
                width *= 2
            if event.key == pygame.K_LEFTBRACKET:
                width //= 2
                if width < 1:
                    width = 1
            if event.key == pygame.K_EQUALS:
                POINTS = POINTS*2
            if event.key == pygame.K_MINUS:
                POINTS = POINTS//2
                if POINTS < 10:
                    POINTS = 10
            if event.key == pygame.K_SPACE:
                if wait == -1:
                    wait = 0
                else:
                    wait = -1
            if event.key == pygame.K_UP:
                count = validate(count + 1*mod_1, 1)
            if event.key == pygame.K_DOWN:
                count = validate(count - 1*mod_1, 1)
            if event.key == pygame.K_LEFT:
                count = validate(STEPS*((count - 1)//STEPS) - STEPS*mod_2 + STEPS, STEPS*mod_2)
            if event.key == pygame.K_RIGHT:
                count = validate(STEPS*(count//STEPS) + STEPS*mod_2)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                mod_1 = 1
                mod_2 = 1

    if doBlur:
        s.fill((0, 0, 0, 10))
        screen.blit(s, (0, FONTSIZE))
    else:
        screen.fill((0, 0, 0))

    b = 0
    h = 0
    if beautify == True:
        t = time.process_time()
        lines = []
        for a in range(0, POINTS + 1):
            if a != 0:
                b = (a*(count/STEPS))%POINTS
            a_x, a_y = cartesian(a)
            b_x, b_y = cartesian(b)
            distance = sqrt((a_x - b_x)**2 + (a_y - b_y)**2)
            lines.append(((a, b), distance))
        lines_sorted = sorted(lines, key=(lambda x : x[1]), reverse=True) # sort each line from longest to shortest
        for line in lines_sorted:
            connect(line[0][0], line[0][1], highlightIntegers, onlyIntegers, width, extend)  
    else:
        for a in range(0, POINTS + 1):
            if a != 0:
                b = (a*(count/STEPS))%POINTS
            connect(a, b, highlightIntegers, onlyIntegers, width, extend)
            if showLabels:
                a_x, a_y = cartesian(a)
                message(a_x + RADIUS + BORDER, a_y + RADIUS + BORDER + FONTSIZE*2, str(a))

    string_1 = "[1]Labels: {:1.1}, [2]Ints only: {:1.1}, [3]Lightning: {:1.1}, [4]Blur: {:1.1}, [5]Beautify: {:1.1} [6]Extend: {:1.1}, [7]Reverse: {:1.1}".format(str(showLabels), str(onlyIntegers), str(highlightIntegers), str(doBlur), str(beautify), str(extend > 0), str(reverse))
    string_2 = "Multiple: {:.3f}, Points: {}, Line width: {}".format(count/STEPS, POINTS, width)
    string_3 = "[Space]Pause, [Left/Right]Next/Prev Integer, [Up/Down]Next/Prev Step, [Shift]Faster Selection"
    string_4 = "[Left/Right Bracket]Line Width, [+/-]Point Count"
    draw_header(string_1, string_2, string_3, string_4)

    point((count/STEPS)%POINTS)
    point(((POINTS*count)/STEPS)%POINTS)

    if showLabels:
        a_x, a_y = cartesian((count/STEPS)%POINTS)
        message(a_x + RADIUS + BORDER, a_y + RADIUS + BORDER + FONTSIZE*2, "{:.3f}".format((count/STEPS)%POINTS))

        b_x, b_y = cartesian(((POINTS*count)/STEPS)%POINTS)
        message(b_x + RADIUS + BORDER, b_y + RADIUS + BORDER + FONTSIZE*2, "{:.3f}".format(((POINTS*count)/STEPS)%POINTS))
    
    pygame.display.flip() # update display
    clock.tick(FRAMERATE) # wait for 1/framerate seconds

    if (count%STEPS == 0 and wait == 0): # whole number multiple and not already waiting
        wait = 0 # frames to wait on whole number 

    if wait == -1:
        continue
    if wait > 1: # redraw without incrementing count
        wait -= 1
        continue
    if wait == 1: # last one is a special case, must increment count to move on
        count += 1
        wait = 0
        continue

    if reverse:
        count = validate(count - 1, 1)
    else:
        count = validate(count + 1)
