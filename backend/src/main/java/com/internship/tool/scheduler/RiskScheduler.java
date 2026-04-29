package com.internship.tool.scheduler;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import java.util.List;

@Component
public class RiskScheduler {

    @Autowired
    private RiskRepository riskRepository;

    // Daily reminder — runs every day at 8 AM
    @Scheduled(cron = "0 0 8 * * ?")
    public void dailyOverdueReminder() {
        List<Risk> risks = riskRepository.findByStatus("OPEN");
        System.out.println("[SCHEDULER] Daily reminder — Open risks count: " + risks.size());
    }

    // 7-day advance deadline alert — runs every day at 9 AM
    @Scheduled(cron = "0 0 9 * * ?")
    public void weeklyDeadlineAlert() {
        List<Risk> risks = riskRepository.findByStatus("IN_PROGRESS");
        System.out.println("[SCHEDULER] Weekly alert — In progress risk
cat > src/main/java/com/internship/tool/scheduler/RiskScheduler.java << 'EOF'
package com.internship.tool.scheduler;

import com.internship.tool.entity.Risk;
import com.internship.tool.repository.RiskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import java.util.List;

@Component
public class RiskScheduler {

    @Autowired
    private RiskRepository riskRepository;

    // Daily reminder — runs every day at 8 AM
    @Scheduled(cron = "0 0 8 * * ?")
    public void dailyOverdueReminder() {
        List<Risk> risks = riskRepository.findByStatus("OPEN");
        System.out.println("[SCHEDULER] Daily reminder — Open risks count: " + risks.size());
    }

    // 7-day advance deadline alert — runs every day at 9 AM
    @Scheduled(cron = "0 0 9 * * ?")
    public void weeklyDeadlineAlert() {
        List<Risk> risks = riskRepository.findByStatus("IN_PROGRESS");
        System.out.println("[SCHEDULER] Weekly alert — In progress risks: " + risks.size());
    }

    // Weekly summary — runs every Monday at 7 AM
    @Scheduled(cron = "0 0 7 * * MON")
    public void weeklySummary() {
        long total = riskRepository.count();
        System.out.println("[SCHEDULER] Weekly summary — Total risks: " + total);
    }
}
