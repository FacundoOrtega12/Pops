import pygame

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