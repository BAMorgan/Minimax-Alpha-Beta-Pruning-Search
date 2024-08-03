#Brandon Morgan
#6-23-24
#TCSS435

import random
import pyamaze as maze

#can change size with maze(x,y)
m = maze.maze(20,30)

#random goal cell
x = random.randint(1,20)
y = random.randint(1,30)

m.CreateMaze(x,y,theme=maze.COLOR.light)

#agents
a = maze.agent(m,8,9,shape = 'arrow', footprints= True)
b = maze.agent(m,14,15,shape = 'square', footprints= True, color=maze.COLOR.red)

#path can be dictionary, list or string
#m.tracePath({a:[(8,9),(7,9),(6,9)]})
#m.tracePath({a:‘EENWWSES’})
a_path = {(8,9):(7,9), (7,9):(6,9)}

#random direction string
directions = ['E', 'E','E','W', 'W', 'W', 'N','N', 'N','S', 'S', 'S']

random.shuffle(directions)
random_directions = ''.join(directions)

#tracing
m.tracePath({b:random_directions})
m.tracePath({a:a_path})

m.run()