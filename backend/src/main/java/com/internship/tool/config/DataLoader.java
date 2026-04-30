package com.internship.tool.config;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataLoader implements CommandLineRunner {

    @Autowired
    private RiskRepository riskRepository;

    @Override
    public void run(String... args) throws Exception {
        if (riskRepository.count() >= 30) {
            System.out.println("[DataLoader] Data already seeded. Skipping.");
            return;
        }

        String[] titles = {
            "Budget Overrun Risk", "Data Breach Risk", "System Downtime Risk",
            "Regulatory Compliance Risk", "Vendor Failure Risk", "Cybersecurity Risk",
            "Project Delay Risk", "Staff Turnover Risk", "Market Volatility Risk",
            "Supply Chain Risk", "Natural Disaster Risk", "Reputational Risk",
            "Operational Risk", "Legal Risk", "Technology Risk",
            "Financial Fraud Risk", "Infrastructure Risk", "Data Loss Risk",
            "Privacy Violation Risk", "Contract Breach Risk", "Audit Failure Risk",
            "System Integration Risk", "Change Management Risk", "Resource Shortage Risk",
            "Communication Failure Risk", "Quality Control Risk", "Procurement Risk",
            "Environmental Risk", "Strategic Risk", "Innovation Risk"
        };

        String[] categories = {"FINANCIAL", "OPERATIONAL", "TECHNICAL", "LEGAL", "STRATEGIC"};
        String[] statuses = {"OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"};

        for (int i = 0; i < 30; i++) {
            Risk risk = new Risk();
            risk.setTitle(titles[i]);
            risk.setDescription("Description for " + titles[i]);
            risk.setCategory(categories[i % categories.length]);
            risk.setStatus(statuses[i % statuses.length]);
            risk.setScore((i % 10) + 1);
            risk.setDeleted(false);
            riskRepository.save(risk);
        }
        System.out.println("[DataLoader] 30 demo records seeded successfully!");
    }
}
