"""
"""
import imp
import math

import pymel.core as pm
import pymel.core.datatypes as dt

from mgear.shifter import component
from mgear.core import attribute, primitive

import boundless_dcclib.maya.skeleton
from  boundless_dcclib.skeleton import Skeleton, Bone
import boundless_dcclib.serializeable
from boundless_dcclib.serializeable import SerializeableEntity, SerializeableComponent

from maya import cmds


#############################################
# COMPONENT
#############################################


class Component(component.Main):
    """Shifter component Class"""

    # =====================================================
    # OBJECTS
    # =====================================================
    def addObjects(self):
        """Add all the objects needed to create the component."""

        if self.settings["attachedSkeleton"]:
            skeleton = eval(self.settings["attachedSkeleton"])

            constraint_map = eval(self.settings["constraintMapping"])
       
            for row in constraint_map.components:
                guide = boundless_dcclib.maya.skeleton.from_node( row.info['guides'].name )
                guide.add_components( boundless_dcclib.maya.skeleton.from_node( row.info['guides'].child_bones[0].name ))
                
                joint_ref = skeleton.find_components( name=row.info['joints'].child_bones[0].name )
                #TODO: find every joint in between first and last, and apply the coefficient
                coefficient = row.info['guides'].length / guide.length 

                joint_ref[0].coefficient = coefficient


            boundless_dcclib.maya.skeleton.to_joint_hierarchy(skeleton)


    def finalize(self):
        """
        This runs after all the connections are made and the
        hierarchy is built.
        """
        # Run default finalize logic.
        super(Component, self).finalize()

    # =====================================================
    # CONNECTOR
    # =====================================================
    def setRelation(self):
        """Set the relation beetween object from guide to rig"""


    def addConnection(self):
        """Add more connection definition to the set"""
