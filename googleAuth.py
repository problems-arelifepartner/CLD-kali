import google.auth
from google.cloud import compute_v1

def create_kali_vm(project_id, zone, instance_name):
    # Initialize the Compute Engine client
    instance_client = compute_v1.InstancesClient()

    # Define the machine type and image
    machine_type = f"zones/{zone}/machineTypes/e2-medium"
    source_disk_image = "projects/kalilinux/images/kali-linux-2023"

    # Configure the instance
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.zone = zone
    instance.machine_type = machine_type
    instance.disks = [
        compute_v1.AttachedDisk(
            boot=True,
            auto_delete=True,
            initialize_params=compute_v1.AttachedDiskInitializeParams(
                source_image=source_disk_image,
                disk_size_gb=10,
            ),
        )
    ]
    instance.network_interfaces = [
        compute_v1.NetworkInterface(
            name="default",
            access_configs=[compute_v1.AccessConfig(name="External NAT", type_="ONE_TO_ONE_NAT")],
        )
    ]

    # Create the instance
    operation = instance_client.insert(project=project_id, zone=zone, instance_resource=instance)
    operation.result()  # Wait for the operation to complete

    print(f"Instance {instance_name} created successfully.")

if __name__ == "__main__":
    # Replace these variables with your own values
    PROJECT_ID = "your-project-id"
    ZONE = "us-central1-a"  # Choose your preferred zone
    INSTANCE_NAME = "kali-linux-vm"

    create_kali_vm(PROJECT_ID, ZONE, INSTANCE_NAME)
