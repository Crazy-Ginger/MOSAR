from morse.builder import *


class CubeModule(Robot):
    """
    A template robot model for cubemodule, with a motion controller and a pose sensor.
    """
    def __init__(self, name = None, colour = None, debug = False):

        # cubemodule.blend is located in the data/robots directory
        Robot.__init__(self, "modules/robots/cubemodule.blend", name) #determines Blender model.blend
        self.properties(classpath = "modules.robots.cubemodule.CubeModule") #determines robot script.py

        if colour is not None:
                print(dir(self))
                self._bpy_object.color = colour

        ###################################
        # Actuators
        ###################################

        # (v,w) motion controller
        # Check here the other available actuators:
        # http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
        #self.motion = MotionVW()
        #self.motion.add_stream('socket')
        #self.append(self.motion)

        destination = Destination()
        destination.add_stream('socket')
        destination.add_service('socket')
        destination.properties(Speed=2.0, Tolerance=0.05, RemainAtDestination = False)
        self.append(destination)

        # Optionally allow to move the robot with the keyboard

        if debug:
            keyboard = Keyboard()
            keyboard.properties(ControlType = 'Position')
            self.append(keyboard)

        ###################################
        # Sensors
        ###################################

        pose = Pose()
        self.append(pose)
        pose.add_stream('socket')

        ###################################
        # Services
        ###################################

        self.add_service('socket')

        ###################################
        # Other Properties
        ###################################

        #self.set_rigid_body() #done in Blender model
        #self.set_collision_bounds() #done in Blender model
        #self.set_no_collision() #if you don't want collisions
