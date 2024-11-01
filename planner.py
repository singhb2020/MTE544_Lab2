from numpy import exp, linspace

# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # DONE Part 6: Implement the trajectories here
    def trajectory_planner(self):
        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]

        #parabola
        def func1():
            #Step chosen arbitrarily
            #start=0, stop=1.5, samples=100
            #stop should be 1.5 but was adjusted to 1.1 for simulation testing
            full_range = linspace(start=0, stop=1.1, num=20)
            return [[i, i**2] for i in full_range]
        
        #sigmoid
        def func2():
            #Step chosen arbitrarily
            #start=0, stop=2.5, samples=100
            full_range = linspace(start=0, stop=2.5, num=20)
            return [[i, 2 / (1 + exp(-2 * i)) - 1] for i in full_range]

        return func1()

