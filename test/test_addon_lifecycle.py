import addon_utils
import rclpy


def test_registered():
    import addon_utils

    addon_names = [mod.bl_info.get("name", "") for mod in addon_utils.modules()]

    assert "omcp" in addon_names


def test_enabled():
    import bpy

    enabled_addon_names = bpy.context.preferences.addons.keys()

    assert "omcp_blender" in enabled_addon_names


def test_ensure_rclpy_shutdown_after_unregister():
    addon_utils.disable("omcp_blender")

    assert not rclpy.ok()

