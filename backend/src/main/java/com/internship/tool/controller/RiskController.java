package com.internship.tool.controller;

import com.internship.tool.dto.RiskDTO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/risks")
public class RiskController {

    private List<RiskDTO> list = new ArrayList<>();

    @Operation(summary = "Get all risks")
    @ApiResponse(responseCode = "200", description = "Fetched successfully")
    @GetMapping
    public List<RiskDTO> getAll() {
        return list;
    }

    @Operation(summary = "Add risk")
    @ApiResponse(responseCode = "200", description = "Risk added")
    @PostMapping
    public RiskDTO add(@RequestBody RiskDTO dto) {
        list.add(dto);
        return dto;
    }

    @Operation(summary = "Get risk by ID")
    @ApiResponse(responseCode = "200", description = "Risk found")
    @GetMapping("/{id}")
    public RiskDTO get(@PathVariable Long id) {
        return list.stream()
                .filter(r -> r.getId().equals(id))
                .findFirst()
                .orElse(null);
    }

    @Operation(summary = "Delete risk")
    @ApiResponse(responseCode = "200", description = "Risk deleted")
    @DeleteMapping("/{id}")
    public String delete(@PathVariable Long id) {
        list.removeIf(r -> r.getId().equals(id));
        return "Deleted";
    }
}