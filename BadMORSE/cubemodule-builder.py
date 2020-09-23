import logging; logger = logging.getLogger("morserobots." + __name__)

from morse.builder import GroundRobot, Robot, WheeledRobot


class CubeModule(Robot):
    def __init__(self, name=None):
        Robot.__init__(self, "cubemodule", name)  # determines Blender model.blend
        self.properties(classpath="morse.robots.cubemodule.CubeModule")  # determines robot script.py
        # self.set_rigid_body()  # done in Blender model
        # self.set_collision_bounds()  # done in Blender model
        # self.set_no_collision() #if you don't want collisions
