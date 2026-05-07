package com.internship.tool.dto;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Risk DTO object")
public class RiskDTO {

    @Schema(example = "1")
    private Long id;

    @Schema(example = "Server Failure")
    private String title;

    @Schema(example = "HIGH")
    private String severity;

    public RiskDTO() {}

    public RiskDTO(Long id, String title, String severity) {
        this.id = id;
        this.title = title;
        this.severity = severity;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { this.severity = severity; }
}