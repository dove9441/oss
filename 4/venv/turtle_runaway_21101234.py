# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time
import math

class RunawayGame:
    def __init__(self, canvas, runner, chaser, AiChaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.AiChaser = AiChaser
        self.catch_radius2 = catch_radius**2
        self.score = 0
        

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()
        self.runner.game = self

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        self.AiChaser.shape('turtle')
        self.AiChaser.color('green')
        self.AiChaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        # 타이머
        self.timer_drawer = turtle.RawTurtle(canvas)
        self.timer_drawer.hideturtle()
        self.timer_drawer.penup()
        
        # 점수 표시
        self.score_drawer = turtle.RawTurtle(canvas)
        self.score_drawer.hideturtle()
        self.score_drawer.penup()

    def increase_score(self):
        self.score += 10

    def update_score_display(self):
        self.score_drawer.undo()
        self.score_drawer.penup()
        self.score_drawer.setpos(-200, 300)
        self.score_drawer.write(f'score: {self.score}\nscore : travel distance(10 points per up/down) + time(\'elapsed time\' points whenever timer update)')

    
    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        r = self.AiChaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        a, b = p[0] - r[0], p[1] - r[1]
        return (dx**2 + dy**2 < self.catch_radius2) or (a**2 + b**2 < self.catch_radius2)

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        self.AiChaser.setpos((+init_dist / 2, 0))
        self.AiChaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        self.start_time = time.time()


    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        self.AiChaser.run_ai(self.runner.pos(), self.runner.heading())
        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}')
        if(is_catched):
            self.drawer.penup()
            self.drawer.setpos(0, 0)
            self.drawer.write(f'Game over.\nscore : {self.score}\n exit after 3 seconds ...',align='center',font=('Arial', 16, 'normal'))
            time.sleep(3)
            exit()

        self.update_timer()
        self.update_score_display()
        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def update_timer(self):
        elapsed_time = float(time.time() - self.start_time)
        self.timer_drawer.undo()
        self.timer_drawer.penup()
        self.timer_drawer.setpos(-300, 250)  # Set position for the timer display
        self.timer_drawer.write(f'버틴 시간: {elapsed_time:.2f} 초')
        
        self.score += int(elapsed_time)


class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10, game=None):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.game = game
        # Register event handlers

        # up 또는 down 시 점수 증가(도망친 거리)
        canvas.onkeypress(self.move_up, 'Up')
        canvas.onkeypress(self.move_down, 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def move_up(self):
        self.forward(self.step_move)
        if self.game:
            self.game.increase_score()  

    def move_down(self):
        self.backward(self.step_move)
        if self.game:
            self.game.increase_score()  

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=100, step_turn=100): 
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, runner_pos, opp_heading):
        chaser_x, chaser_y = self.pos()
        runner_x, runner_y = runner_pos
        # 랜덤으로 이동하다가 너무 멀리 떨어지면 방향을 유저 쪽으로 재설정
        if(math.hypot(runner_x- chaser_x, runner_y - chaser_y)>325):
            self.setheading(math.degrees(math.atan2(runner_y - chaser_y, runner_x - chaser_x)))
            self.forward(self.step_move)
        else:
            mode = random.randint(1,10)
            if(mode <= 2):
                self.left(self.step_turn)
            elif(mode <= 4):
                self.right(self.step_turn)
            else:
                self.forward(self.step_move)




# ManualMover를 추적하는 chaserMover
class ChaserMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.start_time = time.time()

    def run_ai(self, runner_pos, runner_heading):
        # Chaser는 runner의 위치로 향해 이동해야 함
        chaser_x, chaser_y = self.pos()
        runner_x, runner_y = runner_pos

        # 두 점 사이의 각도 계산
        angle_to_runner = math.degrees(math.atan2(runner_y - chaser_y, runner_x - chaser_x))
        
        # Chaser의 방향을 runner 방향으로 설정하고 이동
        elapsed_time = int(time.time() - self.start_time)   
        self.setheading(angle_to_runner)
        # 시간이 지날 때마다 가속
        self.forward(self.step_move*elapsed_time/5)



if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = ManualMover(screen)
    chaser = RandomMover(screen)
    AiChaser = ChaserMover(screen)

    game = RunawayGame(screen, runner, chaser, AiChaser)
    game.start()
    screen.mainloop()
