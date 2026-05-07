package com.internship.tool.scheduler;

import com.internship.tool.repository.RiskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class RiskScheduler {

    @Autowired
    private RiskRepository riskRepository;

    @Scheduled(fixedRate = 60000)
    public void checkRisks() {
        System.out.println("Scheduler running... Total risks: " + riskRepository.count());
    }
}