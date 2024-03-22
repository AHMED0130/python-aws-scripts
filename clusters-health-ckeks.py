import boto3

client = boto3.client('eks')

clusters = client.list_clusters()['clusters']
print(clusters)
for cluster in clusters:
    response = client.describe_cluster(name = cluster)
    cluster_status = response['cluster']['status']
    cluster_version = response['cluster']['version']
    cluster_endpoint = response['cluster']['endpoint']
    print(f"{cluster} status is {cluster_status} and verion {cluster_version}")
    print(f"endpoint:-{cluster_endpoint}")
    



