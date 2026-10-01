package com.zeroguard.ai.controller;

import com.zeroguard.ai.dto.EventDtos.*;
import com.zeroguard.ai.entity.AlertStatus;
import com.zeroguard.ai.service.EventService;
import jakarta.validation.Valid;
import java.security.Principal;
import java.util.List;
import java.util.UUID;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class EventController {
    private final EventService eventService;

    public EventController(EventService eventService) {
        this.eventService = eventService;
    }

    @PostMapping("/events")
    public EventResponse create(@Valid @RequestBody EventRequest request) {
        return eventService.create(request);
    }

    @PostMapping("/events/batch")
    public List<EventResponse> createBatch(@Valid @RequestBody BatchEventRequest request) {
        return eventService.createBatch(request);
    }

    @GetMapping("/events")
    public Page<EventResponse> list(Pageable pageable) {
        return eventService.list(pageable);
    }

    @GetMapping("/events/{id}")
    public EventResponse get(@PathVariable UUID id) {
        return eventService.get(id);
    }

    @GetMapping("/events/high-risk")
    public Page<EventResponse> highRisk(Pageable pageable) {
        return eventService.list(pageable);
    }

    @GetMapping("/alerts")
    public List<AlertResponse> alerts() {
        return eventService.alerts();
    }

    @PatchMapping("/alerts/{id}/status")
    public AlertResponse updateAlert(@PathVariable UUID id, @RequestParam AlertStatus status) {
        return eventService.updateAlert(id, status);
    }

    @PostMapping("/events/{id}/notes")
    public AnalystNoteResponse addNote(@PathVariable UUID id, @Valid @RequestBody AnalystNoteRequest request, Principal principal) {
        return eventService.addNote(id, request, principal.getName());
    }

    @GetMapping("/dashboard/summary")
    public DashboardSummary summary() {
        return eventService.summary();
    }
}

