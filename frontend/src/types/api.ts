export type Severity = 'NORMAL' | 'SUSPICIOUS' | 'HIGH_RISK' | 'POTENTIAL_UNKNOWN_THREAT';

export interface Detection {
  id: string;
  modelName: string;
  modelVersion: string;
  anomalyScore: number;
  riskScore: number;
  severity: Severity;
  anomaly: boolean;
  reasons: string[];
  createdAt: string;
}

export interface SecurityEvent {
  id: string;
  timestamp: string;
  sourceIdentifier: string;
  destinationIdentifier: string;
  protocol: string;
  sourcePort: number;
  destinationPort: number;
  detection?: Detection;
}

export interface Alert {
  id: string;
  eventId: string;
  severity: Severity;
  status: string;
  title: string;
  description: string;
  createdAt: string;
}

export interface DashboardSummary {
  totalEvents: number;
  normalEvents: number;
  suspiciousEvents: number;
  highRiskEvents: number;
  criticalAlerts: number;
  averageRiskScore: number;
}

