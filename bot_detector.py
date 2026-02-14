"""
Bot Detector
------------
Combines:
- Behavioral features
- Scoring engine
- Classification logic

Produces final structured bot record ready for database insertion.
"""

from scoring_engine import calculate_ai_score, classify_bot


def detect_bot(behavior_profile: dict) -> dict:
    """
    Takes a behavioral profile and returns
    a fully classified bot record.
    """

    # Extract features for scoring
    features = {
        "avg_url_depth": behavior_profile["avg_url_depth"],
        "burst_rate": behavior_profile["burst_rate"],
        "html_ratio": behavior_profile["html_ratio"],
        "repeat_url_ratio": behavior_profile["repeat_url_ratio"],
        "sitemap_hits": behavior_profile["sitemap_hits"]
    }

    # Calculate AI Score
    ai_score = calculate_ai_score(features)

    # Classify bot
    bot_type, confidence_level = classify_bot(ai_score)

    # Return full enriched record
    return {
        "ip_address": behavior_profile["ip_address"],
        "user_agent": behavior_profile["user_agent"],
        "total_requests": behavior_profile["total_requests"],
        "unique_urls": behavior_profile["unique_urls"],
        "avg_url_depth": behavior_profile["avg_url_depth"],
        "burst_rate": behavior_profile["burst_rate"],
        "html_ratio": behavior_profile["html_ratio"],
        "repeat_url_ratio": behavior_profile["repeat_url_ratio"],
        "sitemap_hits": behavior_profile["sitemap_hits"],
        "ai_score": ai_score,
        "bot_type": bot_type,
        "confidence_level": confidence_level,
        "first_seen": behavior_profile["first_seen"],
        "last_seen": behavior_profile["last_seen"]
    }
