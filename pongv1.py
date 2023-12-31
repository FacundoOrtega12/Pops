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




class Frame:
    def __init__(self, nce:dict):
        self.nce = nce
        self.time_index = 0
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.prev_x = 0
        self.prev_y = 0
        self.paddle_a_x = 0
        self.paddle_a_y = 0
        self.paddle_b_x = 0
        self.paddle_b_y = 0
        self.paddles_on = False
        self.inplay = False
        self.score_a = 0
        self.score_b = 0
        self.draw = Draw()
        self.game_start_count = 0


    def init(self,
            start_pos:tuple,
            start_vel:tuple):
        self.time_index = 0
        self.x_pos = start_pos[0]
        self.y_pos = start_pos[1]
        self.x_vel = start_vel[0]
        self.y_vel = start_vel[1]
        self.paddle_a_x = 69
        self.paddle_a_y = 263
        self.paddle_b_x = 756
        self.paddle_b_y = 263
        self.paddles_on = True
        self.inplay = False
        self.draw.init(self.nce)

    def quit(self):
        self.draw.quit()

    def play(self):
        self.score_a = 0
        self.score_b = 0
        self.draw.set_score(0,0)
        self.draw.init(self.nce)
        self.inplay = True

    def tick(self):
        self.game_start_count = (self.game_start_count + 1) % 100

        if self.game_start_count == 0:
            end_score = 11
            if not self.inplay and (self.score_a < end_score and self.score_b < end_score): 
                self.inplay = True
                if self.x_vel < 40:
                    self.x_vel = -self.x_vel
                else: 
                    self.x_vel = 10
                self.y_vel = 0.2*random.randint(-20, 20) # random y-axis velocity for serve

        self.next_frame()

    def next_frame(self):
        if self.inplay:
            next_px, next_py, next_vx, next_vy = self.adjust_next(
                self.paddles_on,
                self.x_pos + self.x_vel,
                self.y_pos + self.y_vel)

            self.x_pos = next_px
            self.y_pos = next_py
            self.x_vel = next_vx
            self.y_vel = next_vy

            if self.detect_point_a():
                self.score_b = self.score_b + 1
            if self.detect_point_b():
                self.score_a = self.score_a + 1

            if self.detect_point_a() or self.detect_point_b():
                self.inplay = False
                self.draw.set_score(self.score_a, self.score_b)
                self.x_pos = self.nce["court_x"]/2
                self.y_pos = self.nce["court_y"]/2

            self.draw.ball(self.nce["ball_size"], (self.x_pos,self.y_pos) )

        self.draw.paddle((self.paddle_a_x, self.paddle_a_y), "a")
        self.draw.paddle((self.paddle_b_x, self.paddle_b_y), "b")

    def adjust_next(
            self,
            paddles_on: bool,
            candidate_px: int,
            candidate_py: int) -> (int, int, int, int):
        
        keys = pygame.key.get_pressed()
        if self.detect_collision_B(paddles_on, candidate_px, candidate_py):
            next_px = self.next_B_px(paddles_on, candidate_px, candidate_py)   
            if keys[pygame.K_UP]:
                next_vx = -self.x_vel - 2
                next_vy = self.y_vel + 5
            if keys[pygame.K_DOWN]:
                next_vx = -self.x_vel - 2
                next_vy = self.y_vel - 5
            else:
                next_vx = -self.x_vel

        elif self.detect_collision_A(paddles_on, candidate_px, candidate_py):
            next_px = self.next_A_px(paddles_on, candidate_px, candidate_py)
            if keys[pygame.K_q]:
                next_vx = -self.x_vel + 2
                next_vy = self.y_vel + 5
            if keys[pygame.K_a]:
                next_vx = -self.x_vel + 2
                next_vy = self.y_vel - 5
            else:
                next_vx = -self.x_vel
        else:
            next_px = candidate_px
            next_vx = self.x_vel

        if candidate_py > self.nce["court_y"]:
            delta_y_pos = candidate_py - self.nce["court_y"]
            next_py = self.nce["court_y"] - delta_y_pos
            next_vy = -self.y_vel
        elif candidate_py < 0:
            next_py = -candidate_py
            next_vy = -self.y_vel
        else:
            next_py = candidate_py
            next_vy = self.y_vel

        return next_px, next_py, next_vx, next_vy

    def detect_collision_A(
        self,
        paddles_on: bool,
        candidate_px: int,
        candidate_py: int) -> bool:

        if not paddles_on:
            return candidate_px < 0

        return (candidate_px <= self.paddle_a_x) and (candidate_py <= self.paddle_a_y + self.nce['paddle_y']/2) and (candidate_py >= self.paddle_a_y - self.nce['paddle_y']/2)

    def detect_collision_B(
        self,
        paddles_on: bool,
        candidate_px: int,
        candidate_py: int) -> bool:

        if not paddles_on:
            return candidate_px > self.nce["court_x"]

        return (candidate_px >= self.paddle_b_x) and (candidate_py <= self.paddle_b_y + self.nce['paddle_y']/2) and (candidate_py >= self.paddle_b_y - self.nce['paddle_y']/2)

    def next_B_px(
        self,
        paddles_on: bool,
        candidate_px: int,
        candidate_py: int) -> int:

        if not paddles_on:
            delta_x_pos = candidate_px - self.nce["court_x"]
            next_px = self.nce["court_x"] - delta_x_pos
            return next_px

        delta_x_pos = candidate_px - self.paddle_b_x
        next_px = self.paddle_b_x - delta_x_pos
        return next_px

    def next_A_px(
        self,
        paddles_on: bool,
        candidate_px: int,
        candidate_py: int) -> int:

        if not paddles_on:
            return -candidate_px

        delta_x_pos = candidate_px - self.paddle_a_x
        next_px = self.paddle_a_x - delta_x_pos
        return next_px

    def detect_point_a(self):
        return (self.x_pos <= self.paddle_a_x) and not ( (self.y_pos <= self.paddle_a_y + self.nce['paddle_y']/2) and (self.y_pos >= self.paddle_a_y - self.nce['paddle_y']/2) )

    def detect_point_b(self):
        return (self.x_pos >= self.paddle_b_x) and not ( (self.y_pos <= self.paddle_b_y + self.nce['paddle_y']/2) and (self.y_pos >= self.paddle_b_y - self.nce['paddle_y']/2) )

    def move_pad_a_up(self):
        if self.paddle_a_y > 0:
            self.paddle_a_y = self.paddle_a_y - 20

    def move_pad_a_down(self):
        if self.paddle_a_y < self.nce['court_y']:
            self.paddle_a_y = self.paddle_a_y + 20

    def move_pad_b_up(self):
        if self.paddle_b_y > 0:
            self.paddle_b_y = self.paddle_b_y - 20

    def move_pad_b_down(self):
        if self.paddle_b_y < self.nce['court_y']:
            self.paddle_b_y = self.paddle_b_y + 20

class Draw:
    digits = [  #digits written in 4x5 arrays 
        ((1,1,1,1),(1,0,0,1),(1,0,0,1),(1,0,0,1),(1,1,1,1)), #0
        ((0,0,0,1),(0,0,0,1),(0,0,0,1),(0,0,0,1),(0,0,0,1)), #1
        ((1,1,1,1),(0,0,0,1),(1,1,1,1),(1,0,0,0),(1,1,1,1)), #2
        ((1,1,1,1),(0,0,0,1),(0,0,1,1),(0,0,0,1),(1,1,1,1)), #3
        ((1,0,0,1),(1,0,0,1),(1,1,1,1),(0,0,0,1),(0,0,0,1)), #4
        ((1,1,1,1),(1,0,0,0),(1,1,1,1),(0,0,0,1),(1,1,1,1)), #5
        ((1,1,1,1),(1,0,0,0),(1,1,1,1),(1,0,0,1),(1,1,1,1)), #6
        ((1,1,1,1),(0,0,0,1),(0,0,0,1),(0,0,0,1),(0,0,0,1)), #7
        ((1,1,1,1),(1,0,0,1),(1,1,1,1),(1,0,0,1),(1,1,1,1)), #8
        ((1,1,1,1),(1,0,0,1),(1,1,1,1),(0,0,0,1),(1,1,1,1)), #9
    ]
    
    def __init__(self):
        self.court = None
        self.prev_x = 0
        self.prev_y = 0
        self.nce = None
        self.score_a = 0        
        self.score_b = 0
        self.prev_pad_a_y = 0
        self.prev_pad_b_y = 0
                
    def init(self, nc_state:dict):
        pygame.init()
        self.nce = nc_state
        self.court = pygame.display.set_mode((nc_state["court_x"], nc_state["court_y"])) 
        self.pitch()

    def quit(self):
        pygame.quit()

    def halfcourt_line(self):
        y_pos = 7
        x_pos = 412
        for _ in range(43):
            pygame.draw.rect(self.court, (255, 255, 255), (x_pos, y_pos, 2, 8))
            y_pos = y_pos + 12

    def pitch(self):
        self.court.fill((0, 0, 0))
        self.halfcourt_line()
        self.display_score() 
        pygame.display.flip()

    def paddle(self, paddle_xy_pos, paddle_name:str):
        paddle_size = (self.nce['paddle_x'], self.nce['paddle_y'])
        paddle = pygame.Surface(paddle_size)
        
        new_pad_x = paddle_xy_pos[0]-int(0.5*paddle_size[0])
        new_pad_y = paddle_xy_pos[1]-int(0.5*paddle_size[1])

        # draws the black paddle to cover previous frame's paddle
        paddle.fill((0, 0, 0))
        if paddle_name == "a":
            self.court.blit(paddle, (new_pad_x, self.prev_pad_a_y)) # "plugs hole" with black 
        else:
            self.court.blit(paddle, (new_pad_x, self.prev_pad_b_y)) # "plugs hole" with black 
        #pygame.display.flip()

        # repaints in case the black removed other things
        self.halfcourt_line()
        self.display_score() 

        # draws the whit paddle, starting from up-left corner

        paddle.fill((255,255,255))
        self.court.blit(paddle, (new_pad_x, new_pad_y))
        pygame.display.flip()

        # save for next black painting
        if paddle_name == "a":
            self.prev_pad_a_y = new_pad_y
        else:
            self.prev_pad_b_y = new_pad_y

    def ball(self, ball_size, ball_xy_pos):
        ball = pygame.Surface((ball_size, ball_size))
        
        ball.fill((0, 0, 0)) # creates black ball to cover previous frame's ball
        self.court.blit(ball, (self.prev_x, self.prev_y)) # "plugs hole" with black ball
        self.halfcourt_line()
        self.display_score() 

        new_x = ball_xy_pos[0]-int(0.5*ball_size)
        new_y = ball_xy_pos[1]-int(0.5*ball_size)
        self.prev_x = new_x
        self.prev_y = new_y     
        #pygame.display.flip()

        ball.fill((255,255,255))
        self.court.blit(ball, (new_x, new_y))

        pygame.display.flip()

    def set_score(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b
            
    def display_score(self):
        self.score(self.score_a, self.nce["ball_size"], "left", (self.nce["court_x"], self.nce["court_y"])) 
        self.score(self.score_b, self.nce["ball_size"], "right", (self.nce["court_x"], self.nce["court_y"]))

    def score(self, score:int, ball_size:int, side, screen_size):
        if side == 'left':
            offset_x = 0.33 * screen_size[0]
            offset_y = 0.1 * screen_size[1] 
        if side == 'right':
            offset_x = 0.8 * screen_size[0]
            offset_y = 0.1 * screen_size[1] 

        units = score % 10
        self.digit(Draw.digits[units], ball_size, (offset_x + ball_size, offset_y))
        tens = int(score / 10)
        if tens > 0:
            self.digit(Draw.digits[tens], ball_size, (offset_x - 6 * ball_size, offset_y))
        pygame.display.flip()

    def digit(self, digit:tuple, ball_size:int, offset_xy):    
        for i_line in range(len(digit)):
            line = digit[i_line]
            for i_column in range(len(line)):
                column = line[i_column]
                pixel = pygame.Surface((ball_size,ball_size))
                if column == 1:
                    pixel.fill((255,255,255))
                if column == 0:
                    pixel.fill((0,0,0))

                self.court.blit(pixel, (offset_xy[0] + ball_size*i_column, offset_xy[1] + ball_size*i_line))


#center
                
#paddle positions
                
#

def calc_fps(x):
    
   return int(1000/x)




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
    
    fps = calc_fps(60) # changes fps to desired amount
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, fps)

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

