CREATE TABLE audit_log (
                           id BIGSERIAL PRIMARY KEY,
                           entity_type VARCHAR(100) NOT NULL,
                           entity_id BIGINT NOT NULL,
                           action VARCHAR(50) NOT NULL,
                           old_value TEXT,
                           new_value TEXT,
                           changed_by VARCHAR(100),
                           changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Composite index on entity_type and entity_id
CREATE INDEX idx_audit_entity_type_id
    ON audit_log(entity_type, entity_id);

-- Index on changed_at for date range queries
CREATE INDEX idx_audit_changed_at
    ON audit_log(changed_at);

-- Index on changed_by for user query filters
CREATE INDEX idx_audit_changed_by
    ON audit_log(changed_by);