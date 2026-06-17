# YOLOv8 ByteTrack Intelligent Pedestrian Flow Analytics System

基于 **YOLOv8 + ByteTrack + OpenCV + Flask** 的智能人流分析系统，用于对视频中的行人进行实时检测、目标跟踪、ROI 区域统计、越线计数、轨迹绘制和事件展示。

项目不仅包含 OpenCV 本地可视化窗口，也提供了一个 Flask Dashboard，通过 `/api/status` 接口实时展示系统运行状态，适合作为计算机视觉工程实践项目和实习求职作品集项目。

## 1. 项目简介

本项目面向商场、通道、展厅、园区等场景中的人流分析需求，使用 YOLOv8 完成人员检测，并结合 ByteTrack 进行多目标跟踪。系统会根据每个目标的 Track ID 维护轨迹历史，统计 ROI 区域内人数，并基于计数线判断人员进入和离开方向。

当前项目已实现从视频输入、目标检测、目标跟踪、业务统计、事件管理、画面可视化到 Web Dashboard 状态展示的完整流程。

## 2. 技术栈

- Python
- OpenCV
- Ultralytics YOLOv8
- ByteTrack
- Flask
- HTML / CSS / JavaScript
- Fetch API
- Threading / Lock

## 3. 项目结构

```text
YOLO_Tracking_System/
├── main.py                  # 主程序入口，负责模型推理、跟踪、统计和可视化主循环
├── config.py                # 项目配置，包括模型路径、视频路径、置信度和 ROI 坐标
├── dashboard.py             # Flask Dashboard 服务与 API 路由
├── shared_status.py         # 主线程与 Dashboard 之间的共享状态管理
├── requirements.txt         # Python 依赖列表
├── requirements_full.txt    # 完整环境依赖快照，适合复现开发环境
├── README.md                # 项目说明文档
│
├── managers/
│   ├── roi_manager.py       # ROI 区域判断、进入/离开事件、停留时间统计
│   ├── track_manager.py     # 轨迹历史管理、越线计数、Enter/Exit 统计
│   └── event_manager.py     # 实时事件缓存与最近事件查询
│
├── utils/
│   └── visualizer.py        # OpenCV 可视化绘制，包括 ROI、计数线、统计信息和轨迹
│
├── templates/
│   └── index.html           # Dashboard 前端页面
│
├── models/
│   └── yolov8n.pt           # YOLOv8 模型文件
│
├── videos/
│   ├── test.mp4             # 测试视频
│   └── test1.mp4            # 测试视频
│
├── outputs/                 # 输出目录
└── runs/                    # YOLO 运行结果目录
```

## 4. 核心功能

### YOLOv8 行人检测

项目通过 Ultralytics YOLOv8 加载本地模型文件，对视频中的行人进行检测。目前代码中指定 `classes=[0]`，只检测 COCO 数据集中的 `person` 类别。

### ByteTrack 多目标跟踪

系统使用 YOLOv8 内置的 `model.track()` 接口，并指定 `tracker="bytetrack.yaml"`，为每个检测到的行人分配稳定的 Track ID，用于后续轨迹绘制、越线判断和去重统计。

### ROI 区域统计

`ROIManager` 负责判断目标是否进入指定 ROI 区域，并维护每个 Track ID 的区域内外状态。系统支持：

- 当前 ROI 区域人数统计
- ROI ENTER 事件
- ROI EXIT 事件
- ROI 停留时间统计

### 越线计数

`TrackManager` 根据目标中心点与计数线的位置关系判断目标移动方向，并统计：

- Enter Count
- Exit Count
- LINE ENTER 事件
- LINE EXIT 事件

### 轨迹绘制

系统会为每个 Track ID 保存最近一段历史坐标，并在画面中绘制运动轨迹，方便观察目标移动路径。

### Event 事件管理

`EventManager` 使用队列保存最近事件，包括 ROI 进入、ROI 离开、越线进入和越线离开。事件会同时显示在 OpenCV 画面和 Web Dashboard 中。

### OpenCV 可视化

`Visualizer` 负责绘制：

- ROI 区域框
- 越线计数线
- 当前人数
- 累计 Track ID 数量
- Enter / Exit 计数
- ROI 区域人数
- FPS
- 事件面板
- 目标历史轨迹

## 5. Dashboard 说明

项目内置 Flask Dashboard，用于展示系统实时状态。

启动主程序后，Dashboard 会在本地启动：

```text
http://127.0.0.1:5000
```

Dashboard 当前展示以下信息：

- FPS
- ROI Count
- Enter Count
- Exit Count
- Current Person Count
- Total Unique IDs
- Recent Events

前端页面通过 JavaScript `fetch()` 每秒请求一次：

```text
/api/status
```

该接口返回主程序中的共享状态数据。`shared_status.py` 使用 `Lock` 保证视频处理线程和 Flask 线程之间的数据读写安全。

## 6. 运行方法

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd YOLO_Tracking_System
```

### 2. 安装依赖

项目提供两个依赖文件：

- `requirements.txt`：核心运行依赖，推荐优先使用。
- `requirements_full.txt`：完整开发环境依赖快照，适合需要严格复现环境时参考。

推荐安装核心依赖：

```bash
pip install -r requirements.txt
```

如需复现完整开发环境，可以参考：

```bash
pip install -r requirements_full.txt
```

如果 `requirements_full.txt` 中存在本地路径依赖导致安装失败，建议优先使用 `requirements.txt`。

### 3. 准备模型和视频

确认以下文件存在：

```text
models/yolov8n.pt
videos/test1.mp4
```

如果需要更换模型、视频、置信度或 ROI 区域，可以修改 `config.py`：

```python
MODEL_PATH = "models/yolov8n.pt"
VIDEO_PATH = "videos/test1.mp4"
CONF = 0.25

ROI_X1 = 350
ROI_Y1 = 250
ROI_X2 = 1500
ROI_Y2 = 850
```

### 4. 启动系统

```bash
python main.py
```

启动后会打开 OpenCV 实时可视化窗口，同时启动 Flask Dashboard。

### 5. 打开 Dashboard

在浏览器访问：

```text
http://127.0.0.1:5000
```

### 6. 退出程序

在 OpenCV 窗口中按下 `q` 退出。

## 7. 项目亮点

- 使用 YOLOv8 + ByteTrack 实现行人检测与多目标跟踪，具备完整的 CV 推理链路。
- 基于 Track ID 实现 ROI 进入/离开、停留时间、越线方向和去重统计。
- 将 ROI、轨迹、事件和可视化逻辑拆分到独立模块，项目结构比单文件 Demo 更清晰。
- 使用 Flask Dashboard 提供实时状态接口，支持前端自动刷新展示。
- 使用共享状态和线程锁解决视频处理线程与 Web 服务线程之间的数据同步问题。
- 同时支持 OpenCV 本地画面展示和 Web Dashboard 数据展示，便于演示和扩展。

## 8. 系统流程

```text
Input Video
    ↓
YOLOv8 Detection
    ↓
ByteTrack Tracking
    ↓
ROIManager / TrackManager
    ↓
EventManager
    ↓
shared_status
    ↓
Flask Dashboard
    ↓
Frontend Fetch Auto Refresh
```

## 9. 后续优化方向

- 将事件改为结构化数据，并支持 CSV / JSON 导出。
- 优化 Dashboard 页面样式，增加图表、历史事件列表和运行状态提示。
- 引入 WebSocket，实现更实时的数据推送。
- 支持摄像头实时输入和 RTSP 视频流。
- 增加 Docker 部署文件，方便在服务器环境中运行。
- 支持多摄像头输入和多区域 ROI 分析。
