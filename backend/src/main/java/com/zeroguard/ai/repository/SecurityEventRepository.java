package com.zeroguard.ai.repository;

import com.zeroguard.ai.entity.SecurityEvent;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface SecurityEventRepository extends JpaRepository<SecurityEvent, UUID>, JpaSpecificationExecutor<SecurityEvent> {
}

