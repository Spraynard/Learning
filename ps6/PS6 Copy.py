import math
import random

import ps6_visualize
import matplotlib as mpl
mpl.use('TkAgg')
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y): 
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

#Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        if width < 0 or height < 0:
            raise ValueError("Width and height must both be above zero")
        self.x = width
        self.y = height
        self.tiles = {}

        for i in range(self.x):
            for j in range(self.y):
                self.tiles[(i,j)] = "d"
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x, y = math.floor(pos.getX()), math.floor(pos.getY())
        
        self.tiles[(x,y)] = "c"

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.tiles[(m,n)] == "c":
            return True
        return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.x*self.y

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        count = 0

        for key in self.tiles.keys():
            if self.tiles[key] == "c":
                count += 1
        return count
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        xList = list(range(self.x))
        yList = list(range(self.y))

        return Position(random.choice(xList),random.choice(yList))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if (pos.getX() > self.x) or (pos.getY() > self.y):
            return False
        elif (pos.getX() < 0) or (pos.getY() < 0):
            return False
        return True

    def getRoom(self):
        print self.tiles

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        self.direction = random.randrange(0,360)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position
        
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction
        
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotPosition(getNewPosition(self.getRobotDirection(),self.speed))
        self.room.cleanTileAtPosition(self.position)

#Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        temp = self.position.getNewPosition(self.getRobotDirection(),self.speed)

        while (not self.room.isPositionInRoom(temp)):
            self.setRobotDirection(random.randrange(0,360))            
            temp = self.position.getNewPosition(self.getRobotDirection(),self.speed)

        self.setRobotPosition(temp)
        self.room.cleanTileAtPosition(self.getRobotPosition())
        
#Problem 3 
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    
    count_array = []
    
    #Dictionary with robots as keys and positions of robots as values

    for i in range(num_trials):
        count = 0
        #anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width,height)
        tiles_needed = min_coverage*room.getNumTiles()
        #roblist for the visualizer
        robList = []
        robPosDict = {}
        for num in range(num_robots):
            robList.append(StandardRobot(room,speed))
            if not type(robList[num]) == robot_type:
                robList[num] = RandomWalkRobot(room, speed)
                
            robPosDict[robList[num]] = robList[num].getRobotPosition()
            #print robPosDict[robList[num]].getX(), robPosDict[robList[num]].getY()
            
        while room.getNumCleanedTiles() < tiles_needed:
            #print "Number of Clean Tiles: ",room.getNumCleanedTiles()
            for robot in robPosDict.keys():
                robot.updatePositionAndClean()
                robPosDict[robot] = robot.getRobotPosition()
            #anim.update(room, robList)
            count += 1
        count_array.append(count)
        #anim.done()
    return sum(count_array)/len(count_array)
    
# === Problem 4

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    robotNum = [1,2,3,4,5,6,7,8,9,10]
    cleaningTimes = []

    for num in robotNum:
        cleaningTimes.append(runSimulation(num,1.0,20,20,.8,10,StandardRobot))

    pylab.xlabel('Number of Robots')
    pylab.ylabel('Cleaning Time')
    pylab.title ('Time it takes for increasing robots to clean 100% of a 25x25 square room')
    pylab.plot(robotNum,cleaningTimes)
    #pylab.axis([1,10,0,1000])
    pylab.show()
    
def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    fig = pylab.figure()
    ax = pylab.subplot(111)
    
    roomShapes = [[20,20],[25,16],[40,10],[50,8],[80,5],[100,4]]
    roomShapesStr = []
    cleaningTimes = []

    for shape in roomShapes:
        cleaningTimes.append(runSimulation(2,1.0,shape[0],shape[1],.80,10,StandardRobot))
        roomShapesStr.append(str(shape))

    print cleaningTimes
    pylab.xlabel('Room Shape')
    pylab.ylabel('Cleaning Time')
    pylab.title ('Time it takes for two robots to clean 80% of room based on room shape')
    ax.set_xticklabels(roomShapesStr)
    pylab.bar(roomShapes,cleaningTimes)
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        
        self.setRobotDirection(random.randrange(0,360))
        
        test = self.getRobotPosition().getNewPosition(self.getRobotDirection(),self.speed)

        while not (self.room.isPositionInRoom(test)):
            self.setRobotDirection(random.randrange(0,360))
            test = self.getRobotPosition().getNewPosition(self.getRobotDirection(),self.speed)

        self.setRobotPosition(test)
        self.room.cleanTileAtPosition(self.getRobotPosition())
            
#=== Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    regTimeSteps = []
    ranTimeSteps = []
    
    robot = [1,2,3,4,5,6,7,8,9,10]

    for num_bots in robot:
        regTimeSteps.append(runSimulation(num_bots,1.0,20,20,.8,3,StandardRobot))
        ranTimeSteps.append(runSimulation(num_bots,1.0,20,20,.8,3,RandomWalkRobot))
        
    pylab.xlabel("Number of Robots")
    pylab.ylabel("Time to Clean Room")
    pylab.title("Time difference of movestyle strategies based on # of robots")
    a = pylab.plot(robot,regTimeSteps, label = 'Standard Robot')
    b = pylab.plot(robot,ranTimeSteps, label = 'Random Robot')
    pylab.legend()
    pylab.show()
