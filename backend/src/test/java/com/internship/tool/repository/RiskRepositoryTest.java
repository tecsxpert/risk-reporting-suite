package com.internship.tool.repository;

import com.internship.tool.entity.Risk;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
class RiskRepositoryTest {

    @Autowired
    private RiskRepository repo;

    @Test
    void saveRisk() {
        Risk r = new Risk();
        r.setTitle("Test");

        Risk saved = repo.save(r);

        assertThat(saved.getId()).isNotNull();
    }
}