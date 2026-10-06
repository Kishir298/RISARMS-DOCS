# Prometheus Metrics

All RISARMS systems expose Prometheus metrics at `/metrics` endpoint.

## Endpoint Access

```bash
# CORE-HOST
curl http://localhost:8765/metrics

# CORE-CLIENT (if running portal)
curl http://localhost:8766/metrics

# RESCS
curl http://localhost:8081/metrics

# ASIS (if running web UI)
curl http://localhost:8787/metrics

# ASCS (if running web UI)
curl http://localhost:8787/metrics

# TIVISS (if running web UI)
curl http://localhost:8787/metrics
```

## Key Metrics by System

### CORE-HOST
| Metric | Type | Description |
|--------|------|-------------|
| `core_connections_active` | Gauge | Active connections |
| `core_messages_total` | Counter | Total messages (sent/received) |
| `core_portal_requests_total` | Counter | Portal HTTP requests |
| `core_rescs_adapter_latency_seconds` | Histogram | RESCS adapter latency |
| `core_device_registrations_total` | Counter | Device registrations |
| `core_service_dispatch_latency_seconds` | Histogram | Service dispatch latency |

### CORE-CLIENT
| Metric | Type | Description |
|--------|------|-------------|
| `core_client_connections_active` | Gauge | Active connections |
| `core_client_requests_total` | Counter | Requests sent |
| `core_client_unsolicited_queue_size` | Gauge | Unsolicited queue size |
| `core_client_reconnects_total` | Counter | Reconnects |

### RESCS
| Metric | Type | Description |
|--------|------|-------------|
| `rescs_http_requests_total` | Counter | HTTP requests |
| `rescs_records_created_total` | Counter | Records created |
| `rescs_files_uploaded_total` | Counter | Files uploaded |
| `rescs_quota_exceeded_total` | Counter | Quota exceeded |

### ASIS
| Metric | Type | Description |
|--------|------|-------------|
| `asis_tool_executions_total` | Counter | Tool executions |
| `asis_ascs_invocations_total` | Counter | ASCS invocations |
| `asis_ollama_requests_total` | Counter | Ollama requests |
| `asis_voice_capture_total` | Counter | Voice captures |

### ASCS
| Metric | Type | Description |
|--------|------|-------------|
| `ascs_tasks_total` | Counter | Tasks executed |
| `ascs_tool_executions_total` | Counter | Tool executions |
| `ascs_verification_total` | Counter | Verifications |
| `ascs_file_operations_total` | Counter | File operations |

### TIVISS
| Metric | Type | Description |
|--------|------|-------------|
| `tiviss_memory_operations_total` | Counter | Memory operations |
| `tiviss_tool_calls_total` | Counter | Tool calls |
| `tiviss_ollama_requests_total` | Counter | Ollama requests |
| `tiviss_handovers_total` | Counter | Handovers |

## Grafana Dashboards

Import the JSON dashboard files from `monitoring/dashboards/*.json` into Grafana.

## Alerting Rules

Example alerting rules:

```yaml
groups:
  - name: risarms-alerts
    rules:
      - alert: CoreHostConnectionsDown
        expr: core_connections_active == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "CORE-HOST has no active connections"

      - alert: RescsQuotaExceeded
        expr: increase(rescs_quota_exceeded_total[5m]) > 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "RESCS quota exceeded"

      - alert: AscsTaskFailureRate
        expr: rate(ascs_tasks_total{status="failed"}[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "ASCS task failure rate high"
```

## Scraping Configuration

```yaml
scrape_configs:
  - job_name: 'risarms'
    static_configs:
      - targets: ['core-host:8765', 'core-client:8766', 'rescs:8081']
        labels:
          environment: 'production'
```