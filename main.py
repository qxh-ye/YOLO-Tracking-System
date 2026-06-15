import cv2
import time
import threading
from ultralytics import YOLO

from managers.event_manager import EventManager
from managers.roi_manager import ROIManager
from utils.visualizer import Visualizer
from config import *
from managers.track_manager import TrackManager
from dashboard import run_dashboard
from shared_status import update_status

def main():
    model = YOLO(MODEL_PATH)
    dashboard_thread = threading.Thread(
        target=run_dashboard,
        daemon=True
    )
    dashboard_thread.start()

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
        conf=CONF,
        verbose=False
    )
    prev_time = time.time()

    tracked_ids = set()

    track_manager = TrackManager()
    fps = 0
    event_manager = EventManager()
    roi_manager = ROIManager(ROI_X1, ROI_Y1, ROI_X2, ROI_Y2)

    for result in results:
        frame = result.plot()
        roi_count = 0
        current_time = time.time()
        instant_fps = 1 / (current_time - prev_time)
        fps = fps * 0.9 + instant_fps * 0.1
        prev_time = current_time

        # 导包调用画框
        Visualizer.draw_roi(
            frame,
            ROI_X1,
            ROI_Y1,
            ROI_X2,
            ROI_Y2
        )

        frame_h, frame_w = frame.shape[:2]
        line_y = int(frame_h * 0.55)
        # 导包调用画线
        Visualizer.draw_counting_line(
            frame,
            line_y
        )

        current_person_count = 0
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
                tracked_ids.add(track_id)

                x, y, w, h = xywh
                frame_h, frame_w = frame.shape[:2]

                bottom_center_x = int(x)
                bottom_center_y = int(y + h / 2)

                bottom_center_x = max(0, min(bottom_center_x, frame_w - 1))
                bottom_center_y = max(0, min(bottom_center_y, frame_h - 1))

                is_in_roi, event = roi_manager.update(
                    track_id,
                    bottom_center_x,
                    bottom_center_y
                )

                if is_in_roi:
                    roi_count += 1

                if event:
                    event_manager.add_event(event)
                    print("=" * 30)
                    for log in event_manager.get_recent_events():
                        print(log)

                line_event = track_manager.update(
                    track_id,
                    bottom_center_x,
                    bottom_center_y,
                    line_y
                )
                if line_event:
                    event_manager.add_event(line_event)
                points = track_manager.get_history(track_id)
                # 画历史轨迹线
                Visualizer.draw_track_history(frame, points)
        if int(current_time) % 2 == 0:
            print(
                f"Current persons: {current_person_count}, "
                f"Total track IDs: {len(tracked_ids)}"
            )
        update_status({
            "fps": round(fps, 1),
            "roi_count": roi_count,
            "enter_count": track_manager.enter_count,
            "exit_count": track_manager.exit_count,
            "current_person_count": current_person_count,
            "total_unique_ids": len(tracked_ids),
            "events": event_manager.get_recent_events()
        })
        # 画状态栏
        Visualizer.draw_stats(
            frame,
            current_person_count,
            len(tracked_ids),
            track_manager.enter_count,
            track_manager.exit_count,
            roi_count,
            fps
        )
        y_offset = 300

        # =========================
        # Event Panel
        # =========================
        # 显示事件
        Visualizer.draw_event_panel(frame, event_manager.get_recent_events())

        cv2.imshow("YOLO Tracking", frame)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()
    print("=" * 40)
    print(f"Final total track IDs: {len(tracked_ids)}")



if __name__ == "__main__":
    main()