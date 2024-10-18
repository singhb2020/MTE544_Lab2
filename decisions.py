# Imports


import sys

from utilities import euler_from_quaternion, calculate_angular_error, calculate_linear_error
from pid import PID_ctrl

from rclpy import init, spin, spin_once
from rclpy.node import Node
from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile
from nav_msgs.msg import Odometry as odom

from localization import localization, rawSensor

from planner import TRAJECTORY_PLANNER, POINT_PLANNER, planner
from controller import controller, trajectoryController

# You may add any other imports you may need/want to use below
# import ...
from numpy import cos, sin


class decision_maker(Node):
    
    def __init__(self, publisher_msg, publishing_topic, qos_publisher, goalPoint, rate=10, motion_type=POINT_PLANNER):

        super().__init__("decision_maker")

        # DONE Part 4: Create a publisher for the topic responsible for robot's motion
        self.publisher=self.create_publisher(publisher_msg, publishing_topic, qos_publisher)

        publishing_period=1/rate
        
        #Threshold for goal pose error
        self.threshold_lin = 0.1
        self.threshold_ang = 0.1
        self.traj_index = 0

        # Instantiate the controller
        # TODO Part 5: Tune your parameters here
    
        if motion_type == POINT_PLANNER:
            self.controller=controller(klp=0.2, klv=0.5, kap=0.8, kav=0.6)
            self.planner=planner(POINT_PLANNER)    
    
    
        elif motion_type==TRAJECTORY_PLANNER:
            self.controller=trajectoryController(klp=0.2, klv=0.5, kap=0.8, kav=0.6)
            self.planner=planner(TRAJECTORY_PLANNER)

        else:
            print("Error! you don't have this planner", file=sys.stderr)


        # Instantiate the localization, use rawSensor for now  
        self.localizer=localization(rawSensor)

        # Instantiate the planner
        # NOTE: goalPoint is used only for the pointPlanner
        self.goal=self.planner.plan(goalPoint)

        self.create_timer(publishing_period, self.timerCallback)


    def timerCallback(self):
        
        # DONE Part 3: Run the localization node
        # Remember that this file is already running the decision_maker node.
        spin_once(self.localizer)

        if self.localizer.getPose()  is  None:
            print("waiting for odom msgs ....")
            return

        vel_msg=Twist()
        
        # DONE Part 3: Check if you reached the goal
        reached_goal = False
        curr_pose = self.localizer.getPose()

        #Trajectory is of type list, Point is else
        if type(self.goal) == list:
            # Trajectory
            # Check that the linear error and the angular error are within the threshold
            # for the current target point in the trajectory
            if (calculate_linear_error(curr_pose, self.goal[self.traj_index]) < self.threshold_lin
            and calculate_angular_error(curr_pose, self.goal[self.traj_index]) < self.threshold_ang):
                # True if this is the last point in the trajectory list
                # (length of list is 1 greater than last index of list)
                if (self.traj_index + 1 == len(self.goal)):
                    reached_goal = True
                    self.traj_index = 0
                else:
                    # Otherwise increment to next point in the trajectory
                    self.traj_index += 1
        else:
            #Point
            if (calculate_linear_error(curr_pose, self.goal) < self.threshold_lin and calculate_angular_error(curr_pose, self.goal) < self.threshold_ang):
                reached_goal = True
        

        if reached_goal:
            print("reached goal")
            self.publisher.publish(vel_msg)
            
            self.controller.PID_angular.logger.save_log()
            self.controller.PID_linear.logger.save_log()
            
            # DONE Part 3: exit the spin
            # Might be wrong
            raise SystemExit
        
        velocity, yaw_rate = self.controller.vel_request(self.localizer.getPose(), self.goal, True)

        # DONE Part 4: Publish the velocity to move the robot

        # Get the current theta relative to the global frame
        theta = self.localizer.getPose()[2]

        # Calculate the x and y components of the velocity
        x_vel = velocity * cos(theta)
        y_vel = velocity * sin(theta)

        # Add the linear and angular velocities to the twist message
        vel_msg.linear.x = x_vel
        vel_msg.linear.y = y_vel
        vel_msg.angular.z = yaw_rate       

        # Publish the twist message
        self.publisher.publish(vel_msg)

import argparse


def main(args=None):
    
    init()

    # DONE Part 3: You migh need to change the QoS profile based on whether you're using the real robot or in simulation.
    # Remember to define your QoS profile based on the information available in "ros2 topic info /odom --verbose" as explained in Tutorial 3
    
    odom_qos=QoSProfile(reliability=2, durability=2, history=1, depth=10)
    

    # TODO Part 4: instantiate the decision_maker with the proper parameters for moving the robot
    if args.motion.lower() == "point":
        # Third argument has an associated assumption in decision_maker class that qos_publisher
        # [1.0, -1.0] is the point we are going towards
        DM=decision_maker(publisher_msg=Twist,
                          publishing_topic='/cmd_vel',
                          qos_publisher=10,
                          goalPoint=[1.0, -1.0],
                          rate=10,
                          motion_type=POINT_PLANNER)
    # TODO Part 5: Tyler added to add instantiating message for trajectory case
    elif args.motion.lower() == "trajectory":
        DM=decision_maker(...)
    else:
        print("invalid motion type", file=sys.stderr)        
    
    
    
    try:
        spin(DM)
    except SystemExit:
        print(f"reached there successfully {DM.localizer.pose}")


if __name__=="__main__":

    argParser=argparse.ArgumentParser(description="point or trajectory") 
    argParser.add_argument("--motion", type=str, default="point")
    args = argParser.parse_args()

    main(args)
