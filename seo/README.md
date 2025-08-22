# Fast SEO Audit Tool

A **high-performance** SEO and technical audit tool with **parallel processing** that fetches a URL, runs comprehensive checks, scores the page, and generates detailed reports. Features **5-10x faster** analysis through concurrent link checking and smart optimization.

## 🚀 Performance Features

- **Parallel Processing**: Concurrent link checking with configurable workers (1-20)
- **Smart Link Sampling**: Prioritizes important navigation and content links
- **Fast Mode**: Skip link checking for instant results (2-5 seconds)
- **Optimized Timeouts**: Reduced from 5s to 3s for faster failure detection
- **Progress Tracking**: Real-time analysis status and completion timing
- **Resource Optimization**: Balanced CPU/memory usage for stable performance

## ✨ Core Features

- **CLI with summary or full output**
- **Interactive mode for multiple URLs**
- **Local web UI with performance controls**
- **Optimizer panel with prioritized, actionable steps**
- **Data visualizations (bar and pie charts) in HTML reports**
- **Automatic report cleanup and management**

## 🔍 SEO & Technical Checks

### On-page Elements
- Title length and presence (30-60 character optimization)
- Meta description length and presence (120-160 character target)
- H1 count and content validation
- Images missing `alt` text detection
- Canonical link presence and domain consistency
- Viewport meta presence for mobile optimization
- Robots meta (`noindex`, `nofollow`) detection
- Language and charset (`<html lang>`, `<meta charset>`) validation
- Hreflang tags for international SEO

### Social & Structured Data
- Open Graph (og:*) tags for social sharing
- Twitter Card meta tags
- JSON-LD blocks and validation
- Structured data error detection

### Link Analysis
- **Smart sampling** of internal/external links (configurable limit)
- **Parallel processing** for 5-10x faster link checking
- Broken link detection (internal and external)
- Redirect chain identification
- Link health scoring and prioritization

### Technical Performance
- HTTP status code validation
- TTFB (Time To First Byte) measurement
- Page size analysis (Content-Length)
- Compression detection (gzip/brotli/deflate)
- Security headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy, CSP
- HSTS (HTTP Strict Transport Security) validation

### Robots & Sitemap
- robots.txt presence and content analysis
- sitemap.xml availability
- SEO directive validation

## 📊 Scoring & Recommendations

- **100-point scoring system** with category-based deductions
- **Human-readable recommendations** with priority levels
- **Dynamic optimizer panel** with targeted fixes based on actual findings
- **Performance metrics** and analysis timing
- **Link health breakdown** and optimization suggestions

## 📈 Reports & Outputs

### Report Formats
- **JSON**: Console output and file export
- **HTML**: Rich reports with data visualizations
- **Summary Mode**: Concise JSON output for quick review

### Data Visualizations
- **Bar Charts**: Your metrics vs. best-practice targets
- **Pie Charts**: Link health distribution (valid vs. broken vs. redirects)
- **Performance Metrics**: Analysis time, workers used, processing speed

### Best-Practice Targets
- TTFB ≤ 800 ms
- Page size ≤ 1.0 MB
- Missing alt text = 0
- H1 count = 1
- Security headers present = 4
- Social tags present = 2 (Open Graph + Twitter Card)
- Broken links = 0
- Redirects ≤ 2

## 🖥️ Web Interface

### Features
- **Performance Controls**: Adjust workers, max links, fast mode
- **Real-time Progress**: Visual progress bar and status updates
- **Performance Metrics**: Analysis time and processing details
- **Responsive Design**: Mobile-friendly interface
- **Results Clearing**: Automatic cleanup between analyses

### Usage
```bash
# Start web server
python seo_audit.py --serve --host 127.0.0.1 --port 5000

# Open in browser: http://127.0.0.1:5000
```

## 💻 Command Line Interface

### Basic Usage
```bash
# Single URL analysis
python seo_audit.py https://example.com

# Summary mode (concise output)
python seo_audit.py https://example.com --summary

# Interactive mode (multiple URLs)
python seo_audit.py --interactive
```

### Performance Options
```bash
# High-speed analysis with 15 workers
python seo_audit.py https://example.com --workers 15 --max-links 50

# Ultra-fast mode (skip link checking)
python seo_audit.py https://example.com --fast

# Balanced performance (recommended)
python seo_audit.py https://example.com --workers 10 --max-links 25
```

### Advanced Options
```bash
# Custom output directory
python seo_audit.py https://example.com --out-dir reports/

# HTML report only
python seo_audit.py https://example.com --output html

# Keep old reports
python seo_audit.py https://example.com --keep-reports
```

## ⚡ Performance Optimization Guide

### Worker Configuration
- **5-10 workers**: Best for slow networks or limited resources
- **10-15 workers**: **Optimal balance** for most scenarios
- **15-20 workers**: Maximum recommended for high-speed networks
- **20+ workers**: Diminishing returns, may slow down due to overhead

### Fast Mode Scenarios
- **Quick checks**: Use `--fast` for instant results
- **Large sites**: Combine `--fast` with `--summary` for overview
- **Batch processing**: Fast mode for multiple URL screening

### Link Checking Strategy
- **Small sites**: 10-25 links with 10 workers
- **Medium sites**: 25-50 links with 15 workers
- **Large sites**: 50-100 links with 20 workers
- **Enterprise**: 100+ links with 20 workers (max)

## 📦 Requirements

- **Python 3.9+**
- **Dependencies**:
  ```bash
  python -m pip install -r requirements.txt
  ```

### Dependencies
- `requests>=2.31.0` - HTTP client with session management
- `beautifulsoup4>=4.12.2` - HTML parsing and analysis
- `flask>=3.0.0` - Web interface (only needed for `--serve`)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Basic Analysis
```bash
python seo_audit.py https://example.com
```

### 3. Web Interface
```bash
python seo_audit.py --serve
# Open http://127.0.0.1:5000
```

### 4. High-Performance Analysis
```bash
python seo_audit.py https://example.com --workers 15 --max-links 50
```

## 📊 Performance Benchmarks

| Configuration | Links | Workers | Expected Time | Speed Improvement |
|---------------|-------|---------|---------------|-------------------|
| Sequential    | 25    | 1       | ~25 seconds   | 1x (baseline)     |
| Parallel      | 25    | 10      | ~3-5 seconds  | **5-8x faster**   |
| Parallel      | 50    | 15      | ~6-10 seconds | **5-8x faster**   |
| Parallel      | 100   | 20      | ~12-20 seconds| **5-8x faster**   |
| Fast Mode     | 0     | N/A     | ~2-5 seconds  | **10-15x faster** |

## 🔧 Troubleshooting

### Performance Issues
- **Charts not rendering**: Ensure internet access for Chart.js CDN
- **Slow analysis**: Reduce `--workers` to 5-10 for stability
- **Memory issues**: Lower `--max-links` and `--workers`
- **Network errors**: Check firewall and rate limiting

### Common Issues
- **Flask import warning**: Install with `pip install flask`
- **External link failures**: Some sites block automated requests
- **Windows PowerShell**: Retype commands on single lines if wrapping

### Optimization Tips
- **Start with 10 workers**: Best balance of speed and stability
- **Use fast mode**: For quick overviews and large site screening
- **Monitor resources**: Increase workers gradually while monitoring performance
- **Network conditions**: Adjust workers based on internet speed

## 🛡️ Security & Performance Notes

- **Respectful crawling**: Built-in delays and reasonable request rates
- **No JavaScript execution**: Analyzes server-rendered HTML only
- **Configurable limits**: Adjustable workers and link limits
- **Resource management**: Automatic cleanup and memory optimization
- **Rate limiting**: Respects server response codes and delays

## 📝 Examples

### Quick Analysis
```bash
# Fast overview
python seo_audit.py https://example.com --fast --summary

# Performance-focused
python seo_audit.py https://example.com --workers 15 --max-links 50
```

### Batch Processing
```bash
# Multiple sites with progress tracking
python seo_audit.py --interactive --workers 12 --max-links 30
```

### Web Interface
```bash
# Start server with custom settings
python seo_audit.py --serve --host 0.0.0.0 --port 8080
```

## 📄 License

This project is provided as-is for educational and auditing purposes. Review and adapt before production use.

## 🔄 Recent Updates

- **Parallel Processing**: 5-10x faster link analysis
- **Smart Link Sampling**: Prioritizes important links
- **Fast Mode**: Instant results without link checking
- **Performance Controls**: Configurable workers and limits
- **Progress Tracking**: Real-time analysis status
- **Enhanced Web UI**: Performance options and metrics display
- **Resource Optimization**: Balanced performance and stability
