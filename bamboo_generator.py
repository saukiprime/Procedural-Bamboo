import bpy
import bmesh
from bpy.types import Operator
import math
import random
from mathutils import Vector, Matrix

import numpy as np



class BambooGenerator(Operator):
    bl_idname = "object.bamboo"
    bl_label = "Mesh"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # TODO: generate Bamboo

        return {"FINISHED"}


class BambooGeneratorPanel(bpy.types.Panel):
    bl_label = "Panel"
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_category = "Bamboo Generator"

    # TODO: allow custom bamboo parameters

    def draw(self, context):
        layout = self.layout
        layout.operator("object.geosphere", text="Add Geosphere", icon='MESH_ICOSPHERE')
        layout.operator("object.bamboo", text="Add Bamboos", icon='MESH_ICOSPHERE')


classes = [BambooGenerator, BambooGeneratorPanel]

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()