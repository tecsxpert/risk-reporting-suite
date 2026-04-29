package com.internship.tool.repository;

import com.internship.tool.entity.Risk;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface RiskRepository extends JpaRepository<Risk, Long> {

    List<Risk> findByTitleContainingIgnoreCase(String title);
    List<Risk> findByStatus(String status);
    List<Risk> findByCategory(String category);
    Page<Risk> findByDeletedFalse(Pageable pageable);
    Page<Risk> findByTitleContainingIgnoreCaseAndDeletedFalse(String title, Pageable pageable);

    @Query("SELECT r FROM Risk r WHERE r.createdAt BETWEEN :startDate AND :endDate")
    List<Risk> findByDateRange(LocalDateTime startDate, LocalDateTime endDate);

    @Query("SELECT r.status, COUNT(r) FROM Risk r GROUP BY r.status")
    List<Object[]> countByStatus();

    @Query("SELECT r.category, COUNT(r) FROM Risk r GROUP BY r.category")
    List<Object[]> countByCategory();
}
