import boto3


def get_mysql_instance_specs_alternative():
    try:
        rds_client = boto3.client('rds')
        instance_specs = []
        seen_classes = set()

        # Use a specific MySQL version (8.0.28 is widely supported)
        paginator = rds_client.get_paginator('describe_orderable_db_instance_options')

        for page in paginator.paginate(
                Engine='mysql',
                EngineVersion='8.0.28',
                Vpc=True
        ):
            for instance in page['OrderableDBInstanceOptions']:
                instance_class = instance['DBInstanceClass']

                if instance_class in seen_classes:
                    continue

                seen_classes.add(instance_class)

                # Extract family
                parts = instance_class.split('.')
                family = parts[1] if len(parts) > 1 else 'unknown'

                # Create specification entry
                spec = {
                    'Family': family,
                    'Instance Class': instance_class,
                    'vCPU': instance.get('VCpu', 'N/A'),
                    'Memory': f"{instance.get('MemoryInfo', {}).get('SizeInMiB', 0) / 1024:.0f}",
                    'Storage Types': ', '.join(instance.get('StorageTypes', ['N/A'])),
                }

                instance_specs.append(spec)

        # Sort and display results
        instance_specs.sort(key=lambda x: (x['Family'], x['Instance Class']))

        current_family = None
        for spec in instance_specs:
            if current_family != spec['Family']:
                current_family = spec['Family']
                print(f"\n=== {current_family.upper()} Family Instances ===")
                print(f"{'Instance Class':<20} {'vCPU':<6} {'Memory (GiB)':<12} {'Storage Types':<30}")
                print("-" * 68)

            print(
                f"{spec['Instance Class']:<20} {spec['vCPU']:<6} {spec['Memory']:<12} "
                f"{spec['Storage Types']:<30}"
            )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    print("Getting MySQL RDS Instance Specifications (Alternative Method)...")
    get_mysql_instance_specs_alternative()
import boto3

def get_mysql_instance_specs():
    try:
        rds_client = boto3.client('rds')
        instance_specs = []
        seen_classes = set()

        # Get the latest MySQL version
        versions = rds_client.describe_db_engine_versions(
            Engine='mysql',
            DefaultOnly=True
        )

        if not versions['DBEngineVersions']:
            print("No MySQL versions found")
            return

        latest_version = versions['DBEngineVersions'][0]['EngineVersion']

        # Get instance specifications
        paginator = rds_client.get_paginator('describe_orderable_db_instance_options')

        for page in paginator.paginate(
            Engine='mysql',
            EngineVersion=latest_version,
            Vpc=True
        ):
            for instance in page['OrderableDBInstanceOptions']:
                instance_class = instance['DBInstanceClass']

                if instance_class in seen_classes:
                    continue

                seen_classes.add(instance_class)

                # Extract family
                parts = instance_class.split('.')
                family = parts[1] if len(parts) > 1 else 'unknown'

                # Get vCPU count based on instance class
                vcpu = {
                    'micro': 1,
                    'small': 1,
                    'medium': 2,
                    'large': 2,
                    'xlarge': 4,
                    '2xlarge': 8,
                    '4xlarge': 16,
                    '8xlarge': 32,
                    '12xlarge': 48,
                    '16xlarge': 64,
                    '24xlarge': 96
                }

                size = parts[2] if len(parts) > 2 else ''
                vcpu_count = vcpu.get(size, 'N/A')

                # Get memory based on instance class
                memory = {
                    't3.micro': 1,
                    't3.small': 2,
                    't3.medium': 4,
                    't3.large': 8,
                    't3.xlarge': 16,
                    't3.2xlarge': 32,
                    'm5.large': 8,
                    'm5.xlarge': 16,
                    'm5.2xlarge': 32,
                    'm5.4xlarge': 64,
                    'm5.8xlarge': 128,
                    'm5.12xlarge': 192,
                    'm5.16xlarge': 256,
                    'm5.24xlarge': 384,
                    'r5.large': 16,
                    'r5.xlarge': 32,
                    'r5.2xlarge': 64,
                    'r5.4xlarge': 128,
                    'r5.8xlarge': 256,
                    'r5.12xlarge': 384,
                    'r5.16xlarge': 512,
                    'r5.24xlarge': 768
                }

                mem = memory.get(instance_class, 'N/A')

                # Create specification entry
                spec = {
                    'Family': family,
                    'Instance Class': instance_class,
                    'vCPU': vcpu_count,
                    'Memory': mem,
                    'Storage Types': ', '.join(instance.get('StorageTypes', ['gp2', 'gp3', 'io1']))
                }

                instance_specs.append(spec)

        # Sort and display results
        instance_specs.sort(key=lambda x: (x['Family'], x['Instance Class']))

        current_family = None
        for spec in instance_specs:
            if current_family != spec['Family']:
                current_family = spec['Family']
                print(f"\n=== {current_family.upper()} Family Instances ===")
                print(f"{'Instance Class':<20} {'vCPU':<6} {'Memory (GiB)':<12} {'Storage Types':<30}")
                print("-" * 68)

            print(
                f"{spec['Instance Class']:<20} {spec['vCPU']:<6} {spec['Memory']:<12} "
                f"{spec['Storage Types']:<30}"
            )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    print("Getting MySQL RDS Instance Specifications...")
    get_mysql_instance_specs()
