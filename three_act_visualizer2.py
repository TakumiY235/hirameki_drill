import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 各プロットポイントの情報をまとめた辞書
PLOT_POINTS = [
    ("Opening Image", 1), ("Set-up", 5), ("Theme Stated", 10),
    ("Catalyst", 15), ("Debate", 20), ("Fun & Games", 35),
    ("Pinch 1", 40), ("Fall Start", 65), ("Pinch 2", 70),
    ("All is Lost", 75), ("Dark Night of the Soul", 80),
    ("Restart", 95), ("Climax", 100), ("Climactic Moment", 105), ("Resolution", 110)
]

# Turning Points
TURNING_POINTS = [
    ("Turning Point 1", 30),
    ("Midpoint", 60),
    ("Turning Point 2", 90)
]

# プロットポイントのチェックボックスをまとめる関数
def plot_point_inputs(total_minutes):
    plot_data = {}
    with st.expander("Act 1: Opening Image to Debate"):
        for name, default_value in PLOT_POINTS[:5]:
            col1, col2 = st.columns([1, 1])
            with col1:
                time = st.number_input(f'{name} (minutes)', min_value=0, max_value=total_minutes, value=min(default_value, total_minutes))
            with col2:
                show = st.checkbox(f'Show {name}', value=True)
            plot_data[name] = (time, show)
    with st.expander("Act 2-1: Fun & Games to Pinch 1"):
        for name, default_value in PLOT_POINTS[5:7]:
            col1, col2 = st.columns([1, 1])
            with col1:
                time = st.number_input(f'{name} (minutes)', min_value=0, max_value=total_minutes, value=min(default_value, total_minutes))
            with col2:
                show = st.checkbox(f'Show {name}', value=True)
            plot_data[name] = (time, show)
    with st.expander("Act 2-2: Fall Start to Dark Night of the Soul"):
        for name, default_value in PLOT_POINTS[7:11]:
            col1, col2 = st.columns([1, 1])
            with col1:
                time = st.number_input(f'{name} (minutes)', min_value=0, max_value=total_minutes, value=min(default_value, total_minutes))
            with col2:
                show = st.checkbox(f'Show {name}', value=True)
            plot_data[name] = (time, show)
    with st.expander("Act 3: Restart to Resolution"):
        for name, default_value in PLOT_POINTS[11:]:
            col1, col2 = st.columns([1, 1])
            with col1:
                time = st.number_input(f'{name} (minutes)', min_value=0, max_value=total_minutes, value=min(default_value, total_minutes))
            with col2:
                show = st.checkbox(f'Show {name}', value=True)
            plot_data[name] = (time, show)
    return plot_data

# Turning Pointsの入力をまとめる関数
def turning_point_inputs(total_minutes):
    turning_data = {}
    for name, default_value in TURNING_POINTS:
        time = st.number_input(f'{name} (minutes)', min_value=0, max_value=total_minutes, value=min(default_value, total_minutes))
        turning_data[name] = time
    return turning_data

# ユーザーが追加するプロットポイントグループの入力をまとめる関数
def additional_plot_point_groups():
    additional_groups = []
    additional_lines_data = []  # 追加プロットポイント間の線分の情報を格納するリスト
    show_additional_groups = st.checkbox("Show Additional Plot Point Groups", value=False)
    if show_additional_groups:
        num_groups = st.number_input("Number of additional plot point groups", min_value=0, value=0, step=1)
        for group_index in range(num_groups):
            group_points = []
            group_name = st.text_input(f"Name of plot point group {group_index + 1}", value=f"Additional Plot Point Group {group_index + 1}")
            with st.expander(f"### {group_name}"):
                color = st.selectbox(f'Select color for {group_name}', COLOR_OPTIONS.keys(), index=2)
                num_points = st.number_input(f"Number of plot points in group {group_index + 1}", min_value=0, value=0, step=1)
                for i in range(num_points):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        name = st.text_input(f"Name of plot point {i + 1} in group {group_index + 1}", value=f"{group_name} - Point {i + 1}")
                    with col2:
                        time = st.number_input(f"Time of plot point {i + 1} in group {group_index + 1} (minutes)", min_value=0, max_value=300, value=10)
                    group_points.append((name, time))
                if len(group_points) > 1:
                    st.write(f"### Connect Additional Plot Points in {group_name} with Lines")
                    for i in range(len(group_points) - 1):
                        connect = st.checkbox(f"Connect {group_points[i][0]} to {group_points[i + 1][0]} in {group_name}", value=True)
                        if connect:
                            additional_lines_data.append((group_points[i], group_points[i + 1], color))
            additional_groups.append((group_name, group_points, color))
    return additional_groups, additional_lines_data

# レイアウト設定
def layout_input():
    col1, col2 = st.columns([3, 1])
    with col1:
        title = st.text_input("Title", "Three-Act Structure Visualization", key="unique_title")
    with col2:
        total_minutes = st.number_input('Running time (minutes)', min_value=1, max_value=300, value=120)

    # オープニングとエンドクレジット
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        main_start_time = st.number_input('Main content start time (minutes)', min_value=0, max_value=total_minutes, value=min(1, total_minutes))
    with col2:
        opening_color = st.selectbox("Select color for Opening credits", COLOR_OPTIONS.keys(), index=2)
    with col3:
        end_credits_start = st.number_input('End credits start time (minutes)', min_value=0, max_value=total_minutes, value=min(115, total_minutes))
    with col4:
        end_credits_color = st.selectbox("Select color for End credits", COLOR_OPTIONS.keys(), index=2)

    # 各プロットポイントの入力
    plot_data = plot_point_inputs(total_minutes)

    # Turning Pointsの入力
    turning_data = turning_point_inputs(total_minutes)

    # Additional Plot Point Groupsの入力
    additional_groups, additional_lines = additional_plot_point_groups()

    # Act Colors
    act1_color = st.selectbox("Select color for Act 1", COLOR_OPTIONS.keys(), index=4)
    act2_color = st.selectbox("Select color for Act 2", COLOR_OPTIONS.keys(), index=7)
    act3_color = st.selectbox("Select color for Act 3", COLOR_OPTIONS.keys(), index=6)

    include_credits = st.checkbox('Include Opening and End Credits in main runtime', value=True)

    return title, total_minutes, main_start_time, end_credits_start, plot_data, turning_data, additional_groups, additional_lines, include_credits, opening_color, end_credits_color, act1_color, act2_color, act3_color

# 三幕構成の描画 (Plotlyによる動的なグラフ)
def plot_three_act_structure(title, total_minutes, main_start_time, end_credits_start, plot_data, turning_data, additional_groups, additional_lines, include_credits, opening_color_code, end_credits_color_code, act1_color_code, act2_color_code, act3_color_code):
    if not include_credits:
        main_start_time = 0
    adjusted_total_minutes = total_minutes if include_credits else total_minutes - (plot_data["Opening Image"][0] + (total_minutes - end_credits_start))
    radians = lambda time: (time - plot_data["Opening Image"][0]) / adjusted_total_minutes * 360 if not include_credits else time / adjusted_total_minutes * 360

    fig = go.Figure()

    # Act sections (扇形の領域を色付け)
    # Act 1: Opening Image to Turning Point 1 (Arc)
    theta_act1 = list(np.linspace(radians(plot_data["Opening Image"][0]), radians(turning_data["Turning Point 1"]), num=50))
    fig.add_trace(go.Scatterpolar(
        r=[0] + [1] * len(theta_act1) + [0],
        theta=[radians(plot_data["Opening Image"][0])] + theta_act1 + [theta_act1[-1]],
        fill='tonext',
        name='Act 1',
        line=dict(color=act1_color_code, width=0),
        opacity=0.5
    ))

    # Act 2: Turning Point 1 to Turning Point 2 (Arc)
    theta_act2 = list(np.linspace(radians(turning_data["Turning Point 1"]), radians(turning_data["Turning Point 2"]), num=50))
    fig.add_trace(go.Scatterpolar(
        r=[0] + [1] * len(theta_act2) + [0],
        theta=[radians(turning_data["Turning Point 1"])] + theta_act2 + [theta_act2[-1]],
        fill='tonext',
        name='Act 2',
        line=dict(color=act2_color_code, width=0),
        opacity=0.5
    ))

    # Act 3: Turning Point 2 to End Credits Start (Arc)
    theta_act3 = list(np.linspace(radians(turning_data["Turning Point 2"]), radians(end_credits_start), num=50))
    fig.add_trace(go.Scatterpolar(
        r=[0] + [1] * len(theta_act3) + [0],
        theta=[radians(turning_data["Turning Point 2"])] + theta_act3 + [theta_act3[-1]],
        fill='tonext',
        name='Act 3',
        line=dict(color=act3_color_code, width=0),
        opacity=0.5
    ))

    # プロットポイントの描画
    for name, (time, show) in plot_data.items():
        if show:
            textposition = 'top center'
            if name in ["Opening Image", "Set-up", "Theme Stated", "Catalyst", "Debate", "Fun & Games"]:
                textposition = 'top right'
            elif name in ["Midpoint", "Pinch 1", "Fall Start"]:
                textposition = 'bottom center'
            else:
                textposition = 'top left'

            fig.add_trace(go.Scatterpolar(
                r=[1],
                theta=[radians(time)],
                mode='markers+text',
                marker=dict(size=10, color='blue'),
                text=[name],
                textposition=textposition,
                name=name
            ))

    # Turning Pointsの描画
    for name, time in turning_data.items():
        textposition = 'top center'
        if name == "Turning Point 1":
            textposition = 'top right'
        elif name == "Midpoint":
            textposition = 'bottom center'
        elif name == "Turning Point 2":
            textposition = 'top left'

        fig.add_trace(go.Scatterpolar(
            r=[1],
            theta=[radians(time)],
            mode='markers+text',
            marker=dict(size=10, color='red'),
            text=[name],
            textposition=textposition,
            name=name
        ))

    # 追加プロットポイントグループの描画
    for group_name, group_points, color in additional_groups:
        for name, time in group_points:
            fig.add_trace(go.Scatterpolar(
                r=[1],
                theta=[radians(time)],
                mode='markers+text',
                marker=dict(size=10, color=COLOR_OPTIONS[color]),
                text=[name],
                textposition='top center',
                name=f'{group_name}: {name}'
            ))

    # 追加プロットポイント間の線分の描画
    for point1, point2, color in additional_lines:
        fig.add_trace(go.Scatterpolar(
            r=[1, 1],
            theta=[radians(point1[1]), radians(point2[1])],
            mode='lines',
            line=dict(color=COLOR_OPTIONS[color], width=1),
            name=f'Line from {point1[0]} to {point2[0]}'
        ))

    # 中心からOpening Image、中心からTurning Point 1、中心からTurning Point 2を結ぶ線分を追加
    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[0, radians(plot_data["Opening Image"][0])],
        mode='lines',
        line=dict(color='black', width=1),
        name='Center to Opening Image'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[0, radians(turning_data["Turning Point 1"])],
        mode='lines',
        line=dict(color='black', width=1),
        name='Center to TP1'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[0, radians(turning_data["Turning Point 2"])],
        mode='lines',
        line=dict(color='black', width=1),
        name='Center to TP2'
    ))

    # レイアウト設定 (角度の表示を非表示に設定)
    fig.update_layout(
        title=title,
        polar=dict(
            angularaxis=dict(visible=False, direction="clockwise"),
            radialaxis=dict(visible=False)
        )
    )

    # グラフを表示
    st.plotly_chart(fig)

# 色オプション
COLOR_OPTIONS = {
    "Red": "#FF0000",
    "Blue": "#0000FF",
    "Green": "#008000",
    "Pink": "#FFC0CB",
    "Gray (Light)": "#D3D3D3",
    "Gray (Medium)": "#A9A9A9",
    "Gray (Dark)": "#696969",
    "Light Blue": "#ADD8E6",
    "Light Green": "#90EE90",
    "Light Red": "#F08080",
    "Light Yellow": "#FFFFE0"
}

def main():
    (title, total_minutes, main_start_time, end_credits_start, plot_data, turning_data,
     additional_groups, additional_lines, include_credits, opening_color, end_credits_color,
     act1_color, act2_color, act3_color) = layout_input()

    plot_three_act_structure(
        title, total_minutes, main_start_time, end_credits_start, plot_data, turning_data,
        additional_groups, additional_lines, include_credits, COLOR_OPTIONS[opening_color], COLOR_OPTIONS[end_credits_color],
        COLOR_OPTIONS[act1_color], COLOR_OPTIONS[act2_color], COLOR_OPTIONS[act3_color]
    )

if __name__ == "__main__":
    main()
