import logging; logger = logging.getLogger("morserobots." + __name__)
import os
from morse.builder import AbstractComponent, Robot, MORSE_COMPONENTS

class Human(Robot):
    """ Append a human model to the scene.

    The human model currently available in MORSE comes with its
    own subjective camera and several features for object manipulation.

    It also exposes a :doc:`human posture component <morse/user/sensors/human_posture>`
    that can be accessed by the ``armature`` member.

    Usage example:

    .. code-block:: python

       #! /usr/bin/env morseexec

       from morse.builder import *

       human = Human()
       human.translate(x=5.5, y=-3.2, z=0.0)
       human.rotate(z=-3.0)

       human.armature.configure_mw('pocolibs',
                        ['Pocolibs',
                         'export_posture',
                         'morse/middleware/pocolibs/sensors/human_posture',
                         'human_posture'])

    Currently, only one human per simulation is supported.
    """
    def __init__(self, filename='human'):
        """ The 'style' parameter is only to switch to the mocap_human file.

        :param filename: 'human' (default) or 'mocap_human'
        """
        Robot.__init__(self, filename)

        self.armature = None

        try:
            armature_object = self.get_selected("HumanArmature")
            self.armature = AbstractComponent(armature_object, "human_posture")
            # self.append(self.armature) # force parent ?
        except KeyError:
            logger.error("Could not find the human armature! (I was looking " +\
                         "for an object called 'HumanArmature' in the 'Human'" +\
                         " children). I won't be able to export the human pose" +\
                         " to any middleware.")

        # fix for Blender 2.6 Animations
        if armature_object:
            hips = self.get_selected("Hips_Empty")
            # IK human has no object called Hips_Empty, so avoid this step
            if hips:
                for i, actuator in enumerate(hips.game.actuators):
                    actuator.layer = i
                for i, actuator in enumerate(armature_object.game.actuators):
                    actuator.layer = i

    def use_world_camera(self):
        self.properties(WorldCamera = True)

    def disable_keyboard_control(self):
        self.properties(disable_keyboard_control = True)