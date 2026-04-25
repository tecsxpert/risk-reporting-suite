package com.internship.tool.controller;

import com.internship.tool.entity.Risk;
import com.internship.tool.service.RiskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/risks")
@CrossOrigin(origins = "*")
public class RiskController {

    @Autowired
    private RiskService riskService;

    @GetMapping("/all")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public ResponseEntity<List<Risk>> getAllRisks() {
        return ResponseEntity.ok(riskService.getAllRisks());
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public ResponseEntity<Risk> getRiskById(@PathVariable Long id) {
        return ResponseEntity.ok(riskService.getRiskById(id));
    }

    @PostMapping("/create")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public ResponseEntity<Risk> createRisk(@RequestBody Risk risk) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(riskService.createRisk(risk));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER')")
    public ResponseEntity<Risk> updateRisk(@PathVariable Long id,
                                           @RequestBody Risk risk) {
        return ResponseEntity.ok(riskService.updateRisk(id, risk));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> deleteRisk(@PathVariable Long id) {
        riskService.deleteRisk(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/search")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public ResponseEntity<List<Risk>> searchRisks(@RequestParam String q) {
        return ResponseEntity.ok(riskService.searchRisks(q));
    }

    @GetMapping("/filter")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public ResponseEntity<List<Risk>> filterByStatus(@RequestParam String status) {
        return ResponseEntity.ok(riskService.filterByStatus(status));
    }

    @GetMapping("/stats")
    @PreAuthorize("hasAnyRole('ADMIN','MANAGER','VIEWER')")
    public ResponseEntity<?> getStats() {
        return ResponseEntity.ok(riskService.getStats());
    }
}
