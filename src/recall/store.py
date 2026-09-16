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