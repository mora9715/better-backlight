from better_backlight.state import SharedState


def test_shared_state_enabled():
    state = SharedState(last_input_activity_at=None, last_brightness=50, max_brightness=100)
    assert state.enabled


def test_shared_state_disabled():
    state = SharedState(last_input_activity_at=None, last_brightness=0, max_brightness=100)
    assert not state.enabled


def test_shared_state_disabled_by_user():
    state = SharedState(last_input_activity_at=None, last_brightness=50, max_brightness=0)
    assert state.disabled_by_user


def test_shared_state_not_disabled_by_user():
    state = SharedState(last_input_activity_at=None, last_brightness=50, max_brightness=100)
    assert not state.disabled_by_user
