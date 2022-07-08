"""
"""
from calendar import c
import pymel.core as pm
import pymel.core.datatypes as dt

from mgear.shifter import component
from mgear.core import attribute, primitive

import boundless_dcclib.maya.skeleton
from boundless_dcclib.skeleton import Skeleton, Bone
from boundless_dcclib.transform import Vector, Rotation, Transform
from boundless_dcclib.serializeable import SerialEntity, SerialComponent

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

        if not self.settings["attachedSkeleton"]:
            return
            
        template_skeleton = eval(self.settings["attachedSkeleton"])
        out_skeleton = eval(self.settings["attachedSkeleton"])

        #Store rotated joints to ensure joints aren't aimed more than once
        #TODO: Should designate this in the template, instead of just taking the first entry
        rotated = []

        for row in eval(self.settings["constraintMapping"]).components:
            if not (row.info['guides'][0] and row.info['guides'][1]):
                continue

            #get the joint referenced by uuid in the constraint map from the skeleton template
            template_joints = [ template_skeleton.get_component( uuid_ ) for uuid_ in row.info['joints'] ]

            if not template_joints[0] or not template_joints[1]:
                continue
            
            #Keep a copy of the joints as they were to reference their original transforms
            out_joints = [ out_skeleton.get_component( uuid_ ) for uuid_ in row.info['joints'] ]

            #The guide as it's positioned in this scene
            scene_guide_matrix = [Transform(cmds.xform( g, q=True, m=True, ws=True )) 
                                for g in row.info['guides']]


            template_guide_forward = Vector(*row.info['guide_vector'])

            #FIXME: this bizarre for loop was a quick way to prevent an infinte
            # while loop, but should be replace witho something more sane
            for i in range(0, len(out_skeleton.components) ):
                if out_joints[1].parent != out_joints[0]:
                    out_joints.insert(1, out_skeleton.get_component(out_joints[1].parent))
                else:
                    break
            else:
                #TODO: Handle this case - the provided joints werent correctly related
                continue

            #Coeffcient is uniform scale for translation
            #FIXME: Should this just be called "Translation Scale?"
            coefficient =  template_guide_forward.magnitude / scene_guide_matrix[0].translation.distance(scene_guide_matrix[1].translation)
            for ref in out_joints[1:]:
                ref.coefficient = coefficient


            if template_joints[0] in rotated:
                continue
            rotated.append(template_joints[0])
            
            scene_guide_forward = (scene_guide_matrix[1].translation - scene_guide_matrix[0].translation)


            #the constraint mapping
            template_guide_rotation = Rotation.from_vector(template_guide_forward)


            scene_guide_rotation = Rotation.from_vector(scene_guide_forward)

            #calc and apply
            delta_transform = template_joints[0].world * (template_guide_rotation.inverse * scene_guide_rotation)
            out_joints[0].rotation =  delta_transform.to_local(out_joints[0].parent).rotation


        boundless_dcclib.maya.skeleton.to_joint_hierarchy(out_skeleton)


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
