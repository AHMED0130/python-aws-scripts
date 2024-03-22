import boto3
import schedule
from operator import itemgetter


client = boto3.client('ec2')

def cleanup_snpashots():
    volumes = client.describe_volumes()['Volumes']
    for volume in volumes:
        snapshots = client.describe_snapshots(
            Filters=[
                {
                    'Name': 'volume-id',
                    'Values': [volume['VolumeId']]
                },
            ]
        )['Snapshots']
        sorted_snapshots = sorted(snapshots, key=itemgetter('StartTime'), reverse=True)

        for snapshot in sorted_snapshots[1:]:
            response = client.delete_snapshot(
                SnapshotId=snapshot['SnapshotId']
            )
            print(response)

schedule.every().week.do(cleanup_snpashots)

while True:
    schedule.run_pending()
