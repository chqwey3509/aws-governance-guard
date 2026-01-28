# AWS Governance Guard 🛡️

A lightweight portfolio project demonstrating AWS DevOps skills with a focus on **FinOps** (Financial Operations) and **Troubleshooting** for cloud infrastructure management.

## 📋 Project Overview

This project showcases practical AWS automation skills through two key monitoring tools:

1. **Cost Guard** - Monitors AWS spending and alerts when budgets are exceeded
2. **CPU Monitor** - Identifies EC2 instances with high CPU utilization for proactive troubleshooting

## 🎯 Purpose

Designed as a portfolio project to demonstrate:

- ✅ AWS SDK (`boto3`) proficiency
- ✅ Cost optimization and FinOps practices
- ✅ Infrastructure monitoring and alerting
- ✅ Professional documentation and SOPs
- ✅ Clean, production-ready Python code
- ✅ Error handling and logging best practices

## 🏗️ Project Structure

```
aws-governance-guard/
├── cost_guard.py                          # AWS Cost Explorer monitoring
├── cpu_monitor.py                         # EC2 CPU utilization monitoring
├── requirements.txt                       # Python dependencies
├── docs/
│   └── SOP-High-CPU-Troubleshooting.md   # Professional troubleshooting playbook
└── README.md                              # This file
```

## 🚀 Features

### Cost Guard (`cost_guard.py`)

- Fetches current month's AWS spending using Cost Explorer API
- Configurable cost threshold alerting (default: $100)
- Simulates SNS notifications for budget overages
- Comprehensive error handling and logging

### CPU Monitor (`cpu_monitor.py`)

- Lists all EC2 instances across regions
- Identifies running instances
- Simulates CPU usage monitoring (mock data for demo)
- Generates detailed alert reports with instance metadata
- References professional SOP for remediation

### Documentation

- **SOP-High-CPU-Troubleshooting.md**: Enterprise-grade troubleshooting guide
  - Structured incident response workflow
  - Linux diagnostic commands (`top`, `htop`, `ps`, `iostat`)
  - Escalation procedures
  - Post-incident analysis templates

## 📦 Installation

### Prerequisites

- Python 3.8+
- AWS Account with appropriate IAM permissions
- AWS CLI configured with credentials

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/aws-governance-guard.git
cd aws-governance-guard
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure AWS credentials**

```bash
aws configure
```

Enter your AWS Access Key ID, Secret Access Key, and default region.

## 🔑 Required AWS Permissions

### Cost Guard

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    }
  ]
}
```

### CPU Monitor

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

## 💻 Usage

### Run Cost Guard

```bash
python cost_guard.py
```

**Sample Output:**

```
🛡️  AWS Cost Guard - FinOps Monitoring
============================================================

📊 Fetching AWS costs from 2026-01-01 to 2026-02-01...

💰 Current Month AWS Spending: $127.45
📏 Alert Threshold: $100.00

============================================================
🚨 COST ALERT TRIGGERED!
============================================================
Current Month Spending: $127.45
Alert Threshold: $100.00
Overage: $27.45

📧 Simulating SNS Alert...
   Topic ARN: arn:aws:sns:us-east-1:123456789012:cost-alerts
   Subject: AWS Cost Alert - Threshold Exceeded
   Message: Your AWS spending has reached $127.45, exceeding the $100.00 threshold.
============================================================
```

### Run CPU Monitor

```bash
python cpu_monitor.py
```

**Sample Output:**

```
🖥️  AWS EC2 CPU Monitor
================================================================================

🔍 Scanning EC2 instances in region: us-east-1...
✅ Found 5 total instances
✅ 3 instances in 'running' state

📊 Checking CPU usage for running instances...
================================================================================
Instance ID          Name                      CPU %      Status         
--------------------------------------------------------------------------------
i-0abc123def456789   web-server-prod           45.32      ✅ Normal
i-0def456abc789012   api-server-prod           87.64      ⚠️ HIGH CPU
i-0ghi789jkl012345   database-server           62.18      ✅ Normal
================================================================================

============================================================
🚨 HIGH CPU ALERT - INSTANCES REQUIRING ATTENTION
============================================================

📍 Instance ID: i-0def456abc789012
   Name: api-server-prod
   Instance Type: t3.medium
   CPU Usage: 87.64%
   Launch Time: 2026-01-15 08:30:00 UTC
   Private IP: 10.0.1.45
   Public IP: 54.123.45.67

   ⚠️  Action Required: CPU usage exceeds 80.0% threshold
   📖 Refer to: docs/SOP-High-CPU-Troubleshooting.md
--------------------------------------------------------------------------------

💡 Recommendation: Follow the High CPU Troubleshooting SOP for diagnostic steps.
============================================================
```

## 🛠️ Customization

### Modify Cost Threshold

Edit `cost_guard.py`:

```python
COST_THRESHOLD = 150.0  # Change to your desired threshold in USD
```

### Modify CPU Threshold

Edit `cpu_monitor.py`:

```python
CPU_THRESHOLD = 85.0  # Change to your desired threshold percentage
```

### Change AWS Region

Edit `cpu_monitor.py`:

```python
AWS_REGION = 'us-west-2'  # Change to your target region
```

## 📚 Learning Outcomes

This project demonstrates:

1. **AWS API Integration**
   - Cost Explorer API for billing data
   - EC2 API for instance management
   - Proper error handling for AWS SDK calls

2. **FinOps Practices**
   - Proactive cost monitoring
   - Budget threshold alerting
   - Cost optimization awareness

3. **Infrastructure Monitoring**
   - Resource utilization tracking
   - Automated alerting workflows
   - Incident response procedures

4. **Professional Documentation**
   - Enterprise-grade SOPs
   - Clear troubleshooting procedures
   - Escalation paths and post-incident analysis

5. **Code Quality**
   - PEP8 compliance
   - Comprehensive error handling
   - Detailed inline documentation

## 🔮 Future Enhancements

- [ ] Integrate real CloudWatch metrics for CPU monitoring
- [ ] Implement actual SNS notifications
- [ ] Add Slack/Teams webhook integration
- [ ] Create Lambda functions for serverless execution
- [ ] Add CloudFormation/Terraform IaC templates
- [ ] Implement multi-region scanning
- [ ] Add unit tests and CI/CD pipeline
- [ ] Create dashboard with visualization (Grafana/CloudWatch)

## 📄 License

This project is open source and available for portfolio demonstration purposes.

## 👤 Author

**Chih Cheng Hsu**  
DevOps Engineer | AWS Enthusiast  
[LinkedIn](https://www.linkedin.com/in/xuviig) | [GitHub](https://github.com/chqwey3509)

---

**Note:** This is a demonstration project. For production use, implement proper security measures, use AWS Secrets Manager for credentials, and follow your organization's security policies.
