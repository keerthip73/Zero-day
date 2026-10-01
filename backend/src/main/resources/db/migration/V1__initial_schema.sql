create table users (
    id uuid primary key,
    email varchar(255) not null unique,
    password_hash varchar(255) not null,
    role varchar(40) not null,
    created_at timestamp with time zone not null
);

create table security_events (
    id uuid primary key,
    event_timestamp timestamp with time zone,
    source_identifier varchar(255),
    destination_identifier varchar(255),
    protocol varchar(40),
    source_port integer,
    destination_port integer,
    duration_ms double precision,
    forward_packets double precision,
    backward_packets double precision,
    forward_bytes double precision,
    backward_bytes double precision,
    flow_bytes_per_sec double precision,
    flow_packets_per_sec double precision,
    packet_length_mean double precision,
    packet_length_std double precision,
    flow_iat_mean_ms double precision,
    tcp_syn_count double precision,
    tcp_ack_count double precision,
    tcp_rst_count double precision,
    created_at timestamp with time zone not null
);

create table detections (
    id uuid primary key,
    event_id uuid not null references security_events(id),
    model_name varchar(255),
    model_version varchar(255),
    anomaly_score double precision,
    risk_score double precision,
    severity varchar(60),
    anomaly boolean,
    explanation varchar(2000),
    created_at timestamp with time zone not null
);

create table alerts (
    id uuid primary key,
    detection_id uuid not null references detections(id),
    title varchar(255),
    description varchar(2000),
    severity varchar(60),
    status varchar(60),
    assigned_to uuid references users(id),
    acknowledged_at timestamp with time zone,
    resolved_at timestamp with time zone,
    created_at timestamp with time zone
);

create table analyst_notes (
    id uuid primary key,
    event_id uuid not null references security_events(id),
    author_id uuid not null references users(id),
    note varchar(2000) not null,
    created_at timestamp with time zone
);

create index idx_users_email on users(email);
create index idx_events_timestamp on security_events(event_timestamp);
create index idx_events_protocol on security_events(protocol);
create index idx_detections_risk on detections(risk_score);
create index idx_alerts_status on alerts(status);

