#!/usr/bin/env python3
"""
AWS Cost Guard - FinOps Monitoring Tool

This script monitors AWS spending for the current month using AWS Cost Explorer.
If spending exceeds a defined threshold, it triggers an alert (simulated SNS).

Author: Portfolio Project
Purpose: Demonstrate AWS SDK usage, error handling, and FinOps practices
"""

import boto3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from botocore.exceptions import ClientError, NoCredentialsError


# Configuration
COST_THRESHOLD = 100.0  # Alert threshold in USD
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:cost-alerts"  # Mock ARN


def get_current_month_date_range():
    """
    Calculate the start and end dates for the current month.
    
    Cost Explorer API requires dates in YYYY-MM-DD format.
    
    Returns:
        tuple: (start_date, end_date) as strings in YYYY-MM-DD format
    """
    # Get the first day of the current month
    today = datetime.now()
    start_date = today.replace(day=1).strftime('%Y-%m-%d')
    
    # Get the first day of next month (end date for Cost Explorer)
    # Cost Explorer uses exclusive end dates
    next_month = today + relativedelta(months=1)
    end_date = next_month.replace(day=1).strftime('%Y-%m-%d')
    
    return start_date, end_date


def fetch_current_month_cost():
    """
    Fetch AWS spending for the current month using Cost Explorer API.
    
    Uses the get_cost_and_usage API call with:
    - TimePeriod: Current month's date range
    - Granularity: MONTHLY (aggregated view)
    - Metrics: UnblendedCost (actual costs without RI/SP discounts applied)
    
    Returns:
        float: Total cost for the current month in USD
        
    Raises:
        ClientError: If AWS API call fails
        NoCredentialsError: If AWS credentials are not configured
    """
    try:
        # Initialize Cost Explorer client
        # Requires AWS credentials configured via ~/.aws/credentials or environment variables
        ce_client = boto3.client('ce', region_name='us-east-1')
        
        # Get date range for current month
        start_date, end_date = get_current_month_date_range()
        
        print(f"Fetching AWS costs from {start_date} to {end_date}...")
        
        # Call Cost Explorer API
        # Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',  # DAILY, MONTHLY, or HOURLY
            Metrics=['UnblendedCost']  # Actual costs incurred
        )
        
        # Extract cost from response
        # Response structure: ResultsByTime[0].Total.UnblendedCost.Amount
        results = response.get('ResultsByTime', [])
        
        if not results:
            print("No cost data available for the current month.")
            return 0.0
        
        # Get the cost amount (returned as string, convert to float)
        cost_data = results[0].get('Total', {}).get('UnblendedCost', {})
        total_cost = float(cost_data.get('Amount', 0.0))
        
        return total_cost
        
    except NoCredentialsError:
        print("ERROR: AWS credentials not found!")
        print("   Configure credentials using 'aws configure' or set environment variables.")
        raise
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"AWS API Error [{error_code}]: {error_message}")
        raise
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise


def send_sns_alert(current_cost, threshold):
    """
    Simulate sending an SNS alert when cost threshold is exceeded.
    
    In production, this would use boto3.client('sns').publish()
    
    Args:
        current_cost (float): Current month's AWS spending
        threshold (float): Alert threshold in USD
    """
    print("\n" + "="*60)
    print("COST ALERT TRIGGERED!")
    print("="*60)
    print(f"Current Month Spending: ${current_cost:.2f}")
    print(f"Alert Threshold: ${threshold:.2f}")
    print(f"Overage: ${current_cost - threshold:.2f}")
    print("\n Simulating SNS Alert...")
    print(f"   Topic ARN: {SNS_TOPIC_ARN}")
    print(f"   Subject: AWS Cost Alert - Threshold Exceeded")
    print(f"   Message: Your AWS spending has reached ${current_cost:.2f}, "
          f"exceeding the ${threshold:.2f} threshold.")
    print("="*60 + "\n")
    
    # In production, uncomment and configure:
    # sns_client = boto3.client('sns', region_name='us-east-1')
    # sns_client.publish(
    #     TopicArn=SNS_TOPIC_ARN,
    #     Subject='AWS Cost Alert - Threshold Exceeded',
    #     Message=f'Current spending: ${current_cost:.2f}\nThreshold: ${threshold:.2f}'
    # )


def main():
    """
    Main execution function for AWS Cost Guard.
    
    Workflow:
    1. Fetch current month's AWS spending
    2. Compare against threshold
    3. Trigger alert if threshold exceeded
    """
    print("AWS Cost Guard - FinOps Monitoring")
    print("="*60 + "\n")
    
    try:
        # Fetch current month's cost
        current_cost = fetch_current_month_cost()
        
        # Display results
        print(f"Current Month AWS Spending: ${current_cost:.2f}")
        print(f"Alert Threshold: ${COST_THRESHOLD:.2f}")
        
        # Check threshold and alert if exceeded
        if current_cost > COST_THRESHOLD:
            send_sns_alert(current_cost, COST_THRESHOLD)
        else:
            remaining = COST_THRESHOLD - current_cost
            print(f"Spending is within budget. ${remaining:.2f} remaining before alert.\n")
            
    except Exception as e:
        print(f"\n Cost Guard execution failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
