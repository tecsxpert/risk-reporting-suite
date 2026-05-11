package com.internship.tool.service;

import org.junit.jupiter.api.Test;

class AuditServiceTest {

    @Test
    void testLog() {
        AuditService s = new AuditService();
        s.logAction("TEST");
    }
}