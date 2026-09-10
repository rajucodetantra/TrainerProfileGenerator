import streamlit as st


# =========================================================
# GLOBAL APPLICATION STYLES
# =========================================================

def apply_global_styles():

    st.markdown(
        """
        <style>

        /* =========================================================
           DESIGN VARIABLES
        ========================================================= */

        :root {

            /* Brand Accent */
            --ct-orange: #F28C18;
            --ct-orange-hover: #D97706;
            --ct-orange-soft: #FFF4E6;

            /* Sidebar */
            --ct-sidebar: #284B63;
            --ct-sidebar-hover: #355F7A;
            --ct-sidebar-active: #1F3A56;
            --ct-sidebar-border: #426B84;

            /* Main UI */
            --ct-navy: #172B4D;
            --ct-blue: #2F6FA3;
            --ct-blue-hover: #245A85;

            /* Text */
            --ct-text: #243447;
            --ct-text-secondary: #475569;
            --ct-muted: #667085;

            /* Backgrounds */
            --ct-page-bg: #F5F7FA;
            --ct-white: #FFFFFF;
            --ct-soft-bg: #F8FAFC;

            /* Borders */
            --ct-border: #D8E0E8;
            --ct-border-dark: #C7D0DA;

            /* Status */
            --ct-success-bg: #EAF7EF;
            --ct-success-text: #166534;

            --ct-info-bg: #EAF3FA;
            --ct-info-text: #1F4E79;

            --ct-warning-bg: #FFF7E6;
            --ct-warning-text: #92400E;

            --ct-error-bg: #FCECEC;
            --ct-error-text: #B42318;
        }


        /* =========================================================
           APPLICATION
        ========================================================= */

        html,
        body {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;
        }


        .stApp {
            background-color:
                var(--ct-page-bg) !important;

            color:
                var(--ct-text) !important;
        }


        [data-testid="stAppViewContainer"] {
            background-color:
                var(--ct-page-bg) !important;

            color:
                var(--ct-text) !important;
        }


        [data-testid="stMain"] {
            background-color:
                var(--ct-page-bg) !important;
        }


        .block-container {

            max-width:
                1500px !important;

            padding-top:
                1.6rem !important;

            padding-left:
                2.2rem !important;

            padding-right:
                2.2rem !important;

            padding-bottom:
                3rem !important;
        }


        /* =========================================================
           STREAMLIT TOP HEADER
        ========================================================= */

        [data-testid="stHeader"] {

            background-color:
                rgba(245, 247, 250, 0.96) !important;

            border-bottom:
                1px solid var(--ct-border) !important;
        }


        /* =========================================================
           HEADINGS
        ========================================================= */

        h1 {

            color:
                var(--ct-navy) !important;

            font-size:
                2rem !important;

            font-weight:
                750 !important;

            line-height:
                1.25 !important;

            letter-spacing:
                -0.35px !important;
        }


        h2 {

            color:
                #243B53 !important;

            font-weight:
                700 !important;

            line-height:
                1.3 !important;
        }


        h3 {

            color:
                #243B53 !important;

            font-weight:
                650 !important;
        }


        h4,
        h5,
        h6 {

            color:
                var(--ct-text) !important;
        }


        /* =========================================================
           NORMAL TEXT
        ========================================================= */

        [data-testid="stMarkdownContainer"] p {

            color:
                var(--ct-text) !important;
        }


        [data-testid="stMarkdownContainer"] li {

            color:
                var(--ct-text) !important;
        }


        [data-testid="stCaptionContainer"] {

            color:
                var(--ct-muted) !important;
        }


        /* =========================================================
           SIDEBAR
        ========================================================= */

        [data-testid="stSidebar"] {

            background-color:
                var(--ct-sidebar) !important;

            border-right:
                1px solid
                var(--ct-sidebar-border) !important;
        }


        [data-testid="stSidebar"] > div {

            background-color:
                var(--ct-sidebar) !important;
        }


        [data-testid="stSidebarContent"] {

            background-color:
                var(--ct-sidebar) !important;
        }


        /* =========================================================
           SIDEBAR NAVIGATION
        ========================================================= */

        [data-testid="stSidebarNav"] {

            padding-top:
                0.4rem !important;
        }


        [data-testid="stSidebarNav"] ul {

            gap:
                1px !important;
        }


        [data-testid="stSidebarNav"] li {

            margin:
                1px 0 !important;
        }


        /* =========================================================
           SIDEBAR PAGE LINKS
        ========================================================= */

        [data-testid="stSidebarNav"] a {

            background-color:
                transparent !important;

            border-radius:
                7px !important;

            border:
                1px solid transparent !important;

            border-left:
                4px solid transparent !important;

            margin:
                2px 8px !important;

            padding:
                7px 11px !important;

            min-height:
                38px !important;

            display:
                flex !important;

            align-items:
                center !important;

            transition:
                background-color 0.15s ease,
                border-color 0.15s ease !important;
        }


        /* =========================================================
           NORMAL SIDEBAR PAGE TEXT
        ========================================================= */

        [data-testid="stSidebarNav"]
        a:not([aria-current="page"]) p,

        [data-testid="stSidebarNav"]
        a:not([aria-current="page"]) span {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;

            opacity:
                1 !important;

            font-size:
                15px !important;

            font-weight:
                500 !important;

            line-height:
                1.2 !important;
        }


        /* =========================================================
           SIDEBAR HOVER
        ========================================================= */

        [data-testid="stSidebarNav"]
        a:not([aria-current="page"]):hover {

            background-color:
                var(--ct-sidebar-hover) !important;

            border-left-color:
                #A9C6D8 !important;
        }


        [data-testid="stSidebarNav"]
        a:not([aria-current="page"]):hover p,

        [data-testid="stSidebarNav"]
        a:not([aria-current="page"]):hover span {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        /* =========================================================
           ACTIVE / SELECTED PAGE
        ========================================================= */

        [data-testid="stSidebarNav"]
        a[aria-current="page"],

        [data-testid="stSidebarNavLink"]
        [aria-current="page"],

        [data-testid="stSidebarNavLink"][aria-current="page"] {

            background-color:
                var(--ct-sidebar-active) !important;

            border:
                1px solid #345675 !important;

            border-left:
                5px solid
                var(--ct-orange) !important;

            border-radius:
                7px !important;

            box-shadow:
                0 2px 6px
                rgba(0, 0, 0, 0.14) !important;
        }


        /* Selected page text must always remain white */

        [data-testid="stSidebarNav"]
        a[aria-current="page"] *,

        [data-testid="stSidebarNav"]
        a[aria-current="page"] p,

        [data-testid="stSidebarNav"]
        a[aria-current="page"] span,

        [data-testid="stSidebarNavLink"]
        [aria-current="page"] *,

        [data-testid="stSidebarNavLink"][aria-current="page"] * {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;

            opacity:
                1 !important;

            font-weight:
                650 !important;
        }


        /* =========================================================
           NAVIGATION GROUP HEADINGS
        ========================================================= */

        [data-testid="stSidebarNav"] header,

        [data-testid="stSidebarNav"] h2,

        [data-testid="stSidebarNav"] h3 {

            color:
                #D9EAF4 !important;

            -webkit-text-fill-color:
                #D9EAF4 !important;

            font-size:
                12px !important;

            font-weight:
                700 !important;

            letter-spacing:
                0.65px !important;

            text-transform:
                uppercase !important;
        }


        /* =========================================================
           OTHER SIDEBAR TEXT
        ========================================================= */

        [data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"] p,

        [data-testid="stSidebar"]
        [data-testid="stCaptionContainer"],

        [data-testid="stSidebar"]
        label {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        [data-testid="stSidebar"] hr {

            border-color:
                #52758C !important;

            opacity:
                1 !important;
        }


        /* =========================================================
           SIDEBAR LOGOUT / BUTTON
        ========================================================= */

        [data-testid="stSidebar"]
        .stButton > button {

            background-color:
                #FFFFFF !important;

            color:
                var(--ct-sidebar) !important;

            border:
                1px solid #D9EAF4 !important;

            border-radius:
                7px !important;

            min-height:
                40px !important;

            font-weight:
                650 !important;
        }


        [data-testid="stSidebar"]
        .stButton > button * {

            color:
                var(--ct-sidebar) !important;

            -webkit-text-fill-color:
                var(--ct-sidebar) !important;
        }


        [data-testid="stSidebar"]
        .stButton > button:hover {

            background-color:
                var(--ct-orange) !important;

            color:
                #FFFFFF !important;

            border-color:
                var(--ct-orange) !important;
        }


        [data-testid="stSidebar"]
        .stButton > button:hover * {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        /* =========================================================
           WIDGET LABELS
        ========================================================= */

        [data-testid="stWidgetLabel"] p,

        [data-testid="stWidgetLabel"] span {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;

            font-size:
                14px !important;

            font-weight:
                600 !important;
        }


        /* =========================================================
           TEXT INPUT
        ========================================================= */

        [data-testid="stTextInput"] input {

            background-color:
                #FFFFFF !important;

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;

            border-radius:
                7px !important;

            caret-color:
                var(--ct-orange) !important;
        }


        /* =========================================================
           NUMBER INPUT
        ========================================================= */

        [data-testid="stNumberInput"] input {

            background-color:
                #FFFFFF !important;

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* =========================================================
           TEXTAREA
        ========================================================= */

        [data-testid="stTextArea"] textarea {

            background-color:
                #FFFFFF !important;

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;

            border-radius:
                7px !important;
        }


        /* =========================================================
           INPUT PLACEHOLDERS
        ========================================================= */

        input::placeholder,
        textarea::placeholder {

            color:
                #8996A5 !important;

            -webkit-text-fill-color:
                #8996A5 !important;

            opacity:
                1 !important;
        }


        /* =========================================================
           SELECTBOX
        ========================================================= */

        [data-testid="stSelectbox"]
        [data-baseweb="select"] > div {

            background-color:
                #FFFFFF !important;

            border-color:
                var(--ct-border-dark) !important;

            color:
                var(--ct-text) !important;

            border-radius:
                7px !important;
        }


        [data-testid="stSelectbox"]
        [data-baseweb="select"] span {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* =========================================================
           MULTISELECT
        ========================================================= */

        [data-testid="stMultiSelect"]
        [data-baseweb="select"] > div {

            background-color:
                #FFFFFF !important;

            border-color:
                var(--ct-border-dark) !important;

            border-radius:
                7px !important;
        }


        [data-testid="stMultiSelect"]
        [data-baseweb="tag"] {

            background-color:
                #EAF3FA !important;

            color:
                var(--ct-navy) !important;
        }


        [data-testid="stMultiSelect"]
        [data-baseweb="tag"] * {

            color:
                var(--ct-navy) !important;

            -webkit-text-fill-color:
                var(--ct-navy) !important;
        }


        /* =========================================================
           DROPDOWN OPTIONS
        ========================================================= */

        [data-baseweb="popover"] {

            background-color:
                #FFFFFF !important;
        }


        [role="listbox"] {

            background-color:
                #FFFFFF !important;
        }


        [role="option"] {

            background-color:
                #FFFFFF !important;

            color:
                var(--ct-text) !important;
        }


        [role="option"] * {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        [role="option"]:hover {

            background-color:
                var(--ct-orange-soft) !important;
        }


        /* =========================================================
           RADIO BUTTONS
        ========================================================= */

        [data-testid="stRadio"] label,

        [data-testid="stRadio"] label p,

        [data-testid="stRadio"] label span {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* =========================================================
           CHECKBOX
        ========================================================= */

        [data-testid="stCheckbox"] label,

        [data-testid="stCheckbox"] label p,

        [data-testid="stCheckbox"] label span {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* =========================================================
           TOGGLE
        ========================================================= */

        [data-testid="stToggle"] label,

        [data-testid="stToggle"] label p,

        [data-testid="stToggle"] label span {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* =========================================================
           BUTTONS
        ========================================================= */

        .stButton > button {

            border-radius:
                7px !important;

            min-height:
                40px !important;

            font-weight:
                600 !important;

            transition:
                all 0.15s ease-in-out !important;
        }


        /* Primary */

        [data-testid="stBaseButton-primary"] {

            background-color:
                var(--ct-blue) !important;

            border:
                1px solid
                var(--ct-blue) !important;

            color:
                #FFFFFF !important;

            box-shadow:
                0 2px 4px
                rgba(47, 111, 163, 0.18) !important;
        }


        [data-testid="stBaseButton-primary"] * {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        [data-testid="stBaseButton-primary"]:hover {

            background-color:
                var(--ct-blue-hover) !important;

            border-color:
                var(--ct-blue-hover) !important;

            color:
                #FFFFFF !important;
        }


        /* Secondary */

        [data-testid="stBaseButton-secondary"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border-dark) !important;

            color:
                var(--ct-navy) !important;
        }


        [data-testid="stBaseButton-secondary"] * {

            color:
                var(--ct-navy) !important;

            -webkit-text-fill-color:
                var(--ct-navy) !important;
        }


        [data-testid="stBaseButton-secondary"]:hover {

            background-color:
                var(--ct-orange-soft) !important;

            border-color:
                var(--ct-orange) !important;

            color:
                var(--ct-orange-hover) !important;
        }


        /* =========================================================
           FORM SUBMIT BUTTON
        ========================================================= */

        [data-testid="stFormSubmitButton"] button {

            background-color:
                var(--ct-blue) !important;

            color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-blue) !important;

            border-radius:
                7px !important;

            min-height:
                41px !important;

            font-weight:
                600 !important;
        }


        [data-testid="stFormSubmitButton"] button * {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        [data-testid="stFormSubmitButton"] button:hover {

            background-color:
                var(--ct-blue-hover) !important;

            border-color:
                var(--ct-blue-hover) !important;
        }


        /* =========================================================
           DOWNLOAD BUTTON
        ========================================================= */

        .stDownloadButton > button {

            background-color:
                var(--ct-blue) !important;

            color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-blue) !important;

            border-radius:
                7px !important;

            min-height:
                40px !important;

            font-weight:
                600 !important;
        }


        .stDownloadButton > button * {

            color:
                #FFFFFF !important;

            -webkit-text-fill-color:
                #FFFFFF !important;
        }


        .stDownloadButton > button:hover {

            background-color:
                var(--ct-blue-hover) !important;

            border-color:
                var(--ct-blue-hover) !important;
        }


        /* =========================================================
           FILE UPLOADER
        ========================================================= */

        [data-testid="stFileUploaderDropzone"] {

            background-color:
                #FFFFFF !important;

            border:
                2px dashed
                #AEBBC8 !important;

            border-radius:
                10px !important;

            padding:
                18px !important;
        }


        [data-testid="stFileUploaderDropzone"]:hover {

            background-color:
                var(--ct-orange-soft) !important;

            border-color:
                var(--ct-orange) !important;
        }


        [data-testid="stFileUploaderDropzone"] p,

        [data-testid="stFileUploaderDropzone"] span {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* Uploaded file */

        [data-testid="stFileUploaderFile"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border) !important;

            border-radius:
                7px !important;
        }


        [data-testid="stFileUploaderFile"] * {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* =========================================================
           FORMS
        ========================================================= */

        [data-testid="stForm"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border) !important;

            border-top:
                4px solid
                var(--ct-orange) !important;

            border-radius:
                11px !important;

            padding:
                22px !important;

            box-shadow:
                0 3px 10px
                rgba(15, 23, 42, 0.04) !important;
        }


        /* =========================================================
           ALERTS
        ========================================================= */

        [data-testid="stAlert"] {

            border-radius:
                8px !important;

            border:
                1px solid
                var(--ct-border) !important;
        }


        [data-testid="stAlert"] p,

        [data-testid="stAlert"] span {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;

            font-weight:
                500 !important;
        }


        /* =========================================================
           EXPANDERS
        ========================================================= */

        [data-testid="stExpander"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border) !important;

            border-radius:
                9px !important;
        }


        [data-testid="stExpander"] summary * {

            color:
                var(--ct-navy) !important;

            -webkit-text-fill-color:
                var(--ct-navy) !important;

            font-weight:
                600 !important;
        }


        /* =========================================================
           CONTAINERS / CARDS
        ========================================================= */

        [data-testid="stVerticalBlockBorderWrapper"] {

            background-color:
                #FFFFFF !important;

            border-color:
                var(--ct-border) !important;

            border-radius:
                10px !important;
        }


        /* =========================================================
           METRIC CARDS
        ========================================================= */

        [data-testid="stMetric"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border) !important;

            border-top:
                4px solid
                var(--ct-orange) !important;

            border-radius:
                9px !important;

            padding:
                15px !important;

            box-shadow:
                0 2px 6px
                rgba(15, 23, 42, 0.04) !important;
        }


        [data-testid="stMetricLabel"] * {

            color:
                var(--ct-text-secondary) !important;

            -webkit-text-fill-color:
                var(--ct-text-secondary) !important;
        }


        [data-testid="stMetricValue"] * {

            color:
                var(--ct-navy) !important;

            -webkit-text-fill-color:
                var(--ct-navy) !important;

            font-weight:
                750 !important;
        }


        /* =========================================================
           TABS
        ========================================================= */

        [data-baseweb="tab-list"] {

            gap:
                5px !important;

            border-bottom:
                1px solid
                var(--ct-border) !important;
        }


        [data-baseweb="tab"] {

            color:
                var(--ct-text-secondary) !important;
        }


        [data-baseweb="tab"] * {

            color:
                var(--ct-text-secondary) !important;

            -webkit-text-fill-color:
                var(--ct-text-secondary) !important;

            font-weight:
                600 !important;
        }


        [data-baseweb="tab"]
        [aria-selected="true"] {

            color:
                var(--ct-navy) !important;
        }


        [data-baseweb="tab"][aria-selected="true"] * {

            color:
                var(--ct-navy) !important;

            -webkit-text-fill-color:
                var(--ct-navy) !important;

            font-weight:
                700 !important;
        }


        [data-baseweb="tab-highlight"] {

            background-color:
                var(--ct-orange) !important;
        }


        /* =========================================================
           TABLE
        ========================================================= */

        [data-testid="stTable"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border) !important;

            border-radius:
                8px !important;

            overflow:
                hidden !important;
        }


        [data-testid="stTable"] table {

            color:
                var(--ct-text) !important;
        }


        [data-testid="stTable"] thead tr th {

            background-color:
                var(--ct-sidebar) !important;

            color:
                #FFFFFF !important;

            font-weight:
                650 !important;
        }


        [data-testid="stTable"] tbody tr td {

            background-color:
                #FFFFFF !important;

            color:
                var(--ct-text) !important;
        }


        [data-testid="stTable"]
        tbody tr:nth-child(even) td {

            background-color:
                #F8FAFC !important;
        }


        /* =========================================================
           DATAFRAME
        ========================================================= */

        [data-testid="stDataFrame"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border) !important;

            border-radius:
                8px !important;

            overflow:
                hidden !important;
        }


        /* =========================================================
           DATA EDITOR
        ========================================================= */

        [data-testid="stDataEditor"] {

            background-color:
                #FFFFFF !important;

            border:
                1px solid
                var(--ct-border) !important;

            border-radius:
                8px !important;
        }


        /* =========================================================
           DIVIDER
        ========================================================= */

        hr {

            border-color:
                var(--ct-border) !important;

            opacity:
                1 !important;
        }


        /* =========================================================
           PROGRESS
        ========================================================= */

        [data-testid="stProgressBar"] > div > div {

            background-color:
                var(--ct-orange) !important;
        }


        /* =========================================================
           SPINNER / STATUS TEXT
        ========================================================= */

        [data-testid="stSpinner"] *,

        [data-testid="stStatusWidget"] * {

            color:
                var(--ct-text) !important;

            -webkit-text-fill-color:
                var(--ct-text) !important;
        }


        /* =========================================================
           CODE BLOCK
        ========================================================= */

        [data-testid="stCodeBlock"] {

            border-radius:
                8px !important;
        }


        /* =========================================================
           OPTIONAL PAGE HEADER CLASS
        ========================================================= */

        .ct-page-header {

            background-color:
                #FFFFFF;

            border:
                1px solid
                var(--ct-border);

            border-left:
                5px solid
                var(--ct-orange);

            border-radius:
                10px;

            padding:
                19px 22px;

            margin-bottom:
                22px;

            box-shadow:
                0 2px 7px
                rgba(15, 23, 42, 0.04);
        }


        .ct-page-title {

            color:
                var(--ct-navy);

            font-size:
                29px;

            font-weight:
                750;

            line-height:
                1.25;

            margin:
                0;
        }


        .ct-page-subtitle {

            color:
                var(--ct-muted);

            font-size:
                14px;

            margin-top:
                6px;

            margin-bottom:
                0;
        }


        /* =========================================================
           OPTIONAL CONTENT CARD
        ========================================================= */

        .ct-card {

            background-color:
                #FFFFFF;

            border:
                1px solid
                var(--ct-border);

            border-radius:
                10px;

            padding:
                20px;

            margin-bottom:
                18px;

            box-shadow:
                0 2px 6px
                rgba(15, 23, 42, 0.035);
        }


        /* =========================================================
           OPTIONAL SECTION TITLE
        ========================================================= */

        .ct-section-title {

            color:
                var(--ct-navy);

            font-size:
                20px;

            font-weight:
                700;

            border-left:
                4px solid
                var(--ct-orange);

            padding-left:
                10px;

            margin-top:
                8px;

            margin-bottom:
                14px;
        }


        /* =========================================================
           CUSTOM STATUS BOXES
        ========================================================= */

        .ct-success {

            background-color:
                var(--ct-success-bg);

            color:
                var(--ct-success-text);

            border:
                1px solid #B7DFC4;

            border-left:
                4px solid #2E8B57;

            border-radius:
                8px;

            padding:
                12px 14px;

            margin:
                10px 0 16px 0;
        }


        .ct-info {

            background-color:
                var(--ct-info-bg);

            color:
                var(--ct-info-text);

            border:
                1px solid #C4DAEA;

            border-left:
                4px solid var(--ct-blue);

            border-radius:
                8px;

            padding:
                12px 14px;

            margin:
                10px 0 16px 0;
        }


        .ct-warning {

            background-color:
                var(--ct-warning-bg);

            color:
                var(--ct-warning-text);

            border:
                1px solid #F3D9A6;

            border-left:
                4px solid var(--ct-orange);

            border-radius:
                8px;

            padding:
                12px 14px;

            margin:
                10px 0 16px 0;
        }


        .ct-error {

            background-color:
                var(--ct-error-bg);

            color:
                var(--ct-error-text);

            border:
                1px solid #F0C5C2;

            border-left:
                4px solid #C73A32;

            border-radius:
                8px;

            padding:
                12px 14px;

            margin:
                10px 0 16px 0;
        }


        /* =========================================================
           SCROLLBAR
        ========================================================= */

        ::-webkit-scrollbar {

            width:
                8px;

            height:
                8px;
        }


        ::-webkit-scrollbar-track {

            background:
                #E8EDF2;
        }


        ::-webkit-scrollbar-thumb {

            background:
                #7E9AAC;

            border-radius:
                8px;
        }


        ::-webkit-scrollbar-thumb:hover {

            background:
                #607F93;
        }


        /* =========================================================
           MOBILE / SMALLER SCREENS
        ========================================================= */

        @media (max-width: 900px) {

            .block-container {

                padding-left:
                    1rem !important;

                padding-right:
                    1rem !important;

                padding-top:
                    1.2rem !important;
            }


            h1 {

                font-size:
                    1.65rem !important;
            }


            [data-testid="stSidebarNav"] a {

                min-height:
                    36px !important;
            }

        }


        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# OPTIONAL REUSABLE COMPONENTS
# =========================================================

def page_header(title, subtitle=""):

    subtitle_html = ""

    if subtitle:

        subtitle_html = f"""
            <p class="ct-page-subtitle">
                {subtitle}
            </p>
        """

    st.markdown(
        f"""
        <div class="ct-page-header">

            <div class="ct-page-title">
                {title}
            </div>

            {subtitle_html}

        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(title):

    st.markdown(
        f"""
        <div class="ct-section-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


def success_box(message):

    st.markdown(
        f"""
        <div class="ct-success">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def info_box(message):

    st.markdown(
        f"""
        <div class="ct-info">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def warning_box(message):

    st.markdown(
        f"""
        <div class="ct-warning">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def error_box(message):

    st.markdown(
        f"""
        <div class="ct-error">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def divider():

    st.divider()