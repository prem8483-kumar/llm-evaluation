import boto3


def run_testset_generator():

    cluster_name = ""
    task_definition = ""
    launch_type = 'FARGATE'
    subnet_ids = [""]
    security_group_ids = [""]

    network_configuration = {
        'awsvpcConfiguration': {
            'subnets': subnet_ids,
            'securityGroups': security_group_ids,
            'assignPublicIp': 'DISABLED'
        }
    }

    ecs_client = boto3.client('ecs', region_name='eu-west-1')

    try:
        run_task_response = ecs_client.run_task(
            cluster=cluster_name,
            taskDefinition=task_definition,
            launchType=launch_type,
            networkConfiguration=network_configuration,
            count=1
        )

        if 'failures' in run_task_response and len(run_task_response['failures']) > 0:
            raise Exception(f"ECS Task failed to start: {run_task_response['failures']}")

        return {
            "taskArn": run_task_response['tasks'][0]['taskArn']
        }

    except Exception as e:
        return {
            'error': str(e)
        }


if __name__ == '__main__':
    taskArn = run_testset_generator()
    print(taskArn)

