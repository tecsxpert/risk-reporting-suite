package com.internship.tool.service;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.junit.jupiter.api.Test;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

class RiskServiceTest {

    @Test
    void testAdd() {
        RiskRepository repo = mock(RiskRepository.class);
        RiskService service = new RiskService(repo);

        Risk r = new Risk();
        r.setTitle("Risk");

        when(repo.save(r)).thenReturn(r);

        Risk result = service.addRisk(r);

        assertEquals("Risk", result.getTitle());
    }
}