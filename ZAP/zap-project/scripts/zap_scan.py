import time
import requests
from zapv2 import ZAPv2

def run_scan():
    target_url = "https://www.udemy.com/"  # Change this to your target URL
    zap_api = "http://localhost:8080"
    
    print("Testing ZAP connection...")
    
    # Test basic connection first
    try:
        response = requests.get(f"{zap_api}/JSON/core/view/version/", timeout=10)
        if response.status_code == 200:
            print("✓ ZAP API is accessible")
        else:
            print(f"✗ ZAP API returned status: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Cannot connect to ZAP API: {e}")
        print("Make sure ZAP is running with: docker-compose up -d")
        return

    # Initialize ZAP client
    zap = ZAPv2(apikey=None, proxies={'http': zap_api, 'https': zap_api})
    
    try:
        print(f"ZAP version: {zap.core.version}")
        
        # Clear previous session and context
        print("Clearing previous session data...")
        zap.core.new_session()
        
        # Create a new context for our target
        context_id = zap.context.new_context("target_context")
        zap.context.include_in_context("target_context", f"{target_url}.*")
        zap.context.exclude_from_context("target_context", ".*logout.*")
        
        print(f"Starting scan for: {target_url}")
        
        # Spider scan with context
        print("Starting spider...")
        scan_id = zap.spider.scan(target_url, contextname="target_context")
        while int(zap.spider.status(scan_id)) < 100:
            progress = zap.spider.status(scan_id)
            print(f"Spider progress: {progress}%")
            time.sleep(2)
        print("✓ Spider completed")
        
        # Wait a bit after spidering
        time.sleep(2)
        
        # Active scan with context
        print("Starting active scan...")
        scan_id = zap.ascan.scan(target_url, contextid=context_id)
        while int(zap.ascan.status(scan_id)) < 100:
            progress = zap.ascan.status(scan_id)
            print(f"Active scan progress: {progress}%")
            time.sleep(5)
        print("✓ Active scan completed")
        
        # Generate report for ONLY our target URL
        print("Generating report...")
        
        # Get alerts only for our target
        alerts = zap.core.alerts(baseurl=target_url)
        
        # Create custom HTML report
        report_html = generate_custom_report(target_url, alerts, zap)
        
        with open('zap_report.html', 'w', encoding='utf-8') as f:
            f.write(report_html)
        print("✓ Report saved as zap_report.html")
        
        # Show summary
        print(f"Found {len(alerts)} security alerts for {target_url}")
        
        # Print alert summary
        for alert in alerts:
            print(f"- {alert['risk']} risk: {alert['alert']}")
            
    except Exception as e:
        print(f"Error during scan: {e}")
        import traceback
        traceback.print_exc()

def generate_custom_report(target_url, alerts, zap):
    """Generate a custom HTML report showing only results for the target URL"""
    
    # Sort alerts by risk level (High to Low)
    risk_order = {'High': 0, 'Medium': 1, 'Low': 2, 'Informational': 3}
    sorted_alerts = sorted(alerts, key=lambda x: risk_order.get(x.get('risk', 'Informational'), 3))
    
    # Count alerts by risk level
    risk_counts = {
        'High': len([a for a in alerts if a.get('risk') == 'High']),
        'Medium': len([a for a in alerts if a.get('risk') == 'Medium']),
        'Low': len([a for a in alerts if a.get('risk') == 'Low']),
        'Informational': len([a for a in alerts if a.get('risk') == 'Informational'])
    }
    
    # Generate HTML report
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>ZAP Security Scan Report - {target_url}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .alert {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .high {{ border-left: 5px solid #ff4d4d; background: #fff5f5; }}
        .medium {{ border-left: 5px solid #ffa64d; background: #fffaf5; }}
        .low {{ border-left: 5px solid #4d94ff; background: #f5f9ff; }}
        .info {{ border-left: 5px solid #4dff4d; background: #f5fff5; }}
        .risk-high {{ color: #ff4d4d; font-weight: bold; }}
        .risk-medium {{ color: #ffa64d; font-weight: bold; }}
        .risk-low {{ color: #4d94ff; font-weight: bold; }}
        .risk-info {{ color: #4dff4d; font-weight: bold; }}
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
        <h2>Scan Summary</h2>
        <p><span class="risk-high">High:</span> {risk_counts['High']} alerts</p>
        <p><span class="risk-medium">Medium:</span> {risk_counts['Medium']} alerts</p>
        <p><span class="risk-low">Low:</span> {risk_counts['Low']} alerts</p>
        <p><span class="risk-info">Informational:</span> {risk_counts['Informational']} alerts</p>
        <p><strong>Total:</strong> {len(alerts)} alerts</p>
    </div>
    
    <h2>Detailed Findings</h2>
    """
    
    if not alerts:
        html += "<p>No security alerts found for this target URL.</p>"
    else:
        for alert in sorted_alerts:
            risk_class = alert.get('risk', 'Informational').lower()
            html += f"""
            <div class="alert {risk_class}">
                <h3><span class="risk-{risk_class}">{alert.get('risk', 'Informational')}</span>: {alert.get('alert', 'Unknown')}</h3>
                <p><strong>URL:</strong> {alert.get('url', 'N/A')}</p>
                <p><strong>Description:</strong> {alert.get('description', 'No description available')}</p>
                <p><strong>Solution:</strong> {alert.get('solution', 'No solution provided')}</p>
                <p><strong>Reference:</strong> {alert.get('reference', 'No reference available')}</p>
                <p><strong>Parameter:</strong> {alert.get('param', 'N/A')}</p>
                <p><strong>Evidence:</strong> {alert.get('evidence', 'No evidence')}</p>
                <p><strong>CWE ID:</strong> {alert.get('cweid', 'N/A')}</p>
                <p><strong>WASC ID:</strong> {alert.get('wascid', 'N/A')}</p>
            </div>
            """
    
    html += """
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    run_scan()