import argparse
import json
import time
import os
import glob
from typing import Dict, Any, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def _ensure_url_scheme(input_url: str) -> str:
    """Ensure the URL has a scheme; default to https if missing."""
    try:
        parsed = urlparse(input_url)
        if not parsed.scheme:
            return f"https://{input_url}"
        return input_url
    except Exception:
        return input_url


def _fetch(url: str, timeout: int = 10) -> Tuple[Optional[requests.Response], Optional[str], float]:
    """Fetch a URL, returning (response, error, elapsed_seconds)."""
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS, allow_redirects=True)
        elapsed = time.time() - start
        return response, None, elapsed
    except Exception as exc:
        elapsed = time.time() - start
        return None, str(exc), elapsed


def _soupify(html_text: str) -> BeautifulSoup:
    return BeautifulSoup(html_text, "html.parser")


def _absolute_url(base_url: str, href: str) -> str:
    try:
        return urljoin(base_url, href)
    except Exception:
        return href


def _domain(url: str) -> str:
    p = urlparse(url)
    return p.netloc.lower()


def _is_internal(base_url: str, href: str) -> bool:
    try:
        return _domain(base_url) == _domain(_absolute_url(base_url, href))
    except Exception:
        return False


def _check_title(soup: BeautifulSoup, recommendations: List[str]) -> Tuple[Optional[str], Dict[str, Any]]:
    data: Dict[str, Any] = {"length": 0, "issues": []}
    title_tag = soup.find("title")
    if title_tag and title_tag.text.strip():
        title = title_tag.text.strip()
        data["length"] = len(title)
        if len(title) < 30:
            data["issues"].append("Title too short (<30 chars)")
            recommendations.append("Increase title length to ~50-60 characters.")
        if len(title) > 60:
            data["issues"].append("Title too long (>60 chars)")
            recommendations.append("Shorten title to <=60 characters.")
        return title, data
    else:
        recommendations.append("Missing <title> tag.")
        data["issues"].append("Missing title")
        return None, data


def _check_meta_description(soup: BeautifulSoup, recommendations: List[str]) -> Tuple[Optional[str], Dict[str, Any]]:
    data: Dict[str, Any] = {"length": 0, "issues": []}
    tag = soup.find("meta", attrs={"name": "description"})
    if tag and tag.get("content"):
        content = tag["content"].strip()
        data["length"] = len(content)
        if len(content) < 50:
            data["issues"].append("Description too short (<50 chars)")
            recommendations.append("Expand meta description to 120-160 characters.")
        if len(content) > 160:
            data["issues"].append("Description too long (>160 chars)")
            recommendations.append("Shorten meta description to <=160 characters.")
        return content, data
    else:
        data["issues"].append("Missing meta description")
        recommendations.append("Add a unique meta description (120-160 characters).")
        return None, data


def _check_h1(soup: BeautifulSoup, recommendations: List[str]) -> Tuple[List[str], Dict[str, Any]]:
    data: Dict[str, Any] = {"count": 0, "issues": []}
    h1s = [h1.text.strip() for h1 in soup.find_all("h1") if h1.text and h1.text.strip()]
    data["count"] = len(h1s)
    if len(h1s) == 0:
        data["issues"].append("No H1")
        recommendations.append("Add one descriptive H1 heading.")
    elif len(h1s) > 1:
        data["issues"].append("Multiple H1s")
        recommendations.append("Use only one primary H1 heading per page.")
    return h1s, data


def _check_images(soup: BeautifulSoup, recommendations: List[str]) -> Tuple[List[str], Dict[str, Any]]:
    data: Dict[str, Any] = {"total": 0}
    missing: List[str] = []
    images = soup.find_all("img")
    data["total"] = len(images)
    for img in images:
        if not img.get("alt") or img.get("alt", "").strip() == "":
            missing.append(img.get("src", "unknown"))
    if missing:
        recommendations.append(f"{len(missing)} images missing alt text.")
    return missing, data


def _check_canonical(base_url: str, soup: BeautifulSoup, recommendations: List[str]) -> Tuple[Optional[str], Dict[str, Any]]:
    data: Dict[str, Any] = {"issues": []}
    link = soup.find("link", rel=lambda x: x and "canonical" in x)
    if link and link.get("href"):
        href = _absolute_url(base_url, link["href"])
        # basic self-reference check
        page_no_fragment = _absolute_url(base_url, "")
        if urlparse(href).netloc != urlparse(page_no_fragment).netloc:
            data["issues"].append("Canonical points to different domain")
            recommendations.append("Ensure canonical URL points to the same domain.")
        return href, data
    else:
        data["issues"].append("Missing canonical")
        recommendations.append("Add a canonical <link> to avoid duplicate content.")
        return None, data


def _check_viewport(soup: BeautifulSoup, recommendations: List[str]) -> bool:
    vp = soup.find("meta", attrs={"name": "viewport"})
    if not vp:
        recommendations.append("Add responsive viewport meta tag.")
        return False
    return True


def _check_meta_robots(soup: BeautifulSoup, recommendations: List[str]) -> Dict[str, Any]:
    data: Dict[str, Any] = {"noindex": False, "nofollow": False}
    tag = soup.find("meta", attrs={"name": "robots"})
    if tag and tag.get("content"):
        content = tag["content"].lower()
        data["noindex"] = "noindex" in content
        data["nofollow"] = "nofollow" in content
        if data["noindex"]:
            recommendations.append("Page is set to noindex.")
        if data["nofollow"]:
            recommendations.append("Page is set to nofollow.")
    return data


def _check_lang_and_charset(soup: BeautifulSoup, recommendations: List[str]) -> Dict[str, Any]:
    info: Dict[str, Any] = {"lang": None, "charset": None}
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        info["lang"] = html_tag["lang"].strip()
    else:
        recommendations.append("Set <html lang> attribute for accessibility and SEO.")
    meta_charset = soup.find("meta", attrs={"charset": True})
    if meta_charset and meta_charset.get("charset"):
        info["charset"] = meta_charset["charset"].strip().lower()
    else:
        # Some pages set via http-equiv
        http_equiv = soup.find("meta", attrs={"http-equiv": "Content-Type"})
        if http_equiv and http_equiv.get("content"):
            info["charset"] = http_equiv["content"].lower()
        else:
            recommendations.append("Declare a charset (e.g., UTF-8).")
    return info


def _check_hreflang(base_url: str, soup: BeautifulSoup, recommendations: List[str]) -> List[Dict[str, str]]:
    tags = soup.find_all("link", attrs={"rel": "alternate"})
    hreflangs: List[Dict[str, str]] = []
    for tag in tags:
        if tag.get("hreflang") and tag.get("href"):
            hreflangs.append({
                "hreflang": tag.get("hreflang"),
                "href": _absolute_url(base_url, tag.get("href"))
            })
    # If a few exist, recommend ensuring reciprocity and x-default
    if hreflangs:
        has_x_default = any(h.get("hreflang", "").lower() == "x-default" for h in hreflangs)
        if not has_x_default:
            recommendations.append("Add x-default hreflang for international pages.")
    return hreflangs


def _check_social_and_structured(soup: BeautifulSoup, recommendations: List[str]) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "open_graph": False,
        "twitter_card": False,
        "json_ld_blocks": 0,
        "json_ld_errors": 0,
    }
    # OG
    if soup.find("meta", property=lambda v: v and v.startswith("og:")):
        data["open_graph"] = True
    else:
        recommendations.append("Add Open Graph tags for better social sharing.")
    # Twitter
    if soup.find("meta", attrs={"name": "twitter:card"}):
        data["twitter_card"] = True
    else:
        recommendations.append("Add Twitter Card meta tags.")
    # JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            json.loads(script.text)
            data["json_ld_blocks"] += 1
        except Exception:
            data["json_ld_errors"] += 1
            recommendations.append("Fix invalid JSON-LD structured data.")
    return data


def _smart_link_sampling(soup: BeautifulSoup, max_links: int) -> Tuple[List[str], List[str]]:
    """Smart sampling: prioritize navigation and main content links"""
    anchors = soup.find_all("a", href=True)
    internal: List[str] = []
    external: List[str] = []
    
    # Score links by importance
    scored_internal = []
    scored_external = []
    
    for a in anchors:
        href = a.get("href")
        if href.startswith(("javascript:", "mailto:", "tel:")):
            continue
            
        score = 0
        text = a.get_text(strip=True)
        
        # Higher priority for navigation links
        if a.find_parent("nav"):
            score += 10
        # Higher priority for main content
        if a.find_parent("main") or a.find_parent("article"):
            score += 8
        # Higher priority for header
        if a.find_parent("header"):
            score += 6
        # Higher priority for footer
        if a.find_parent("footer"):
            score += 4
        # Lower priority for social/ads
        if any(word in href.lower() for word in ["social", "ad", "analytics", "tracking"]):
            score -= 5
        # Bonus for descriptive text
        if len(text) > 3 and len(text) < 50:
            score += 2
            
        link_data = (href, score)
        
        # Categorize by domain
        full_url = _absolute_url("https://placeholder.com", href)  # Temporary base
        if _is_internal("https://placeholder.com", full_url):
            scored_internal.append(link_data)
        else:
            scored_external.append(link_data)
    
    # Sort by score and take top links
    scored_internal.sort(key=lambda x: x[1], reverse=True)
    scored_external.sort(key=lambda x: x[1], reverse=True)
    
    internal = [link[0] for link in scored_internal[:max_links]]
    external = [link[0] for link in scored_external[:max_links]]
    
    return internal, external

def _check_links(base_url: str, soup: BeautifulSoup, max_links: int, recommendations: List[str], workers: int = 10) -> Dict[str, Any]:
    # Use smart sampling instead of basic extraction
    internal, external = _smart_link_sampling(soup, max_links)
    
    # Deduplicate
    def unique(xs: List[str]) -> List[str]:
        seen = set()
        out: List[str] = []
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    internal = unique(internal)
    external = unique(external)

    broken_internal: List[Tuple[str, int]] = []
    broken_external: List[Tuple[str, int]] = []
    redirects: List[Tuple[str, int]] = []

    def head_or_get(u: str) -> Optional[requests.Response]:
        try:
            r = requests.head(u, timeout=3, headers=DEFAULT_HEADERS, allow_redirects=True)
            if r.status_code >= 400 or (r.status_code in (405, 501)):
                r = requests.get(u, timeout=3, headers=DEFAULT_HEADERS, allow_redirects=True)
            return r
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(head_or_get, link): link for link in internal + external}
        for future in as_completed(futures):
            link = futures[future]
            try:
                resp = future.result()
                status = resp.status_code
                if 300 <= status < 400:
                    redirects.append((link, status))
                if status >= 400:
                    if _is_internal(base_url, link):
                        broken_internal.append((link, status))
                    else:
                        broken_external.append((link, status))
            except Exception as exc:
                if _is_internal(base_url, link):
                    broken_internal.append((link, 0))
                else:
                    broken_external.append((link, 0))

    if broken_internal:
        recommendations.append(f"{len(broken_internal)} internal links appear broken.")
    if redirects:
        recommendations.append(f"{len(redirects)} links redirect; update to final URLs where possible.")

    return {
        "internal_count": len(internal),
        "external_count": len(external),
        "broken_internal": broken_internal[:10],
        "broken_external": broken_external[:10],
        "redirects": redirects[:10],
    }


def _check_technical_headers(url: str, response: requests.Response, elapsed: float, recommendations: List[str]) -> Dict[str, Any]:
    headers = {k.lower(): v for k, v in response.headers.items()}
    tech: Dict[str, Any] = {
        "status_code": response.status_code,
        "response_time_ms": int(elapsed * 1000),
        "content_length": int(headers.get("content-length") or 0),
        "gzip": headers.get("content-encoding", "").lower() in ("gzip", "br", "deflate"),
        "hsts": headers.get("strict-transport-security") is not None,
        "x_content_type_options": headers.get("x-content-type-options") == "nosniff",
        "x_frame_options": headers.get("x-frame-options") is not None,
        "referrer_policy": headers.get("referrer-policy") is not None,
        "csp": headers.get("content-security-policy") is not None,
        "server": headers.get("server"),
        "cache_control": headers.get("cache-control"),
    }
    if tech["response_time_ms"] > 1500:
        recommendations.append("Page load (first byte) seems slow (>1.5s). Optimize performance.")
    if tech["content_length"] > 2 * 1024 * 1024:
        recommendations.append("Large page size (>2MB). Consider optimizing assets.")
    if urlparse(url).scheme == "https" and not tech["hsts"]:
        recommendations.append("Enable HSTS for better transport security.")
    if not tech["x_content_type_options"]:
        recommendations.append("Add X-Content-Type-Options: nosniff header.")
    if not tech["x_frame_options"]:
        recommendations.append("Add X-Frame-Options header to prevent clickjacking.")
    if not tech["referrer_policy"]:
        recommendations.append("Set a Referrer-Policy header.")
    if not tech["csp"]:
        recommendations.append("Consider adding a Content-Security-Policy header.")
    return tech


def _check_robots_and_sitemap(base_url: str, recommendations: List[str]) -> Dict[str, Any]:
    info: Dict[str, Any] = {"robots_txt": "Missing", "sitemap": "Missing", "robots_notes": []}
    robots_url = urljoin(base_url, "/robots.txt")
    resp, err, _ = _fetch(robots_url, timeout=3)
    if resp and resp.status_code == 200:
        info["robots_txt"] = "Present"
        content = resp.text
        if "Disallow:" not in content and "Allow:" not in content:
            info["robots_notes"].append("robots.txt seems permissive (no explicit rules).")
        if "Sitemap:" in content:
            info["robots_notes"].append("robots.txt references a sitemap.")
    else:
        recommendations.append("Missing robots.txt file.")

    sitemap_url = urljoin(base_url, "/sitemap.xml")
    s_resp, _, _ = _fetch(sitemap_url, timeout=3)
    if s_resp and s_resp.status_code == 200:
        info["sitemap"] = "Present"
    else:
        recommendations.append("Missing sitemap.xml file.")
    return info


def _score(report: Dict[str, Any]) -> Dict[str, Any]:
    # Simple scoring: start from 100 and subtract based on issues
    score = 100
    deductions: List[str] = []

    def deduct(points: int, reason: str):
        nonlocal score
        score -= points
        deductions.append(f"-{points}: {reason}")

    # On-page
    title_info = report["on_page"]["title_info"]
    if title_info["issues"]:
        deduct(5, "Title issues")
    desc_info = report["on_page"]["meta_description_info"]
    if desc_info["issues"]:
        deduct(5, "Meta description issues")
    h1_info = report["on_page"]["h1_info"]
    if h1_info["issues"]:
        deduct(5, "H1 count issues")
    if len(report["on_page"]["images_missing_alt"]) > 5:
        deduct(3, "Many images missing alt")
    canonical_info = report["on_page"]["canonical_info"]
    if canonical_info["issues"]:
        deduct(2, "Canonical issues")
    if not report["on_page"]["has_viewport_meta"]:
        deduct(2, "Missing viewport")

    # Indexing
    robots_meta = report["on_page"]["meta_robots"]
    if robots_meta.get("noindex"):
        deduct(10, "noindex set")

    # Social/structured
    social = report["social_structured"]
    if not social["open_graph"]:
        deduct(2, "Missing Open Graph")
    if not social["twitter_card"]:
        deduct(1, "Missing Twitter Card")
    if social["json_ld_errors"] > 0:
        deduct(2, "Invalid JSON-LD")

    # Links
    links = report["links"]
    if len(links["broken_internal"]) > 0:
        deduct(5, "Broken internal links")
    if len(links["broken_external"]) > 3:
        deduct(2, "Multiple broken external links")

    # Technical
    tech = report["technical"]
    if tech["response_time_ms"] > 1500:
        deduct(5, "Slow TTFB")
    if tech["content_length"] > 2 * 1024 * 1024:
        deduct(4, "Large page size")
    if not tech["hsts"] and urlparse(report["url"]).scheme == "https":
        deduct(2, "Missing HSTS")
    if not tech["x_content_type_options"]:
        deduct(1, "Missing X-Content-Type-Options")
    if not tech["x_frame_options"]:
        deduct(1, "Missing X-Frame-Options")
    if not tech["referrer_policy"]:
        deduct(1, "Missing Referrer-Policy")
    if not tech["csp"]:
        deduct(1, "Missing CSP")

    # Robots/Sitemap
    rs = report["robots_sitemap"]
    if rs["robots_txt"] != "Present":
        deduct(2, "Missing robots.txt")
    if rs["sitemap"] != "Present":
        deduct(2, "Missing sitemap.xml")

    return {"overall": max(score, 0), "deductions": deductions}


def seo_audit(url: str, max_links: int = 25, workers: int = 10) -> Dict[str, Any]:
    url = _ensure_url_scheme(url.strip())
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    report: Dict[str, Any] = {
        "url": url,
        "on_page": {},
        "social_structured": {},
        "links": {},
        "technical": {},
        "robots_sitemap": {},
        "recommendations": [],
    }

    response, err, elapsed = _fetch(url, timeout=15)
    if not response:
        report["technical"] = {"error": err}
        report["recommendations"].append(f"Could not fetch website: {err}")
        report["score"] = {"overall": 0, "deductions": ["Critical: site unreachable"]}
        return report

    if response.status_code >= 400:
        report["technical"] = {"status_code": response.status_code, "response_time_ms": int(elapsed * 1000)}
        report["recommendations"].append(f"Website returned status code {response.status_code}. Check server health.")
        report["score"] = {"overall": 0, "deductions": ["Critical: HTTP error"]}
        return report

    soup = _soupify(response.text)

    # On-page checks
    title, title_info = _check_title(soup, report["recommendations"])
    desc, desc_info = _check_meta_description(soup, report["recommendations"])
    h1s, h1_info = _check_h1(soup, report["recommendations"])
    missing_alts, img_info = _check_images(soup, report["recommendations"])
    canonical, canonical_info = _check_canonical(url, soup, report["recommendations"])
    has_viewport = _check_viewport(soup, report["recommendations"])
    robots_meta = _check_meta_robots(soup, report["recommendations"])
    lang_charset = _check_lang_and_charset(soup, report["recommendations"])
    hreflangs = _check_hreflang(url, soup, report["recommendations"])

    report["on_page"] = {
        "title": title,
        "title_info": title_info,
        "meta_description": desc,
        "meta_description_info": desc_info,
        "h1_tags": h1s,
        "h1_info": h1_info,
        "images_missing_alt": missing_alts,
        "images_info": img_info,
        "canonical": canonical,
        "canonical_info": canonical_info,
        "has_viewport_meta": has_viewport,
        "meta_robots": robots_meta,
        "lang_charset": lang_charset,
        "hreflang": hreflangs,
    }

    # Social and structured data
    report["social_structured"] = _check_social_and_structured(soup, report["recommendations"])

    # Technical headers and perf
    report["technical"] = _check_technical_headers(url, response, elapsed, report["recommendations"])

    # Robots / Sitemap
    report["robots_sitemap"] = _check_robots_and_sitemap(base_url, report["recommendations"])

    # Links
    report["links"] = _check_links(url, soup, max_links, report["recommendations"], workers)

    # Score
    report["score"] = _score(report)
    report["analysis_time"] = elapsed # Add analysis time to report
    report["workers_used"] = workers # Add workers used to report

    return report


def _render_html(report: Dict[str, Any]) -> str:
    def esc(s: Any) -> str:
        try:
            return str(s).replace("<&", "").replace("<", "&lt;").replace(">", "&gt;")
        except Exception:
            return ""

    rec_items = "".join(f"<li>{esc(r)}</li>" for r in report.get("recommendations", []))
    broken_internal = report.get("links", {}).get("broken_internal", [])
    broken_external = report.get("links", {}).get("broken_external", [])
    redirects = report.get("links", {}).get("redirects", [])

    # Visualization metrics
    tech = report.get("technical", {})
    onp = report.get("on_page", {})
    social = report.get("social_structured", {})
    links = report.get("links", {})

    ttfb_ms = int(tech.get("response_time_ms") or 0)
    content_len = int(tech.get("content_length") or 0)
    size_mb = round(content_len / (1024 * 1024), 2)
    missing_alts_cnt = len(onp.get("images_missing_alt", []) or [])
    h1_count = len(onp.get("h1_tags", []) or [])
    security_headers_cnt = int(bool(tech.get("x_content_type_options"))) + int(bool(tech.get("x_frame_options"))) + int(bool(tech.get("referrer_policy"))) + int(bool(tech.get("csp")))
    social_cnt = int(bool(social.get("open_graph"))) + int(bool(social.get("twitter_card")))
    broken_total = len(broken_internal) + len(broken_external)
    redirects_count = len(redirects)
    checked_total = int(links.get("internal_count", 0)) + int(links.get("external_count", 0))
    valid_count = max(checked_total - broken_total - redirects_count, 0)

    # Targets for comparison
    target_ttfb_ms = 800
    target_size_mb = 1.0
    target_missing_alts = 0
    target_h1_count = 1
    target_security_headers = 4
    target_social = 2
    target_broken = 0
    target_redirects = 2

    def link_rows(items: List[Tuple[str, int]]) -> str:
        return "".join(f"<tr><td>{esc(u)}</td><td>{code}</td></tr>" for (u, code) in items)

    html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
<title>SEO Audit Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #222; }}
h1 {{ font-size: 24px; margin-bottom: 8px; }}
h2 {{ font-size: 18px; margin-top: 24px; }}
code, pre {{ background: #f6f8fa; padding: 2px 4px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; font-size: 14px; }}
th {{ background: #fafafa; text-align: left; }}
.score {{ font-size: 32px; font-weight: bold; }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; background: #eef; margin-left: 8px; }}
.charts {{ display: grid; grid-template-columns: 1fr; gap: 16px; }}
.charts .card {{ background:#fff; border:1px solid #eee; border-radius:8px; padding:12px; }}
</style>
</head>
<body>
  <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>
  <h1>SEO Audit Report <span class=\"badge\">{esc(report.get('url'))}</span></h1>
  <div class=\"score\">Score: {report.get('score', {}).get('overall', 0)}</div>

  <div style=\"background:#f0f9ff; border:1px solid #bae6fd; border-radius:8px; padding:16px; margin:16px 0;\">
    <h3 style=\"margin:0 0 8px 0; color:#0369a1;\">⚡ Performance Analysis</h3>
    <div style=\"display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:12px;\">
      <div><strong>Analysis Time:</strong> {report.get('analysis_time', 0):.1f} seconds</div>
      <div><strong>Workers Used:</strong> {report.get('workers_used', 10)} concurrent</div>
      <div><strong>Fast Mode:</strong> {'Yes' if report.get('fast_mode') else 'No'}</div>
      <div><strong>Links Checked:</strong> {int(report.get('links', {}).get('internal_count', 0)) + int(report.get('links', {}).get('external_count', 0))}</div>
    </div>
  </div>

  <h2>Visualizations</h2>
  <div class=\"charts\">
    <div class=\"card\">
      <h3 style=\"margin:0 0 8px 0;\">Benchmarks vs Your Page</h3>
      <canvas id=\"barMetrics\"></canvas>
    </div>
    <div class=\"card\">
      <h3 style=\"margin:0 0 8px 0;\">Link Health</h3>
      <canvas id=\"pieLinks\"></canvas>
    </div>
  </div>

  <h2>On-page</h2>
  <table>
    <tr><th>Title</th><td>{esc(report.get('on_page', {}).get('title'))}</td></tr>
    <tr><th>Meta Description</th><td>{esc(report.get('on_page', {}).get('meta_description'))}</td></tr>
    <tr><th>H1</th><td>{esc(', '.join(report.get('on_page', {}).get('h1_tags', [])))}</td></tr>
    <tr><th>Canonical</th><td>{esc(report.get('on_page', {}).get('canonical'))}</td></tr>
    <tr><th>Viewport Meta</th><td>{'Yes' if report.get('on_page', {}).get('has_viewport_meta') else 'No'}</td></tr>
    <tr><th>Images Missing Alt</th><td>{len(report.get('on_page', {}).get('images_missing_alt', []))}</td></tr>
    <tr><th>Lang/Charset</th><td>{esc(report.get('on_page', {}).get('lang_charset'))}</td></tr>
  </table>

  <h2>Social & Structured Data</h2>
  <table>
    <tr><th>Open Graph</th><td>{'Present' if report.get('social_structured', {}).get('open_graph') else 'Missing'}</td></tr>
    <tr><th>Twitter Card</th><td>{'Present' if report.get('social_structured', {}).get('twitter_card') else 'Missing'}</td></tr>
    <tr><th>JSON-LD Blocks</th><td>{report.get('social_structured', {}).get('json_ld_blocks')}</td></tr>
    <tr><th>JSON-LD Errors</th><td>{report.get('social_structured', {}).get('json_ld_errors')}</td></tr>
  </table>

  <h2>Technical</h2>
  <table>
    <tr><th>Status</th><td>{report.get('technical', {}).get('status_code')}</td></tr>
    <tr><th>Response Time (ms)</th><td>{report.get('technical', {}).get('response_time_ms')}</td></tr>
    <tr><th>Content Length</th><td>{report.get('technical', {}).get('content_length')}</td></tr>
    <tr><th>Gzip/Brotli</th><td>{'Yes' if report.get('technical', {}).get('gzip') else 'No'}</td></tr>
    <tr><th>HSTS</th><td>{'Yes' if report.get('technical', {}).get('hsts') else 'No'}</td></tr>
    <tr><th>Security Headers</th><td>
      X-Content-Type-Options: {'Yes' if report.get('technical', {}).get('x_content_type_options') else 'No'}<br/>
      X-Frame-Options: {'Yes' if report.get('technical', {}).get('x_frame_options') else 'No'}<br/>
      Referrer-Policy: {'Yes' if report.get('technical', {}).get('referrer_policy') else 'No'}<br/>
      CSP: {'Yes' if report.get('technical', {}).get('csp') else 'No'}
    </td></tr>
  </table>

  <h2>Robots & Sitemap</h2>
  <table>
    <tr><th>robots.txt</th><td>{report.get('robots_sitemap', {}).get('robots_txt')}</td></tr>
    <tr><th>sitemap.xml</th><td>{report.get('robots_sitemap', {}).get('sitemap')}</td></tr>
    <tr><th>Notes</th><td>{esc(', '.join(report.get('robots_sitemap', {}).get('robots_notes', [])))}</td></tr>
  </table>

  <h2>Links</h2>
  <table>
    <tr><th>Internal Links Checked</th><td>{report.get('links', {}).get('internal_count')}</td></tr>
    <tr><th>External Links Checked</th><td>{report.get('links', {}).get('external_count')}</td></tr>
  </table>

  <h3>Broken Internal</h3>
  <table><tr><th>URL</th><th>Status</th></tr>{link_rows(broken_internal)}</table>
  <h3>Broken External</h3>
  <table><tr><th>URL</th><th>Status</th></tr>{link_rows(broken_external)}</table>
  <h3>Redirects</h3>
  <table><tr><th>URL</th><th>Status</th></tr>{link_rows(redirects)}</table>

  <h2>Recommendations</h2>
  <ul>{rec_items}</ul>

  <script>
    (function() {{
      const barCtx = document.getElementById('barMetrics').getContext('2d');
      const pieCtx = document.getElementById('pieLinks').getContext('2d');

      const labels = ['TTFB (ms)', 'Page size (MB)', 'Missing alts', 'H1 count', 'Security headers', 'Social tags', 'Broken links', 'Redirects'];
      const userData = [{ttfb_ms}, {size_mb}, {missing_alts_cnt}, {h1_count}, {security_headers_cnt}, {social_cnt}, {broken_total}, {redirects_count}];
      const targetData = [{target_ttfb_ms}, {target_size_mb}, {target_missing_alts}, {target_h1_count}, {target_security_headers}, {target_social}, {target_broken}, {target_redirects}];

      new Chart(barCtx, {{
        type: 'bar',
        data: {{
          labels: labels,
          datasets: [
            {{ label: 'Your page', data: userData, backgroundColor: 'rgba(37, 99, 235, 0.7)' }},
            {{ label: 'Best practice', data: targetData, backgroundColor: 'rgba(16, 185, 129, 0.5)' }}
          ]
        }},
        options: {{
          responsive: true,
          scales: {{
            y: {{ beginAtZero: true }}
          }},
          plugins: {{
            legend: {{ position: 'top' }}
          }}
        }}
      }});

      const valid = {valid_count};
      const broken = {broken_total};
      const redirects = {redirects_count};
      new Chart(pieCtx, {{
        type: 'pie',
        data: {{
          labels: ['Valid', 'Broken', 'Redirects'],
          datasets: [{{
            data: [valid, broken, redirects],
            backgroundColor: ['#22c55e', '#ef4444', '#f59e0b']
          }}]
        }},
        options: {{ responsive: true }}
      }});
    }})();
  </script>

</body>
</html>
"""
    return html


def _clean_old_reports(out_dir: str) -> int:
    removed = 0
    try:
        pattern = os.path.join(out_dir, "seo_report_*.*")
        for path in glob.glob(pattern):
            try:
                os.remove(path)
                removed += 1
            except Exception:
                pass
    except Exception:
        pass
    return removed


def _truncate(text: Optional[str], max_len: int) -> Optional[str]:
    if text is None:
        return None
    text_str = str(text)
    return text_str if len(text_str) <= max_len else text_str[: max_len - 1] + "…"


def _build_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    links = report.get("links", {})
    onp = report.get("on_page", {})
    tech = report.get("technical", {})
    social = report.get("social_structured", {})
    rs = report.get("robots_sitemap", {})
    recs = report.get("recommendations", [])

    return {
        "url": report.get("url"),
        "score": report.get("score", {}).get("overall"),
        "status": {
            "code": tech.get("status_code"),
            "response_time_ms": tech.get("response_time_ms"),
            "size_bytes": tech.get("content_length"),
        },
        "on_page": {
            "title": _truncate(onp.get("title"), 70),
            "meta_description_len": (len(onp.get("meta_description", "")) if onp.get("meta_description") else 0),
            "h1_count": len(onp.get("h1_tags", [])),
            "images_missing_alt": len(onp.get("images_missing_alt", [])),
            "canonical_present": onp.get("canonical") is not None,
            "viewport": onp.get("has_viewport_meta", False),
            "noindex": onp.get("meta_robots", {}).get("noindex", False),
            "nofollow": onp.get("meta_robots", {}).get("nofollow", False),
        },
        "links": {
            "internal_checked": links.get("internal_count", 0),
            "external_checked": links.get("external_count", 0),
            "broken_internal": len(links.get("broken_internal", [])),
            "broken_external": len(links.get("broken_external", [])),
            "redirects": len(links.get("redirects", [])),
        },
        "social_structured": {
            "open_graph": social.get("open_graph", False),
            "twitter_card": social.get("twitter_card", False),
            "json_ld_blocks": social.get("json_ld_blocks", 0),
            "json_ld_errors": social.get("json_ld_errors", 0),
        },
        "robots_sitemap": {
            "robots_txt": rs.get("robots_txt"),
            "sitemap": rs.get("sitemap"),
        },
        "top_recommendations": recs[:5],
    }


def _serve_web(host: str, port: int, default_max_links: int) -> None:
    try:
        from flask import Flask, request
    except Exception as exc:
        print("Flask is required for web UI. Install with: pip install flask")
        print(f"Error: {exc}")
        return

    app = Flask(__name__)

    PAGE_TEMPLATE = (
        """
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Fast SEO Checker</title>
  <style>
    :root { --bg:#f6f8fb; --card:#fff; --muted:#6b7280; --text:#111827; --pri:#2563eb; --pri2:#3b82f6; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Ubuntu, 'Helvetica Neue', Arial, 'Noto Sans'; color: var(--text); background: linear-gradient(180deg,#f8fafc,#f6f8fb); }
    .nav { background:#0f172a; color:#e5e7eb; padding:14px 20px; display:flex; align-items:center; justify-content:flex-start; gap:12px; }
    .nav .brand { font-weight:600; letter-spacing:0.3px; }
    .nav a { color:#cbd5e1; text-decoration:none; margin-left:14px; }
    .container { max-width: 1080px; margin: 24px auto; padding: 0 16px; }
    .hero { display:flex; align-items:center; justify-content:space-between; gap:24px; margin-bottom:16px; }
    .hero h1 { margin:0; font-size:28px; }
    .card { background: var(--card); border-radius:12px; box-shadow: 0 1px 3px rgba(0,0,0,0.07); padding:18px; }
    form .row { display:flex; flex-wrap:wrap; gap:12px; align-items:flex-end; }
    label { font-size:12px; color: var(--muted); display:block; margin-bottom:6px; }
    input[type=text], input[type=number], select { border:1px solid #e5e7eb; border-radius:8px; padding:10px 12px; width: 360px; max-width:100%; box-shadow: 0 1px 0 rgba(0,0,0,0.02) inset; }
    button { background: linear-gradient(180deg,var(--pri),var(--pri2)); color:#fff; border:none; padding:10px 14px; border-radius:8px; cursor:pointer; box-shadow: 0 6px 16px rgba(37,99,235,0.25); }
    button:hover { filter: brightness(0.97); }
    .grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(220px,1fr)); gap:12px; }
    .kpi { border:1px solid #e5e7eb; border-radius:10px; padding:12px; background:#fff; }
    .kpi h3 { margin:0 0 6px 0; font-size:14px; color: var(--muted); }
    .kpi .val { font-size:20px; font-weight:600; }
    .section { margin-top:18px; }
    .pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; background:#eef2ff; color:#3730a3; }
    .list { margin:0; padding-left:18px; }
    .list li { margin:4px 0; }
    .footer { color: var(--muted); font-size:12px; text-align:center; margin: 24px 0; }
    .two-col { display:grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); gap: 12px; align-items:start; }
    .opt-item { border:1px solid #e5e7eb; border-radius:10px; padding:10px 12px; margin: 8px 0; background:#fff; }
    .opt-item h4 { margin:0 0 6px 0; font-size:14px; }
    .opt-item .badge { display:inline-block; font-size:11px; padding:2px 6px; border-radius:999px; background:#f1f5f9; color:#0f172a; margin-left:6px; }
    .opt-item ul { margin: 6px 0 0 18px; padding:0; }
    .muted { color: var(--muted); font-size:12px; }
    .progress { background:#f1f5f9; border-radius:8px; height:8px; overflow:hidden; margin:12px 0; }
    .progress-bar { background:linear-gradient(90deg,var(--pri),var(--pri2)); height:100%; width:0%; transition:width 0.3s ease; }
    .status { font-size:14px; color:var(--muted); margin:8px 0; }
    .performance-info { background:#f0f9ff; border:1px solid #bae6fd; border-radius:8px; padding:12px; margin:12px 0; }
    .performance-info h4 { margin:0 0 8px 0; color:#0369a1; }
    @media (max-width: 600px) { .hero { flex-direction:column; align-items:flex-start; } }
  </style>
  <script>
    window.addEventListener('DOMContentLoaded', function() {
      var url = document.getElementById('url');
      if (url) {
        url.addEventListener('input', function() {
          var r = document.getElementById('result');
          if (r) { r.innerHTML = ''; }
        });
      }
    });
    
    function showProgress() {
      document.getElementById('progress').style.display = 'block';
      document.getElementById('analyzeBtn').disabled = true;
      document.getElementById('analyzeBtn').textContent = 'Analyzing...';
      
      // Simulate progress bar
      var bar = document.getElementById('progressBar');
      var width = 0;
      var interval = setInterval(function() {
        if (width >= 90) {
          clearInterval(interval);
        } else {
          width++;
          bar.style.width = width + '%';
        }
      }, 100);
    }
  </script>
  </head>
  <body>
    <div class=\"nav\"> 
      <div class=\"brand\">Fast SEO Checker</div>
    </div>
    <div class=\"container\">
      <div class=\"hero\"> 
        <div>
          <h1>Fast SEO & Technical Analysis</h1>
          <p>Parallel processing for quick results. Enter a URL to get instant analysis.</p>
          <div style=\"background:#f0f9ff; border:1px solid #bae6fd; border-radius:8px; padding:12px; margin-top:12px; font-size:14px;\">
            <strong>🚀 Performance Features:</strong> Parallel link checking (5-10x faster), smart link sampling, configurable workers, fast mode for instant results.
          </div>
        </div>
      </div>
      <div class=\"card\">
        <form method=\"post\" action=\"/\" onsubmit=\"showProgress()\">
          <div class=\"row\">
            <div>
              <label for=\"url\">Website URL</label>
              <input id=\"url\" name=\"url\" type=\"text\" placeholder=\"https://example.com or example.com\" value=\"__URL_VALUE__\" required />
            </div>
            <div>
              <label for=\"max_links\">Max links to check</label>
              <input id=\"max_links\" name=\"max_links\" type=\"number\" min=\"0\" max=\"200\" value=\"__MAX_LINKS__\" />
            </div>
            <div>
              <label for=\"workers\">Concurrent workers</label>
              <input id=\"workers\" name=\"workers\" type=\"number\" min=\"1\" max=\"20\" value=\"__WORKERS__\" />
            </div>
            <div>
              <label for=\"fast_mode\">Fast mode</label>
              <input id=\"fast_mode\" name=\"fast_mode\" type=\"checkbox\" value=\"1\" />
              <span class=\"muted\">Skip link checking</span>
            </div>
            <div>
              <button id=\"analyzeBtn\" type=\"submit\">Analyze</button>
            </div>
          </div>
        </form>
        
        <div id=\"progress\" style=\"display:none;\">
          <div class=\"status\">Analyzing website...</div>
          <div class=\"progress\">
            <div id=\"progressBar\" class=\"progress-bar\"></div>
          </div>
        </div>
      </div>

      <div id=\"result\">__RESULT_SECTION__</div>

      <div class=\"footer\">© 2025 - Fast SEO Checker with Parallel Processing</div>
    </div>
  </body>
 </html>
"""
    )

    def _build_optimizer(report: Dict[str, Any]) -> List[Dict[str, Any]]:
        suggestions: List[Dict[str, Any]] = []
        onp = report.get("on_page", {})
        tech = report.get("technical", {})
        links = report.get("links", {})
        social = report.get("social_structured", {})
        rs = report.get("robots_sitemap", {})

        def add(title: str, priority: str, steps: List[str]):
            suggestions.append({"title": title, "priority": priority, "steps": steps})

        # Title
        title_info = onp.get("title_info", {})
        title_len = title_info.get("length")
        if title_info.get("issues"):
            issues_text = ", ".join(title_info.get("issues", []))
            add(
                "Optimize <title> tag",
                "High",
                [
                    f"Current issues: {issues_text} (length: {title_len})",
                    "Target ~50–60 chars; include primary keyword and brand when appropriate",
                ],
            )

        # Meta description
        desc_info = onp.get("meta_description_info", {})
        desc_len = desc_info.get("length")
        if desc_info.get("issues") or not onp.get("meta_description"):
            issue_note = "Missing" if not onp.get("meta_description") else ", ".join(desc_info.get("issues", []))
            add(
                "Write/adjust meta description",
                "High",
                [
                    f"Current status: {issue_note} (length: {desc_len})",
                    "Aim for 120–160 chars with a clear value proposition",
                    "Add <meta name=\"description\" content=\"...\"> in <head>",
                ],
            )

        # H1
        h1_info = onp.get("h1_info", {})
        h1_count = h1_info.get("count", 0)
        h1_issues = h1_info.get("issues", [])
        if h1_issues:
            add(
                "Fix H1 usage",
                "High",
                [
                    f"Current H1 count: {h1_count}",
                    "Use exactly one descriptive H1 matching page intent",
                ],
            )

        # Image alts
        missing_alts = onp.get("images_missing_alt", []) or []
        if missing_alts:
            sample = ", ".join(missing_alts[:5])
            add(
                "Add descriptive alt text to images",
                "Medium",
                [
                    f"Missing alt on {len(missing_alts)} images",
                    f"Examples: {sample}" if sample else "",
                    "Describe image purpose; avoid keyword stuffing",
                ],
            )

        # Viewport
        if not onp.get("has_viewport_meta"):
            add(
                "Add responsive viewport meta tag",
                "Medium",
                ["Add <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> in <head>"],
            )

        # Canonical
        canonical_info = onp.get("canonical_info", {})
        if canonical_info.get("issues") or not onp.get("canonical"):
            details = ", ".join(canonical_info.get("issues", [])) or "Missing canonical"
            add(
                "Add/validate canonical link",
                "Medium",
                [
                    f"Current: {details}",
                    "Include <link rel=\"canonical\" href=\"<absolute URL>\"> in <head>",
                    "Ensure canonical points to same domain and returns 200",
                ],
            )

        # Robots meta
        robots_meta = onp.get("meta_robots", {})
        if robots_meta.get("noindex") or robots_meta.get("nofollow"):
            flags = ", ".join([flag for flag in ["noindex" if robots_meta.get("noindex") else None, "nofollow" if robots_meta.get("nofollow") else None] if flag])
            add(
                "Adjust robots meta",
                "High",
                [
                    f"Current flags: {flags}",
                    "Remove noindex/nofollow on pages that should rank",
                ],
            )

        # Lang/charset
        lc = onp.get("lang_charset", {})
        if not lc.get("lang") or not lc.get("charset"):
            missing = [k for k in ["lang" if not lc.get("lang") else None, "charset" if not lc.get("charset") else None] if k]
            add(
                "Set language and charset",
                "Low",
                [
                    f"Missing: {', '.join(missing)}",
                    "Add lang on <html> (e.g., lang=\"en\"); ensure <meta charset=\"UTF-8\">",
                ],
            )

        # Social tags
        if not social.get("open_graph") or not social.get("twitter_card"):
            missing = [lab for lab, ok in [("Open Graph", social.get("open_graph")), ("Twitter Card", social.get("twitter_card"))] if not ok]
            add(
                "Add social sharing meta tags",
                "Low",
                [
                    f"Missing: {', '.join(missing)}",
                    "Add og:title, og:description, og:image, og:url and twitter:card, twitter:title, twitter:description, twitter:image",
                ],
            )

        # JSON-LD
        if social.get("json_ld_errors", 0) > 0:
            add(
                "Fix JSON-LD errors",
                "Medium",
                [
                    f"Invalid JSON-LD blocks: {social.get('json_ld_errors')}",
                    "Validate at validator.schema.org; ensure proper @context/@type",
                ],
            )

        # Broken links
        broken_int = links.get("broken_internal") or []
        broken_ext = links.get("broken_external") or []
        if broken_int or broken_ext:
            step_lines: List[str] = []
            if broken_int:
                examples = "; ".join([f"{u} ({c})" for u, c in broken_int[:5]])
                step_lines.append(f"Internal broken: {len(broken_int)}. Examples: {examples}")
            if broken_ext:
                examples = "; ".join([f"{u} ({c})" for u, c in broken_ext[:5]])
                step_lines.append(f"External broken: {len(broken_ext)}. Examples: {examples}")
            step_lines.extend(["Fix URLs or add 301 redirects to final destinations"]) 
            add("Resolve broken links", "High", step_lines)

        # Performance
        rtt = tech.get("response_time_ms", 0) or 0
        if rtt > 1500:
            add(
                "Improve server response time (TTFB)",
                "High",
                [
                    f"Measured TTFB: {rtt} ms",
                    "Enable CDN and caching; review backend hotspots and DB queries",
                    "Defer non-critical JS; preconnect/preload critical resources",
                ],
            )

        # Page weight
        size_b = tech.get("content_length", 0) or 0
        if size_b > 2 * 1024 * 1024:
            mb = round(size_b / (1024 * 1024), 2)
            add(
                "Reduce total page size",
                "Medium",
                [
                    f"Current size: {mb} MB (> 2MB)",
                    "Compress/resize images (WebP/AVIF); minify CSS/JS; lazy-load",
                ],
            )

        # Security headers
        missing_sec: List[str] = []
        if not tech.get("x_content_type_options"):
            missing_sec.append("X-Content-Type-Options: nosniff")
        if not tech.get("x_frame_options"):
            missing_sec.append("X-Frame-Options")
        if not tech.get("referrer_policy"):
            missing_sec.append("Referrer-Policy")
        if not tech.get("csp"):
            missing_sec.append("Content-Security-Policy")
        if missing_sec:
            add(
                "Set recommended security headers",
                "Low",
                [
                    f"Missing: {', '.join(missing_sec)}",
                    "Configure at web server/CDN (Nginx/Apache) or app middleware",
                ],
            )

        # HSTS
        if (report.get("url", "").startswith("https") and not tech.get("hsts")):
            add(
                "Enable HSTS",
                "Low",
                [
                    "Add Strict-Transport-Security response header (includeSubDomains; preload optional)",
                ],
            )

        # robots.txt / sitemap
        if rs.get("robots_txt") != "Present":
            add(
                "Create robots.txt",
                "Low",
                [
                    "Add robots.txt at /robots.txt",
                    "Reference sitemap with `Sitemap: https://example.com/sitemap.xml`",
                ],
            )
        if rs.get("sitemap") != "Present":
            add(
                "Provide XML sitemap",
                "Low",
                [
                    "Generate sitemap.xml and host at /sitemap.xml",
                    "Submit in Google Search Console and reference in robots.txt",
                ],
            )

        # Prioritize: High > Medium > Low
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        suggestions.sort(key=lambda s: priority_order.get(s.get("priority", "Medium"), 1))
        return suggestions[:12]

    def _render_optimizer(suggestions: List[Dict[str, Any]]) -> str:
        if not suggestions:
            return "<div class=\"card\"><div class=\"muted\">No major issues detected.</div></div>"
        parts: List[str] = []
        parts.append("<div class=\"card\">")
        parts.append("  <h3 style=\"margin:0 0 10px 0;\">Optimizer</h3>")
        for s in suggestions:
            steps = "".join(f"<li>{st}</li>" for st in s.get("steps", []))
            parts.append(
                f"  <div class=\"opt-item\"><h4>{s.get('title')}<span class=\"badge\">{s.get('priority')}</span></h4><ul>{steps}</ul></div>"
            )
        parts.append("</div>")
        return "".join(parts)

    def _render_results_section(summary: Optional[Dict[str, Any]], full_link: Optional[str], report: Dict[str, Any]) -> str:
        if not summary:
            return ""
        def yn(flag: bool) -> str:
            return "Yes" if flag else "No"
        parts: List[str] = []
        parts.append("<div class=\"section two-col\">")
        parts.append("  <div class=\"card\">")
        parts.append("    <div style=\"display:flex;align-items:center;justify-content:space-between;gap:12px;\">")
        parts.append(f"      <div class=\"pill\">Score: {summary.get('score')}</div>")
        if full_link:
            parts.append(f"      <a href=\"{full_link}\" target=\"_blank\" style=\"text-decoration:none\"><button type=\"button\">Open Full Report</button></a>")
        parts.append("    </div>")
        
        # Add performance info if available
        if 'analysis_time' in report:
            parts.append(f"    <div class=\"performance-info\">")
            parts.append(f"      <h4>⚡ Performance Analysis</h4>")
            parts.append(f"      <div>Analysis completed in {report.get('analysis_time', 0):.1f} seconds</div>")
            if report.get('links', {}).get('internal_count', 0) == 0:
                parts.append(f"      <div>Fast mode: Link checking skipped for speed</div>")
            else:
                parts.append(f"      <div>Parallel processing: {report.get('workers_used', 10)} concurrent workers</div>")
            parts.append(f"    </div>")
        
        parts.append("    <div class=\"grid\" style=\"margin-top:12px;\">")
        parts.append(f"      <div class=\"kpi\"><h3>Status</h3><div class=\"val\">{summary.get('status',{}).get('code')}</div><div class=\"muted\">{summary.get('status',{}).get('response_time_ms')} ms</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>Title</h3><div class=\"val\">{summary.get('on_page',{}).get('title')}</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>H1 Count</h3><div class=\"val\">{summary.get('on_page',{}).get('h1_count')}</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>Missing Alts</h3><div class=\"val\">{summary.get('on_page',{}).get('images_missing_alt')}</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>Links Broken</h3><div class=\"val\">{summary.get('links',{}).get('broken_internal')} in / {summary.get('links',{}).get('broken_external')} ex</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>Robots.txt</h3><div class=\"val\">{summary.get('robots_sitemap',{}).get('robots_txt')}</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>Sitemap</h3><div class=\"val\">{summary.get('robots_sitemap',{}).get('sitemap')}</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>Open Graph</h3><div class=\"val\">{yn(summary.get('social_structured',{}).get('open_graph'))}</div></div>")
        parts.append(f"      <div class=\"kpi\"><h3>Twitter Card</h3><div class=\"val\">{yn(summary.get('social_structured',{}).get('twitter_card'))}</div></div>")
        parts.append("    </div>")
        rec_items = "".join(f"<li>{r}</li>" for r in (summary.get("top_recommendations", []) or []))
        if rec_items:
            parts.append(f"    <div class=\"section\" style=\"margin-top:14px;\"><h3>Top recommendations</h3><ul class=\"list\">{rec_items}</ul></div>")
        parts.append("  </div>")
        # Right column: optimizer panel
        suggestions = _build_optimizer(report)
        parts.append("  <div>")
        parts.append(_render_optimizer(suggestions))
        parts.append("  </div>")
        parts.append("</div>")
        return "".join(parts)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "GET":
            return PAGE_TEMPLATE.replace("__MAX_LINKS__", str(default_max_links)).replace("__URL_VALUE__", "").replace("__WORKERS__", "10").replace("__RESULT_SECTION__", "")
        target_url = (request.form.get("url") or "").strip()
        try:
            max_links = int(request.form.get("max_links") or default_max_links)
            workers = int(request.form.get("workers") or 10)
            fast_mode = request.form.get("fast_mode") == "1"
        except Exception:
            max_links = default_max_links
            workers = 10
            fast_mode = False
        if not target_url:
            return PAGE_TEMPLATE.replace("__MAX_LINKS__", str(max_links)).replace("__URL_VALUE__", "").replace("__WORKERS__", str(workers)).replace("__RESULT_SECTION__", "")
        
        # Apply fast mode
        if fast_mode:
            max_links = 0
        
        # Cap workers
        workers = min(workers, 20)
        
        start_time = time.time()
        report = seo_audit(target_url, max_links=max_links, workers=workers)
        elapsed = time.time() - start_time
        
        report["analysis_time"] = elapsed
        report["workers_used"] = workers
        report["fast_mode"] = fast_mode
        
        
        link = f"/full?url={requests.utils.quote(target_url, safe='')}&max_links={max_links}&workers={workers}&fast_mode={fast_mode}"
        summary = _build_summary(report)
        results_html = _render_results_section(summary, link, report)
        return PAGE_TEMPLATE.replace("__MAX_LINKS__", str(max_links)).replace("__URL_VALUE__", "").replace("__WORKERS__", str(workers)).replace("__RESULT_SECTION__", results_html)

    @app.get("/full")
    def full():
        target_url = (request.args.get("url") or "").strip()
        try:
            max_links = int(request.args.get("max_links") or default_max_links)
            workers = int(request.args.get("workers") or 10)
            fast_mode = request.args.get("fast_mode") == "1"
        except Exception:
            max_links = default_max_links
            workers = 10
            fast_mode = False
        if not target_url:
            return "Missing url query parameter", 400
        
        # Apply fast mode
        if fast_mode:
            max_links = 0
        
        # Cap workers
        workers = min(workers, 20)
        
        start_time = time.time()
        report = seo_audit(target_url, max_links=max_links, workers=workers)
        elapsed = time.time() - start_time
        
        # Add timing info to report
        report["analysis_time"] = elapsed
        report["workers_used"] = workers
        report["fast_mode"] = fast_mode
        
        return _render_html(report)

    print(f"Starting web UI on http://{host}:{port}")
    app.run(host=host, port=port)

def main():
    parser = argparse.ArgumentParser(description="Fast SEO/Technical web audit tool with parallel processing")
    parser.add_argument("url", nargs="?", help="Website URL")
    parser.add_argument("--max-links", type=int, default=25, help="Max internal/external links to check")
    parser.add_argument("--output", choices=["json", "html", "both"], default="both", help="Output format")
    parser.add_argument("--out-dir", default=".", help="Directory to write report files")
    parser.add_argument("--interactive", action="store_true", help="Prompt to manually enter one or more URLs")
    parser.add_argument("--serve", action="store_true", help="Start a simple web UI to run audits")
    parser.add_argument("--host", default="127.0.0.1", help="Host for web UI (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port for web UI (default 5000)")
    parser.add_argument("--summary", action="store_true", help="Print a concise summary instead of full JSON")
    parser.add_argument("--keep-reports", action="store_true", help="Do not delete old seo_report_* files before writing new ones")
    parser.add_argument("--workers", type=int, default=10, help="Number of concurrent workers for link checking (default: 10, max: 20)")
    parser.add_argument("--fast", action="store_true", help="Quick analysis: skip detailed link checking for speed")

    args = parser.parse_args()

    if args.serve:
        _serve_web(args.host, args.port, args.max_links)
        return

    # Build list of URLs to audit
    urls: List[str] = []
    if args.interactive:
        while True:
            entered = input("Enter website URL (blank to finish): ").strip()
            if not entered:
                break
            urls.append(entered)
        if not urls:
            print("No URLs entered. Exiting.")
            return
    else:
        if not args.url:
            single = input("Enter website URL (e.g., https://example.com or example.com): ").strip()
            if not single:
                print("No URL provided. Exiting.")
                return
            urls = [single]
        else:
            urls = [args.url]

    for target_url in urls:
        print(f"Analyzing {target_url}...")
        
        # Use fast mode if requested
        max_links = 0 if args.fast else args.max_links
        workers = min(args.workers, 20)  # Cap at 20 workers
        
        if max_links > 0:
            print(f"Checking up to {max_links} links with {workers} concurrent workers...")
        
        start_time = time.time()
        report = seo_audit(target_url, max_links=max_links, workers=workers)
        elapsed = time.time() - start_time
        
        print(f"Analysis completed in {elapsed:.1f} seconds")
        print(f"Score: {report.get('score', {}).get('overall', 0)}/100")
        print(f"Found {len(report.get('recommendations', []))} recommendations")
        print("-" * 50)

        # Print concise or full JSON to console
        if args.summary:
            print(json.dumps(_build_summary(report), indent=4))
        else:
            print(json.dumps(report, indent=4))

        # Write outputs per URL
        if not args.keep_reports:
            _clean_old_reports(args.out_dir)
        safe_domain = _domain(_ensure_url_scheme(target_url)).replace(":", "_")
        timestamp = str(int(time.time()))
        if args.output in ("json", "both"):
            json_path = f"{args.out_dir}/seo_report_{safe_domain}_{timestamp}.json"
            try:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"Saved JSON report to: {json_path}")
            except Exception as exc:
                print(f"Could not write JSON report: {exc}")
        if args.output in ("html", "both"):
            html_path = f"{args.out_dir}/seo_report_{safe_domain}_{timestamp}.html"
            try:
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(_render_html(report))
                print(f"Saved HTML report to: {html_path}")
            except Exception as exc:
                print(f"Could not write HTML report: {exc}")


if __name__ == "__main__":
    main()
