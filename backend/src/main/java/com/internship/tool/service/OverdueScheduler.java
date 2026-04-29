package com.internship.tool.service;

import com.internship.tool.entity.Risk;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
public class OverdueScheduler {

    @Autowired
    private RiskService riskService;

    @Autowired
    private EmailService emailService;

    @Scheduled(fixedRate = 60000)
    public void checkOverdue() {
        System.out.println("Checking overdue risks..."); // ✅ Step 3

        List<Risk> risks = riskService.getAllRisks();

        for (Risk risk : risks) {
            if (risk.getDueDate() != null &&
                risk.getDueDate().isBefore(LocalDate.now())) {

                emailService.sendEmail(risk, "⚠ Overdue Risk");
            }
        }
    }
}