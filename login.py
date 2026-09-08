import streamlit as st


# =========================================================
# GET LOGIN CREDENTIALS
# =========================================================

def get_credentials():
    """
    Reads username and password from .streamlit/secrets.toml

    Supported formats:

    USERNAME = "admin"
    PASSWORD = "password"

    OR

    [auth]
    username = "admin"
    password = "password"
    """

    try:

        # -----------------------------------------------
        # FORMAT 1:
        #
        # [auth]
        # username = "admin"
        # password = "password"
        # -----------------------------------------------

        if "auth" in st.secrets:

            username = str(
                st.secrets["auth"]["username"]
            )

            password = str(
                st.secrets["auth"]["password"]
            )

            return username, password

        # -----------------------------------------------
        # FORMAT 2:
        #
        # USERNAME = "admin"
        # PASSWORD = "password"
        # -----------------------------------------------

        username = str(
            st.secrets["USERNAME"]
        )

        password = str(
            st.secrets["PASSWORD"]
        )

        return username, password

    except Exception:

        return None, None


# =========================================================
# LOGIN
# =========================================================

def check_login():
    """
    Returns True when user is logged in.
    Otherwise displays login form and returns False.
    """

    # Already logged in
    if st.session_state.get(
        "logged_in",
        False
    ):

        return True

    # -----------------------------------------------
    # LOGIN PAGE DESIGN
    # -----------------------------------------------

    st.markdown(
        """
        <style>

        .login-title {
            text-align: center;
            font-size: 34px;
            font-weight: 700;
            color: #1F4E79;
            margin-top: 30px;
        }

        .login-subtitle {
            text-align: center;
            color: #666666;
            font-size: 16px;
            margin-bottom: 25px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='login-title'>👨‍🏫 Trainer Profile Generator</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='login-subtitle'>Training Operations Management System</div>",
        unsafe_allow_html=True
    )

    # Center login form
    left, center, right = st.columns(
        [1, 1.4, 1]
    )

    with center:

        st.markdown(
            "### 🔐 Login"
        )

        with st.form(
            "trainer_profile_login"
        ):

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            login_button = (
                st.form_submit_button(
                    "Login",
                    type="primary",
                    use_container_width=True
                )
            )

        if login_button:

            correct_username, correct_password = (
                get_credentials()
            )

            # Secrets not configured
            if (
                correct_username is None
                or correct_password is None
            ):

                st.error(
                    "Login credentials are not configured. "
                    "Please configure .streamlit/secrets.toml."
                )

                return False

            # Empty fields
            if not username.strip():

                st.warning(
                    "Please enter username."
                )

                return False

            if not password:

                st.warning(
                    "Please enter password."
                )

                return False

            # Correct login
            if (
                username == correct_username
                and password == correct_password
            ):

                st.session_state.logged_in = True

                st.session_state.username = (
                    username
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

    return False


# =========================================================
# LOGOUT
# =========================================================

def show_logout():

    if not st.session_state.get(
        "logged_in",
        False
    ):

        return

    st.sidebar.divider()

    username = st.session_state.get(
        "username",
        "User"
    )

    st.sidebar.markdown(
        f"👤 **Logged in as:** {username}"
    )

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True,
        key="global_logout_button"
    ):

        # Remove login information
        st.session_state.pop(
            "logged_in",
            None
        )

        st.session_state.pop(
            "username",
            None
        )

        st.rerun()


# =========================================================
# COMMON PAGE AUTHENTICATION
# =========================================================

def require_login():
    """
    Call this after st.set_page_config() on every page.

    Example:

        st.set_page_config(...)
        require_login()
    """

    if not check_login():

        st.stop()

    show_logout()