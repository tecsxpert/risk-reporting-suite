package com.internship.tool.service;

import com.internship.tool.entity.Risk;
import org.springframework.stereotype.Service;

@Service
public class EmailService {

    public void sendRiskCreatedEmail(Risk risk) {
        System.out.println("Email sent for risk: " + risk);
    }
}