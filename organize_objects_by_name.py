bl_info = {
    "name": "Enhanced Object Organizer with Visual Color",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0, 1),
    "description": "Rename an object, move it to a new collection with a visible color, and ask to save the project.",
}

import bpy
import random

class OBJECT_OT_EnhancedOrganizer(bpy.types.Operator):
    """Rename object, move to collection, and save project"""
    bl_idname = "object.enhanced_organizer"
    bl_label = "Enhanced Organizer with Visual Color"
    bl_options = {'REGISTER', 'UNDO'}

    object_name: bpy.props.StringProperty(name="New Object Name")
    collection_name: bpy.props.StringProperty(name="New Collection Name")
    collection_color: bpy.props.FloatVectorProperty(
        name="Collection Color",
        description="Color displayed for the collection",
        subtype='COLOR',
        size=4,
        default=(0.5, 0.5, 0.5, 1.0),
        min=0.0, max=1.0
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object selected!")
            return {'CANCELLED'}

        # Rename the object
        obj.name = self.object_name

        # Create or get the new collection
        if self.collection_name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(name=self.collection_name)
            context.scene.collection.children.link(new_collection)
        else:
            new_collection = bpy.data.collections[self.collection_name]

        # Move the object to the new collection
        for col in obj.users_collection:
            col.objects.unlink(obj)
        new_collection.objects.link(obj)

        # Create a dummy object to display the color
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        color_sphere = context.active_object
        color_sphere.name = f"{self.collection_name}_Color"
        new_collection.objects.link(color_sphere)

        # Unlink dummy object from the scene's main collection
        context.scene.collection.objects.unlink(color_sphere)

        # Assign a material with the chosen color
        mat = bpy.data.materials.new(name=f"{self.collection_name}_Material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled = nodes.get("Principled BSDF")
        if principled:
            principled.inputs["Base Color"].default_value = self.collection_color
        color_sphere.data.materials.append(mat)

        # Prompt to save the file
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        self.report({'INFO'}, "Object renamed, moved to collection, and color displayed.")
        return {'FINISHED'}

# Add to the M key map
def add_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(OBJECT_OT_EnhancedOrganizer.bl_idname, 'M', 'PRESS')

def remove_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.get('Object Mode')
        if km:
            for kmi in km.keymap_items:
                if kmi.idname == OBJECT_OT_EnhancedOrganizer.bl_idname:
                    km.keymap_items.remove(kmi)

def register():
    bpy.utils.register_class(OBJECT_OT_EnhancedOrganizer)
    add_shortcut()

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_EnhancedOrganizer)
    remove_shortcut()

if __name__ == "__main__":
    register()
