from managers.roi_manager import ROIManager



def test_point_inside_roi():
    roi = ROIManager(100, 100, 300, 300)

    assert roi.is_inside(200, 200) is True


def test_point_outside_roi():
    roi = ROIManager(100, 100, 300, 300)

    assert roi.is_inside(50, 200) is False


def test_roi_enter_event():
    roi = ROIManager(100, 100, 300, 300)

    is_in_roi, event = roi.update(1, 200, 200)

    assert is_in_roi is True
    assert event == "ID 1 ROI ENTER"


def test_roi_no_repeat_enter_event():
    roi = ROIManager(100, 100, 300, 300)

    roi.update(1, 200, 200)
    is_in_roi, event = roi.update(1, 220, 220)

    assert is_in_roi is True
    assert event is None


def test_roi_exit_event():
    roi = ROIManager(100, 100, 300, 300)

    roi.update(1, 200, 200)
    is_in_roi, event = roi.update(1, 400, 400)

    assert is_in_roi is False
    assert "ID 1 ROI EXIT" in event
    assert "Stay" in event