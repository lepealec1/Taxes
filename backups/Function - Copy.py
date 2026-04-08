import streamlit as st

def ask_question(answers, key_name, question, input_type="text", options=None, columns=True, help_text=None, allow_none=False):
    if input_type in ["text", "text_input"]:
        answers[key_name] = st.text_input(question, key=key_name, help=help_text)

    elif input_type == "radio":
        # Use session state to allow no initial selection
        if key_name not in st.session_state:
            st.session_state[key_name] = None  # start unselected

        selected = st.radio(
            question,
            options,
            index=0 if not allow_none else None,  # None prevents auto-selection
            key=key_name,
            help=help_text
        )
        answers[key_name] = selected

    elif input_type == "checkbox":
        st.write(question)
        if help_text:
            st.caption(help_text)

        selected = []
        cols_list = st.columns(len(options)) if columns else [st]
        for col, option in zip(cols_list, options):
            if col.checkbox(option, key=f"{key_name}_{option}"):
                selected.append(option)
        answers[key_name] = selected

    return answers[key_name]