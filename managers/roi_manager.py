import time

class ROIManager:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.enter_time = {}
        self.inside_status = {}

    def is_inside(self, x, y):
        return self.x1 < x < self.x2 and self.y1 < y < self.y2

    def update(self, track_id, x, y):
        is_in_roi = self.is_inside(x, y)
        last_in_roi = self.inside_status.get(track_id, False)

        event = None

        if is_in_roi and not last_in_roi:
            self.enter_time[track_id] = time.time()
            event = f"ID {track_id} ROI ENTER"
        elif not is_in_roi and last_in_roi:
            if track_id in self.enter_time:
                stay_time = time.time() - self.enter_time[track_id]
                event = f"ID {track_id} ROI EXIT, Stay {stay_time:.1f}s"
                del self.enter_time[track_id]

        self.inside_status[track_id] = is_in_roi

        return is_in_roi, event