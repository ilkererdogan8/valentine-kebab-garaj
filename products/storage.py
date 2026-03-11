import uuid
from django.conf import settings
from azure.storage.blob import BlobServiceClient, ContentSettings


def upload_to_blob(file):
    """Upload a file to Azure Blob Storage and return its public URL."""
    connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
    container_name = settings.AZURE_STORAGE_CONTAINER

    if not connection_string:
        return ''

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Create container if it doesn't exist
    try:
        container_client.get_container_properties()
    except Exception:
        container_client.create_container(public_access='blob')

    # Generate unique filename
    extension = file.name.rsplit('.', 1)[-1] if '.' in file.name else 'bin'
    blob_name = f"{uuid.uuid4().hex}.{extension}"

    # Determine content type
    content_type = file.content_type or 'application/octet-stream'

    # Upload
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(
        file.read(),
        overwrite=True,
        content_settings=ContentSettings(content_type=content_type),
    )

    return blob_client.url


def delete_from_blob(image_url):
    """Delete a file from Azure Blob Storage by its URL."""
    connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
    container_name = settings.AZURE_STORAGE_CONTAINER

    if not connection_string or not image_url:
        return

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        # Extract blob name from URL
        blob_name = image_url.split('/')[-1]
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        blob_client.delete_blob()
    except Exception:
        pass
