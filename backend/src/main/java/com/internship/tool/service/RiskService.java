package com.internship.tool.service;

import com.internship.tool.entity.Risk;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RiskService {

    // Temporary in-memory storage
   private List<Risk> riskList = new ArrayList<>();
private Long idCounter = 1L;

    // Get all risks
    public List<Risk> getAllRisks() {
        return riskList;
    }

    // Add new risk
    public Risk addRisk(Risk risk) {
    risk.setId(idCounter++);   // ✅ assign ID
    riskList.add(risk);
    return risk;
}

    // Get risk by ID
    public Risk getRiskById(Long id) {
        return riskList.stream()
                .filter(r -> r.getId() != null && r.getId().equals(id))
                .findFirst()
                .orElse(null);
    }

    // Delete risk
    public String deleteRisk(Long id) {
        riskList.removeIf(r -> r.getId() != null && r.getId().equals(id));
        return "Risk deleted successfully";
    }
}