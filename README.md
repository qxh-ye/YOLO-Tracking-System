# YOLO Tracking System

## 1. 项目简介

本项目基于 YOLOv8 + ByteTrack 实现人员检测、目标跟踪、ROI区域统计、跨线计数、事件记录和轨迹可视化。

项目使用 OpenCV 进行视频处理，支持对视频中的行人进行实时跟踪和统计。

## 2. 核心功能

- YOLOv8人员检测
- ByteTrack多目标跟踪
- ROI区域人数统计
- ROI进入/离开事件
- ROI停留时间统计
- 跨线 Enter / Exit 计数
- Track ID轨迹绘制
- Event Panel事件显示
- FPS实时显示

## 3. 技术栈

- Python
- OpenCV
- Ultralytics YOLOv8
- ByteTrack
- NumPy
- Git / GitHub

## 4. 项目结构

```text
YOLO_Tracking_System
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── dashboard.py
├── shared_status.py
├── managers
│   ├── event_manager.py
│   ├── roi_manager.py
│   └── track_manager.py
├── templates
│   └── index.html
├── utils
│   └── visualizer.py
├── models
│   └── yolov8n.pt
├── videos
└── outputs
```

## 5. 模块说明
EventManager
负责统一管理事件日志，例如 ROI ENTER、ROI EXIT、LINE ENTER、LINE EXIT。

ROIManager
负责ROI区域判断、进入离开状态管理、停留时间计算。

TrackManager
负责轨迹历史管理、跨线检测、Enter / Exit 计数。

Visualizer
负责所有画面显示逻辑，例如ROI框、计数线、统计信息、事件面板和轨迹绘制。

shared_status.py：负责 main.py 和 dashboard.py 之间的实时状态共享。
dashboard.py：负责 Flask Dashboard 和 /api/status 接口。
templates/index.html：负责前端页面展示，并通过 fetch 定时请求接口刷新数据。

## 6. 运行方式
pip install -r requirements.txt
python main.py


## 7. 项目亮点
使用 YOLOv8 + ByteTrack 实现多目标跟踪
支持 ROI 区域进入、离开和停留时间统计
使用 Manager 结构拆分事件、ROI、轨迹管理模块
使用 Visualizer 解耦显示逻辑
通过 config.py 统一管理配置参数
具备进一步扩展为 Web Dashboard 和多摄像头系统的基础

## 8. 后续优化
- 支持多摄像头输入
- 增加报警截图保存
- 增加日志文件保存
- 支持 Linux 部署
- 支持 WebSocket 实时推送
- Docker 容器化部署