package com.zeroguard.ai.repository;

import com.zeroguard.ai.entity.Detection;
import com.zeroguard.ai.entity.Severity;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DetectionRepository extends JpaRepository<Detection, UUID> {
    long countBySeverity(Severity severity);
    List<Detection> findTop10ByOrderByCreatedAtDesc();
}

