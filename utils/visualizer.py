import cv2

class Visualizer:
    @staticmethod  # @staticmethod 不需要创建对象便可直接调用
    def draw_roi(
            frame,
            x1,
            y1,
            x2,
            y2
    ):
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 255),
            2
        )

    @staticmethod
    def draw_counting_line(
            frame,
            line_y
    ):
        frame_h, frame_w = frame.shape[:2]

        cv2.line(
            frame,
            (0, line_y),
            (frame_w, line_y),
            (0, 0, 255),
            2
        )

    @staticmethod
    def draw_stats(
            frame,
            current_person_count,
            total_unique_ids,
            enter_count,
            exit_count,
            roi_count,
            fps
    ):
        cv2.putText(frame, f"Current persons: {current_person_count}",
                    (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, f"Total Unique IDs: {total_unique_ids}",
                    (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, f"Enter Count: {enter_count}",
                    (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f"Exit Count: {exit_count}",
                    (30, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f"ROI Person: {roi_count}",
                    (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.putText(frame, f"FPS: {fps:.1f}",
                    (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    @staticmethod
    def draw_event_panel(frame, events):
        panel_x = 30
        panel_y = 330
        line_height = 26

        cv2.putText(
            frame,
            "Recent Events: ",
            (30, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        for i, log in enumerate(events):
            cv2.putText(
                frame,
                log,
                (panel_x, panel_y + (i + 1) * line_height),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )