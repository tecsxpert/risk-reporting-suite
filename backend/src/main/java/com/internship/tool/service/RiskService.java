package com.internship.tool.service;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


@Service
public class RiskService {

    @Autowired
    private RiskRepository riskRepository;

    // CREATE
    public Risk createRisk(Risk risk) {
        if (risk.getTitle() == null || risk.getTitle().isEmpty()) {
            throw new RuntimeException("Title cannot be empty");
        }
        risk.setDeleted(false);
        return riskRepository.save(risk);
    }

    // READ ALL with pagination
    public Page<Risk> getAllRisks(int page, int size, String sortBy, String sortDir) {
        Sort sort = sortDir.equalsIgnoreCase("desc")
                ? Sort.by(sortBy).descending()
                : Sort.by(sortBy).ascending();
        Pageable pageable = PageRequest.of(page, size, sort);
        return riskRepository.findByDeletedFalse(pageable);
    }

    // READ ALL (simple list for internal use)
    public List<Risk> getAllRisks() {
        return riskRepository.findAll();
    }

    // READ BY ID
    public Risk getRiskById(Long id) {
        return riskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Risk not found"));
    }

    // UPDATE
    public Risk updateRisk(Long id, Risk updatedRisk) {
        Risk existing = getRiskById(id);
        existing.setTitle(updatedRisk.getTitle());
        existing.setDescription(updatedRisk.getDescription());
        existing.setCategory(updatedRisk.getCategory());
        existing.setStatus(updatedRisk.getStatus());
        existing.setScore(updatedRisk.getScore());
        return riskRepository.save(existing);
    }

    // SOFT DELETE
    public void deleteRisk(Long id) {
        Risk risk = getRiskById(id);
        risk.setDeleted(true);
        riskRepository.save(risk);
    }

    // SEARCH with pagination
    public Page<Risk> searchRisks(String query, int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return riskRepository.findByTitleContainingIgnoreCaseAndDeletedFalse(query, pageable);
    }

    // SEARCH simple list
    public List<Risk> searchRisks(String query) {
        return riskRepository.findByTitleContainingIgnoreCase(query);
    }

    // FILTER by status
    public List<Risk> filterByStatus(String status) {
        return riskRepository.findByStatus(status);
    }

    // STATS for dashboard
    public Map<String, Object> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalRisks", riskRepository.count());
        stats.put("byStatus", riskRepository.countByStatus());
        stats.put("byCategory", riskRepository.countByCategory());
        return stats;
    }

    // EXPORT to CSV
    public String exportToCsv() {
        List<Risk> risks = riskRepository.findAll();
        StringBuilder csv = new StringBuilder();
        csv.append("ID,Title,Description,Category,Status,Score,Deleted,CreatedAt\n");
        for (Risk r : risks) {
            csv.append(r.getId()).append(",")
               .append(r.getTitle()).append(",")
               .append(r.getDescription() != null ? r.getDescription() : "").append(",")
               .append(r.getCategory() != null ? r.getCategory() : "").append(",")
               .append(r.getStatus() != null ? r.getStatus() : "").append(",")
               .append(r.getScore() != null ? r.getScore() : "").append(",")
               .append(r.getDeleted()).append(",")
               .append(r.getCreatedAt() != null ? r.getCreatedAt() : "").append("\n");
        }
        return csv.toString();
    }
}
