# Implementation of classic arcade game Pong

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 8
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
acc = 2
vel_acc = 5
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0]
score1 = 0
score2 = 0
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
paddle1_pos = [PAD_WIDTH, (HEIGHT/2-HALF_PAD_HEIGHT)]
paddle2_pos = [PAD_WIDTH, (HEIGHT/2-HALF_PAD_HEIGHT)]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, acc # these are vectors stored as lists
    
    if (direction == LEFT):
        ball_pos = [WIDTH/2, HEIGHT/2]
        ball_vel=[0,0]
        ball_vel[0] -= acc
        ball_vel[1] -= acc
        frame.set_draw_handler(draw)
    elif (direction == RIGHT):
        ball_pos = [WIDTH/2, HEIGHT/2]
        ball_vel=[0,0]
        ball_vel[0] += acc
        ball_vel[1] -= acc
        frame.set_draw_handler(draw)
        
def spawn_paddles():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    paddle1_pos = [PAD_WIDTH, (HEIGHT/2-HALF_PAD_HEIGHT)]
    paddle2_pos = [PAD_WIDTH, (HEIGHT/2-HALF_PAD_HEIGHT)]

        


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_paddles()
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
     
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -(ball_vel[1])
    elif(ball_pos[1] >= (HEIGHT-BALL_RADIUS)):
        ball_vel[1] = -(ball_vel[1])
    
        
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS, 5, 'white', 'white') 
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1 = [(0,paddle1_pos[1]),(0,(paddle1_pos[1]+PAD_HEIGHT)),(PAD_WIDTH,(paddle1_pos[1]+PAD_HEIGHT)), (PAD_WIDTH,paddle1_pos[1])]
    paddle2 = [((WIDTH-PAD_WIDTH),paddle2_pos[1]),((WIDTH-PAD_WIDTH),(paddle2_pos[1]+PAD_HEIGHT)),(WIDTH,(paddle2_pos[1]+PAD_HEIGHT)), (WIDTH,paddle2_pos[1])]
    
    if((0 < paddle1_pos[1]) and (paddle1_vel[1] == -5)):
        paddle1_pos[1] += paddle1_vel[1]
    if ((paddle1_pos[1] < (HEIGHT-PAD_HEIGHT)) and (paddle1_vel[1] == 5)):
        paddle1_pos[1] += paddle1_vel[1]
    
   
        
    if((0 < paddle2_pos[1]) and (paddle2_vel[1] == -5)):
        paddle2_pos[1] += paddle2_vel[1]
    if ((paddle2_pos[1] < (HEIGHT-PAD_HEIGHT)) and (paddle2_vel[1] == 5)):
        paddle2_pos[1] += paddle2_vel[1]
    
    
    # draw paddles
    canvas.draw_polygon(paddle1,2,'red','red')
    canvas.draw_polygon(paddle2,2,'blue','blue')
    
    # determine whether paddle and ball collide    
    if (ball_pos[0] <= BALL_RADIUS+PAD_WIDTH):
        if ((paddle1_pos[1]-(BALL_RADIUS*(0.85))) <= (ball_pos[1]) <= (paddle1_pos[1]+PAD_HEIGHT+BALL_RADIUS*(0.85))): 
            ball_vel[0] = -(ball_vel[0]-0.5)
        else:
            score2 += 1
            spawn_ball(RIGHT)
    if (ball_pos[0] >= ((WIDTH-BALL_RADIUS)-PAD_WIDTH)):
            if ((paddle2_pos[1]-(BALL_RADIUS*(0.85))) <= (ball_pos[1]) <= (paddle2_pos[1]+PAD_HEIGHT+BALL_RADIUS*(0.85))):
                ball_vel[0] = -(ball_vel[0]+0.5)
            else:
                score1 += 1
                spawn_ball(LEFT)
    # draw scores
    canvas.draw_text(str(score1),[(WIDTH/4),40],40,'white')
    canvas.draw_text(str(score2),[(WIDTH-WIDTH/4),40],40,'white')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if (key == simplegui.KEY_MAP['w']):
        paddle1_vel[1] -= vel_acc
  
    if (key == simplegui.KEY_MAP['up'] ) :
        paddle2_vel[1] -= vel_acc  
            
    if (key == simplegui.KEY_MAP['s']):
        paddle1_vel[1] += vel_acc
        
    if (key == simplegui.KEY_MAP['down']):
        paddle2_vel[1] += vel_acc
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if (key == simplegui.KEY_MAP['w']):
        paddle1_vel[1] = 0
    if (key == simplegui.KEY_MAP['up'] ) :
        paddle2_vel[1] = 0
       
    if (key == simplegui.KEY_MAP['s']):
        paddle1_vel[1] = 0
    if (key == simplegui.KEY_MAP['down']):
         paddle2_vel[1] = 0
    
   

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(new_game)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('RESTART GAME',new_game)



# start frame
new_game()
frame.start()
