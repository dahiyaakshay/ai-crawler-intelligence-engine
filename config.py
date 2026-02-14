"""
Configuration File
------------------
Central place for:
- Scoring weights
- Behavioral thresholds
- Burst detection window
- Allowed content types
"""

# =========================================
# Scoring Weights (Backend Authority)
# =========================================

SCORING_WEIGHTS = {
    "depth": 2.0,        # AI bots prefer deeper URLs
    "burst": 1.5,        # Burst activity suggests retrieval behavior
    "html": 1.2,         # High HTML ratio indicates content targeting
    "repeat": 1.0,       # Repeated hits to same URLs
    "sitemap": -1.5      # Traditional indexers hit sitemaps
}

# =========================================
# Behavioral Thresholds
# =========================================

# Time window (seconds) to calculate burst rate
BURST_WINDOW_SECONDS = 5

# Minimum requests required to consider a bot valid
MIN_REQUEST_THRESHOLD = 1

# File extensions considered non-HTML (assets)
NON_HTML_EXTENSIONS = (
    ".js",
    ".css",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".webp",
    ".woff",
    ".woff2",
    ".ttf",
    ".map"
)

# URL pattern considered sitemap
SITEMAP_KEYWORDS = (
    "sitemap",
    "robots.txt"
)
