    ["🎨 Design & interlacement", "🧶 Fabric simulation", "📊 Technical analysis", "⬇️ Export design"]
)

with tab_design:
    st.subheader(design_name)
    st.caption(f"{weave_label}  •  Designed by {designer}")
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("**Interlacement plan**")
        fig = draw_interlacement(mat, warp_color, weft_color)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with right:
        st.markdown("**How to read this design**")
        st.markdown(f"""
        - **W (warp up):** warp yarn passes over the weft yarn.
        - **F (weft up):** weft yarn passes over the warp yarn.
        - **Columns:** warp ends in one repeat.
        - **Rows:** weft picks in one repeat.
        - **Repeat:** {mat.shape[1]} ends × {mat.shape[0]} picks.
        """)
        st.info("This draft uses a binary interlacement convention: 1 = warp over, 0 = weft over.")
        st.markdown("**Construction inputs**")
        st.write(f"Warp: {warp_count}  |  {epi} EPI  |  {warp_color}")
        st.write(f"Weft: {weft_count}  |  {ppi} PPI  |  {weft_color}")

with tab_visual:
    st.subheader("Woven fabric appearance")
    st.caption("A conceptual colour-and-weave rendering, not a photorealistic or production-accurate fabric prediction.")
    # Repeat selected yarn colours across the design.
    warp_palette = [warp_color]
    weft_palette = [weft_color]
    fabric_fig = draw_fabric(mat, warp_palette, weft_palette, epi, ppi)
    st.pyplot(fabric_fig, use_container_width=True)
    plt.close(fabric_fig)

with tab_analysis:
    st.subheader("Weave structure analysis")
    metrics = pattern_metrics(mat)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Warp ends / repeat", metrics["repeat_warp"])
    m2.metric("Weft picks / repeat", metrics["repeat_weft"])
    m3.metric("Max warp float", metrics["warp_float_max"])
    m4.metric("Max weft float", metrics["weft_float_max"])
    st.markdown("**Interlacement statistics**")
    st.write(f"Warp-over interlacements: **{int(mat.sum())}** out of **{mat.size}** cells ({metrics['warp_up_percent']}%).")
    st.write(f"Average warp float per end: **{metrics['warp_float_mean']}** picks.")
    st.write(f"Average weft float per pick: **{metrics['weft_float_mean']}** ends.")
    st.markdown("**Construction calculations**")
    c1, c2 = st.columns(2)
    c1.metric("Ends per cm (approx.)", f"{epi / 2.54:.1f}")
    c2.metric("Picks per cm (approx.)", f"{ppi / 2.54:.1f}")
    st.markdown("**Interpretation")
    if weave_type in ["Plain 1/1", "Basket 2/2"]:
        st.write("Plain-derived structures generally have frequent interlacements. This often improves fabric stability but can increase crimp and reduce yarn mobility.")
    elif weave_type == "Twill":
        st.write("Twill structures form diagonal lines. Longer floats than plain weave can improve drape and surface smoothness, depending on yarn and construction.")
    elif weave_type == "Satin":
        st.write("Satin structures distribute interlacements to create longer floats and a smoother face. Float length and snagging risk should be considered.")
    else:
        st.write("For a custom weave, inspect the maximum floats and interlacement distribution. Very long floats may affect snagging and abrasion performance.")
    st.warning("These are structural observations only. Actual performance depends on fibre, yarn properties, twist, sett, finishing and testing.")

with tab_export:
    st.subheader("Export your woven design")
    st.write("Create a technical record for your project exhibition or lab submission.")
    summary = {
        "Design name": design_name,
        "Designer": designer,
        "Weave structure": weave_label,
        "Repeat (warp ends)": mat.shape[1],
        "Repeat (weft picks)": mat.shape[0],
        "EPI": epi,
        "PPI": ppi,
        "Warp yarn count": warp_count,
        "Weft yarn count": weft_count,
        "Warp colour": warp_color,
        "Weft colour": weft_color,
        "Warp-over cells": int(mat.sum()),
        "Weft-over cells": int(mat.size - mat.sum()),
        "Maximum warp float": metrics["warp_float_max"],
        "Maximum weft float": metrics["weft_float_max"],
        "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.dataframe(pd.DataFrame(summary.items(), columns=["Parameter", "Value"]),
                 use_container_width=True, hide_index=True)
    csv_data = pd.DataFrame(summary.items(), columns=["Parameter", "Value"]).to_csv(index=False).encode("utf-8")
    draft_csv = pd.DataFrame(mat, index=[f"Pick {i+1}" for i in range(mat.shape[0])],
                             columns=[f"End {i+1}" for i in range(mat.shape[1])]).to_csv().encode("utf-8")
    export_fig = draw_interlacement(mat, warp_color, weft_color, f"{design_name} — {weave_label}")
    png_data = fig_to_png(export_fig)
    plt.close(export_fig)
    b1, b2, b3 = st.columns(3)
    b1.download_button("⬇️ Download technical sheet (CSV)", csv_data,
                       file_name="weave_technical_sheet.csv", mime="text/csv",
                       use_container_width=True)
    b2.download_button("⬇️ Download weave matrix (CSV)", draft_csv,
                       file_name="weave_interlacement_matrix.csv", mime="text/csv",
                       use_container_width=True)
    b3.download_button("⬇️ Download weave diagram (PNG)", png_data,
                       file_name="weave_interlacement.png", mime="image/png",
                       use_container_width=True)

st.divider()
st.markdown(
    "<div style='text-align:center;color:#667085;font-size:.82rem'>"
    "Fabric Weave Studio | Textile Engineering Learning Project | "
    "Educational simulation — validate designs before production</div>",
    unsafe_allow_html=True,
)
