package com.internship.tool;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ToolApplication {

	public static void main(String[] args) {
		SpringApplication.run(ToolApplication.class, args);
	}

}
spring:
datasource:
url: jdbc:postgresql://localhost:5432/riskdb
username: postgres
password: password

jpa:
hibernate:
ddl-auto: validate
show-sql: true

flyway:
enabled: true
