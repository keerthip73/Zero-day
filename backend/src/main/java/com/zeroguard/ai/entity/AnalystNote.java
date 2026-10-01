package com.zeroguard.ai.entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "analyst_notes")
public class AnalystNote {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "event_id")
    private SecurityEvent event;

    @ManyToOne(optional = false)
    @JoinColumn(name = "author_id")
    private User author;

    @Column(nullable = false, length = 2000)
    private String note;

    private Instant createdAt = Instant.now();

    public UUID getId() { return id; }
    public SecurityEvent getEvent() { return event; }
    public void setEvent(SecurityEvent event) { this.event = event; }
    public User getAuthor() { return author; }
    public void setAuthor(User author) { this.author = author; }
    public String getNote() { return note; }
    public void setNote(String note) { this.note = note; }
    public Instant getCreatedAt() { return createdAt; }
}

