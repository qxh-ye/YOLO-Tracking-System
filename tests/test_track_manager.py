from managers.track_manager import TrackManager


def test_first_position_no_event():
    manager = TrackManager()

    event = manager.update(
        track_id=1,
        x=100,
        y=50,
        line_y=100
    )

    assert event is None
    assert manager.enter_count == 0
    assert manager.exit_count == 0


def test_line_enter_event():
    manager = TrackManager()

    manager.update(
        track_id=1,
        x=100,
        y=50,
        line_y=100
    )

    event = manager.update(
        track_id=1,
        x=100,
        y=150,
        line_y=100
    )

    assert event == "ID 1 LINE ENTER"
    assert manager.enter_count == 1
    assert manager.exit_count == 0


def test_line_exit_event():
    manager = TrackManager()

    manager.update(
        track_id=1,
        x=100,
        y=150,
        line_y=100
    )

    event = manager.update(
        track_id=1,
        x=100,
        y=50,
        line_y=100
    )

    assert event == "ID 1 LINE EXIT"
    assert manager.enter_count == 0
    assert manager.exit_count == 1


def test_same_id_only_count_once():
    manager = TrackManager()

    manager.update(1, 100, 50, 100)
    event1 = manager.update(1, 100, 150, 100)

    manager.update(1, 100, 50, 100)
    event2 = manager.update(1, 100, 150, 100)

    assert event1 == "ID 1 LINE ENTER"
    assert event2 is None
    assert manager.enter_count == 1


def test_track_history_saved():
    manager = TrackManager()

    manager.update(1, 100, 50, 100)
    manager.update(1, 120, 70, 100)

    history = manager.get_history(1)

    assert history == [(100, 50), (120, 70)]


def test_track_history_max_length():
    manager = TrackManager(max_history=2)

    manager.update(1, 100, 50, 100)
    manager.update(1, 120, 70, 100)
    manager.update(1, 140, 90, 100)

    history = manager.get_history(1)

    assert len(history) == 2
    assert history == [(120, 70), (140, 90)]