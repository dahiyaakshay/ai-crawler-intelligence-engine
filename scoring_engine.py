"""
Scoring Engine
--------------
Backend authority for AI Retrieval scoring.

This file contains:
- Weight configuration
- Score calculation logic
- Normalization
- Confidence classification

NO database logic.
NO parsing logic.
Pure deterministic intelligence.
"""

from config import SCORING_WEIGHTS


# ==============================
# Score Normalization
# ==============================

def normalize_score(raw_score: float) -> float:
    """
    Normalize raw weighted score to 0–100 range.
    """
    normalized = raw_score * 5  # scale factor
    return max(0.0, min(100.0, round(normalized, 2)))


# ==============================
# AI Score Calculation
# ==============================

def calculate_ai_score(features: dict) -> float:
    """
    Calculate AI Retrieval score based on behavioral features.
    """
    raw_score = (
        features["avg_url_depth"] * SCORING_WEIGHTS["depth"] +
        features["burst_rate"] * SCORING_WEIGHTS["burst"] +
        features["html_ratio"] * SCORING_WEIGHTS["html"] +
        features["repeat_url_ratio"] * SCORING_WEIGHTS["repeat"] +
        features["sitemap_hits"] * SCORING_WEIGHTS["sitemap"]
    )

    return normalize_score(raw_score)


# ==============================
# Classification Logic
# ==============================

def classify_bot(ai_score: float) -> tuple:
    """
    Classify bot based on AI score.

    Returns:
        (bot_type, confidence_level)
    """

    if ai_score >= 60:
        return "AI_Retrieval", "High"

    if 30 <= ai_score < 60:
        return "Suspicious", "Medium"

    return "Indexer", "Low"
