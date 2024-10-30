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

TURNING_POINTS = [
    ("Turning Point 1", 30),
    ("Midpoint", 60),
    ("Turning Point 2", 90)
]

COLOR_OPTIONS = {
    "Red": "#FF0000", "Blue": "#0000FF", "Green": "#008000",
    "Pink": "#FFC0CB", "Gray (Light)": "#D3D3D3",
    "Gray (Medium)": "#A9A9A9", "Gray (Dark)": "#696969",
    "Light Blue": "#ADD8E6", "Light Green": "#90EE90",
    "Light Red": "#F08080", "Light Yellow": "#FFFFE0"
}

# 角度を計算するヘルパー関数
def calc_radians(time, main_start_time, total_minutes, end_credits_start, include_credits):
    adjusted_minutes = total_minutes - (main_start_time + (total_minutes - end_credits_start)) if not include_credits else total_minutes
    return (time - main_start_time) / adjusted_minutes * 360

# プロットポイントの入力
def plot_point_inputs(total_minutes):
    plot_data = {}
    for i, (name, default_value) in enumerate(PLOT_POINTS):
        expander_name = f"Act {i // 5 + 1}"
        with st.expander(expander_name, expanded=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                time = st.number_input(f'{name} (minutes)', min_value=0, max_value=total_minutes, value=min(default_value, total_minutes))
            with col2:
                show = st.checkbox(f'Show {name}', value=True)
            plot_data[name] = (time, show)
    return plot_data

# Turning Pointsの入力
def turning_point_inputs(total_minutes):
    return {name: st.number_input(f'{name} (minutes)', min_value=0, max_value=total_minutes, value=min(default_value, total_minutes)) 
            for name, default_value in TURNING_POINTS}

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
                color = get_color_option(f'Select color for {group_name}', "Gray (Medium)")
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

# 色設定
def get_color_option(label, default_color):
    return st.selectbox(label, COLOR_OPTIONS.keys(), index=list(COLOR_OPTIONS.keys()).index(default_color))

# レイアウト設定
def layout_input():
    col1, col2 = st.columns([3, 1])
    with col1:
        title = st.text_input("Title", "Three-Act Structure Visualization", key="unique_title")
    with col2:
        total_minutes = st.number_input('Running time (minutes)', min_value=1, max_value=300, value=120)

    main_start_time = st.number_input('Main content start time (minutes)', min_value=0, max_value=total_minutes, value=min(1, total_minutes))
    end_credits_start = st.number_input('End credits start time (minutes)', min_value=0, max_value=total_minutes, value=min(115, total_minutes))

    act1_color = get_color_option("Select color for Act 1", "Gray (Light)")
    act2_color = get_color_option("Select color for Act 2", "Light Blue")
    act3_color = get_color_option("Select color for Act 3", "Gray (Dark)")

    include_credits = st.checkbox('Include Opening and End Credits in main runtime', value=True)

    return title, total_minutes, main_start_time, end_credits_start, include_credits, act1_color, act2_color, act3_color

# plot_three_act_structure 関数内で追加プロットポイントを描画
def plot_three_act_structure(title, total_minutes, main_start_time, end_credits_start, plot_data, turning_data, 
                             additional_groups, additional_lines, include_credits, 
                             act1_color_code, act2_color_code, act3_color_code):
    fig = go.Figure()
    radians = lambda time: calc_radians(time, plot_data["Opening Image"][0], total_minutes, end_credits_start, include_credits)

    fig.add_trace(create_act_arc('Act 1', radians, plot_data["Opening Image"][0], turning_data["Turning Point 1"], act1_color_code))
    fig.add_trace(create_act_arc('Act 2', radians, turning_data["Turning Point 1"], turning_data["Turning Point 2"], act2_color_code))
    fig.add_trace(create_act_arc('Act 3', radians, turning_data["Turning Point 2"], end_credits_start, act3_color_code))

    for name, (time, show) in plot_data.items():
        if show:
            fig.add_trace(create_plot_point(name, radians(time), 'blue'))

    for name, time in turning_data.items():
        fig.add_trace(create_plot_point(name, radians(time), 'red'))

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

    # グラフのレイアウト設定
    fig.update_layout(
        title=title,
        polar=dict(
            angularaxis=dict(visible=False, direction="clockwise"),
            radialaxis=dict(visible=False)
        )
    )

    # グラフの表示
    st.plotly_chart(fig)

# Actセクションの扇形を生成するヘルパー関数
def create_act_arc(act_name, radians_func, start_time, end_time, color_code):
    theta_vals = list(np.linspace(radians_func(start_time), radians_func(end_time), num=50))[::-1]
    return go.Scatterpolar(
        r=[0] + [1] * len(theta_vals) + [0],
        theta=[radians_func(start_time)] + theta_vals + [theta_vals[-1]],
        fill='toself',
        name=act_name,
        line=dict(color=color_code, width=1),
        opacity=1
    )

# プロットポイントの描画設定
def create_plot_point(name, angle, color):
    return go.Scatterpolar(
        r=[1],
        theta=[angle],
        mode='markers+text',
        marker=dict(size=10, color=color),
        text=[name],
        textposition='top center',
        name=name
    )

# main関数に組み込む
def main():
    # layout_input からの返り値に合わせて変数を受け取る
    title, total_minutes, main_start_time, end_credits_start, include_credits, act1_color, act2_color, act3_color = layout_input()

    # plot_data と turning_data を個別に取得
    plot_data = plot_point_inputs(total_minutes)
    turning_data = turning_point_inputs(total_minutes)

    # 追加プロットポイントグループを取得
    additional_groups, additional_lines = additional_plot_point_groups()

    # 三幕構成の描画
    plot_three_act_structure(
        title, total_minutes, main_start_time, end_credits_start, plot_data, turning_data,
        additional_groups, additional_lines, include_credits, 
        COLOR_OPTIONS[act1_color], COLOR_OPTIONS[act2_color], COLOR_OPTIONS[act3_color]
    )

if __name__ == "__main__":
    main()
