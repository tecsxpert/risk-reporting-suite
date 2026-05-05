package com.internship.tool;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@Transactional
public class RiskRepositoryTest {

    @Autowired
    private RiskRepository riskRepository;

    @Test
    public void testSaveAndFindRisk() {
        Risk risk = new Risk();
        risk.setTitle("Test Risk");
        risk.setStatus("OPEN");
        risk.setCategory("OPERATIONAL");
        risk.setScore(5);
        risk.setDeleted(false);

        Risk saved = riskRepository.save(risk);
        assertNotNull(saved.getId());
    }

    @Test
    public void testFindByStatus() {
        Risk risk = new Risk();
        risk.setTitle("Status Test");
        risk.setStatus("OPEN");
        risk.setDeleted(false);
        riskRepository.save(risk);

        List<Risk> risks = riskRepository.findByStatus("OPEN");
        assertFalse(risks.isEmpty());
    }

    @Test
    public void testFindByTitleContaining() {
        Risk risk = new Risk();
        risk.setTitle("Unique Title XYZ");
        risk.setDeleted(false);
        riskRepository.save(risk);

        List<Risk> risks = riskRepository.findByTitleContainingIgnoreCase("unique");
        assertFalse(risks.isEmpty());
    }

    @Test
    public void testSoftDelete() {
        Risk risk = new Risk();
        risk.setTitle("Delete Test");
        risk.setDeleted(false);
        Risk saved = riskRepository.save(risk);

        saved.setDeleted(true);
        riskRepository.save(saved);

        Optional<Risk> found = riskRepository.findById(saved.getId());
        assertTrue(found.isPresent());
        assertTrue(found.get().getDeleted());
    }

    @Test
    public void testCountRisks() {
        long before = riskRepository.count();
        Risk risk = new Risk();
        risk.setTitle("Count Test");
        risk.setDeleted(false);
        riskRepository.save(risk);
        long after = riskRepository.count();
        assertEquals(before + 1, after);
    }
}
