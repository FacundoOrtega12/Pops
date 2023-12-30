from frame import Frame
import random
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    K_RETURN,
    K_q,
    K_a,
    QUIT,
)

def main(): 
    non_changing_state = {
        'court_x': 825,   # constants: 825x525 was original resolution of Pong
        'court_y': 525, 
        'paddle_x': 10,   # paddle width
        'paddle_y': 50,   # paddle length  
        'ball_size': 10 } 
    frame = Frame(non_changing_state)
    start_vel = (random.randint(10, 20), random.randint(10,15))
    frame.init(
        start_pos=(408,258), 
        start_vel=start_vel 
        )

    running = True
    
    time_delay = 50 
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:      # only deals with first instance of pressed button
                if event.key == K_ESCAPE:
                    running = False                
                if event.key == K_RETURN:
                    frame.play()
            if event.type == pygame.QUIT:
                running = False
            if event.type == timer_event:
                frame.tick()
                keys = pygame.key.get_pressed()   # allows user to hold down button and still move
                if keys[pygame.K_UP]:           #up-arrow
                    frame.move_pad_b_up()
                if keys[pygame.K_DOWN]:         #down-arrow
                    frame.move_pad_b_down()
                if keys[pygame.K_q]:            #q-key
                    frame.move_pad_a_up()
                if keys[pygame.K_a]:            #a-key
                    frame.move_pad_a_down()          

    frame.quit()

if __name__ == "__main__":
    main()

