from collections import deque
import time

class EventManager:
    def __init__(self):
        self.events = deque(maxlen=20)          # 最多保存20条事件，超过自动删除最早的数据

    def add_event(self, message):
        event = (
            f"[{time.strftime('%H:%M:%S')}] "
            f"{message}"
        )
        self.events.append(event)

    def get_recent_events(self, count=5):
        return list(self.events)[-count:]           # 获取最近count条事件