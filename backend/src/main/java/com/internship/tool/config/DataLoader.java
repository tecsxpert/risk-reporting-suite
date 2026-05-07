package com.internship.tool.config;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
public class DataLoader implements CommandLineRunner {

    private final RiskRepository riskRepository;

    public DataLoader(RiskRepository riskRepository) {
        this.riskRepository = riskRepository;
    }

    @Override
    public void run(String... args) {

        if (riskRepository.count() > 0) {
            return;
        }

        List<Risk> risks = List.of(

                new Risk("Server Downtime", "OPEN", 95, LocalDate.now().plusDays(2)),
                new Risk("Database Failure", "HIGH", 90, LocalDate.now().plusDays(5)),
                new Risk("Payment Gateway Issue", "MEDIUM", 70, LocalDate.now().plusDays(7)),
                new Risk("Login API Failure", "LOW", 40, LocalDate.now().plusDays(10)),
                new Risk("Security Vulnerability", "CRITICAL", 99, LocalDate.now().plusDays(1)),

                new Risk("Redis Connection Failure", "OPEN", 80, LocalDate.now().plusDays(4)),
                new Risk("Docker Crash", "HIGH", 88, LocalDate.now().plusDays(6)),
                new Risk("Email Service Delay", "LOW", 35, LocalDate.now().plusDays(12)),
                new Risk("Cloud Storage Error", "MEDIUM", 65, LocalDate.now().plusDays(9)),
                new Risk("CPU Usage Spike", "CRITICAL", 97, LocalDate.now().plusDays(3)),

                new Risk("Memory Leak", "OPEN", 75, LocalDate.now().plusDays(8)),
                new Risk("Token Expiration Issue", "HIGH", 85, LocalDate.now().plusDays(2)),
                new Risk("Swagger API Error", "LOW", 25, LocalDate.now().plusDays(11)),
                new Risk("Session Timeout Bug", "MEDIUM", 60, LocalDate.now().plusDays(13)),
                new Risk("Audit Log Missing", "CRITICAL", 92, LocalDate.now().plusDays(4)),

                new Risk("Risk Report Failure", "OPEN", 72, LocalDate.now().plusDays(5)),
                new Risk("MySQL Slow Query", "HIGH", 89, LocalDate.now().plusDays(6)),
                new Risk("Frontend Crash", "LOW", 30, LocalDate.now().plusDays(10)),
                new Risk("Backup Failure", "MEDIUM", 68, LocalDate.now().plusDays(7)),
                new Risk("Scheduler Delay", "CRITICAL", 94, LocalDate.now().plusDays(1)),

                new Risk("Unauthorized Access", "OPEN", 78, LocalDate.now().plusDays(3)),
                new Risk("Cache Miss Issue", "HIGH", 87, LocalDate.now().plusDays(8)),
                new Risk("Notification Failure", "LOW", 28, LocalDate.now().plusDays(14)),
                new Risk("Report Generation Error", "MEDIUM", 66, LocalDate.now().plusDays(9)),
                new Risk("Data Sync Failure", "CRITICAL", 96, LocalDate.now().plusDays(2)),

                new Risk("API Timeout", "OPEN", 74, LocalDate.now().plusDays(6)),
                new Risk("JWT Validation Failure", "HIGH", 91, LocalDate.now().plusDays(5)),
                new Risk("UI Alignment Bug", "LOW", 20, LocalDate.now().plusDays(15)),
                new Risk("File Upload Error", "MEDIUM", 63, LocalDate.now().plusDays(12)),
                new Risk("Production Deployment Risk", "CRITICAL", 100, LocalDate.now().plusDays(1))
        );

        riskRepository.saveAll(risks);

        System.out.println("30 demo risk records inserted successfully!");
    }
}