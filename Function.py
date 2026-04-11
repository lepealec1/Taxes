import streamlit as st
yes_no=['Yes','No']
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

import streamlit as st

def ask_question(
    answers,
    key_name,
    question,
    input_type="text",
    options=None,
    columns=True,
    help_text=None,
    allow_none=False,
    multiple=False
):
    """
    Generic helper to ask a question in Streamlit and store in `answers` dict.
    
    Parameters:
        answers (dict): dictionary to store results
        key_name (str): key to store the answer
        question (str): question text
        input_type (str): "text", "number", "radio", "checkbox", "date"
        options (list): list of options (for radio/checkbox)
        columns (bool): if radio/checkbox, display horizontally
        help_text (str): optional help text
        allow_none (bool): allow None selection for radio
        multiple (bool): allow multiple entries for text/number (line-separated)
    """
    
    if input_type in ["text", "text_input"]:
        if multiple:
            # Use a text area for multiple entries (one per line)
            values = st.text_area(f"{question} (one per line)", key=key_name, help=help_text)
            answers[key_name] = [v.strip() for v in values.split("\n") if v.strip()]
        else:
            answers[key_name] = st.text_input(question, key=key_name, help=help_text)

    elif input_type == "number":
        if multiple:
            # Text area for multiple numbers (one per line)
            values = st.text_area(f"{question} (one per line)", key=key_name, help=help_text)
            cleaned = []
            for v in values.split("\n"):
                v = v.strip()
                if v:
                    try:
                        cleaned.append(float(v))
                    except ValueError:
                        st.warning(f"Invalid number skipped: {v}")
            answers[key_name] = cleaned
        else:
            answers[key_name] = st.number_input(question, key=key_name, min_value=0.0, step=1.0, format="%.2f", help=help_text)

    elif input_type == "radio":
        # Ensure session state exists
        if key_name not in st.session_state:
            st.session_state[key_name] = None  # start unselected

        radio_options = options
        if allow_none:
            radio_options = ["None"] + (options or [])

        selected = st.radio(
            question,
            options=radio_options,
            index=0 if not allow_none else 0,  # start unselected if allow_none
            key=key_name,
            help=help_text,
            horizontal=columns
        )
        answers[key_name] = None if selected == "None" else selected

    elif input_type == "checkbox":
        st.write(question)
        if help_text:
            st.caption(help_text)

        selected = []

        if columns:
            cols_list = st.columns(len(options))
        else:
            cols_list = [st] * len(options)  # ✅ repeat st for each option

        for col, option in zip(cols_list, options):
            if col.checkbox(option, key=f"{key_name}_{option}"):
                selected.append(option)

        answers[key_name] = selected

    elif input_type == "date":
        answers[key_name] = st.date_input(question, key=key_name, help=help_text)

    return answers[key_name]














def ask_question(
    answers: dict,
    key_name: str,
    question: str,
    input_type: str = "text",
    options: list | None = None,
    columns: bool = True,
    help_text: str | None = None,
    allow_none: bool = False,
    multiple: bool = False,
    step: float | int = 1,
    min_value: float | int | None = 0,
    max_value: float | int | None = None,
    format_str: str | None = None,
):
    """
    Robust Streamlit input helper with safe typing + session handling.
    """

    import streamlit as st

    def _reset_if_type_mismatch(expected_types):
        """Clear session state if stored value has wrong type."""
        if key_name in st.session_state:
            if not isinstance(st.session_state[key_name], expected_types):
                del st.session_state[key_name]

    value = None

    # ---------- TEXT ----------
    if input_type in ("text", "text_input"):
        _reset_if_type_mismatch((str,))

        if multiple:
            raw = st.text_area(
                f"{question} (one per line)",
                key=key_name,
                help=help_text
            )
            value = [v.strip() for v in raw.split("\n") if v.strip()]
        else:
            value = st.text_input(
                question,
                key=key_name,
                help=help_text
            )

    # ---------- NUMBER ----------
    elif input_type == "number":
        if multiple:
            _reset_if_type_mismatch((str,))

            raw = st.text_area(
                f"{question} (one per line)",
                key=key_name,
                help=help_text
            )

            cleaned = []
            for v in raw.split("\n"):
                v = v.strip()
                if not v:
                    continue
                try:
                    cleaned.append(float(v))
                except ValueError:
                    st.warning(f"Invalid number skipped: {v}")

            value = cleaned

        else:
            # 🔥 AUTO MODE: detect int vs float
            is_int_mode = all(
                isinstance(x, int) or x is None
                for x in (step, min_value, max_value)
            )

            if is_int_mode:
                _reset_if_type_mismatch((int,))

                min_v = int(min_value) if min_value is not None else 0
                max_v = int(max_value) if max_value is not None else None
                step_v = int(step)

                value = st.number_input(
                    question,
                    key=key_name,
                    min_value=min_v,
                    max_value=max_v,
                    step=step_v,
                    value=min_v,
                    format=format_str or "%d",
                    help=help_text
                )

            else:
                _reset_if_type_mismatch((int, float))

                min_v = float(min_value) if min_value is not None else 0.0
                max_v = float(max_value) if max_value is not None else None
                step_v = float(step)

                value = st.number_input(
                    question,
                    key=key_name,
                    min_value=min_v,
                    max_value=max_v,
                    step=step_v,
                    value=min_v,
                    format=format_str or "%.2f",
                    help=help_text
                )

    # ---------- RADIO ----------
    elif input_type == "radio":
        if not options:
            raise ValueError("Radio input requires 'options'")

        _reset_if_type_mismatch((str, type(None)))

        opts = options.copy()

        if allow_none:
            opts = ["— Select —"] + opts

        selected = st.radio(
            question,
            options=opts,
            index=0,
            key=key_name,
            help=help_text,
            horizontal=columns
        )

        value = None if allow_none and selected == "— Select —" else selected

    # ---------- CHECKBOX ----------
    elif input_type == "checkbox":
        if not options:
            raise ValueError("Checkbox input requires 'options'")

        st.write(question)
        if help_text:
            st.caption(help_text)

        selected = []

        layout = st.columns(len(options)) if columns else [st] * len(options)

        for col, option in zip(layout, options):
            if col.checkbox(option, key=f"{key_name}_{option}"):
                selected.append(option)

        value = selected

    # ---------- DATE ----------
    elif input_type == "date":
        _reset_if_type_mismatch((object,))  # date objects

        value = st.date_input(
            question,
            key=key_name,
            help=help_text
        )

    # ---------- INVALID ----------
    else:
        raise ValueError(f"Unsupported input_type: {input_type}")

    answers[key_name] = value
    return value