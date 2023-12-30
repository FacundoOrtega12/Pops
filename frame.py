from draw import Draw
import random
import pygame
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

