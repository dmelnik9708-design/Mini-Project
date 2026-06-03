import streamlit as st
import requests
from urllib.parse import urlparse
import time

# --- Configure Page ---
st.set_page_config(page_title="WebCheck Pro", page_icon="🌐", layout="centered")

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "dict_focus" not in st.session_state:
    st.session_state.dict_focus = None
if "language" not in st.session_state:
    st.session_state.language = "EN"

# --- Translations Dictionary ---
texts = {
    "EN": {
        "nav_home": "Home", "nav_about": "About Us", "nav_why": "Why Us", "nav_dict": "Dictionary",
        "nav_login": "Login", "nav_dash": "Dashboard", "nav_logout": "Logout",
        "lang_toggle": "🌍 Language",
        "home_title": "Welcome to WebCheck Pro",
        "home_desc": "Welcome to the Website Security Checker, a school project developed to analyze and evaluate website security and performance. This tool allows users to test website availability, compare HTTP and HTTPS connections, and check important security headers such as Content-Security-Policy, X-Frame-Options, and Strict-Transport-Security. \n\nThe goal of this project is to demonstrate practical knowledge in Python programming, web technologies, and cybersecurity while helping users better understand the security configuration of websites. Please log in to access the dashboard and explore the available website analysis and security checking features.",
        "about_title": "About Us",
        "about_desc": "",
        "why_title": "Why Us",
        "why_desc": "Unlike other platforms, we don't just give you raw data. We connect every check to our comprehensive **Website Dictionary**.",
        "login_title": "Login to Your Account",
        "login_user": "Username", "login_pass": "Password", "login_btn": "Secure Login",
        "dash_warn": "Please log in to view the dashboard.", "go_login": "Go to Login",
        "dash_title": "Website Auditor Dashboard",
        "dash_desc": "Enter a domain (e.g., example.com) below to run a real live diagnostic check.",
        "url_ph": "example.com", "run_check": "Run Website Check",
        "scanning": "Scanning", "audit_report": "Audit Report", "sec_score": "Security Score",
        "status_code": "Status Code",
        "https_ok": "✅ HTTPS Connection Successful", "https_fail": "❌ HTTPS Failed",
        "http_redir_ok": "✅ HTTP automatically redirects to HTTPS", "http_redir_warn": "⚠️ HTTP does not redirect securely",
        "btn_https": "What is HTTPS? ➔", "btn_headers": "What are Headers? ➔",
        "sec_headers": "Security Headers", "found": "Found", "missing": "Missing",
        "dict_title": "Website Dictionary", "dict_desc": "Detailed explanations for our checks.",
        "dict_arr_https": "💡 **You arrived here from the dashboard to learn about HTTPS.**",
        "dict_arr_head": "💡 **You arrived here from the dashboard to learn about Security Headers.**",
        "h_https": "HTTP vs HTTPS",
        "p_https": "HTTP transfers data in plain text, making it vulnerable to interception. HTTPS encrypts this data. A secure website should always load in HTTPS and automatically redirect any HTTP traffic to the secure version.",
        "h_headers": "Security Headers",
        "p_headers": "Security headers are instructions sent by the server to the browser to restrict certain behaviors and prevent attacks:\n* **Content-Security-Policy (CSP):** Prevents Cross-Site Scripting (XSS).\n* **X-Frame-Options:** Prevents clickjacking.\n* **Strict-Transport-Security (HSTS):** Forces the browser to strictly use secure HTTPS connections."
    },
    "DE": {
        "nav_home": "Startseite", "nav_about": "Über uns", "nav_why": "Warum wir", "nav_dict": "Wörterbuch",
        "nav_login": "Anmelden", "nav_dash": "Dashboard", "nav_logout": "Abmelden",
        "lang_toggle": "🌍 Sprache",
        "home_title": "Willkommen bei WebCheck Pro",
        "home_desc": "Willkommen beim Website Security Checker. Dieses Schulprojekt wurde entwickelt, um die Sicherheit und Erreichbarkeit von Webseiten zu analysieren. Das System überprüft HTTP- und HTTPS-Verbindungen, analysiert wichtige Sicherheits-Header und hilft dabei, mögliche Schwachstellen einer Website zu erkennen. \n\nDas Ziel dieses Projekts ist es, praktische Erfahrungen in den Bereichen Python-Programmierung, Webtechnologien und Cybersicherheit zu sammeln. Melden Sie sich an, um das Dashboard zu nutzen und verschiedene Sicherheitsprüfungen auf Webseiten durchzuführen.",
        "about_title": "Über uns",
        "about_desc": "Ich bin ein Schüler mit großem Interesse an Informatik, Programmierung und Cybersicherheit. Da die Sicherheit im Internet im Alltag immer wichtiger wird, habe ich dieses Schulprojekt entwickelt, um Webseiten auf mögliche Sicherheitslücken und fehlende Sicherheitseinstellungen zu überprüfen. /n/n Mit dem Website Security Checker möchte ich zeigen, wie wichtig Sicherheitsmechanismen wie HTTPS und HTTP Security Header für den Schutz von Daten und Benutzern sind. Gleichzeitig bietet mir dieses Projekt die Möglichkeit, meine Kenntnisse in Python, Webtechnologien und Cybersicherheit zu erweitern und praktische Erfahrungen in der Softwareentwicklung zu sammeln. \n\n Dieses Projekt ist ein wichtiger Schritt auf meinem Weg in die IT- und Cybersecurity-Branche. Mein Ziel ist es, mein Wissen kontinuierlich auszubauen und in Zukunft weitere innovative Lösungen im Bereich der Cybersicherheit zu entwickeln.",
        "why_title": "Warum wir",
        "why_desc": "Im Gegensatz zu anderen Plattformen geben wir Ihnen nicht nur Rohdaten. Wir verbinden jede Überprüfung mit unserem umfassenden **Website-Wörterbuch**.",
        "login_title": "Bei Ihrem Konto anmelden",
        "login_user": "Benutzername", "login_pass": "Passwort", "login_btn": "Sichere Anmeldung",
        "dash_warn": "Bitte melden Sie sich an, um das Dashboard zu sehen.", "go_login": "Zur Anmeldung",
        "dash_title": "Website-Auditor Dashboard",
        "dash_desc": "Geben Sie unten eine Domain (z.B. example.com) ein, um eine echte Live-Diagnose durchzuführen.",
        "url_ph": "example.com", "run_check": "Website-Prüfung starten",
        "scanning": "Scanne", "audit_report": "Audit-Bericht", "sec_score": "Sicherheitsbewertung",
        "status_code": "Statuscode",
        "https_ok": "✅ HTTPS-Verbindung erfolgreich", "https_fail": "❌ HTTPS fehlgeschlagen",
        "http_redir_ok": "✅ HTTP leitet automatisch auf HTTPS um", "http_redir_warn": "⚠️ HTTP leitet nicht sicher um",
        "btn_https": "Was ist HTTPS? ➔", "btn_headers": "Was sind Header? ➔",
        "sec_headers": "Sicherheits-Header", "found": "Gefunden", "missing": "Fehlt",
        "dict_title": "Website-Wörterbuch", "dict_desc": "Detaillierte Erklärungen für unsere Überprüfungen.",
        "dict_arr_https": "💡 **Sie sind vom Dashboard hierher gelangt, um mehr über HTTPS zu erfahren.**",
        "dict_arr_head": "💡 **Sie sind vom Dashboard hierher gelangt, um mehr über Sicherheits-Header zu erfahren.**",
        "h_https": "HTTP vs HTTPS",
        "p_https": "HTTP überträgt Daten im Klartext, was sie anfällig für das Abfangen macht. HTTPS verschlüsselt diese Daten. Eine sichere Website sollte immer in HTTPS geladen werden und HTTP-Datenverkehr automatisch umleiten.",
        "h_headers": "Sicherheits-Header",
        "p_headers": "Sicherheits-Header sind Anweisungen, die vom Server an den Browser gesendet werden, um bestimmte Angriffe zu verhindern:\n* **Content-Security-Policy (CSP):** Verhindert Cross-Site Scripting (XSS).\n* **X-Frame-Options:** Verhindert Clickjacking.\n* **Strict-Transport-Security (HSTS):** Erzwingt, dass der Browser ausschließlich sichere HTTPS-Verbindungen nutzt."
    }
}

# Helper function to get text based on current language
def t(key):
    return texts[st.session_state.language][key]

# --- Navigation Functions ---
def go_to(page, focus=None):
    st.session_state.current_page = page
    st.session_state.dict_focus = focus

def login():
    st.session_state.logged_in = True
    st.session_state.current_page = "Dashboard"

def logout():
    st.session_state.logged_in = False
    st.session_state.current_page = "Home"

# --- Backend Logic ---
def analyze_website(target_url):
    results = {
        "status_code": None, "error": None, "https_works": False,
        "http_redirects": False, "headers": {}, "missing_headers": [], "score": 100
    }
    parsed = urlparse(target_url)
    domain = parsed.netloc if parsed.netloc else parsed.path
    if not domain:
        results["error"] = "Invalid URL format."
        return results

    url_http = f"http://{domain}"
    url_https = f"https://{domain}"

    try:
        resp_http = requests.get(url_http, timeout=5, allow_redirects=False)
        if resp_http.status_code in [301, 302, 307, 308] and 'https' in resp_http.headers.get('Location', ''):
            results["http_redirects"] = True
        else:
            results["score"] -= 15
            
        resp_https = requests.get(url_https, timeout=5)
        results["status_code"] = resp_https.status_code
        results["https_works"] = True
        headers_lower = {k.lower(): v for k, v in resp_https.headers.items()}
        
    except requests.exceptions.RequestException as e:
        results["error"] = f"Connection failed: {str(e)}"
        results["score"] = 0
        return results

    security_headers_to_check = {
        "content-security-policy": "Content-Security-Policy",
        "x-frame-options": "X-Frame-Options",
        "strict-transport-security": "Strict-Transport-Security"
    }

    for lower_key, original_key in security_headers_to_check.items():
        if lower_key in headers_lower:
            results["headers"][original_key] = True
        else:
            results["headers"][original_key] = False
            results["missing_headers"].append(original_key)
            results["score"] -= 10

    results["score"] = max(0, results["score"])
    return results

# --- Sidebar Navigation ---
st.sidebar.title("🌐 Website Security Checker")

# Language Switcher
st.session_state.language = st.sidebar.radio(
    t("lang_toggle"), 
    options=["EN", "DE"], 
    index=0 if st.session_state.language == "EN" else 1,
    horizontal=True
)

st.sidebar.markdown("---")

# Navigation Buttons
st.sidebar.button(t("nav_home"), on_click=go_to, args=("Home",), use_container_width=True)
st.sidebar.button(t("nav_about"), on_click=go_to, args=("About Us",), use_container_width=True)
st.sidebar.button(t("nav_why"), on_click=go_to, args=("Why Us",), use_container_width=True)
st.sidebar.button(t("nav_dict"), on_click=go_to, args=("Dictionary",), use_container_width=True)

st.sidebar.markdown("---")

if not st.session_state.logged_in:
    st.sidebar.button(t("nav_login"), on_click=go_to, args=("Login",), type="primary", use_container_width=True)
else:
    st.sidebar.button(t("nav_dash"), on_click=go_to, args=("Dashboard",), type="primary", use_container_width=True)
    st.sidebar.button(t("nav_logout"), on_click=logout, use_container_width=True)

# --- Main Page Content ---
page = st.session_state.current_page

if page == "Home":
    st.title(t("home_title"))
    st.write(t("home_desc"))

elif page == "About Us":
    st.title(t("about_title"))
    st.write(t("about_desc"))

elif page == "Why Us":
    st.title(t("why_title"))
    st.write(t("why_desc"))

elif page == "Login":
    st.title(t("login_title"))
    with st.form("login_form"):
        # Assign the inputs to variables
        username = st.text_input(t("login_user"), placeholder="Login")
        password = st.text_input(t("login_pass"), type="password", placeholder="****")
        submitted = st.form_submit_button(t("login_btn"))
        
        if submitted:
            # Check for the specific username and password
            if username == "Michael.Herzog" and password == "Admin.Panel.Herzog":
                login()
                st.rerun()
            else:
                # Display an error if the credentials don't match
                st.error("Invalid username or password. Please try again.")

elif page == "Dashboard":
    if not st.session_state.logged_in:
        st.warning(t("dash_warn"))
        st.button(t("go_login"), on_click=go_to, args=("Login",))
    else:
        st.title(t("dash_title"))
        st.write(t("dash_desc"))
        
        with st.form("audit_form"):
            url = st.text_input("URL", placeholder=t("url_ph"), label_visibility="collapsed")
            run = st.form_submit_button(t("run_check"))
        
        if run and url:
            with st.spinner(f"{t('scanning')} {url}..."):
                report = analyze_website(url)
            
            st.markdown(f"### {t('audit_report')}")
            
            if report["error"]:
                st.error(f"❌ **Error:** {report['error']}")
            else:
                score = report["score"]
                color = "green" if score > 80 else "orange" if score > 50 else "red"
                st.markdown(f"**{t('sec_score')}:** :{color}[{score} / 100]")
                st.markdown("---")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{t('status_code')}:** {report['status_code']}")
                    if report['https_works']: st.write(t("https_ok"))
                    else: st.write(t("https_fail"))
                        
                    if report['http_redirects']: st.write(t("http_redir_ok"))
                    else: st.write(t("http_redir_warn"))
                with col2:
                    st.button(t("btn_https"), key="btn_https", on_click=go_to, args=("Dictionary", "HTTPS"))
                
                st.markdown("---")
                st.markdown(f"#### {t('sec_headers')}")
                col3, col4 = st.columns([3, 1])
                with col3:
                    for header, present in report["headers"].items():
                        if present: st.write(f"✅ {t('found')}: `{header}`")
                        else: st.write(f"❌ {t('missing')}: `{header}`")
                with col4:
                    st.button(t("btn_headers"), key="btn_headers", on_click=go_to, args=("Dictionary", "Headers"))

elif page == "Dictionary":
    st.title(t("dict_title"))
    st.write(t("dict_desc"))
    st.markdown("---")
    
    focus = st.session_state.dict_focus

    if focus == "HTTPS": st.info(t("dict_arr_https"))
    st.subheader(t("h_https"))
    st.write(t("p_https"))
    st.markdown("---")

    if focus == "Headers": st.info(t("dict_arr_head"))
    st.subheader(t("h_headers"))
    st.write(t("p_headers"))

if st.session_state.current_page == "Dictionary":
    st.session_state.dict_focus = None
    
