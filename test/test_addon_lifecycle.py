import rclpy
import pytest


@pytest.fixture
def open_mcp_blender(blender):
    blender.bootstrap()
    blender.install_addon("open-mcp-blender")
    yield blender
    blender.teardown()


def test_registered(open_mcp_blender):
    import addon_utils

    addon_names = [mod.bl_info.get("name", "") for mod in addon_utils.modules()]

    assert "open-mcp-blender" in addon_names


def test_enabled(open_mcp_blender):
    import bpy

    enabled_addon_names = bpy.context.preferences.addons.keys()

    assert "open-mcp-blender" in enabled_addon_names


def test_ensure_no_rclpy_shutdown_after_unregister(open_mcp_blender):
    import addon_utils

    addon_utils.disable("open-mcp-blender")

    assert rclpy.ok()

    addon_utils.enable("open-mcp-blender")


def test_ensure_cannot_enable_with_no_rclpy_context(open_mcp_blender):
    import addon_utils
    import bpy

    open_mcp_blender.teardown()
    addon_utils.disable("open-mcp-blender", default_set=True)

    assert not rclpy.ok()
    addon_utils.enable("open-mcp-blender", default_set=True)

    enabled_addon_names = bpy.context.preferences.addons.keys()
    assert "open-mcp-blender" not in enabled_addon_names


def test_restart_and_reload_preferences(open_mcp_blender):
    import bpy

    assert bpy.context.preferences.addons["open-mcp-blender"].preferences.domain_id == 0
    assert rclpy.utilities.get_default_context().get_domain_id() == 0

    bpy.context.preferences.addons["open-mcp-blender"].preferences.domain_id = 42
    bpy.ops.open_mcp.restart_and_reload_preferences("EXEC_DEFAULT")

    assert bpy.context.preferences.addons["open-mcp-blender"].preferences.domain_id == 42
