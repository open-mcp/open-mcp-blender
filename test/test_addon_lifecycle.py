import rclpy
import pytest


@pytest.fixture
def open-mcp-blender(blender):
    blender.bootstrap()
    blender.install_addon("open-mcp-blender")
    yield blender
    blender.teardown()


def test_registered(open-mcp-blender):
    import addon_utils

    addon_names = [mod.bl_info.get("name", "") for mod in addon_utils.modules()]

    assert "open-mcp-blender" in addon_names


def test_enabled(open-mcp-blender):
    import bpy

    enabled_addon_names = bpy.context.preferences.addons.keys()

    assert "open-mcp-blender" in enabled_addon_names


def test_ensure_no_rclpy_shutdown_after_unregister(open-mcp-blender):
    import addon_utils

    addon_utils.disable("open-mcp-blender")

    assert rclpy.ok()

    addon_utils.enable("open-mcp-blender")


def test_ensure_cannot_enable_with_no_rclpy_context(open-mcp-blender):
    import addon_utils
    import bpy

    open-mcp-blender.teardown()
    addon_utils.disable("open-mcp-blender", default_set=True)

    assert not rclpy.ok()
    addon_utils.enable("open-mcp-blender", default_set=True)

    enabled_addon_names = bpy.context.preferences.addons.keys()
    assert "open-mcp-blender" not in enabled_addon_names


def test_restart_and_reload_preferences(open-mcp-blender):
    import bpy

    assert bpy.context.preferences.addons["open-mcp-blender"].preferences.domain_id == 0
    assert rclpy.utilities.get_default_context().get_domain_id() == 0

    bpy.context.preferences.addons["open-mcp-blender"].preferences.domain_id = 42
    bpy.ops.open-mcp.restart_and_reload_preferences("EXEC_DEFAULT")

    assert bpy.context.preferences.addons["open-mcp-blender"].preferences.domain_id == 42
