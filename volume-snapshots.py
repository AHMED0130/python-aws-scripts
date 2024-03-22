import boto3
import schedule

client = boto3.client('ec2')

def create_snapshots():
    volumes = client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'prod',
                ]
            },
        ],
    )['Volumes']
    for volume in volumes:
        response =client.create_snapshot(
                VolumeId =volume['VolumeId']
            )

schedule.every().minute.do(create_snapshots)
while True:
    schedule.run_pending()
