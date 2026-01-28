#!/usr/bin/env python3
"""
AWS EC2 CPU Monitor

This script monitors EC2 instances and identifies those with high CPU usage.
For demonstration purposes, CPU usage is simulated using mock data.

Author: Portfolio Project
Purpose: Demonstrate EC2 API usage, instance monitoring, and troubleshooting workflows
"""

import boto3
import random
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


# Configuration
CPU_THRESHOLD = 80.0  # Alert threshold for CPU usage percentage
AWS_REGION = 'us-east-1'  # Default region to scan


def list_ec2_instances(region=AWS_REGION):
    """
    List all EC2 instances in the specified region.
    
    Uses the describe_instances API to fetch instance metadata including:
    - Instance ID
    - Instance State (running, stopped, terminated, etc.)
    - Launch Time
    - Instance Type
    - Tags (Name, etc.)
    
    Args:
        region (str): AWS region to query
        
    Returns:
        list: List of instance dictionaries with relevant metadata
        
    Raises:
        ClientError: If AWS API call fails
        NoCredentialsError: If AWS credentials are not configured
    """
    try:
        # Initialize EC2 client for the specified region
        # Requires AWS credentials configured via ~/.aws/credentials or IAM role
        ec2_client = boto3.client('ec2', region_name=region)
        
        print(f"Scanning EC2 instances in region: {region}...")
        
        # Call EC2 describe_instances API
        # Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
        response = ec2_client.describe_instances()
        
        instances = []
        
        # Parse response structure: Reservations -> Instances
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                # Extract relevant instance metadata
                instance_data = {
                    'instance_id': instance.get('InstanceId'),
                    'state': instance.get('State', {}).get('Name'),
                    'instance_type': instance.get('InstanceType'),
                    'launch_time': instance.get('LaunchTime'),
                    'private_ip': instance.get('PrivateIpAddress', 'N/A'),
                    'public_ip': instance.get('PublicIpAddress', 'N/A'),
                }
                
                # Extract Name tag if available
                tags = instance.get('Tags', [])
                name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'N/A')
                instance_data['name'] = name_tag
                
                instances.append(instance_data)
        
        return instances
        
    except NoCredentialsError:
        print("ERROR: AWS credentials not found!")
        print("Configure credentials using 'aws configure' or set environment variables.")
        raise
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"AWS API Error [{error_code}]: {error_message}")
        raise
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise


def simulate_cpu_usage(instance_id):
    """
    Simulate CPU usage for demonstration purposes.
    
    In production, you would use CloudWatch GetMetricStatistics API:
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=datetime.now() - timedelta(minutes=10),
        EndTime=datetime.now(),
        Period=300,
        Statistics=['Average']
    )
    
    Args:
        instance_id (str): EC2 Instance ID
        
    Returns:
        float: Simulated CPU usage percentage (0-100)
    """
    # Generate pseudo-random CPU based on instance ID hash
    # This ensures consistent results for the same instance across runs
    random.seed(hash(instance_id))
    
    # Weighted random: 70% chance of normal CPU (10-60%), 30% chance of high CPU (60-95%)
    if random.random() < 0.7:
        cpu_usage = random.uniform(10.0, 60.0)
    else:
        cpu_usage = random.uniform(60.0, 95.0)
    
    return round(cpu_usage, 2)


def check_high_cpu_instances(instances):
    """
    Check instances for high CPU usage and flag those exceeding threshold.
    
    Args:
        instances (list): List of instance dictionaries from list_ec2_instances()
        
    Returns:
        list: Instances with high CPU usage
    """
    high_cpu_instances = []
    
    print(f"\n Checking CPU usage for running instances...")
    print("="*80)
    
    # Filter for running instances only
    running_instances = [i for i in instances if i['state'] == 'running']
    
    if not running_instances:
        print("No running instances found.")
        return high_cpu_instances
    
    print(f"{'Instance ID':<20} {'Name':<25} {'CPU %':<10} {'Status':<15}")
    print("-"*80)
    
    for instance in running_instances:
        instance_id = instance['instance_id']
        name = instance['name']
        
        # Simulate CPU usage check
        cpu_usage = simulate_cpu_usage(instance_id)
        
        # Determine status
        if cpu_usage > CPU_THRESHOLD:
            status = "HIGH CPU"
            high_cpu_instances.append({
                **instance,
                'cpu_usage': cpu_usage
            })
        else:
            status = "Normal"
        
        # Print instance details
        print(f"{instance_id:<20} {name:<25} {cpu_usage:<10.2f} {status:<15}")
    
    print("="*80 + "\n")
    
    return high_cpu_instances


def generate_alert_report(high_cpu_instances):
    """
    Generate a detailed alert report for high CPU instances.
    
    Args:
        high_cpu_instances (list): Instances exceeding CPU threshold
    """
    if not high_cpu_instances:
        print("All instances are operating within normal CPU parameters.\n")
        return
    
    print("\n" + "="*80)
    print("HIGH CPU ALERT - INSTANCES REQUIRING ATTENTION")
    print("="*80)
    
    for instance in high_cpu_instances:
        print(f"\n Instance ID: {instance['instance_id']}")
        print(f"Name: {instance['name']}")
        print(f"Instance Type: {instance['instance_type']}")
        print(f"CPU Usage: {instance['cpu_usage']:.2f}%")
        print(f"Launch Time: {instance['launch_time'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Private IP: {instance['private_ip']}")
        print(f"Public IP: {instance['public_ip']}")
        print(f"Action Required: CPU usage exceeds {CPU_THRESHOLD}% threshold")
        print(f"Refer to: docs/SOP-High-CPU-Troubleshooting.md")
        print("-"*80)
    
    print("\nRecommendation: Follow the High CPU Troubleshooting SOP for diagnostic steps.")
    print("="*80 + "\n")


def main():
    """
    Main execution function for EC2 CPU Monitor.
    
    Workflow:
    1. List all EC2 instances in the region
    2. Filter for running instances
    3. Check CPU usage (simulated)
    4. Generate alert report for high CPU instances
    """
    print("🖥️  AWS EC2 CPU Monitor")
    print("="*80 + "\n")
    
    try:
        # List all EC2 instances
        instances = list_ec2_instances(region=AWS_REGION)
        
        print(f"Found {len(instances)} total instances")
        running_count = sum(1 for i in instances if i['state'] == 'running')
        print(f"{running_count} instances in 'running' state\n")
        
        # Check for high CPU usage
        high_cpu_instances = check_high_cpu_instances(instances)
        
        # Generate alert report
        generate_alert_report(high_cpu_instances)
        
    except Exception as e:
        print(f"\n CPU Monitor execution failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
