import cv2
import time
from ultralytics import YOLO
from collections import defaultdict

MODEL_PATH = "models/yolov8n.pt"
VIDEO_PATH = "videos/test1.mp4"

ROI_X1 = 350
ROI_Y1 = 250

ROI_X2 = 1500
ROI_Y2 = 850

def main():
    model = YOLO(MODEL_PATH)

    cv2.namedWindow(
        "YOLO Tracking",
        cv2.WINDOW_NORMAL
    )
    cv2.resizeWindow(
        "YOLO Tracking",
        1280,
        720
    )

    results = model.track(
        source=VIDEO_PATH,
        stream=True,
        show=False,
        save=False,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0],
        conf=0.25,
        verbose=False
    )
    prev_time = time.time()

    tracked_ids = set()

    track_history = defaultdict(list)
    last_positions = {}
    crossed_ids = set()
    enter_count = 0
    exit_count = 0
    fps = 0
    event_log = []

    for result in results:
        frame = result.plot()
        roi_count = 0
        current_time = time.time()
        instant_fps = 1 / (current_time - prev_time)
        fps = fps * 0.9 + instant_fps * 0.1
        prev_time = current_time

        cv2.rectangle(
            frame,
            (ROI_X1, ROI_Y1),
            (ROI_X2, ROI_Y2),
            (0, 255, 255),
            2
        )

        frame_h, frame_w = frame.shape[:2]
        line_y = int(frame_h * 0.55)
        cv2.line(
            frame,
            (0, line_y),
            (frame_w, line_y),
            (0, 0, 255),
            2
        )

        current_person_count = 0
        current_ids = set()
        if result.boxes is None:
            continue

        boxes = result.boxes
        if boxes.id is None:
            continue

        ids = boxes.id.cpu().numpy().astype(int)
        classes = boxes.cls.cpu().numpy().astype(int)
        xywhs = boxes.xywh.cpu().numpy()

        for track_id, cls_id, xywh in zip(ids, classes, xywhs):
            class_name = model.names[cls_id]

            if class_name == "person":
                current_person_count += 1
                current_ids.add(track_id)
                tracked_ids.add(track_id)

                x, y, w, h = xywh
                frame_h, frame_w = frame.shape[:2]

                bottom_center_x = int(x)
                bottom_center_y = int(y + h / 2)

                bottom_center_x = max(0, min(bottom_center_x, frame_w - 1))
                bottom_center_y = max(0, min(bottom_center_y, frame_h - 1))

                if (ROI_X1 < bottom_center_x < ROI_X2 and ROI_Y1 < bottom_center_y < ROI_Y2):
                    roi_count += 1

                current_side = "above" if bottom_center_y < line_y else "below"
                if track_id in last_positions:
                    last_side = last_positions[track_id]

                    if last_side != current_side and track_id not in crossed_ids:
                        if last_side == "above" and current_side == "below":
                            enter_count += 1
                            event_log.append(
                                f"{time.strftime('%H:%M:%S')}"
                                f"ID {track_id} ENTER"
                            )
                            print("=" * 30)
                            for log in event_log[-5:]:
                                print(log)
                        elif last_side == "below" and current_side == "above":
                            exit_count += 1
                            event_log.append(
                                f"{time.strftime('%H:%M:%S')}"
                                f"ID {track_id} EXIT"
                            )
                            print("=" * 30)
                            for log in event_log[-5:]:
                                print(log)

                        crossed_ids.add(track_id)
                        event_log.append(
                            f"ID {track_id} crossed line"
                        )
                        print("=" * 30)
                        for log in event_log[-5:]:
                            print(log)
                        if len(event_log) > 20:
                            event_log.pop(0)

                last_positions[track_id] = current_side

                track_history[track_id].append((bottom_center_x, bottom_center_y))
                if len(track_history[track_id]) > 5:
                    track_history[track_id].pop(0)
                points = track_history[track_id]

                for i in range(1, len(points)):
                    x1, y1 = points[i - 1]
                    x2, y2 = points[i]

                    cv2.line(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

        print(
            f"Current persons: {current_person_count}, "
            f"Total track IDs: {len(tracked_ids)}"
        )
        cv2.putText(
            frame,
            f"Current persons: {current_person_count}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"History IDs: {len(tracked_ids)}",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            "Counting Line",
            (30, line_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )
        cv2.putText(
            frame,
            f"Enter Count: {enter_count}",
            (30, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        cv2.putText(
            frame,
            f"Exit Count: {exit_count}",
            (30, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (30, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"ROI Person: {roi_count}",
            (30, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )
        cv2.imshow("YOLO Tracking", frame)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()
    print("=" * 40)
    print(f"Final total track IDs: {len(tracked_ids)}")



if __name__ == "__main__":
    main()