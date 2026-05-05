package com.internship.tool.config;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;

@Aspect
@Component
public class AuditAspect {

    @Autowired
    private AuditLogRepository auditLogRepository;

    @Around("execution(* com.internship.tool.service.RiskService.createRisk(..))")
    public Object auditCreate(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = joinPoint.proceed();
        saveAuditLog("Risk", "CREATE", null, result.toString(), getUsername());
        return result;
    }

    @Around("execution(* com.internship.tool.service.RiskService.updateRisk(..))")
    public Object auditUpdate(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = joinPoint.proceed();
        saveAuditLog("Risk", "UPDATE", null, result.toString(), getUsername());
        return result;
    }

    @Around("execution(* com.internship.tool.service.RiskService.deleteRisk(..))")
    public Object auditDelete(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        Object result = joinPoint.proceed();
        saveAuditLog("Risk", "DELETE", args[0].toString(), null, getUsername());
        return result;
    }

    private void saveAuditLog(String entityType, String action, 
                               String oldValue, String newValue, String changedBy) {
        AuditLog log = new AuditLog();
        log.setEntityType(entityType);
        log.setAction(action);
        log.setOldValue(oldValue);
        log.setNewValue(newValue);
        log.setChangedBy(changedBy);
        log.setChangedAt(LocalDateTime.now());
        auditLogRepository.save(log);
    }

    private String getUsername() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return auth != null ? auth.getName() : "anonymous";
    }
}
