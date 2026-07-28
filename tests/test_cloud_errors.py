from custom_components.sonoff.core.ewelink import XRegistry
from custom_components.sonoff.core.ewelink.cloud import cloud_error_event


def test_cloud_error_event_is_redacted():
    event = cloud_error_event(
        {
            "error": 411,
            "deviceid": "1000123abc",
            "sequence": "123",
            "apikey": "must-not-leak",
            "uid": "must-not-leak",
        }
    )

    assert event == {
        "error": 411,
        "deviceid": "1000123abc",
        "sequence": "123",
        "action": None,
    }


def test_cloud_error_records_parent_context_without_running_loop():
    registry = XRegistry(None)
    parent = {"deviceid": "10022bd4a5", "productModel": "ZBBridge-P"}
    device = {"deviceid": "1000123abc", "parent": parent}
    registry.devices = {device["deviceid"]: device}
    registry.cloud_pending["123"] = {
        "action": "update",
        "param_keys": ["switch"],
        "safe_retry": True,
    }

    registry.cloud_error({"error": 411, "deviceid": device["deviceid"], "sequence": "123"})

    assert device["last_cloud_error"]["code"] == 411
    assert device["last_cloud_error"]["parent_model"] == "ZBBridge-P"
    assert device["last_cloud_error"]["param_keys"] == ["switch"]


def test_only_explicit_switch_values_are_safe_to_retry():
    assert XRegistry.is_safe_retry({"switch": "on"})
    assert XRegistry.is_safe_retry({"switch": "off"})
    assert not XRegistry.is_safe_retry({"switch": "toggle"})
    assert not XRegistry.is_safe_retry({"switch": "on", "brightness": 10})
    assert not XRegistry.is_safe_retry(None)
