package com.zeroguard.ai.repository;

import com.zeroguard.ai.entity.AnalystNote;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AnalystNoteRepository extends JpaRepository<AnalystNote, UUID> {
    List<AnalystNote> findByEventIdOrderByCreatedAtDesc(UUID eventId);
}

