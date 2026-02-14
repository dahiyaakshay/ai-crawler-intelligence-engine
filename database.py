import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(self):
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL not set in environment variables")
        self.conn = psycopg2.connect(DATABASE_URL)
        self.conn.autocommit = True

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)

    # ==========================
    # Upload Operations
    # ==========================

    def create_upload(self, filename: str, total_lines: int):
        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO uploads (filename, total_lines)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (filename, total_lines),
            )
            return cur.fetchone()["id"]

    def update_processed_bots(self, upload_id, processed_bots: int):
        with self.get_cursor() as cur:
            cur.execute(
                """
                UPDATE uploads
                SET processed_bots = %s
                WHERE id = %s;
                """,
                (processed_bots, upload_id),
            )

    # ==========================
    # Bot Operations
    # ==========================

    def insert_bot(self, upload_id: str, bot_data: dict):
        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO bots (
                    upload_id,
                    ip_address,
                    user_agent,
                    total_requests,
                    unique_urls,
                    avg_url_depth,
                    burst_rate,
                    html_ratio,
                    repeat_url_ratio,
                    sitemap_hits,
                    ai_score,
                    bot_type,
                    confidence_level,
                    first_seen,
                    last_seen
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    upload_id,
                    bot_data["ip_address"],
                    bot_data["user_agent"],
                    bot_data["total_requests"],
                    bot_data["unique_urls"],
                    bot_data["avg_url_depth"],
                    bot_data["burst_rate"],
                    bot_data["html_ratio"],
                    bot_data["repeat_url_ratio"],
                    bot_data["sitemap_hits"],
                    bot_data["ai_score"],
                    bot_data["bot_type"],
                    bot_data["confidence_level"],
                    bot_data["first_seen"],
                    bot_data["last_seen"],
                ),
            )
            return cur.fetchone()["id"]

    # ==========================
    # Dashboard Queries
    # ==========================

    def get_summary(self):
        with self.get_cursor() as cur:
            cur.execute(
                """
                SELECT
                    COUNT(*) AS total_bots,
                    COUNT(*) FILTER (WHERE bot_type = 'AI_Retrieval') AS ai_bots,
                    COUNT(*) FILTER (WHERE bot_type = 'Suspicious') AS suspicious_bots,
                    AVG(ai_score) AS average_ai_score
                FROM bots;
                """
            )
            return cur.fetchone()

    def get_all_bots(self):
        with self.get_cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM bots
                ORDER BY ai_score DESC;
                """
            )
            return cur.fetchall()

    def get_bot_by_id(self, bot_id: str):
        with self.get_cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM bots
                WHERE id = %s;
                """,
                (bot_id,),
            )
            return cur.fetchone()

    # ==========================
    # Cleanup
    # ==========================

    def close(self):
        if self.conn:
            self.conn.close()
