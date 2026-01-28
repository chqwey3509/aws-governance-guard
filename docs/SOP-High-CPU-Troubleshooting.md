# SOP: High CPU Utilization Troubleshooting

**Document ID:** SOP-EC2-CPU-001  
**Version:** 1.0  
**Last Updated:** 2026-01-28  
**Owner:** DevOps Team  
**Severity Level:** P2 - High Priority

---

## 1. Overview

This Standard Operating Procedure (SOP) provides a structured approach to diagnosing and resolving high CPU utilization alerts on AWS EC2 instances. High CPU usage can lead to application performance degradation, increased latency, and potential service outages.

---

## 2. Trigger Conditions

This SOP is activated when:

- ✅ Automated monitoring (e.g., `cpu_monitor.py`) detects CPU usage > 80%
- ✅ CloudWatch alarm triggers for sustained high CPU (>80% for 5+ minutes)
- ✅ Application performance degradation reported by users
- ✅ APM tools (New Relic, Datadog) show CPU saturation

---

## 3. Impact Assessment

### 3.1 Immediate Impact Check

Before proceeding with troubleshooting, assess the business impact:

| **Severity** | **Criteria** | **Response Time** |
|--------------|--------------|-------------------|
| **Critical** | Production service down, customer-facing impact | Immediate (< 15 min) |
| **High** | Performance degradation, intermittent errors | < 30 minutes |
| **Medium** | Non-production environment, no user impact | < 2 hours |

### 3.2 Stakeholder Notification

- **Critical/High:** Notify on-call engineer, team lead, and incident channel
- **Medium:** Log ticket and notify during business hours

---

## 4. Diagnostic Steps

### 4.1 Initial Verification

**Step 1:** Confirm the alert is valid

```bash
# SSH into the affected instance
ssh -i ~/.ssh/your-key.pem ec2-user@<instance-ip>

# Check current CPU usage
top -bn1 | head -20
```

**Expected Output:** Verify CPU usage matches alert (look for `%Cpu(s)` line)

---

### 4.2 Identify Resource-Intensive Processes

**Step 2:** Identify top CPU-consuming processes

```bash
# Real-time process monitoring (interactive)
top

# Press 'P' to sort by CPU usage
# Press 'q' to quit

# Alternative: htop (more user-friendly, if installed)
htop

# Non-interactive snapshot
ps aux --sort=-%cpu | head -10
```

**What to Look For:**
- Process name and PID
- CPU percentage (should match high usage)
- User running the process
- Command/arguments

**Step 3:** Check process details

```bash
# Get detailed process information
ps -p <PID> -o pid,ppid,cmd,%mem,%cpu,etime

# Check process tree (parent-child relationships)
pstree -p <PID>

# View process open files and connections
lsof -p <PID>
```

---

### 4.3 System-Level Analysis

**Step 4:** Check system load and resource contention

```bash
# System load averages (1, 5, 15 minutes)
uptime

# CPU core count (to contextualize load)
nproc

# Detailed CPU statistics
mpstat -P ALL 1 5

# I/O wait time (high iowait can cause CPU bottlenecks)
iostat -x 1 5
```

**Interpretation:**
- Load average > CPU cores → System overloaded
- High `%iowait` → Disk I/O bottleneck (not CPU issue)
- High `%steal` → EC2 instance resource contention (consider upsizing)

**Step 5:** Check for runaway scripts or cron jobs

```bash
# List running cron jobs
crontab -l

# Check system-wide cron jobs
ls -la /etc/cron.*

# View recent cron execution logs
grep CRON /var/log/syslog | tail -20
```

**Step 6:** Review application logs

```bash
# Application-specific logs (adjust paths as needed)
tail -f /var/log/application.log

# Check for error patterns
grep -i "error\|exception\|timeout" /var/log/application.log | tail -50

# System logs
journalctl -xe --since "10 minutes ago"
```

---

## 5. Mitigation Strategies

### 5.1 Immediate Actions (Incident Response)

| **Scenario** | **Action** | **Command** |
|--------------|------------|-------------|
| **Runaway process** | Kill the process | `kill -9 <PID>` |
| **Stuck application** | Restart application service | `sudo systemctl restart <service-name>` |
| **Resource exhaustion** | Scale horizontally (add instances) | Via AWS Console/Auto Scaling |
| **DDoS/Traffic spike** | Enable rate limiting, WAF rules | Via AWS WAF/CloudFront |

### 5.2 Temporary Relief

```bash
# Restart the problematic service (example: nginx)
sudo systemctl restart nginx

# Clear application cache (if applicable)
# Example for Redis:
redis-cli FLUSHALL

# Reboot instance (last resort, coordinate with team)
sudo reboot
```

### 5.3 Long-Term Solutions

1. **Optimize Application Code**
   - Profile code to identify inefficient algorithms
   - Implement caching (Redis, Memcached)
   - Optimize database queries (add indexes, query optimization)

2. **Right-Size EC2 Instance**
   - Analyze CloudWatch metrics over 7-14 days
   - Consider compute-optimized instances (C5, C6i family)
   - Enable Auto Scaling based on CPU thresholds

3. **Implement Monitoring & Alerting**
   - Set CloudWatch alarms for CPU > 70% (warning), > 85% (critical)
   - Use AWS CloudWatch Insights for log analysis
   - Implement APM tools (New Relic, Datadog, X-Ray)

4. **Load Balancing**
   - Distribute traffic across multiple instances
   - Use Application Load Balancer (ALB) or Network Load Balancer (NLB)

---

## 6. Escalation Path

### 6.1 Escalation Criteria

Escalate to the next level if:

- ❌ Issue persists after 30 minutes of troubleshooting
- ❌ Root cause is unclear or requires specialized expertise
- ❌ Business-critical service is impacted
- ❌ Suspected security incident (crypto mining, unauthorized access)

### 6.2 Escalation Contacts

| **Level** | **Contact** | **Escalation Trigger** |
|-----------|-------------|------------------------|
| **L1** | On-call DevOps Engineer | Initial alert response |
| **L2** | Senior DevOps / SRE Lead | Issue unresolved after 30 min |
| **L3** | Application Development Team | Code-level optimization needed |
| **L4** | AWS Support (Enterprise) | AWS infrastructure issue suspected |

---

## 7. Post-Incident Actions

### 7.1 Documentation

- ✅ Update incident ticket with root cause analysis (RCA)
- ✅ Document timeline of events
- ✅ Record mitigation steps taken

### 7.2 Root Cause Analysis (RCA)

**Template:**

```
Incident ID: INC-XXXX
Date: YYYY-MM-DD
Duration: X hours

Root Cause:
[Describe the underlying cause]

Contributing Factors:
- Factor 1
- Factor 2

Resolution:
[Describe how the issue was resolved]

Preventive Measures:
- Action item 1 (Owner: Name, Due: Date)
- Action item 2 (Owner: Name, Due: Date)
```

### 7.3 Continuous Improvement

- Schedule post-mortem meeting within 48 hours
- Update runbooks and automation scripts
- Implement preventive measures (code optimization, auto-scaling, etc.)
- Share learnings with the team

---

## 8. Useful Commands Reference

### Quick Diagnostic Commands

```bash
# CPU usage snapshot
top -bn1 | head -20

# Top 10 CPU processes
ps aux --sort=-%cpu | head -10

# System load
uptime

# CPU core count
nproc

# Detailed CPU stats
mpstat -P ALL 1 5

# I/O statistics
iostat -x 1 5

# Memory usage
free -h

# Disk usage
df -h

# Network connections
netstat -tuln

# Active processes count
ps aux | wc -l
```

### CloudWatch CLI Commands

```bash
# Get CPU utilization metric (last 1 hour)
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

---

## 9. Revision History

| **Version** | **Date** | **Author** | **Changes** |
|-------------|----------|------------|-------------|
| 1.0 | 2026-01-28 | DevOps Team | Initial SOP creation |

---

## 10. Related Documentation

- [AWS EC2 Monitoring Best Practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring_ec2.html)
- [CloudWatch Metrics for EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html)
- [Linux Performance Analysis in 60 Seconds](https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55)

---

**END OF DOCUMENT**
