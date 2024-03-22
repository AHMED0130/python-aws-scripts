import boto3
from operator import itemgetter
import time

client = boto3.client('ec2')
waiter = client.get_waiter('instance_exists')

instance_id=input("enter the instance id:- ").strip()
try:
    waiter.wait(InstanceIds=[instance_id])
except:
    print("no instance with this id found")
    exit()    

instance_volumes = client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
            
        },
    ],
)['Volumes'][0]

volume_id = instance_volumes['VolumeId']

snapshots=client.describe_snapshots(
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [volume_id]
        },
    ],
)['Snapshots']

latest_snapshot = sorted(snapshots, key=itemgetter('StartTime'), reverse=True)[0]

created_volume=client.create_volume(
    SnapshotId= latest_snapshot['SnapshotId'],
    AvailabilityZone='eu-north-1c',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                },
            ]
        },
    ]
)


time.sleep(20)

response = client.attach_volume(
    Device='/dev/xvdb',
    InstanceId=instance_id,
    VolumeId=created_volume['VolumeId'],
)



print('success')