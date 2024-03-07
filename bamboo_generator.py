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

        # Placeholder mesh of a cube
        vertices = [(1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1),
                    (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1)]

        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
                 (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]
        mesh_data = bpy.data.meshes.new("bamboo_mesh_data")
        mesh_obj = bpy.data.objects.new("Bamboo", mesh_data)

        collection = bpy.context.collection
        collection.objects.link(mesh_obj)

        bpy.context.view_layer.objects.active = mesh_obj
        mesh_obj.select_set(True)

        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update()

        return {"FINISHED"}


class BambooGeneratorPanel(bpy.types.Panel):
    bl_label = "Bamboo Generator"
    bl_idname = "OBJECT_PT_bamboo_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bamboo Generator'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        # UI elements for custom bamboo parameters
        layout.prop(context.scene, 'bamboo_segments', text="Number of Segments")
        layout.prop(context.scene, 'bamboo_resolution', text="Resolution")
        layout.prop(context.scene, 'bamboo_stalk_radius', text="Stalk Radius")
        layout.prop(context.scene, 'bamboo_ridge_size', text="Ridge Size")
        layout.prop(context.scene, 'bamboo_waist_size', text="Waist Size")
        layout.prop(context.scene, 'bamboo_height', text="Height")
        layout.prop(context.scene, 'bamboo_tilt', text="Tilt")

        # Existing buttons for adding objects
        layout.operator("object.bamboo", text="Add Bamboo", icon='OUTLINER_OB_FORCE_FIELD')


# Register properties
def register_properties():
    bpy.types.Scene.bamboo_segments = bpy.props.IntProperty(name="Segments", default=5, min=1, max=100)
    bpy.types.Scene.bamboo_resolution = bpy.props.IntProperty(name="Resolution", default=12, min=1, max=64)
    bpy.types.Scene.bamboo_stalk_radius = bpy.props.FloatProperty(name="Stalk Radius", default=1.0, min=0.1, max=10.0)
    bpy.types.Scene.bamboo_ridge_size = bpy.props.FloatProperty(name="Ridge Size", default=0.1, min=0.01, max=1.0)
    bpy.types.Scene.bamboo_waist_size = bpy.props.FloatProperty(name="Waist Size", default=0.5, min=0.1, max=2.0)
    bpy.types.Scene.bamboo_height = bpy.props.FloatProperty(name="Height", default=5.0, min=1.0, max=20.0)
    bpy.types.Scene.bamboo_tilt = bpy.props.FloatProperty(name="Tilt", default=0.0, min=-45.0, max=45.0)


classes = [BambooGenerator, BambooGeneratorPanel]


# Register and unregister classes and properties
def register():
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    register_properties()


def unregister():
    bpy.utils.unregister_class(BambooGeneratorPanel)
    del bpy.types.Scene.bamboo_segments
    del bpy.types.Scene.bamboo_resolution
    del bpy.types.Scene.bamboo_stalk_radius
    del bpy.types.Scene.bamboo_ridge_size
    del bpy.types.Scene.bamboo_waist_size
    del bpy.types.Scene.bamboo_height
    del bpy.types.Scene.bamboo_tilt


if __name__ == "__main__":
    register()
