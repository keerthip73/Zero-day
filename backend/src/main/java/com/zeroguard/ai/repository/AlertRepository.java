package com.zeroguard.ai.repository;

import com.zeroguard.ai.entity.Alert;
import com.zeroguard.ai.entity.AlertStatus;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AlertRepository extends JpaRepository<Alert, UUID> {
    long countByStatus(AlertStatus status);
    List<Alert> findTop10ByOrderByCreatedAtDesc();
}

