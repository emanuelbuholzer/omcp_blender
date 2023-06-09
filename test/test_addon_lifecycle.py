import rclpy
import pytest


@pytest.fixture
def omcp_blender(blender):
    blender.bootstrap()
    blender.install_addon("omcp_blender")
    yield blender
    blender.teardown()


def test_registered(omcp_blender):
    import addon_utils

    addon_names = [mod.bl_info.get("name", "") for mod in addon_utils.modules()]

    assert "omcp_blender" in addon_names


def test_enabled(omcp_blender):
    import bpy

    enabled_addon_names = bpy.context.preferences.addons.keys()

    assert "omcp_blender" in enabled_addon_names


def test_ensure_no_rclpy_shutdown_after_unregister(omcp_blender):
    import addon_utils

    addon_utils.disable("omcp_blender")

    assert rclpy.ok()

    addon_utils.enable("omcp_blender")


def test_ensure_cannot_enable_with_no_rclpy_context(omcp_blender):
    import addon_utils
    import bpy

    omcp_blender.teardown()
    addon_utils.disable("omcp_blender", default_set=True)

    assert not rclpy.ok()
    addon_utils.enable("omcp_blender", default_set=True)

    enabled_addon_names = bpy.context.preferences.addons.keys()
    assert "omcp_blender" not in enabled_addon_names


def test_restart_and_reload_preferences(omcp_blender):
    import bpy

    assert bpy.context.preferences.addons["omcp_blender"].preferences.domain_id == 0
    assert rclpy.utilities.get_default_context().get_domain_id() == 0

    bpy.context.preferences.addons["omcp_blender"].preferences.domain_id = 42
    bpy.ops.omcp.restart_and_reload_preferences("EXEC_DEFAULT")

    assert bpy.context.preferences.addons["omcp_blender"].preferences.domain_id == 42
