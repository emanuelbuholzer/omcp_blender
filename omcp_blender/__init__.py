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

# Support reloading non-bpy dependent modules
if 'rclpy' in locals():
    import importlib

    rclpy = importlib.reload(rclpy)
else:
    import rclpy


def register():
    # Support reloading for bpy dependent modules
    if "omcp_blender.preferences" in sys.modules:
        import importlib

        def reload_module(name):
            print("CHIIIIII")
            module_name = "%s.%s" % (__name__, name)
            module = importlib.reload(sys.modules[module_name])
            sys.modules[module_name] = module
            return module

        preferences = reload_module("preferences")
    else:
        from . import preferences

    preferences.register()


def unregister():
    from . import preferences

    #preferences.unregister()

    rclpy.try_shutdown()