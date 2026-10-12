# thruster-lab

72V 浆板/水下推进器的实验仓库：配置、原始数据、分析脚本、接线图都放在这里，用 git 管版本。

学习路线和每章验收在 Claude 文档「72V 水上推进器 · 系统学习路线」里，日常的每次测试记录在「推进器实验记录」页面里。这个仓库放进度、知识地图和各种文件。

## 学习机制

想学的时候在 Claude 里说「开始学习」或「继续」，从上次停下的地方接着讲。

- **进度：** [PROGRESS.md](PROGRESS.md)
- **知识地图：** [knowledge/map.md](knowledge/map.md)，阶段零 9 课底层原理 + 「会发生什么」情景题 + 错题回炉
- **规则：** [docs/learning-loop.md](docs/learning-loop.md)

## 目录

```
PROGRESS.md        当前进度、安全底线、学习日志
knowledge/
  map.md           知识地图、情景题库、错题回炉
configs/
  vesc/            VESC Tool 导出的配置 XML（电机配置、App 配置）
  square/          方案一方波控制器的参数记录（限流、欠压值、转换板标定）
data/
  runs/            从「推进器实验记录」页面导出的 CSV
  raw/             VESC 实时数据日志、推力传感器日志等原始文件
analysis/
  analyze_runs.py  读取导出的 CSV，对比两套设备，拟合立方律
docs/
  learning-loop.md 学习机制的规则
  wiring/          两套方案的配电图、信号接线图
  notes.md         设备档案、失控保护实测、问题清单
```

## 文件命名

日期打头，方便排序：

- 配置：`configs/vesc/2026-10-12_motor_detect-v1.xml`
- 原始日志：`data/raw/2026-10-12_E3.1_vesc_tank.csv`
- 导出记录：`data/runs/thruster-runs-20261012.csv`（页面导出的默认名，直接放进来）

## 分析脚本

```bash
pip install pandas numpy matplotlib
python analysis/analyze_runs.py data/runs/thruster-runs-20261012.csv
python analysis/analyze_runs.py data/runs/thruster-runs-20261012.csv --exp E3.1
```

输出：

1. 每套设备的记录数、最佳和平均推力效率（克/瓦）、最高电机和电调温度。
2. 功率–转速、推力–转速的拟合指数（E2.3 验证立方律用，理论约 3 和 2）。
3. `analysis/out/thrust_vs_power.png`：两套设备的推力–电池功率对比图。

## 改参数的纪律

一次只改一个参数。改之前先把当前 VESC 配置导出提交，改完测完再导出提交，commit 信息写清楚改了什么、为什么、结果如何，例如：

```
E3.4: Battery Current Max 40A -> 30A，功率计实测电池电流被限在 30.4A
```
