import sqlite3


def save(
    conn,
    *,
    kind: str,
    title: str = "",
    note: str = "",
    content: str = "",
    url: str | None = None,
    lang: str | None = None,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO items (kind, title, note, content, url, lang, created_at)
        VALUES (?, ?, ?, ?, ?, ?, unixepoch())
        """,
        (kind, title, note, content, url, lang),
    )
    conn.commit()
    return cur.lastrowid


def find(conn, query: str, limit: int = 20) -> list:
    return conn.execute(
        """
        SELECT
            items.id,
            items.kind,
            items.title,
            items.url,
            snippet(items_fts, 2, '[', ']', '…', 10) AS excerpt,
            bm25(items_fts, 10.0, 5.0, 1.0) AS score
        FROM items_fts
        JOIN items ON items.id = items_fts.rowid
        WHERE items_fts MATCH ?
        ORDER BY score
        LIMIT ?
        """,
        (query, limit),
    ).fetchall()