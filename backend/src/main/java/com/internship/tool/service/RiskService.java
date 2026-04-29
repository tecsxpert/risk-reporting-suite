package com.internship.tool.service;

import com.internship.tool.entity.Risk;
import com.internship.tool.exception.ResourceNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RiskService {

    private List<Risk> riskList = new ArrayList<>();
    private Long idCounter = 1L;

    public List<Risk> getAllRisks() {
        return riskList;
    }

    public Risk addRisk(Risk risk) {
        risk.setId(idCounter++);
        riskList.add(risk);
        return risk;
    }

    public Risk getRiskById(Long id) {
        return riskList.stream()
                .filter(r -> r.getId().equals(id))
                .findFirst()
                .orElseThrow(() ->
                        new ResourceNotFoundException("Risk not found with id: " + id)
                );
    }

    public String deleteRisk(Long id) {
        riskList.removeIf(r -> r.getId().equals(id));
        return "Risk deleted successfully";
    }
}