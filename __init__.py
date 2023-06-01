bl_info = {
    "name": "omcp",
    "description": "omcp open source motion control photography",
    "author": "Emanuel Buholzer",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf > omcp",
    "doc_url": "https://https://github.com/emanuelbuholzer/omcp-blender",
    "tracker_url": "https://github.com/emanuelbuholzer/omcp-blender/issues",
    "support": "COMMUNITY",
    "category": "Motion Control",
}

import sys

if "bpy" in sys.modules:
    import bpy

    import rclpy

    from .panel import OmcpPanel
    from .transfer import TransferOperator
    from .subscribe import SubscribeOperator

    def register():
        rclpy.init()
        bpy.utils.register_class(TransferOperator)
        bpy.utils.register_class(SubscribeOperator)
        bpy.utils.register_class(OmcpPanel)

    def unregister():
        bpy.utils.unregister_class(OmcpPanel)
        bpy.utils.unregister_class(SubscribeOperator)
        bpy.utils.unregister_class(TransferOperator)
        rclpy.shutdown()



