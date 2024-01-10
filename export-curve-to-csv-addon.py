import bpy, bmesh
import csv

from bpy.types import Operator
from datetime import datetime
from os import path


bl_info = {
  "name": "Export Curve to CSV",
  "author": "Lance Carriere <lance@visiondriven.com",
  "version": (1, 3),
  "blender": (2, 93, 5),
  "description": "Export the selected curve verticies to CSV file",
  "category": "Object",
}

def write_some_data(context):

    thisFile = bpy.data.filepath
    now = datetime.today().strftime('-%Y%m%d-%H%M%S') # -20211009-141333
    path_output_csv = path.splitext(thisFile)[0] + now + '.csv'

    print(f'<-- STARTING OUTPUT TO {path.basename(path_output_csv)} -->')

    # get current selected object
    if len(context.selected_objects) != 1:
        print(f'{path.basename(__file__)} :: select 1 and only 1 mesh')
        ShowMessageBox(f'{path.basename(__file__)} :: select 1 and only 1 mesh')

        return False

    obj = context.active_object

    # got vertices?
    if obj.type != 'MESH':
        print(f'{path.basename(__file__)} :: selected object does not have vertices')
        ShowMessageBox(f'{path.basename(__file__)} :: selected object does not have vertices')
        return False


    ###--- Ian's magic below

    # Get the Object via the blender API
    if obj.mode == 'EDIT':
        # this works only in edit mode,
        bm = bmesh.from_edit_mesh(obj.data)
        verts = [vert.co for vert in bm.verts]

    else:
        # this works only in object mode,
        verts = [vert.co for vert in obj.data.vertices]

    # coordinates as tuples
    plain_verts = [vert.to_tuple() for vert in verts]

    ###--- Ian's kung-fu above


    # output to CSV
    with open(path_output_csv, "w") as csvfile:

        vertWriter = csv.writer(csvfile, dialect='excel', lineterminator='\n')

        vertWriter.writerows(plain_verts) # squirt out all at once - yay



    print(f'\nCSV successfully created:\n{path_output_csv}')



    return path_output_csv


def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


class ExportCurveToCSV(Operator):
    """Export the selected curve verticies to CSV file"""
    bl_idname = "export.curve_to_csv"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Curve to CSV"

    def execute(self, context):
        # return write_some_data(context)
        result = write_some_data(context)
        if result != False:
            self.report({'INFO'}, f'Vertices save to {result}!')
            ShowMessageBox(result, 'Vertices saved to:')
            return {'FINISHED'}
        else:
            return {'CANCELLED'}



# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportCurveToCSV.bl_idname, text="Curve vertices to CSV Export")


def register():
    bpy.utils.register_class(ExportCurveToCSV)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportCurveToCSV)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    # bpy.ops.export.curve_to_csv('INVOKE_DEFAULT')
