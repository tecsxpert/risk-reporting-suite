package com.internship.tool.service;

import org.springframework.stereotype.Service;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.Collections;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;
    // In Docker, use service name. Locally, use localhost.
    private final String aiServiceUrl = "http://localhost:5000";

    public AiServiceClient() {
        this.restTemplate = new RestTemplate();
        // DAY 6 TASK: Set 10 second timeout to prevent hanging
        this.restTemplate.setRequestFactory(new org.springframework.http.client.SimpleClientHttpRequestFactory());
        ((SimpleClientHttpRequestFactory) restTemplate.getRequestFactory()).setConnectTimeout(Duration.ofSeconds(5));
        ((SimpleClientHttpRequestFactory) restTemplate.getRequestFactory()).setReadTimeout(Duration.ofSeconds(10));
    }

    public String callDescribeEndpoint(String userInput) {
        try {
            // Build the JSON payload
            String requestBody = "{\"text\": \"" + userInput + "\"}";

            // Set headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> entity = new HttpEntity<>(requestBody, headers);

            // Make the call to the Python service
            ResponseEntity<String> response = restTemplate.exchange(
                aiServiceUrl + "/describe",
                HttpMethod.POST,
                entity,
                String.class
            );

            return response.getBody();

        } catch (Exception e) {
            // DAY 6 TASK: Graceful null return on error (Never crash the Java app)
            System.err.println("Security Alert: AI Service call failed or timed out. " + e.getMessage());
            return null;
        }
    }
}
