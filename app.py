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
