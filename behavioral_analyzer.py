"""
Behavioral Analyzer
-------------------
Takes parsed log entries and builds behavioral profiles per bot
(IP + User Agent).

Computes:
- total_requests
- unique_urls
- avg_url_depth
- burst_rate
- html_ratio
- repeat_url_ratio
- sitemap_hits
- first_seen
- last_seen
"""

from collections import defaultdict
from datetime import datetime
from config import (
    BURST_WINDOW_SECONDS,
    NON_HTML_EXTENSIONS,
    SITEMAP_KEYWORDS,
    MIN_REQUEST_THRESHOLD
)


def calculate_url_depth(url: str) -> int:
    if not url or url == "/":
        return 0
    return len([segment for segment in url.split("/") if segment])


def is_html_request(url: str) -> bool:
    return not url.lower().endswith(NON_HTML_EXTENSIONS)


def is_sitemap_request(url: str) -> bool:
    return any(keyword in url.lower() for keyword in SITEMAP_KEYWORDS)


def calculate_burst_rate(timestamps):
    if len(timestamps) < 2:
        return 0.0

    timestamps = sorted(timestamps)
    burst_count = 0

    for i in range(1, len(timestamps)):
        delta = (timestamps[i] - timestamps[i - 1]).total_seconds()
        if delta <= BURST_WINDOW_SECONDS:
            burst_count += 1

    return round(burst_count / len(timestamps), 2)


def analyze_behavior(parsed_logs: list) -> list:
    """
    Returns list of behavioral profiles
    """

    grouped = defaultdict(list)

    # Group logs by (ip, user_agent)
    for entry in parsed_logs:
        key = (entry["ip_address"], entry["user_agent"])
        grouped[key].append(entry)

    behavioral_profiles = []

    for (ip, agent), entries in grouped.items():

        if len(entries) < MIN_REQUEST_THRESHOLD:
            continue

        urls = [e["url"] for e in entries]
        timestamps = [e["timestamp"] for e in entries]

        total_requests = len(entries)
        unique_urls = len(set(urls))
        avg_url_depth = round(
            sum(calculate_url_depth(url) for url in urls) / total_requests,
            2
        )

        burst_rate = calculate_burst_rate(timestamps)

        html_requests = sum(1 for url in urls if is_html_request(url))
        html_ratio = round(html_requests / total_requests, 2)

        repeat_url_ratio = round(
            1 - (unique_urls / total_requests),
            2
        )

        sitemap_hits = sum(
            1 for url in urls if is_sitemap_request(url)
        )

        first_seen = min(timestamps)
        last_seen = max(timestamps)

        behavioral_profiles.append({
            "ip_address": ip,
            "user_agent": agent,
            "total_requests": total_requests,
            "unique_urls": unique_urls,
            "avg_url_depth": avg_url_depth,
            "burst_rate": burst_rate,
            "html_ratio": html_ratio,
            "repeat_url_ratio": repeat_url_ratio,
            "sitemap_hits": sitemap_hits,
            "first_seen": first_seen,
            "last_seen": last_seen
        })

    return behavioral_profiles
