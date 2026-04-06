# w2.py
def run_w2():
    import streamlit as st
    # Allow 0 W-2s
    num_w2s = st.number_input("How many W-2s?", min_value=0, step=1)

    w2_list = []

    if num_w2s > 0:
        tabs = st.tabs([f"W-2 {i+1}" for i in range(num_w2s)])

        for i, tab in enumerate(tabs):
            with tab:
                st.header(f"W-2 {i+1} Information")
                wages = st.number_input(
                    f"Wages (Box 1) - W-2 {i+1} ($)", min_value=0, step=100, value=0, key=f"wages_{i}"
                )
                fed_withheld = st.number_input(
                    f"Federal Tax Withheld (Box 2) - W-2 {i+1} ($)", min_value=0, step=10, value=0, key=f"fed_{i}"
                )
                state_wages = st.number_input(
                    f"State Wages (Box 16) - W-2 {i+1} ($)", min_value=0, step=100, value=0, key=f"state_wages_{i}"
                )
                state_withheld = st.number_input(
                    f"State Tax Withheld (Box 17) - W-2 {i+1} ($)", min_value=0, step=10, value=0, key=f"state_withheld_{i}"
                )

                w2_list.append({
                    "wages": wages,
                    "fed_withheld": fed_withheld,
                    "state_wages": state_wages,
                    "state_withheld": state_withheld
                })

    if st.button("Calculate Totals"):
        if w2_list:
            total_wages = sum(item["wages"] for item in w2_list)
            total_fed_withheld = sum(item["fed_withheld"] for item in w2_list)
            total_state_wages = sum(item["state_wages"] for item in w2_list)
            total_state_withheld = sum(item["state_withheld"] for item in w2_list)

            st.write("### Totals Across All W-2s")
            st.write(f"Total Wages (Box 1): ${total_wages:,}")
            st.write(f"Total Federal Tax Withheld (Box 2): ${total_fed_withheld:,}")
            st.write(f"Total State Wages (Box 16): ${total_state_wages:,}")
            st.write(f"Total State Tax Withheld (Box 17): ${total_state_withheld:,}")
        else:
            st.write("No W-2s entered.")