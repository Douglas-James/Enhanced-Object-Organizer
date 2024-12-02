bl_info = {
    "name": "Enhanced Object Organizer with Visual Color and Save Option",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0, 2),
    "description": "Rename an object, move it to a collection, modify the collection's color, and optionally save the project.",
}

import bpy

# Mapping color names to Blender's color tag system
COLOR_TAG_MAPPING = {
    'NONE': 'NONE',
    'RED': 'COLOR_01',
    'ORANGE': 'COLOR_02',
    'YELLOW': 'COLOR_03',
    'GREEN': 'COLOR_04',
    'BLUE': 'COLOR_05',
    'PURPLE': 'COLOR_06',
    'PINK': 'COLOR_07',
    'BROWN': 'COLOR_08',
    'GREY': 'COLOR_08',  # Grey shares the same tag as Brown
    'WHITE': 'COLOR_08', # White also shares the same tag
}

class OBJECT_OT_EnhancedOrganizer(bpy.types.Operator):
    """Rename object, move to collection, modify collection color, and optionally save project"""
    bl_idname = "object.enhanced_organizer"
    bl_label = "Enhanced Organizer with Save Option"
    bl_options = {'REGISTER', 'UNDO'}

    object_name: bpy.props.StringProperty(name="New Object Name")
    collection_name: bpy.props.StringProperty(name="New Collection Name")
    collection_color: bpy.props.EnumProperty(
        name="Collection Color",
        description="Choose the collection color",
        items=[
            ('NONE', "None", "No color tag"),
            ('RED', "Red", "Color red"),
            ('ORANGE', "Orange", "Color orange"),
            ('YELLOW', "Yellow", "Color yellow"),
            ('GREEN', "Green", "Color green"),
            ('BLUE', "Blue", "Color blue"),
            ('PURPLE', "Purple", "Color purple"),
            ('PINK', "Pink", "Color pink"),
            ('BROWN', "Brown", "Color brown"),
            ('GREY', "Grey", "Color grey"),
            ('WHITE', "White", "Color white"),
        ],
        default='NONE'
    )
    save_project: bpy.props.BoolProperty(
        name="Save Project",
        description="Save the Blender project after organizing",
        default=False
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object selected!")
            return {'CANCELLED'}

        # Ensure valid collection name
        if not self.collection_name.strip():
            self.report({'ERROR'}, "Collection name cannot be empty!")
            return {'CANCELLED'}

        # Check if the collection exists, if not create it
        new_collection = bpy.data.collections.get(self.collection_name)
        if not new_collection:
            new_collection = bpy.data.collections.new(self.collection_name)
            context.scene.collection.children.link(new_collection)

        # Rename the object
        obj.name = self.object_name

        # Move the object to the new collection
        for col in obj.users_collection:
            col.objects.unlink(obj)
        new_collection.objects.link(obj)

        # Set the collection's color using the correct color tag
        collection_color_tag = COLOR_TAG_MAPPING.get(self.collection_color, 'NONE')
        new_collection.color_tag = collection_color_tag

        # Save the project if the option is selected
        if self.save_project:
            bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

        self.report({'INFO'}, f"Object renamed, moved to collection '{self.collection_name}', and color updated.")
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
