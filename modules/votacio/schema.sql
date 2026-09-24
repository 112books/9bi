PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS edicions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nom           TEXT NOT NULL,
    data_inici    TEXT NOT NULL,
    data_fi       TEXT NOT NULL,
    secret_token  TEXT NOT NULL UNIQUE,
    mode_geo      TEXT NOT NULL DEFAULT 'off',
    lat           REAL,
    lon           REAL,
    radi          INTEGER,
    collect_data  TEXT NOT NULL DEFAULT 'none',
    vot_limit     INTEGER NOT NULL DEFAULT 1,
    activa        INTEGER NOT NULL DEFAULT 0,
    tancada       INTEGER NOT NULL DEFAULT 0,
    creada        TEXT NOT NULL DEFAULT (datetime('now')),
    tancada_a     TEXT
);

CREATE TABLE IF NOT EXISTS obres (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    edicio_id INTEGER NOT NULL REFERENCES edicions(id),
    numero    INTEGER NOT NULL,
    titol     TEXT,
    autor     TEXT,
    categoria TEXT,
    UNIQUE (edicio_id, numero)
);

CREATE TABLE IF NOT EXISTS vots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    edicio_id       INTEGER NOT NULL REFERENCES edicions(id),
    obra_id         INTEGER NOT NULL REFERENCES obres(id),
    dispositiu_hash TEXT NOT NULL,
    geo_estat       TEXT NOT NULL DEFAULT 'none',
    signatura       TEXT NOT NULL,
    ts              INTEGER NOT NULL,
    paper           INTEGER NOT NULL DEFAULT 0,
    UNIQUE (edicio_id, obra_id, dispositiu_hash)
);

CREATE INDEX IF NOT EXISTS idx_vots_edicio ON vots(edicio_id);
CREATE INDEX IF NOT EXISTS idx_vots_edicio_obra ON vots(edicio_id, obra_id);
CREATE INDEX IF NOT EXISTS idx_vots_ts ON vots(ts);

CREATE TABLE IF NOT EXISTS visites (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    edicio_id       INTEGER NOT NULL REFERENCES edicions(id),
    dispositiu_hash TEXT NOT NULL,
    ts              INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_visites_edicio ON visites(edicio_id);
CREATE INDEX IF NOT EXISTS idx_visites_ts ON visites(ts);