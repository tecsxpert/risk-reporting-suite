package com.internship.tool.controller;

import com.internship.tool.entity.Risk;
import com.internship.tool.service.RiskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/risks")
public class RiskController {

    @Autowired
    private RiskService riskService;

    // GET all risks
    @GetMapping
    public List<Risk> getAllRisks() {
        return riskService.getAllRisks();
    }

    // POST new risk
    @PostMapping
    public Risk addRisk(@RequestBody Risk risk) {
        return riskService.addRisk(risk);
    }

    // GET risk by ID
    @GetMapping("/{id}")
    public Risk getRiskById(@PathVariable Long id) {
        return riskService.getRiskById(id);
    }

    // DELETE risk
    @DeleteMapping("/{id}")
    public String deleteRisk(@PathVariable Long id) {
        return riskService.deleteRisk(id);
    }
}
