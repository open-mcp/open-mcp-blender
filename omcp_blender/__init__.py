import sys

bl_info = {
    "name": "open-mcp-blender",
    "description": "open-mcp open source motion control photography",
    "author": "Emanuel Buholzer",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf > open-mcp",
    "doc_url": "https://https://github.com/open-mcp/open-mcp-blender",
    "tracker_url": "https://github.com/open-mcp/open-mcp-blender/issues",
    "support": "COMMUNITY",
    "category": "Motion Control",
}

# Support reloading non-bpy dependent modules
if "rclpy" in locals():
    import importlib

    rclpy = importlib.reload(rclpy)  # noqa: F821
    rclpy.logging = importlib.reload(rclpy.logging)
else:
    import rclpy
    import rclpy.logging

logger = rclpy.logging.get_logger(__name__)


def register():
    # Support reloading for bpy dependent modules
    if "open-mcp-blender.preferences" in sys.modules:
        import importlib

        def reload_module(name):
            module_name = "%s.%s" % (__name__, name)
            module = importlib.reload(sys.modules[module_name])
            sys.modules[module_name] = module
            return module

        preferences = reload_module("preferences")
    else:
        from . import preferences

    assert rclpy.ok()

    preferences.register()


def unregister():
    from . import preferences

    preferences.unregister()
