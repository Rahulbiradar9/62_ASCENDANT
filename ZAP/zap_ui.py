import time
import requests
import streamlit as st
from zapv2 import ZAPv2

# ===============================
# Run ZAP Scan
# ===============================
def run_scan(target_url, zap_api):
    st.info("Testing ZAP connection...")
    try:
        response = requests.get(f"{zap_api}/JSON/core/view/version/", timeout=10)
        if response.status_code == 200:
            st.success("✓ ZAP API is accessible")
        else:
            st.error(f"✗ ZAP API returned status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"✗ Cannot connect to ZAP API: {e}")
        st.info("Make sure ZAP is running with: docker-compose up -d")
        return None

    zap = ZAPv2(apikey=None, proxies={'http': zap_api, 'https': zap_api})

    try:
        st.write(f"**ZAP version:** {zap.core.version}")
        zap.core.new_session()

        context_id = zap.context.new_context("target_context")
        zap.context.include_in_context("target_context", f"{target_url}.*")
        zap.context.exclude_from_context("target_context", ".*logout.*")

        # Spider scan
        st.info("Starting spider scan...")
        spider_id = zap.spider.scan(target_url, contextname="target_context")
        while int(zap.spider.status(spider_id)) < 100:
            st.write(f"Spider progress: {zap.spider.status(spider_id)}%")
            time.sleep(2)
        st.success("Spider scan completed!")

        time.sleep(2)

        # Active scan
        st.info("Starting active scan...")
        active_id = zap.ascan.scan(target_url, contextid=context_id)
        while int(zap.ascan.status(active_id)) < 100:
            st.write(f"Active scan progress: {zap.ascan.status(active_id)}%")
            time.sleep(5)
        st.success("Active scan completed!")

        alerts = zap.core.alerts(baseurl=target_url)
        st.success(f"Found {len(alerts)} alerts!")

        # Generate and save report
        report_html = generate_custom_report(target_url, alerts, zap)
        with open("zap_report.html", "w", encoding="utf-8") as f:
            f.write(report_html)

        st.download_button(
            label="📥 Download Report",
            data=report_html,
            file_name="zap_report.html",
            mime="text/html"
        )

        return alerts
    except Exception as e:
        st.error(f"Error during scan: {e}")
        return None

# ===============================
# Generate custom HTML report
# ===============================
def generate_custom_report(target_url, alerts, zap):
    risk_order = {'High': 0, 'Medium': 1, 'Low': 2, 'Informational': 3}
    sorted_alerts = sorted(alerts, key=lambda x: risk_order.get(x.get('risk', 'Informational'), 3))
    risk_counts = {
        'High': len([a for a in alerts if a.get('risk') == 'High']),
        'Medium': len([a for a in alerts if a.get('risk') == 'Medium']),
        'Low': len([a for a in alerts if a.get('risk') == 'Low']),
        'Informational': len([a for a in alerts if a.get('risk') == 'Informational'])
    }

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ZAP Security Scan Report - {target_url}</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
            .summary {{ margin: 20px 0; }}
            .alert {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
            .high {{ border-left: 5px solid #ff4d4d; background: #fff5f5; }}
            .medium {{ border-left: 5px solid #ffa64d; background: #fffaf5; }}
            .low {{ border-left: 5px solid #4d94ff; background: #f5f9ff; }}
            .info {{ border-left: 5px solid #4dff4d; background: #f5fff5; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>OWASP ZAP Security Scan Report</h1>
            <p><strong>Target URL:</strong> {target_url}</p>
            <p><strong>Scan Date:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>ZAP Version:</strong> {zap.core.version}</p>
        </div>
        <div class="summary">
            <h2>Summary</h2>
            <p>High: {risk_counts['High']}</p>
            <p>Medium: {risk_counts['Medium']}</p>
            <p>Low: {risk_counts['Low']}</p>
            <p>Informational: {risk_counts['Informational']}</p>
            <p><strong>Total Alerts:</strong> {len(alerts)}</p>
        </div>
    """
    for alert in sorted_alerts:
        risk_class = alert.get('risk', 'Informational').lower()
        html += f"""
        <div class="alert {risk_class}">
            <h3>{alert.get('risk')} - {alert.get('alert')}</h3>
            <p><strong>URL:</strong> {alert.get('url')}</p>
            <p><strong>Description:</strong> {alert.get('description')}</p>
            <p><strong>Solution:</strong> {alert.get('solution')}</p>
        </div>
        """
    html += "</body></html>"
    return html

# ===============================
# Streamlit UI
# ===============================
st.set_page_config(page_title="OWASP ZAP Scanner", layout="wide")
st.title("🔍 OWASP ZAP Security Scanner")

target_url = st.text_input("Enter the target URL", "https://www.example.com")
zap_api = st.text_input("Enter ZAP API URL", "http://localhost:8080")

if st.button("Start Scan"):
    with st.spinner("Running scan... This may take several minutes."):
        run_scan(target_url, zap_api)
