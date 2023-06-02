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
    import addon_utils

    addon_utils.disable("omcp_blender")

    assert not rclpy.ok()

    addon_utils.enable("omcp_blender")


def test_restart_and_reload_preferences():
    import bpy

    assert bpy.context.preferences.addons["omcp_blender"].preferences.domain_id == 0
    assert rclpy.utilities.get_default_context().get_domain_id() == 0

    bpy.context.preferences.addons["omcp_blender"].preferences.domain_id = 42
    bpy.ops.omcp.reload_addon("EXEC_DEFAULT")

    assert bpy.context.preferences.addons["omcp_blender"].preferences.domain_id == 42
    assert rclpy.utilities.get_default_context().get_domain_id() == 42
