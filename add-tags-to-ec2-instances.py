import boto3

client = boto3.client('ec2',region_name='eu-north-1')

response = client.describe_instance_status(IncludeAllInstances=True)
instance_ids = []
for instance in response['InstanceStatuses']:
    instance_id = instance['InstanceId']
    instance_ids.append(instance_id)


response2 = client.create_tags(
    Resources= instance_ids,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)
print(response2)