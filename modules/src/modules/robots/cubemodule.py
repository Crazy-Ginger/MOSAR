import logging

import morse.core.robot
from morse.core import blenderapi
from morse.core.mathutils import Euler, Matrix, Quaternion, Vector
from morse.core.services import service

logger = logging.getLogger("morse." + __name__)

# WTF everything is:
# bge_object contents: ['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'actuators', 'addDebugProperty', 'alignAxisToVect', 'angularDamping', 'angularVelocity', 'angularVelocityMax', 'angularVelocityMin', 'applyForce', 'applyImpulse', 'applyMovement', 'applyRotation', 'applyTorque', 'attrDict', 'children', 'childrenRecursive', 'collisionCallbacks', 'collisionGroup', 'collisionMask', 'color', 'controllers', 'currentLodLevel', 'debug', 'debugRecursive', 'disableRigidBody', 'enableRigidBody', 'endObject', 'get', 'getActionFrame', 'getActionName', 'getAngularVelocity', 'getAxisVect', 'getDistanceTo', 'getLinearVelocity', 'getPhysicsId', 'getPropertyNames', 'getReactionForce', 'getVectTo', 'getVelocity', 'groupMembers', 'groupObject', 'invalid', 'isPlayingAction', 'isSuspendDynamics', 'life', 'linVelocityMax', 'linVelocityMin', 'linearDamping', 'linearVelocity', 'localAngularVelocity', 'localInertia', 'localLinearVelocity', 'localOrientation', 'localPosition', 'localScale', 'localTransform', 'mass', 'meshes', 'name', 'occlusion', 'orientation', 'parent', 'playAction', 'position', 'rayCast', 'rayCastTo', 'record_animation', 'reinstancePhysicsMesh', 'removeParent', 'replaceMesh', 'restoreDynamics', 'scaling', 'scene', 'sendMessage', 'sensors', 'setActionFrame', 'setAngularVelocity', 'setCollisionMargin', 'setDamping', 'setLinearVelocity', 'setOcclusion', 'setParent', 'setVisible', 'state', 'stopAction', 'suspendDynamics', 'timeOffset', 'visible', 'worldAngularVelocity', 'worldLinearVelocity', 'worldOrientation', 'worldPosition', 'worldScale', 'worldTransform']

# Position Vector contents: ['Fill', 'Linspace', 'Range', 'Repeat', '__add__', '__class__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__isub__', '__itruediv__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__neg__', '__new__', '__pos__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__rsub__', '__rtruediv__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', 'angle', 'angle_signed', 'copy', 'cross', 'dot', 'freeze', 'is_frozen', 'is_wrapped', 'length', 'length_squared', 'lerp', 'magnitude', 'negate', 'normalize', 'normalized', 'orthogonal', 'owner', 'project', 'reflect', 'resize', 'resize_2d', 'resize_3d', 'resize_4d', 'resized', 'rotate', 'rotation_difference', 'slerp', 'to_2d', 'to_3d', 'to_4d', 'to_track_quat', 'to_tuple', 'w', 'ww', 'www', 'wwww', 'wwwx', 'wwwy', 'wwwz', 'wwx', 'wwxw', 'wwxx', 'wwxy', 'wwxz', 'wwy', 'wwyw', 'wwyx', 'wwyy', 'wwyz', 'wwz', 'wwzw', 'wwzx', 'wwzy', 'wwzz', 'wx', 'wxw', 'wxww', 'wxwx', 'wxwy', 'wxwz', 'wxx', 'wxxw', 'wxxx', 'wxxy', 'wxxz', 'wxy', 'wxyw', 'wxyx', 'wxyy', 'wxyz', 'wxz', 'wxzw', 'wxzx', 'wxzy', 'wxzz', 'wy', 'wyw', 'wyww', 'wywx', 'wywy', 'wywz', 'wyx', 'wyxw', 'wyxx', 'wyxy', 'wyxz', 'wyy', 'wyyw', 'wyyx', 'wyyy', 'wyyz', 'wyz', 'wyzw', 'wyzx', 'wyzy', 'wyzz', 'wz', 'wzw', 'wzww', 'wzwx', 'wzwy', 'wzwz', 'wzx', 'wzxw', 'wzxx', 'wzxy', 'wzxz', 'wzy', 'wzyw', 'wzyx', 'wzyy', 'wzyz', 'wzz', 'wzzw', 'wzzx', 'wzzy', 'wzzz', 'x', 'xw', 'xww', 'xwww', 'xwwx', 'xwwy', 'xwwz', 'xwx', 'xwxw', 'xwxx', 'xwxy', 'xwxz', 'xwy', 'xwyw', 'xwyx', 'xwyy', 'xwyz', 'xwz', 'xwzw', 'xwzx', 'xwzy', 'xwzz', 'xx', 'xxw', 'xxww', 'xxwx', 'xxwy', 'xxwz', 'xxx', 'xxxw', 'xxxx', 'xxxy', 'xxxz', 'xxy', 'xxyw', 'xxyx', 'xxyy', 'xxyz', 'xxz', 'xxzw', 'xxzx', 'xxzy', 'xxzz', 'xy', 'xyw', 'xyww', 'xywx', 'xywy', 'xywz', 'xyx', 'xyxw', 'xyxx', 'xyxy', 'xyxz', 'xyy', 'xyyw', 'xyyx', 'xyyy', 'xyyz', 'xyz', 'xyzw', 'xyzx', 'xyzy', 'xyzz', 'xz', 'xzw', 'xzww', 'xzwx', 'xzwy', 'xzwz', 'xzx', 'xzxw', 'xzxx', 'xzxy', 'xzxz', 'xzy', 'xzyw', 'xzyx', 'xzyy', 'xzyz', 'xzz', 'xzzw', 'xzzx', 'xzzy', 'xzzz', 'y', 'yw', 'yww', 'ywww', 'ywwx', 'ywwy', 'ywwz', 'ywx', 'ywxw', 'ywxx', 'ywxy', 'ywxz', 'ywy', 'ywyw', 'ywyx', 'ywyy', 'ywyz', 'ywz', 'ywzw', 'ywzx', 'ywzy', 'ywzz', 'yx', 'yxw', 'yxww', 'yxwx', 'yxwy', 'yxwz', 'yxx', 'yxxw', 'yxxx', 'yxxy', 'yxxz', 'yxy', 'yxyw', 'yxyx', 'yxyy', 'yxyz', 'yxz', 'yxzw', 'yxzx', 'yxzy', 'yxzz', 'yy', 'yyw', 'yyww', 'yywx', 'yywy', 'yywz', 'yyx', 'yyxw', 'yyxx', 'yyxy', 'yyxz', 'yyy', 'yyyw', 'yyyx', 'yyyy', 'yyyz', 'yyz', 'yyzw', 'yyzx', 'yyzy', 'yyzz', 'yz', 'yzw', 'yzww', 'yzwx', 'yzwy', 'yzwz', 'yzx', 'yzxw', 'yzxx', 'yzxy', 'yzxz', 'yzy', 'yzyw', 'yzyx', 'yzyy', 'yzyz', 'yzz', 'yzzw', 'yzzx', 'yzzy', 'yzzz', 'z', 'zero', 'zw', 'zww', 'zwww', 'zwwx', 'zwwy', 'zwwz', 'zwx', 'zwxw', 'zwxx', 'zwxy', 'zwxz', 'zwy', 'zwyw', 'zwyx', 'zwyy', 'zwyz', 'zwz', 'zwzw', 'zwzx', 'zwzy', 'zwzz', 'zx', 'zxw', 'zxww', 'zxwx', 'zxwy', 'zxwz', 'zxx', 'zxxw', 'zxxx', 'zxxy', 'zxxz', 'zxy', 'zxyw', 'zxyx', 'zxyy', 'zxyz', 'zxz', 'zxzw', 'zxzx', 'zxzy', 'zxzz', 'zy', 'zyw', 'zyww', 'zywx', 'zywy', 'zywz', 'zyx', 'zyxw', 'zyxx', 'zyxy', 'zyxz', 'zyy', 'zyyw', 'zyyx', 'zyyy', 'zyyz', 'zyz', 'zyzw', 'zyzx', 'zyzy', 'zyzz', 'zz', 'zzw', 'zzww', 'zzwx', 'zzwy', 'zzwz', 'zzx', 'zzxw', 'zzxx', 'zzxy', 'zzxz', 'zzy', 'zzyw', 'zzyx', 'zzyy', 'zzyz', 'zzz', 'zzzw', 'zzzx', 'zzzy', 'zzzz']

# Orientation Matrix contents: ['Identity', 'OrthoProjection', 'Rotation', 'Scale', 'Shear', 'Translation', '__add__', '__class__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__invert__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__rsub__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', 'adjugate', 'adjugated', 'col', 'copy', 'decompose', 'determinant', 'freeze', 'identity', 'invert', 'invert_safe', 'inverted', 'inverted_safe', 'is_frozen', 'is_negative', 'is_orthogonal', 'is_orthogonal_axis_vectors', 'is_wrapped', 'lerp', 'median_scale', 'normalize', 'normalized', 'owner', 'resize_4x4', 'rotate', 'row', 'to_3x3', 'to_4x4', 'to_euler', 'to_quaternion', 'to_scale', 'to_translation', 'translation', 'transpose', 'transposed', 'zero']


class CubeModule(morse.core.robot.Robot):
    """
    Class definition for the cubemodule robot.
    """

    _name = 'Module'
    _size = (0.1, 0.1, 0.1)

    def __init__(self, obj, parent=None):
        """ Constructor method

        Receives the reference to the Blender object.
        Optionally it gets the name of the object's parent,
        but that information is not currently used for a robot.
        """

        logger.info('%s initialization' % obj.name)
        morse.core.robot.Robot.__init__(self, obj, parent)
        self.bge_object['ConnectedObjects'] = []

        # Do here robot specific initializations
        logger.info('Component initialized')

    def default_action(self):
        """ Main loop of the robot
        """

        # This is usually not used (responsibility of the actuators
        # and sensors). But you can add here robot-level actions.
        pass

    def connection_points(self, module_position, module_orientation):
        points = [(module_position + module_orientation*Vector((self._size[0], 0.0, 0.0))),
                  (module_position + module_orientation*Vector((-self._size[0], 0.0, 0.0))),
                  (module_position + module_orientation*Vector((0.0, self._size[0], 0.0))),
                  (module_position + module_orientation*Vector((0.0, -self._size[0], 0.0))),
                  (module_position + module_orientation*Vector((0.0, 0.0, self._size[0]))),
                  (module_position + module_orientation*Vector((0.0, 0.0, -self._size[0])))
                  ]
        return points

    @service
    def colour(self, colour):
        if type(colour) == list and len(colour) == 4:
            self.bge_object.color = colour
        else:
            logger.warning("colour %s is not a list of length 4" % str(colour))

    @service
    def link(self, grab, obj_name=None):
        """
        Link to another object.

        :param grab: set to True to link to an object and False to release it
        :param obj_name: (optional) when None the robot will just use the last object linked
        """
        this_object = self.bge_object
        logger.info("morse link request received from %s to %s" % (this_object.name, obj_name))
        near_object = None

        # logs errors and escapes with return if improperly called
        if obj_name:
            near_objects = [obj for obj in blenderapi.persistantstorage().robotDict.keys() if obj.name == obj_name]
            if not near_objects:
                logger.warning("no object named %s in %s" % (obj_name, str(blenderapi.persistantstorage().robotDict.keys())))
                return
            else:
                near_object = near_objects[0]

        # select last item to unlink if not specified
        elif not grab:
            if this_object['ConnectedObjects']:
                near_object = this_object['ConnectedObjects'][-1]

        # refuse to try to connect when no target given
        else:
            logger.warning("link called with no target")
            return

        if grab:
            # If the object is draggable
            # if near_object is not None and near_object != '':
            # Clear the previously selected object, if any
            logger.debug("Object to connect is %s" % near_object.name)
            this_object['ConnectedObjects'].append(near_object)
            near_object['ConnectedObjects'].append(this_object)

            # Remove Physics simulation (can cause singularities)
            # this_object.suspendDynamics()

            # Locate the nearest adjacent space to place the object
            new_orientation = near_object.worldOrientation
            logger.debug("\n near_object.worldOrientation IS %s\n this_object.worldOrientation IS %s\n new_orientation IS %s" % (str(near_object.worldOrientation), str(this_object.worldOrientation), str(new_orientation)))
            connection_points = self.connection_points(near_object.worldPosition, near_object.worldOrientation)
            logger.debug("POINTS: %s" % str(connection_points))
            new_position = connection_points[0]
            min_distance = this_object.getDistanceTo(connection_points[0])
            for point in connection_points:
                if this_object.getDistanceTo(point) < min_distance:
                    new_position = point
                    min_distance = this_object.getDistanceTo(point)
            logger.debug("\n near_object.worldPosition IS %s\n this_object.worldPosition IS %s\n new_position IS %s" % (str(near_object.worldPosition), str(this_object.worldPosition), str(new_position)))

            # Place object adjacent
            this_object.worldOrientation = new_orientation
            this_object.worldPosition = new_position
            # this_object.setLinearVelocity([0, 0, 0])
            # this_object.setAngularVelocity([0, 0, 0])

            # Parent the selected object to the target
            this_object.setParent(near_object)
            logger.debug("OBJECT %s CONNECTED TO %s" % (this_object.name, near_object.name))
        elif not grab and near_object in this_object['ConnectedObjects']:
            # Restore Physics simulation (can cause singularities)
            # this_object.restoreDynamics()
            # this_object.setLinearVelocity([0, 0, 0])
            # this_object.setAngularVelocity([0, 0, 0])

            # Remove the parent
            this_object.removeParent()

            # Clear the object from connect status
            this_object['ConnectedObjects'].remove(near_object)
            near_object['ConnectedObjects'].remove(this_object)
            logger.info("OBJECT %s DISCONNECTED FROM %s" % (near_object.name, this_object.name))

    @service
    def get_links(self):
        return self.bge_object['ConnectedObjects']
