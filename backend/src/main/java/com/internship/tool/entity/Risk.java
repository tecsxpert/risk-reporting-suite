package com.internship.tool.entity;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "risk")
public class Risk {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    private String status;

    private Integer score;

    private LocalDate dueDate;

    public Risk() {
    }

    public Risk(String title, String status, Integer score, LocalDate dueDate) {
        this.title = title;
        this.status = status;
        this.score = score;
        this.dueDate = dueDate;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getStatus() {
        return status;
    }

    public Integer getScore() {
        return score;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public void setScore(Integer score) {
        this.score = score;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }
}