## Turtle Runaway
author : 21101234 최동주

### Discription
Run away from chaser - There are 3 turtles :  red, blue, and green

- **Blue turtle (_runner, ManualMover_)** : user. you can move by pressing key.
- **Green turtle (_AiChaser, ChaserMover_)** : tracks user, speed increases as time goes by.
- **Red turtle (_chaser, RandomMover_)** :  basically randomly moves, but fast and when too far away from user, then it seek and head toward user.


### Rules:
The objective is to avoid being caught by the two chasers for as long as possible. The game ends when either chaser catches the player. The program exit automatically after game ends.

### Score : 
- when you move up/down, you get 10 points.
- whenever the timer update, you get 'elapsed time' point (because it becomes more difficult to survive as the time passes)

### Code Discription
- used '_time_drawer_' turtle, **function** '_update_timer_'
- edited _ManualMover_(to scoring), _RandomMover_(to seek user when move too far away from user)
- new class '_ChaseMover_' : seek and track user, speed up logic
- new turtle using '_ChaseMover_'
- score system - used '_score_drawer_', **function** '_increase score_', '_update_score_display_' 