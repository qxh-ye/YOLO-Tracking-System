from collections import defaultdict

class TrackManager:
    def __init__(self, max_history=30):
        self.track_history = defaultdict(list)
        self.last_positions = {}
        self.crossed_ids = set()

        self.enter_count = 0
        self.exit_count = 0

        self.max_history = max_history

    def update(self, track_id, x, y, line_y):
        event = None

        current_side = "above" if y < line_y else "below"

        if track_id in self.last_positions:
            last_side = self.last_positions[track_id]

            if last_side != current_side and track_id not in self.crossed_ids:
                if last_side == "above" and current_side == "below":
                    self.enter_count += 1
                    event = f"ID {track_id} LINE ENTER"

                elif last_side == "below" and current_side == "above":
                    self.exit_count += 1
                    event = f"ID {track_id} LINE EXIT"

                self.crossed_ids.add(track_id)

        self.last_positions[track_id] = current_side
        self.track_history[track_id].append((x, y))

        if len(self.track_history[track_id]) > self.max_history:
            self.track_history[track_id].pop(0)

        return event

    def get_history(self, track_id):
        return self.track_history[track_id]
