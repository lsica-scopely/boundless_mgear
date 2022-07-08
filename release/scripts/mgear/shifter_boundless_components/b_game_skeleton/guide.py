"""Boundless Game Skeleton module"""
import mgear
import pymel.core as pm
from maya import cmds

from mgear.shifter.component import guide
from mgear.core import transform, pyqt, attribute
from mgear.vendor.Qt import QtWidgets, QtCore

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

from . import settingsUI as sui

import boundless_dcclib.maya.util
import boundless_dcclib.maya.skeleton

from boundless_dcclib.transform import Vector, Rotation, Transform
from boundless_dcclib.serializeable import SerialEntity, SerialComponent
from boundless_dcclib.skeleton import Skeleton, Bone


# guide info
AUTHOR = "Louis J. Sica"
URL = ""
EMAIL = "louis.sica@scopely.com"
VERSION = [0, 1, 0]
TYPE = "b_game_skeleton"
NAME = "GameSkeleton"
DESCRIPTION = ""

##########################################################
# CLASS
##########################################################


class Guide(guide.ComponentGuide):
    """Component Guide Class"""

    compType = TYPE
    compName = NAME
    description = DESCRIPTION

    author = AUTHOR
    url = URL
    email = EMAIL
    version = VERSION

    # =====================================================
    # Add more parameter to the parameter definition list.
    # @param self
    def addParameters(self):

        self.pAttachedSkeleton = self.addParam("attachedSkeleton","string", None )
        self.pConstraintMapping = self.addParam("constraintMapping","string", None )

        # These are used by Shifter by default. Do not remove
        self.pUseIndex = self.addParam("useIndex", "bool", False)
        self.pParentJointIndex = self.addParam(
            "parentJointIndex", "long", -1, None, None)

    # def postDraw(self):
    #     "Add post guide draw elements to the guide"


##########################################################
# Setting Page
##########################################################


class settingsTab(QtWidgets.QDialog, sui.Ui_Form):
    """The Component settings UI"""

    def __init__(self, parent=None):
        super(settingsTab, self).__init__(parent)
        self.setupUi(self)


class componentSettings(MayaQWidgetDockableMixin, guide.componentMainSettings):
    """Create the component setting window"""

    def __init__(self, parent=None):
        self.toolName = TYPE
        # Delete old instances of the component settings window.
        pyqt.deleteInstances(self, MayaQDockWidget)

        super(self.__class__, self).__init__(parent=parent)
        self.settingsTab = settingsTab()

        self.setup_componentSettingWindow()
        self.create_componentControls()
        self.populate_componentControls()
        self.create_componentLayout()
        self.create_componentConnections()

    def setup_componentSettingWindow(self):
        self.mayaMainWindow = pyqt.maya_main_window()

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(TYPE)
        self.resize(280, 520)

        self.map_table = self.settingsTab.skeleton_map_table

    def create_componentControls(self):
        return

    def populate_componentControls(self):
        """Populate Controls

        Populate the controls values from the custom attributes of the
        component.

        """
        # populate tab
        self.tabs.insertTab(1, self.settingsTab, "Component Settings")

        # populate component settings
        self.loadSkeleton()
        self.loadMapData()

    def create_componentLayout(self):
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.tabs)
        self.settings_layout.addWidget(self.close_button)

        self.setLayout(self.settings_layout)

    def create_componentConnections(self):
        self.settingsTab.skeleton_button.clicked.connect(
            self.setSkeleton
        )

        self.settingsTab.add_row_button.clicked.connect(
             self.addRow 
        )

        self.settingsTab.rem_row_button.clicked.connect(
            self.removeRow
        )

        self.settingsTab.copy_selection_button.clicked.connect(
            self.copySelection
        )

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)

    ### 
    ### Begin Settings Page Callbacks
    ### 

    def setSkeleton( self ):
        """Select the skeleton to use as template data from the scene
        """
        self.settingsTab.skeleton_label.setText("")
    
        root_joint = boundless_dcclib.maya.util.get_selected_root()
        if not root_joint:
            pm.displayWarning( "Nothing Selected" )
            return

        #create a Skeleton object from selected joint hierarchy root, if
        # None is returned this failed because selected object wasn't a joint
        skeleton = boundless_dcclib.maya.skeleton.from_root_joint( root_joint )
        
        if not skeleton:
            pm.displayWarning( "Must select a joint to set attached skeleton" )
            return

        self.settingsTab.skeleton_label.setText(root_joint)
        self.root.attr("attachedSkeleton").set( skeleton.dumps( ) )

    def loadSkeleton( self ):
        """Load template data from the component parameters stored on the guide
        root.
        """
        skeleton_template = self.root.attr("attachedSkeleton").get()
        if not skeleton_template: return

        skeleton_template = eval(skeleton_template)
        if skeleton_template.bones:
            self.settingsTab.skeleton_label.setText(skeleton_template.name)


    def addRow( self ):
        index = self.map_table.currentRow()

        #True if no row is selected
        if index < 0:
            index = self.map_table.rowCount()
        else:
            index += 1

        self.map_table.insertRow( index ) 

        self.saveMapData()

        return index

    def removeRow( self ):
        index = self.map_table.currentRow()

        #True if no row is selected
        if index < 0:
            index = self.map_table.rowCount() - 1

        self.map_table.removeRow( index )

        self.saveMapData()

        return index

    def copySelection( self ):
        """Copys the selected joint or guide's name into the selected map table
        cell. Copies into the first cell of a new row if there is no cell selected
        """
        row = self.map_table.currentRow()
        
        if row < 0:
            row = self.addRow()
        
        col = self.map_table.currentColumn()
        col = max( col, 0 )
        
        selected = boundless_dcclib.maya.util.get_selected()
        if selected \
            and ( ( col < 2 and pm.nodeType( selected ) == 'joint' )
                or (col > 1 and pm.attributeQuery( 'isGearGuide', node = selected, exists=True )) ):
        
            self.map_table.setItem(row, col, QtWidgets.QTableWidgetItem(selected, 0))
            self.saveMapData()

    def saveMapData( self ):
        """Saves the map table as serializeable representation of the joints / guides
        they reference. Saves to the constraintMapping attribute on the guide root
        """
        skeleton_template = self.root.attr("attachedSkeleton").get()
        if not skeleton_template:
            pm.warning("Please select an attached skeleton, map data will NOT save without a skeleton set")
            return

        skeleton_template = eval( skeleton_template )

        constraint_map = SerialEntity()

        for i in range(0, self.map_table.rowCount()):
            row_data = { 'joints':[None]*2
                        , 'guides':[None]*2
                        , 'guide_vector': None }
            for j in range(0, self.map_table.columnCount()):
                
                item = self.map_table.item(i,j)
                if item:
                    if j < 2:
                        components = skeleton_template.find_components(name=item.data(0)) 
                        if components:
                            row_data['joints'][j] = components[0]
                        else:
                            #TODO: Handle this
                            print (f"Couldnt find {item.data(0)}")
                    else:
                        row_data['guides'][j-2] = cmds.ls(item.data(0), long=True)[0]

            if (row_data['guides'][0] and row_data['guides'][1]):
                guide_matrix = [Transform(pm.xform( g, q=True, m=True, ws=True )) 
                                    for g in row_data['guides']]

            row_data['guide_vector'] = guide_matrix[1].translation - guide_matrix[0].translation

            constraint_map.add_components( SerialComponent(**row_data) )

        self.root.attr("constraintMapping").set( constraint_map.dumps( ) )

    def loadMapData( self ):
        """Loads serialized map data back into the ui map table
        """
        constraint_map = self.root.attr("constraintMapping").get()
        skeleton_template = self.root.attr("attachedSkeleton").get()
        
        if not skeleton_template or not constraint_map:
            return

        constraint_map = eval( constraint_map )
        skeleton_template = eval(skeleton_template)
        

        for i, row in enumerate( constraint_map.components ):
            self.map_table.insertRow(i)
            for j, uuid_ in enumerate(row['joints']):
                child = skeleton_template.get_component(uuid_)

                if not child:
                    print (f"Couldn't find component {uuid_}")
                    continue

                self.map_table.setItem(i, j, QtWidgets.QTableWidgetItem( child.name, 0 ))
            
            for j, name in enumerate(row['guides']):
                self.map_table.setItem(i, j+2, QtWidgets.QTableWidgetItem( cmds.ls(name)[0], 0 ))

