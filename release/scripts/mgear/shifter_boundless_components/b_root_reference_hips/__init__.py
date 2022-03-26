"""Component Reference module"""

from mgear.shifter import component

from mgear.core import attribute, transform, primitive
from pymel.core import datatypes
import pymel.core as pm

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

        #Always aligned with world space
        t = transform.getTransformFromPos(self.guide.pos["root"])

        self.have_ctl = True
        self.root_ctl = self.addCtl(self.root,
                                    "root_ctl",
                                    t,
                                    self.color_ik,
                                    self.settings["icon"],
                                    w=self.settings["ctlSize"] * self.size * .5,
                                    h=self.settings["ctlSize"] * self.size * .5,
                                    d=self.settings["ctlSize"] * self.size,
                                    tp=self.parentCtlTag,
                                    guide_loc_ref="root")

        self.ref_ctl = self.addCtl(self.root_ctl,
                            "ref_ctl",
                            t,
                            self.color_ik,
                            self.settings["icon"],
                            w=self.settings["ctlSize"] * self.size * .25,
                            h=self.settings["ctlSize"] * self.size * .25,
                            d=self.settings["ctlSize"] * self.size,
                            tp=self.parentCtlTag,
                            guide_loc_ref="root")


        t = transform.getTransformFromPos(self.guide.pos["hips"])

        self.ik_cns = primitive.addTransform(
            self.root_ctl, self.getName("hips_ik_cns"), t)

        self.hips_ctl = self.addCtl(self.ik_cns,
                                    "hips_ctl",
                                    t,
                                    self.color_ik,
                                    self.settings["icon"],
                                    w=self.settings["ctlSize"] * self.size * .5,
                                    h=self.settings["ctlSize"] * self.size * .5,
                                    d=self.settings["ctlSize"] * self.size,
                                    tp=self.parentCtlTag,
                                    guide_loc_ref="hips")


        # we need to set the rotation order before lock any rotation axis
        if self.settings["k_ro"]:
            rotOderList = ["XYZ", "YZX", "ZXY", "XZY", "YXZ", "ZYX"]
            attribute.setRotOrder(
                self.root_ctl, rotOderList[self.settings["default_rotorder"]])

        params = [s for s in
                    ["tx", "ty", "tz", "ro", "rx",
                    "ry", "rz", "sx", "sy", "sz"]
                    if self.settings["k_" + s]]
        attribute.setKeyableAttributes(self.root_ctl, params)

        if self.settings["joint"]:
            # TODO WIP: add new attr for seeting leaf joint + not build objcts
            if self.settings["leafJoint"]:
                self.jnt_pos.append([transform.getTransformFromPos(self.guide.pos["root"])
                                    , 0
                                    , None
                                    , self.settings["uniScale"]])
            else:
                self.jnt_pos.append( [self.ref_ctl, 0, None, self.settings["uniScale"]] )
                self.jnt_pos.append( [self.hips_ctl, 1, None, self.settings["uniScale"]] )

    def addAttributes(self):
        # Ref
        if self.have_ctl:
            if self.settings["ikrefarray"]:
                ref_names = self.get_valid_alias_list(
                    self.settings["ikrefarray"].split(","))
                if len(ref_names) > 1:
                    self.ikref_att = self.addAnimEnumParam(
                        "ikref",
                        "Ik Ref",
                        0,
                        ref_names)

    def addOperators(self):
        return

    # =====================================================
    # CONNECTOR
    # =====================================================
    def setRelation(self):
        """Set the relation beetween object from guide to rig"""
        if self.have_ctl:
            self.relatives["root"] = self.root_ctl
            self.controlRelatives["root"] = self.root_ctl

            self.relatives["hips"] = self.hips_ctl
            self.controlRelatives["hips"] = self.hips_ctl

        else:
            self.relatives["root"] = self.root
            self.controlRelatives["root"] = None
            self.controlRelatives["hips"] = None


        if self.settings["joint"]:
            self.jointRelatives["root"] = 0
            self.jointRelatives["hips"] = 1

        self.aliasRelatives["root"] = "root_ctl"
        self.aliasRelatives["hips"] = "hips_ctl"


    def addConnection(self):
        """Add more connection definition to the set"""
        self.connections["standard"] = self.connect_standard
        self.connections["orientation"] = self.connect_orientation

    def connect_standard(self):
        """standard connection definition for the component"""
        self.connect_standardWithSimpleIkRef()

    def connect_orientation(self):
        """Orient connection definition for the component"""
        self.connect_orientCns()
