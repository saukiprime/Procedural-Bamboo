import bpy
import bmesh
from bpy.types import Operator
import math
import random


class Bamboo:
    def __init__(self, segments, resolution, stalk_radius, ridge_size, waist_size, height, tilt):
        self.segments = segments
        self.resolution = resolution
        self.stalk_radius = stalk_radius
        self.ridge_size = ridge_size
        self.ridge_height = 1.0 / 8.0
        self.waist_size = waist_size
        self.height = height
        self.tilt = tilt

    def genMeshData(self):
        verts = []
        faces = []

        angle = 360 / self.resolution
        vert_seg = 11

        for z in range(0, self.segments):
            low_height = z * self.height - z * self.height * (
                        self.ridge_height / 2 + random.uniform(-self.ridge_height / 20, self.ridge_height / 20))
            waist = self.waist_size * random.uniform(0.98, 1.02)
            ridge = self.ridge_size * random.uniform(0.98, 1.02)
            radius = self.stalk_radius * random.uniform(0.98, 1.02)

            # Vertices
            for indexV in range(0, self.resolution):
                x, y = radius * math.cos(math.radians(angle * indexV)), radius * math.sin(math.radians(angle * indexV))
                verts.append((x, y, low_height))
                verts.append((x, y, low_height + self.height * self.ridge_height / 4))
                verts.append((x * waist, y * waist, low_height + self.height * self.ridge_height))
                verts.append((x * waist ** 2, y * waist ** 2, low_height + self.height * self.ridge_height * 2))
                verts.append((x * waist ** 2, y * waist ** 2, low_height + self.height * self.ridge_height * 3))
                verts.append((x * waist, y * waist, low_height + self.height * self.ridge_height * 4))
                verts.append((x, y, low_height + self.height * self.ridge_height * 7))
                verts.append((x, y, low_height + self.height * self.ridge_height * 7.55))
                verts.append((x * ridge, y * ridge, low_height + self.height * self.ridge_height * 7.70))
                verts.append((x * ridge, y * ridge, low_height + self.height * self.ridge_height * 7.85))
                verts.append((x, y, low_height + self.height * self.ridge_height * 8))

            # Faces
            for indexF in range(0, self.resolution - 1):
                for h in range(0, vert_seg - 1):
                    a = indexF * vert_seg + h + (z * vert_seg * self.resolution)
                    b = (indexF + 1) * vert_seg + h + (z * vert_seg * self.resolution)
                    c = (indexF + 1) * vert_seg + h + 1 + (z * vert_seg * self.resolution)
                    d = indexF * vert_seg + h + 1 + (z * vert_seg * self.resolution)
                    face = (a, b, c, d)
                    faces.append(face)
            for h in range(0, vert_seg - 1):
                a = (self.resolution - 1) * vert_seg + h + (z * vert_seg * self.resolution)
                b = h + (z * vert_seg * self.resolution)
                c = h + 1 + (z * vert_seg * self.resolution)
                d = (self.resolution - 1) * vert_seg + h + 1 + (z * vert_seg * self.resolution)
                face = (a, b, c, d)
                faces.append(face)

        # Tilt
        tilt = []
        for h in range(0, self.segments):
            tilt.append(self.tilt * random.uniform(0.99, 1.01))
        for i, vert in enumerate(verts):
            x, y, z = vert
            seg = i // (vert_seg * self.resolution)
            x = x * math.cos(math.radians(tilt[seg])) - z * math.sin(math.radians(tilt[seg]))
            z = x * math.sin(math.radians(tilt[seg])) + z * math.cos(math.radians(tilt[seg]))
            verts[i] = (x, y, z)

        self.verts = verts
        self.faces = faces


class BambooGenerator(Operator):
    bl_idname = "object.bamboo"
    bl_label = "Mesh"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Retrieve parameters from the scene
        segments = context.scene.bamboo_segments
        resolution = context.scene.bamboo_resolution
        stalk_radius = context.scene.bamboo_stalk_radius
        ridge_size = context.scene.bamboo_ridge_size
        waist_size = context.scene.bamboo_waist_size
        height = context.scene.bamboo_height
        tilt = context.scene.bamboo_tilt

        mesh_data = bpy.data.meshes.new("bamboo_mesh_data")

        # Create bamboo object
        bamboo = Bamboo(segments, resolution, stalk_radius, ridge_size, waist_size, height, tilt)
        bamboo.genMeshData()
        mesh_data.from_pydata(bamboo.verts, [], bamboo.faces)
        mesh_data.update()

        # Subdivide
        bm = bmesh.new()
        bm.from_mesh(mesh_data)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, smooth=1, cuts=1, use_grid_fill=True, )
        bm.to_mesh(mesh_data)
        mesh_data.update()

        mesh_obj = bpy.data.objects.new("Bamboo", mesh_data)

        collection = bpy.context.collection
        collection.objects.link(mesh_obj)

        bpy.context.view_layer.objects.active = mesh_obj
        mesh_obj.select_set(True)

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
    bpy.types.Scene.bamboo_segments = bpy.props.IntProperty(name="Segments", default=5, min=1, max=50)
    bpy.types.Scene.bamboo_resolution = bpy.props.IntProperty(name="Resolution", default=32, min=16, max=64)
    bpy.types.Scene.bamboo_stalk_radius = bpy.props.FloatProperty(name="Stalk Radius", default=1, min=0.2, max=4.0)
    bpy.types.Scene.bamboo_ridge_size = bpy.props.FloatProperty(name="Ridge Size", default=1.03, min=1.01, max=1.1)
    bpy.types.Scene.bamboo_waist_size = bpy.props.FloatProperty(name="Waist Size", default=0.95, min=0.8, max=0.99)
    bpy.types.Scene.bamboo_height = bpy.props.FloatProperty(name="Height", default=5.0, min=1, max=10.0)
    bpy.types.Scene.bamboo_tilt = bpy.props.FloatProperty(name="Tilt", default=1.0, min=0.0, max=3.0)


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
