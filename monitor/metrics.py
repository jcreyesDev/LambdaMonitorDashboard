import boto3
from datetime import datetime, timezone,timedelta

def get_function_metrics(function_name: str, days: int = 7) -> dict:
    session = boto3.Session(profile_name='jcreyescloud')
    client = session.client('cloudwatch')

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)

    invocations = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Invocations',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=['Sum']
    )
    
    datapoints_invocations = invocations['Datapoints']
    total_invocations = sum(point['Sum'] for point in datapoints_invocations) if datapoints_invocations else 0

    errors = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Errors',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=['Sum']
    )

    datapoints_errors = errors['Datapoints']
    total_errors = sum(point['Sum'] for point in datapoints_errors) if datapoints_errors else 0

    duration = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Duration',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=['Sum']
    )

    datapoints_duration = duration['Datapoints']
    total_duration = sum(point['Average'] for point in datapoints_duration) / len(datapoints_duration) if datapoints_duration else 0
    total_duration_rounded = round(total_duration, 2)

    throttles = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Throttles',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=['Sum']
    )

    datapoints_throttles = throttles['Datapoints']
    total_throttles = sum(point['Sum'] for point in datapoints_throttles) if datapoints_throttles else 0

    return {
        'invocations': total_invocations,
        'errors': total_errors,
        'duration': total_duration_rounded,
        'throttles': total_throttles
    }