'''
Este juego es una implementacion del juego clasico arcade llamado pong en Python 3.3.2

Pong the game
Created by: Jassael Ruiz
Version: 1.0
'''

import sys
sys.path.append("..")
import simplegui
import random as rand

# initialize globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PADDLE1_VEL = 4
PADDLE2_VEL = 4
time = 3
aux = ""
h = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]
h1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
red = "00"
green = "d6"
blue = "00"
color1 = "#"+red+green+blue
color2 = "green"
t = 0
r = 0
g = 0
b = 0
inc = 5
pausa = False

# initialize ball_pos and ball_vel for new bal in middle of table
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_velx = rand.randrange(120, 240) / 60
    ball_vely = rand.randrange(60, 180) / 60
    
    if(direction == 1):
        #1 arrriba a la derecha
        ball_vely *= -1
    #2 abajo a la derecha
    elif(direction == 3):
        #3 arriba a la derecha
        ball_velx *= -1
        ball_vely *= -1
    elif(direction == 4):
        #abajo a la izquierda
        ball_velx *= -1
        
    ball_vel = [ball_velx, ball_vely]  

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    direction = rand.randint(1, 4)
    spawn_ball(direction)
    score1 = 0
    score2 = 0
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT

# convierte un numero del sistema decimal al hexadecimal
def dec_to_hex(n):
    first = h[n % 16]
    second = h[n // 16]
    return str(second)+ str(first)

#convierte un numero del sistema hexadecimal al decimal
def hex_to_dec(n):
    hexa = n[::-1]
    d = 0
    for ind in range(0, len(hexa)):
        d += h1.index(hexa[ind].upper()) * (16 ** ind)
        
    return d

def time_handler():
    global color1, r, g, b, t, red, blue, r, b, inc
    t += inc
    if(t == 200):
        inc *= -1
    elif(t == 0 and inc < 0):
        timer1.stop()
        red = "00"
        blue = "00"
        color1 = "#"+red+green+blue
        t = 0
        r = 0
        b = 0
        inc = 5
    else:
        dibuja()

def dibuja():
    global color1, red, blue, r, b
    r += inc
    b += inc
    red = dec_to_hex(r)
    blue = dec_to_hex(b)
    color1 = "#"+red+green+blue
    
#draw handler
def draw(c):
    global timer, aux, msj, time, score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    # draw mid line and gutters
    #draw line
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    #right gutters
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "#77BDE2")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "#E27777")
 
    #collision top and bottom
    if((ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS - 1)):
        ball_vel[1] *= -1
    if(ball_pos[0] <= BALL_RADIUS + PAD_WIDTH + 1):
        #left side
        #dont collision with the left paddle
        if(not (paddle1_pos <= ball_pos[1] <= paddle1_pos + PAD_HEIGHT)):
            score2 += 1
            aux = "Player 2 scores!! "
            direction = rand.randint(1, 2)
            spawn_ball(direction)
            timer.start()
        else:
            #collision with right paddle dont score
            timer1.start()
            ball_vel[0] *=-1
            #increase the velocity 10%
            ball_vel[0] = ball_vel[0] * .1 + ball_vel[0]

    elif(ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH - 1):
        #right side
         #dont collision with the left paddle
        if(not (paddle2_pos <= ball_pos[1] <= paddle2_pos + PAD_HEIGHT)):
            score1 += 1
            direction = rand.randint(3, 4)
            aux = "Player 1 scores!! "
            spawn_ball(direction)
            timer.start()
        else:
            #collision with right paddle dont score
            timer1.start()
            ball_vel[0] *= -1
            #increase the velocity 10%
            ball_vel[0] = ball_vel[0] * .1 + ball_vel[0]
            
    #circulo medio
    c.draw_circle([WIDTH / 2, HEIGHT / 2], 30, 1, "white") 
    
    # update ball
    if(not timer.is_running() and pausa == False):
        ball_pos[0] += ball_vel[0]   
        ball_pos[1] += ball_vel[1]  
        
    # draw ball
        c.draw_circle(ball_pos, BALL_RADIUS, 2, color2, color1)
        c.draw_line(ball_pos, [ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS], 5, "black")
        c.draw_line(ball_pos, [ball_pos[0] - BALL_RADIUS, ball_pos[1] + BALL_RADIUS], 5, "black")
        c.draw_line(ball_pos, [ball_pos[0] + BALL_RADIUS, ball_pos[1] - BALL_RADIUS], 5, "black")
        c.draw_line(ball_pos, [ball_pos[0] + BALL_RADIUS, ball_pos[1] + BALL_RADIUS], 5, "black")
    else:
    # draw ball
        c.draw_circle(ball_pos, BALL_RADIUS, 2, color2, color1)
        c.draw_line(ball_pos, [ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS], 5, "black")
        c.draw_line(ball_pos, [ball_pos[0] - BALL_RADIUS, ball_pos[1] + BALL_RADIUS], 5, "black")
        c.draw_line(ball_pos, [ball_pos[0] + BALL_RADIUS, ball_pos[1] - BALL_RADIUS], 5, "black")
        c.draw_line(ball_pos, [ball_pos[0] + BALL_RADIUS, ball_pos[1] + BALL_RADIUS], 5, "black")        
    
    if(time > 0 and timer.is_running()):
        msj = aux
        c.draw_text((msj+ str(time)), [WIDTH / 2 - 120, HEIGHT / 3], 20, "white")
    else:
        timer.stop()
        time = 3
        msj = ""
        
    # update paddle's vertical position, keep paddle on the screen        
    if(not timer.is_running() and pausa == False):
        
        if(paddle1_vel <= 0):
            if(paddle1_pos - abs(paddle1_vel) >= 0):
                #up side
                paddle1_pos += paddle1_vel
            else:
                paddle1_vel = 0
        else:
            if(paddle1_pos + abs(paddle1_vel) <= HEIGHT - PAD_HEIGHT):
                #down side
                paddle1_pos += paddle1_vel
            else:
                paddle1_vel = 0
        
        if(paddle2_vel <= 0):
            if(paddle2_pos - abs(paddle2_vel) >= 0):
                #up side
                paddle2_pos += paddle2_vel
            else:
                paddle2_vel = 0
        else:
            if(paddle2_pos + abs(paddle2_vel) <= HEIGHT - PAD_HEIGHT):
                #down side
                paddle2_pos += paddle2_vel
            else:
                paddle2_vel = 0
    
    # draw paddles
    #paddle 2
    c.draw_line([WIDTH - PAD_WIDTH / 2, paddle2_pos], [WIDTH - PAD_WIDTH / 2, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "red")
    #paddle 1
    c.draw_line([PAD_WIDTH / 2, paddle1_pos], [PAD_WIDTH / 2, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "#6EB5DB")
    
    # draw scores
    c.draw_text("Player 1: "+ str(score1), [WIDTH / 2 - 150, 40], 20, "#6EB5DB")
    c.draw_text("Player 2: "+ str(score2), [WIDTH / 2 + 20, 40], 20, "red")

    if(pausa):
        c.draw_text("JUEGO PAUSADO", [WIDTH / 2 - 100, HEIGHT / 2], 20, 'white')

#key down handler
def keydown(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP['w']):
        #is up
        paddle1_vel -= PADDLE1_VEL
    if(key == simplegui.KEY_MAP['s']):
        #is down
        paddle1_vel += PADDLE1_VEL
    
    if(key == simplegui.KEY_MAP['up']):
        #is up
        paddle2_vel -= PADDLE2_VEL
    if(key == simplegui.KEY_MAP['down']):
        #is down
        paddle2_vel += PADDLE2_VEL
    if(key == simplegui.KEY_MAP['space']):
        pause()
        
#key up handler    
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if(key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']):
        paddle1_vel = 0
    if(key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']):
        paddle2_vel = 0

#reset the game
def reset():
    if(not pausa):
        new_game()

#
def score():
    global time
    time -= 1
#pause the game
def pause():
    global pausa
    pausa = not pausa
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 50)
timer = simplegui.create_timer(1000, score)
timer1 = simplegui.create_timer(0.001, time_handler)
frame.add_button("Pausa", pause, 50)
frame.add_label("Presiona space para pausar el juego,\n usa las teclas de direccion arriba\n y abajo para mover al player2,\nusa la letras W y S para mover al player1.")
# start frame
new_game()
frame.start()
