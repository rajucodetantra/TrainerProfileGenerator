import hmac
import os

import streamlit as st


# =========================================================
# SESSION STATE KEYS
# =========================================================

AUTH_KEY = "user_authenticated"
USERNAME_KEY = "authenticated_username"


# =========================================================
# INITIALIZE SESSION
# =========================================================

def _initialize_session():
    """
    Initialize authentication session variables.
    """

    if AUTH_KEY not in st.session_state:
        st.session_state[AUTH_KEY] = False

    if USERNAME_KEY not in st.session_state:
        st.session_state[USERNAME_KEY] = None


# =========================================================
# GET LOGIN CREDENTIALS
# =========================================================

def _get_login_credentials():
    """
    Read login credentials from Streamlit Secrets.

    Supported secrets.toml formats:

    Format 1:

        USERNAME = "admin"
        PASSWORD = "password"

    Format 2:

        [auth]
        username = "admin"
        password = "password"

    Environment variable fallback:

        APP_USERNAME
        APP_PASSWORD
    """

    username = None
    password = None

    # =====================================================
    # STREAMLIT SECRETS
    # =====================================================

    try:

        # -------------------------------------------------
        # FORMAT 1
        #
        # [auth]
        # username = "admin"
        # password = "password"
        # -------------------------------------------------

        if "auth" in st.secrets:

            auth = st.secrets["auth"]

            if "username" in auth:
                username = auth["username"]

            if "password" in auth:
                password = auth["password"]


        # -------------------------------------------------
        # FORMAT 2
        #
        # USERNAME = "admin"
        # PASSWORD = "password"
        # -------------------------------------------------

        if not username and "USERNAME" in st.secrets:
            username = st.secrets["USERNAME"]

        if not password and "PASSWORD" in st.secrets:
            password = st.secrets["PASSWORD"]

    except Exception:
        pass


    # =====================================================
    # ENVIRONMENT VARIABLE FALLBACK
    # =====================================================

    if not username:
        username = os.getenv("APP_USERNAME")

    if not password:
        password = os.getenv("APP_PASSWORD")


    return username, password


# =========================================================
# CHECK LOGIN STATUS
# =========================================================

def is_logged_in():
    """
    Return True when the current Streamlit session
    is authenticated.
    """

    _initialize_session()

    return bool(
        st.session_state.get(
            AUTH_KEY,
            False
        )
    )


# =========================================================
# LOGIN PAGE CSS
# =========================================================

def _login_styles():
    """
    CSS used only on the login screen.
    """

    st.markdown(
        """
        <style>

        /* =====================================================
           HIDE SIDEBAR BEFORE LOGIN
        ===================================================== */

        [data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }


        /* =====================================================
           LOGIN PAGE BACKGROUND
        ===================================================== */

        [data-testid="stAppViewContainer"] {
            background-color: #F5F7FA !important;
        }

        [data-testid="stMain"] {
            background-color: #F5F7FA !important;
        }


        /* =====================================================
           MAIN PAGE SPACING
        ===================================================== */

        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
        }


        /* =====================================================
           LOGIN FORM
        ===================================================== */

        [data-testid="stForm"] {

            background-color: #FFFFFF !important;

            border:
                1px solid #D8E0E8 !important;

            border-top:
                5px solid #F28C18 !important;

            border-radius:
                12px !important;

            padding:
                28px 30px 26px 30px !important;

            box-shadow:
                0 8px 26px
                rgba(15, 23, 42, 0.08) !important;
        }


        /* =====================================================
           FORM LABELS
        ===================================================== */

        [data-testid="stForm"]
        [data-testid="stWidgetLabel"] p {

            color: #243447 !important;

            -webkit-text-fill-color:
                #243447 !important;

            font-size:
                14px !important;

            font-weight:
                600 !important;
        }


        /* =====================================================
           USERNAME / PASSWORD INPUTS
        ===================================================== */

        [data-testid="stForm"]
        [data-testid="stTextInput"] input {

            background-color:
                #FFFFFF !important;

            color:
                #243447 !important;

            -webkit-text-fill-color:
                #243447 !important;

            border-radius:
                7px !important;

            min-height:
                42px !important;
        }


        /* Placeholder text */

        [data-testid="stForm"]
        [data-testid="stTextInput"]
        input::placeholder {

            color:
                #94A3B8 !important;

            -webkit-text-fill-color:
                #94A3B8 !important;

            opacity:
                1 !important;
        }


        /* =====================================================
           LOGIN BUTTON - ORANGE
        ===================================================== */

        [data-testid="stFormSubmitButton"] button {

            background-color:
                #F28C18 !important;

            color:
                #FFFFFF !important;

            border:
                1px solid #F28C18 !important;

            border-radius:
                7px !important;

            width:
                100% !important;

            min-height:
                44px !important;

            font-size:
                15px !important;

            font-weight:
                650 !important;

            margin-top:
                8px !important;

            box-shadow:
                0 2px 5px
                rgba(242, 140, 24, 0.20) !important;
        }


        [data-testid="stFormSubmitButton"]
        button * {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        /* =====================================================
           LOGIN BUTTON HOVER
        ===================================================== */

        [data-testid="stFormSubmitButton"]
        button:hover {

            background-color:
                #D97706 !important;

            border-color:
                #D97706 !important;

            color:
                #FFFFFF !important;
        }


        [data-testid="stFormSubmitButton"]
        button:hover * {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        /* =====================================================
           LOGIN ALERTS
        ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 8px !important;
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 800px) {

            .block-container {

                padding-left:
                    1rem !important;

                padding-right:
                    1rem !important;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LOGIN SCREEN
# =========================================================

def show_login():
    """
    Display the application login screen.
    """

    _initialize_session()

    username_configured, password_configured = (
        _get_login_credentials()
    )


    # =====================================================
    # VERIFY CREDENTIAL CONFIGURATION
    # =====================================================

    if (
        not username_configured
        or not password_configured
    ):

        st.error(
            "Login credentials are not configured."
        )

        st.info(
            "Add USERNAME and PASSWORD to "
            ".streamlit/secrets.toml or "
            "Streamlit Cloud Secrets."
        )

        st.stop()


    # =====================================================
    # APPLY LOGIN PAGE STYLE
    # =====================================================

    _login_styles()


    # =====================================================
    # CENTER LOGIN FORM
    # =====================================================

    left_column, login_column, right_column = (
        st.columns(
            [1.3, 1, 1.3]
        )
    )


    with login_column:

        # =================================================
        # APPLICATION TITLE
        # =================================================

        st.html(
            """
            <div style="
                text-align: center;
                margin-top: 55px;
                margin-bottom: 24px;
            ">

                <div style="
                    width: 58px;
                    height: 5px;
                    background-color: #F28C18;
                    border-radius: 5px;
                    margin: 0 auto 17px auto;
                ">
                </div>

                <div style="
                    color: #172B4D;
                    font-size: 30px;
                    font-weight: 700;
                    line-height: 1.25;
                ">
                    Trainer Profile Generator
                </div>

            </div>
            """
        )


        # =================================================
        # LOGIN FORM
        # =================================================

        with st.form(
            "global_login_form",
            clear_on_submit=False
        ):

            entered_username = st.text_input(
                "Username",
                placeholder="Enter username"
            )


            entered_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )


            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )


        # =================================================
        # LOGIN VALIDATION
        # =================================================

        if submitted:

            entered_username = (
                entered_username.strip()
            )


            # ---------------------------------------------
            # SECURE USERNAME COMPARISON
            # ---------------------------------------------

            username_match = (
                hmac.compare_digest(
                    str(entered_username),
                    str(username_configured)
                )
            )


            # ---------------------------------------------
            # SECURE PASSWORD COMPARISON
            # ---------------------------------------------

            password_match = (
                hmac.compare_digest(
                    str(entered_password),
                    str(password_configured)
                )
            )


            # ---------------------------------------------
            # LOGIN SUCCESS
            # ---------------------------------------------

            if (
                username_match
                and password_match
            ):

                st.session_state[
                    AUTH_KEY
                ] = True


                st.session_state[
                    USERNAME_KEY
                ] = entered_username


                st.rerun()


            # ---------------------------------------------
            # LOGIN FAILURE
            # ---------------------------------------------

            else:

                st.error(
                    "Invalid username or password."
                )


# =========================================================
# LOGOUT
# =========================================================

def show_logout():
    """
    Display the Logout button in the sidebar.
    """

    if not is_logged_in():
        return


    username = st.session_state.get(
        USERNAME_KEY,
        ""
    )


    with st.sidebar:

        st.divider()


        # =================================================
        # CURRENT USER
        # =================================================

        if username:

            st.caption(
                f"Signed in as: {username}"
            )


        # =================================================
        # LOGOUT BUTTON
        # =================================================

        logout_clicked = st.button(
            "Logout",
            key="global_logout_button",
            use_container_width=True
        )


    # =====================================================
    # LOGOUT ACTION
    # =====================================================

    if logout_clicked:

        st.session_state.clear()

        st.rerun()


# =========================================================
# REQUIRE LOGIN
# =========================================================

def require_login(
    show_logout_button=True
):
    """
    Protect application pages.

    Home.py:

        require_login(
            show_logout_button=False
        )

    Child pages:

        require_login()

    Home checks authentication without creating the
    Logout button.

    The selected child page checks authentication again
    and creates the single Logout button.
    """

    _initialize_session()


    # =====================================================
    # NOT LOGGED IN
    # =====================================================

    if not is_logged_in():

        show_login()

        st.stop()


    # =====================================================
    # LOGGED IN
    # =====================================================

    if show_logout_button:

        show_logout()