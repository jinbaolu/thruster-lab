"""读取「推进器实验记录」页面导出的 CSV，对比两套设备，并拟合立方律。

用法：
    python analysis/analyze_runs.py data/runs/thruster-runs-20261012.csv
    python analysis/analyze_runs.py data/runs/thruster-runs-20261012.csv --exp E3.1

输出：
    1. 每套设备的记录数、推力效率（g/W）、最高温度
    2. 功率–转速、推力–转速的对数拟合指数（理论约 3 和 2）
    3. 预测检验：预测值和实测值的偏差
    4. analysis/out/thrust_vs_power.png
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NUMERIC = [
    "throttle_pct", "voltage_v", "i_batt_a", "i_motor_a", "rpm", "thrust_kg",
    "t_motor_c", "t_esc_c", "t_water_c", "pred_power_w", "pred_thrust_kg",
]
DEV_LIMIT = 20  # 预测偏差在 ±20% 以内算「准」，和记录页一致
# 图上用英文标签，避免系统缺中文字体时显示方块
DEVICE_LABELS = {"square": "Scheme 1 (square-wave)", "vesc": "Scheme 2 (VESC FOC)"}
DEVICE_NAMES_CN = {"square": "方案一 方波", "vesc": "方案二 VESC"}
# 固定顺序的分类色：设备颜色跟着设备走，不随筛选变化
DEVICE_COLORS = {"square": "#2a78d6", "vesc": "#eb6834"}
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    for col in NUMERIC:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = np.nan
    # 重新计算，不依赖导出时的取整
    df["power_w"] = df["voltage_v"] * df["i_batt_a"]
    df["g_per_w"] = df["thrust_kg"] * 1000 / df["power_w"].where(df["power_w"] > 0)
    df["power_dev_pct"] = (df["power_w"] - df["pred_power_w"]) / df["pred_power_w"].where(df["pred_power_w"] != 0) * 100
    df["thrust_dev_pct"] = (df["thrust_kg"] - df["pred_thrust_kg"]) / df["pred_thrust_kg"].where(df["pred_thrust_kg"] != 0) * 100
    return df


def print_predictions(df: pd.DataFrame) -> None:
    """三层检验的第二层：预测准不准。"""
    devs = pd.concat([df["power_dev_pct"], df["thrust_dev_pct"]]).dropna()
    print("\n== 预测检验 ==")
    if devs.empty:
        print("  还没有带预测值的记录。实验前在记录页填「预测功率」「预测推力」。")
        return
    hits = (devs.abs() <= DEV_LIMIT).sum()
    print(f"  命中 {hits} / {len(devs)}（偏差在 ±{DEV_LIMIT}% 以内），平均绝对偏差 {devs.abs().mean():.1f}%")
    cols = ["date", "experiment", "device", "power_dev_pct", "thrust_dev_pct"]
    misses = df[(df["power_dev_pct"].abs() > DEV_LIMIT) | (df["thrust_dev_pct"].abs() > DEV_LIMIT)]
    if not misses.empty:
        print("  偏差大的记录（找出原因，写进备注）：")
        for _, r in misses[cols].iterrows():
            print(f"    {r['date']} {r['experiment']} {DEVICE_NAMES_CN.get(r['device'], r['device'])}"
                  f"  功率偏差 {fmt(r['power_dev_pct'])}%  推力偏差 {fmt(r['thrust_dev_pct'])}%")


def fit_exponent(df: pd.DataFrame, y: str, x: str = "rpm"):
    """在对数坐标上拟合 y ∝ x^k，返回 (k, 点数)；点数少于 3 时返回 None。"""
    d = df[[x, y]].dropna()
    d = d[(d[x] > 0) & (d[y] > 0)]
    if len(d) < 3:
        return None
    k, _ = np.polyfit(np.log(d[x]), np.log(d[y]), 1)
    return k, len(d)


def fmt(v, digits=1):
    return "—" if pd.isna(v) else f"{v:.{digits}f}"


def print_summary(df: pd.DataFrame) -> None:
    print("\n== 设备对比 ==")
    for dev in ["square", "vesc"]:
        g = df[df["device"] == dev]
        if g.empty:
            continue
        eff = g["g_per_w"].dropna()
        print(f"\n{DEVICE_NAMES_CN[dev]}：{len(g)} 条记录")
        print(f"  推力效率  最佳 {fmt(eff.max())} g/W   平均 {fmt(eff.mean())} g/W   （有效 {len(eff)} 条）")
        print(f"  最高温度  电机 {fmt(g['t_motor_c'].max(), 0)} °C   电调 {fmt(g['t_esc_c'].max(), 0)} °C")

        for y, label, theory in [("power_w", "功率–转速", 3), ("thrust_kg", "推力–转速", 2)]:
            res = fit_exponent(g, y)
            if res is None:
                print(f"  {label}指数  数据不足（需要至少 3 条同时有转速和{label[:2]}的记录）")
            else:
                k, n = res
                print(f"  {label}指数  {k:.2f}（理论约 {theory}，{n} 个点）")


def plot(df: pd.DataFrame, out: Path, title_suffix: str) -> bool:
    d = df.dropna(subset=["power_w", "thrust_kg"])
    if d.empty:
        return False

    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    for dev in ["square", "vesc"]:
        g = d[d["device"] == dev].sort_values("power_w")
        if g.empty:
            continue
        ax.scatter(
            g["power_w"], g["thrust_kg"], s=64, color=DEVICE_COLORS[dev],
            edgecolors=SURFACE, linewidths=2, label=DEVICE_LABELS[dev], zorder=3,
        )

    ax.set_xlabel("Battery power (W)", color=TEXT_SECONDARY)
    ax.set_ylabel("Thrust (kg)", color=TEXT_SECONDARY)
    ax.set_title("Thrust vs battery power" + title_suffix, color=TEXT_PRIMARY, loc="left", fontsize=12)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.tick_params(colors=TEXT_SECONDARY, length=0)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.legend(frameon=False, labelcolor=TEXT_PRIMARY, loc="upper left")

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, facecolor=SURFACE)
    plt.close(fig)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="推进器实验记录分析")
    parser.add_argument("csv", type=Path, help="从实验记录页面导出的 CSV")
    parser.add_argument("--exp", help="只看某个实验编号，例如 E3.1")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "out" / "thrust_vs_power.png")
    args = parser.parse_args()

    df = load(args.csv)
    if args.exp:
        df = df[df["experiment"].astype(str).str.upper() == args.exp.upper()]
    print(f"读取 {args.csv}：{len(df)} 条记录" + (f"（实验 {args.exp.upper()}）" if args.exp else ""))
    if df.empty:
        return

    print_summary(df)
    print_predictions(df)
    if plot(df, args.out, f" · {args.exp.upper()}" if args.exp else ""):
        print(f"\n图已保存：{args.out}")
    else:
        print("\n没有同时带功率和推力的记录，跳过画图。")


if __name__ == "__main__":
    main()
