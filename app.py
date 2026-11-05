import io
import math
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.colors import to_rgb
from matplotlib.patches import Rectangle

# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Fabric Weave Studio",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Weave-generation functions
# Convention: 1 = warp over weft; 0 = weft over warp.
# Rows = picks; columns = warp ends.
# ---------------------------------------------------------------------
def plain_weave():
    return np.array([[1, 0], [0, 1]], dtype=int)


def basket_weave():
    return np.array(
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
        ],
        dtype=int,
    )


def twill_weave(size, warp_over, step, direction):
    sign = 1 if direction == "Right" else -1
    matrix = np.zeros((size, size), dtype=int)

    for row in range(size):
        for col in range(size):
            position = (col - sign * row * step) % size
            matrix[row, col] = 1 if position < warp_over else 0

    return matrix


def satin_weave(size, step, face):
    if math.gcd(size, step) != 1:
        raise ValueError("The satin step must be relatively prime to the repeat size.")

    matrix = np.zeros((size, size), dtype=int)

    for row in range(size):
        col = (row * step) % size
        matrix[row, col] = 1

    if face == "Weft-faced":
        matrix = 1 - matrix

    return matrix


def get_metrics(matrix):
    warp_floats = matrix.sum(axis=0)
    weft_floats = (1 - matrix).sum(axis=1)

    return {
        "warp_repeat": matrix.shape[1],
        "weft_repeat": matrix.shape[0],
        "warp_float_max": int(warp_floats.max()),
        "weft_float_max": int(weft_floats.max()),
        "warp_float_average": round(float(warp_floats.mean()), 2),
        "weft_float_average": round(float(weft_floats.mean()), 2),
        "warp_over_percent": round(float(matrix.mean() * 100), 1),
        "warp_over_cells": int(matrix.sum()),
        "weft_over_cells": int(matrix.size - matrix.sum()),
    }


def make_draft_figure(matrix, warp_colour, weft_colour, title="Weave draft"):
    rows, cols = matrix.shape
    fig, ax = plt.subplots(figsize=(max(4, cols * 0.55), max(3.5, rows * 0.55)))

    for row in range(rows):
        for col in range(cols):
            is_warp_over = matrix[row, col] == 1
            cell_colour = warp_colour if is_warp_over else weft_colour
            text_colour = "white" if np.mean(to_rgb(cell_colour)) < 0.48 else "#17202a"

            ax.add_patch(
                Rectangle(
                    (col, row),
                    1,
                    1,
                    facecolor=cell_colour,
                    edgecolor="#333333",
                    linewidth=0.8,
                )
            )
            ax.text(
                col + 0.5,
                row + 0.5,
                "W" if is_warp_over else "F",
                ha="center",
                va="center",
                color=text_colour,
                fontsize=9,
                fontweight="bold",
            )

    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(cols) + 0.5)
    ax.set_yticks(np.arange(rows) + 0.5)
    ax.set_xticklabels([str(i + 1) for i in range(cols)])
    ax.set_yticklabels([str(i + 1) for i in range(rows)])
    ax.set_xlabel("Warp ends")
    ax.set_ylabel("Weft picks")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.set_xticks(np.arange(cols + 1), minor=True)
    ax.set_yticks(np.arange(rows + 1), minor=True)
    ax.grid(which="minor", color="#333333", linewidth=0.45)
    ax.tick_params(which="both", length=0)
    fig.tight_layout()
    return fig


def make_fabric_figure(matrix, warp_colour, weft_colour, epi, ppi):
    rows, cols = matrix.shape
    fig, ax = plt.subplots(figsize=(10, 5))

    for row in range(rows):
        for col in range(cols):
            if matrix[row, col] == 1:
                ax.add_patch(
                    Rectangle((col, row), 1, 1, facecolor=warp_colour, edgecolor="none")
                )
                ax.add_patch(
                    Rectangle(
                        (col, row + 0.34),
                        1,
                        0.32,
                        facecolor=warp_colour,
                        edgecolor="none",
                    )
                )
            else:
                ax.add_patch(
                    Rectangle((col, row), 1, 1, facecolor=weft_colour, edgecolor="none")
                )
                ax.add_patch(
                    Rectangle(
                        (col + 0.34, row),
                        0.32,
                        1,
                        facecolor=weft_colour,
                        edgecolor="none",
                    )
                )

    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"Conceptual fabric appearance | {epi} EPI × {ppi} PPI",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    fig.tight_layout()
    return fig


def figure_to_png(figure):
    output = io.BytesIO()
    figure.savefig(
        output,
        format="png",
        dpi=220,
        bbox_inches="tight",
        facecolor="white",
    )
    output.seek(0)
    return output.getvalue()


# ---------------------------------------------------------------------
# Application styling and header
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    .hero {
        background: linear-gradient(115deg, #102a43, #176b87, #38a3a5);
        color: white;
        padding: 1.5rem 1.8rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    .hero h1 {color: white; margin: 0; font-size: 2.15rem;}
    .hero p {color: #e4f4f5; margin: .45rem 0 0 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🧵 FABRIC WEAVE STUDIO</h1>
        <p>Interactive weaving design, interlacement simulation and fabric construction lab</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Sidebar: project details, weave selection and construction parameters
# ---------------------------------------------------------------------
st.sidebar.header("Design workspace")

design_name = st.sidebar.text_input("Design name", "My First Woven Fabric")
designer_name = st.sidebar.text_input("Designer / student name", "Textile Engineering Student")

st.sidebar.divider()
st.sidebar.subheader("Select weave structure")

weave_type = st.sidebar.selectbox(
    "Weave type",
    ["Plain 1/1", "Basket 2/2", "Twill", "Satin", "Custom weave"],
)

if weave_type == "Plain 1/1":
    matrix = plain_weave()
    weave_description = "Plain weave (1/1)"

elif weave_type == "Basket 2/2":
    matrix = basket_weave()
    weave_description = "Basket weave (2/2)"

elif weave_type == "Twill":
    repeat_size = st.sidebar.selectbox("Twill repeat size", [3, 4, 5, 6, 7, 8], index=1)
    warp_over = st.sidebar.slider(
        "Warp floats in each row",
        min_value=1,
        max_value=repeat_size - 1,
        value=min(2, repeat_size - 1),
    )
    twill_step = st.sidebar.selectbox("Twill step", [1, 2, 3], index=0)
    twill_direction = st.sidebar.radio("Twill direction", ["Right", "Left"], horizontal=True)

    matrix = twill_weave(repeat_size, warp_over, twill_step, twill_direction)
    weave_description = (
        f"{warp_over}/{repeat_size - warp_over} "
        f"{twill_direction.lower()}-hand twill"
    )

elif weave_type == "Satin":
    repeat_size = st.sidebar.selectbox("Satin repeat size", [5, 7, 8, 9, 11], index=0)
    valid_steps = [
        value for value in range(2, repeat_size - 1)
        if math.gcd(repeat_size, value) == 1
    ]
    satin_step = st.sidebar.selectbox("Satin step", valid_steps)
    satin_face = st.sidebar.radio("Satin face", ["Warp-faced", "Weft-faced"])

    matrix = satin_weave(repeat_size, satin_step, satin_face)
    weave_description = f"{repeat_size}-end {satin_face.lower()} satin, step {satin_step}"

else:
    custom_size = st.sidebar.selectbox(
        "Custom repeat size",
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
        index=2,
    )

    if (
        "custom_matrix_df" not in st.session_state
        or st.session_state.get("custom_size") != custom_size
    ):
        initial_matrix = np.fromfunction(
            lambda row, col: (row + col) % 2 == 0,
            (custom_size, custom_size),
            dtype=int,
        ).astype(int)

        st.session_state.custom_matrix_df = pd.DataFrame(initial_matrix)
        st.session_state.custom_size = custom_size

    st.sidebar.caption(
        "Edit each cell: 1 = warp over weft; 0 = weft over warp."
    )

    edited_matrix = st.data_editor(
        st.session_state.custom_matrix_df,
        use_container_width=True,
        hide_index=True,
        key=f"custom_weave_editor_{custom_size}",
        column_config={
            column: st.column_config.NumberColumn(
                f"End {column + 1}",
                min_value=0,
                max_value=1,
                step=1,
                format="%d",
            )
            for column in st.session_state.custom_matrix_df.columns
        },
    )

    st.session_state.custom_matrix_df = edited_matrix
    matrix = edited_matrix.to_numpy(dtype=int)
    matrix = np.where(matrix > 0, 1, 0)
    weave_description = f"Custom {custom_size} × {custom_size} weave"

# Fabric construction inputs
st.sidebar.divider()
st.sidebar.subheader("Fabric construction")

epi = st.sidebar.number_input("Ends per inch (EPI)", min_value=1, max_value=300, value=80)
ppi = st.sidebar.number_input("Picks per inch (PPI)", min_value=1, max_value=300, value=60)
warp_yarn_count = st.sidebar.text_input("Warp yarn count", "Ne 30/1")
weft_yarn_count = st.sidebar.text_input("Weft yarn count", "Ne 30/1")

st.sidebar.divider()
st.sidebar.subheader("Yarn colours")

warp_colour = st.sidebar.color_picker("Warp colour", "#176B87")
weft_colour = st.sidebar.color_picker("Weft colour", "#E9B44C")

# ---------------------------------------------------------------------
# Main application tabs
# ---------------------------------------------------------------------
tab_design, tab_simulation, tab_analysis, tab_export = st.tabs(
    [
        "🎨 Design & interlacement",
        "🧶 Fabric simulation",
        "📊 Technical analysis",
        "⬇️ Export design",
    ]
)

metrics = get_metrics(matrix)

# Tab 1: Weave draft
with tab_design:
    st.subheader(design_name)
    st.caption(f"{weave_description} | Designed by {designer_name}")

    draft_column, information_column = st.columns([1.2, 1])

    with draft_column:
        st.markdown("**Interlacement draft**")
        draft_figure = make_draft_figure(matrix, warp_colour, weft_colour)
        st.pyplot(draft_figure, use_container_width=True)
        plt.close(draft_figure)

    with information_column:
        st.markdown("**How to read the weave draft**")
        st.markdown(
            """
            - **W (warp up):** warp yarn passes over the weft yarn.
            - **F (weft up):** weft yarn passes over the warp yarn.
            - **Columns:** warp ends in one repeat.
            - **Rows:** weft picks in one repeat.
            """
        )

        st.info(
            f"Repeat: **{matrix.shape[1]} ends × {matrix.shape[0]} picks**"
        )

        st.markdown("**Construction details**")
        st.write(f"Warp yarn: {warp_yarn_count}")
        st.write(f"Weft yarn: {weft_yarn_count}")
        st.write(f"Warp density: {epi} EPI")
        st.write(f"Weft density: {ppi} PPI")

# Tab 2: Conceptual fabric simulation
with tab_simulation:
    st.subheader("Simulated woven fabric appearance")
    st.caption(
        "This is a conceptual colour rendering of the interlacement pattern, "
        "not a photorealistic or production-calibrated fabric simulation."
    )

    fabric_figure = make_fabric_figure(
        matrix, warp_colour, weft_colour, epi, ppi
    )
    st.pyplot(fabric_figure, use_container_width=True)
    plt.close(fabric_figure)

    st.markdown("**Yarn colour information**")
    colour_col_1, colour_col_2 = st.columns(2)

    with colour_col_1:
        st.markdown(f"Warp yarn: `{warp_colour}`")

    with colour_col_2:
        st.markdown(f"Weft yarn: `{weft_colour}`")

# Tab 3: Technical analysis
with tab_analysis:
    st.subheader("Weave structure analysis")

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Warp ends / repeat", metrics["warp_repeat"])
    metric_2.metric("Weft picks / repeat", metrics["weft_repeat"])
    metric_3.metric("Maximum warp float", metrics["warp_float_max"])
    metric_4.metric("Maximum weft float", metrics["weft_float_max"])

    st.markdown("**Interlacement statistics**")
    st.write(
        f"Warp-over intersections: **{metrics['warp_over_cells']}** "
        f"of {matrix.size} ({metrics['warp_over_percent']}%)."
    )
    st.write(
        f"Weft-over intersections: **{metrics['weft_over_cells']}** "
        f"of {matrix.size}."
    )
    st.write(
        f"Average warp float per end: **{metrics['warp_float_average']} picks**."
    )
    st.write(
        f"Average weft float per pick: **{metrics['weft_float_average']} ends**."
    )

    st.markdown("**Fabric construction conversion**")
    density_col_1, density_col_2 = st.columns(2)
    density_col_1.metric("Ends per cm (approx.)", f"{epi / 2.54:.2f}")
    density_col_2.metric("Picks per cm (approx.)", f"{ppi / 2.54:.2f}")

    st.markdown("**Textile interpretation**")

    if weave_type in ["Plain 1/1", "Basket 2/2"]:
        st.write(
            "Plain-derived structures have frequent interlacements. "
            "This generally gives a relatively stable structure, although "
            "actual properties also depend on yarn and fabric construction."
        )
    elif weave_type == "Twill":
        st.write(
            "Twill structures produce diagonal lines. Their float lengths "
            "and surface characteristics vary with the selected repeat and step."
        )
    elif weave_type == "Satin":
        st.write(
            "Satin structures distribute interlacements to create longer floats "
            "and a smoother face. Float length and snagging behaviour should be considered."
        )
    else:
        st.write(
            "Inspect the maximum floats and interlacement distribution of your "
            "custom design. Long floats can influence snagging and abrasion behaviour."
        )

    st.warning(
        "These calculations describe the weave matrix only. They do not predict "
        "GSM, yarn crimp, cover factor, tensile strength, drape, shrinkage or "
        "production performance."
    )

# Tab 4: Export
with tab_export:
    st.subheader("Export your design")
    st.write("Download a technical summary, the interlacement matrix and a weave diagram.")

    summary = {
        "Design name": design_name,
        "Designer": designer_name,
        "Weave structure": weave_description,
        "Warp repeat (ends)": matrix.shape[1],
        "Weft repeat (picks)": matrix.shape[0],
        "EPI": epi,
        "PPI": ppi,
        "Warp yarn count": warp_yarn_count,
        "Weft yarn count": weft_yarn_count,
        "Warp colour": warp_colour,
        "Weft colour": weft_colour,
        "Warp-over intersections": metrics["warp_over_cells"],
        "Weft-over intersections": metrics["weft_over_cells"],
        "Maximum warp float": metrics["warp_float_max"],
        "Maximum weft float": metrics["weft_float_max"],
        "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    summary_df = pd.DataFrame(
        list(summary.items()),
        columns=["Parameter", "Value"],
    )

    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    summary_csv = summary_df.to_csv(index=False).encode("utf-8")

    matrix_df = pd.DataFrame(
        matrix,
        index=[f"Pick {i + 1}" for i in range(matrix.shape[0])],
        columns=[f"End {i + 1}" for i in range(matrix.shape[1])],
    )
    matrix_csv = matrix_df.to_csv(index=True).encode("utf-8")

    export_figure = make_draft_figure(
        matrix,
        warp_colour,
        weft_colour,
        title=f"{design_name} - {weave_description}",
    )
    draft_png = figure_to_png(export_figure)
    plt.close(export_figure)

    download_col_1, download_col_2, download_col_3 = st.columns(3)

    with download_col_1:
        st.download_button(
            "Download technical sheet (CSV)",
            data=summary_csv,
            file_name="weave_technical_sheet.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with download_col_2:
        st.download_button(
            "Download weave matrix (CSV)",
            data=matrix_csv,
            file_name="weave_interlacement_matrix.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with download_col_3:
        st.download_button(
            "Download weave diagram (PNG)",
            data=draft_png,
            file_name="weave_interlacement_diagram.png",
            mime="image/png",
            use_container_width=True,
        )

# ---------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------
st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#667085; font-size:0.82rem;">
        Fabric Weave Studio | Textile Engineering Learning Project<br>
        Educational simulation — validate designs before production.
    </div>
    """,
    unsafe_allow_html=True,
)
