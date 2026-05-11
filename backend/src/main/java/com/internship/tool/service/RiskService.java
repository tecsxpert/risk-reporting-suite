package com.internship.tool.service;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;


@Service
public class RiskService {

    private final RiskRepository repository;

    public RiskService(RiskRepository repository) {
        this.repository = repository;
    }

    public List<Risk> getAllRisks() {
        return repository.findAll();
    }

    public Risk addRisk(Risk risk) {
        return repository.save(risk);
    }

    public Risk getRiskById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Risk not found"));
    }

    public String deleteRisk(Long id) {
        repository.deleteById(id);
        return "Deleted";
    }
}