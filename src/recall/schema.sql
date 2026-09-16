-- schema.sql

PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS items (
    id  INTEGER PRIMARY KEY,
    kind TEXT NOT NULL
        CHECK (kind IN ('link', 'snippet', 'note')),
    title TEXT NOT NULL DEFAULT '',
    note TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    url TEXT,
    lang TEXT,
    source TEXT NOT NULL DEFAULT 'manual',
    created_at INTEGER NOT NULL,
    deleted_at INTEGER,
    accessed_at INTEGER,
    access_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS item_tags (
    item_id INTEGER NOT NULL REFERENCES items(id),
    tag  TEXT NOT NULL,
    PRIMARY KEY (item_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_item_tags_tag ON item_tags(tag);

CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5 (
    title, note, content,
    content = 'items',
    content_rowid = 'id',
    tokenize = "porter unicode61 tokenchars '_-.'"
);

CREATE TRIGGER IF NOT EXISTS items_ai
AFTER INSERT ON items
BEGIN
INSERT INTO items_fts (rowid, title, note, content)
    VALUES (new.id, new.title, new.note, new.content);
END;

CREATE TRIGGER IF NOT EXISTS items_au
AFTER UPDATE ON items
BEGIN
INSERT INTO items_fts (items_fts, rowid, title, note, content)
    VALUES ('delete', old.id, old.title, old.note, old.content);
INSERT INTO items_fts (rowid, title, note, content)
    VALUES (new.id, new.title, new.note, new.content);
END;

CREATE TRIGGER IF NOT EXISTS items_ad
AFTER DELETE ON items
BEGIN
INSERT INTO items_fts (items_fts, rowid, title, note, content)
        VALUES ('delete', old.id, old.title, old.note, old.content);
END;
