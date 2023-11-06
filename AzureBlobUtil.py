from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

class AzureBlobUtil:
    # TODO: Can this just be a static class? Any reason we'd want to instantiate?
    def __init__(self):
        self.storage_account_url = "https://adiodatistorageaccount.blob.core.windows.net"
        return None

# authenticates to Azure for a given storage account and returns a blob client for said storage account
def get_blob_service_client_account_key(self):
    print("Attempting to authenticate to " + self.storage_account_url + " ...")
    # TODO: If we need multiple storage accounts we'd want to variablize on the function rather than pulling a class prop
    account_url = self.storage_account_url
    shared_access_key = os.getenv("AZURE_STORAGE_ACCESS_KEY")
    credential = shared_access_key

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    return blob_service_client

# downloads a blob to a file path
def download_blob_to_file(self, blob_service_client: BlobServiceClient, container_name, blob_name):
    print("Attempting to download file " + blob_name + " from " + container_name + "...")
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    # variable for determining current path; we will write into the main dir of the repo for now
    package_dir = os.path.dirname(os.path.abspath(__file__))
    with open(file=os.path.join(package_dir, blob_name), mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())

# wrapper function to get a blob client and download the given blob name
def getFileFromBlob(self, container_name, blob_name):
    blob_service_client = get_blob_service_client_account_key(self)
    download_blob_to_file(self, blob_service_client, container_name, blob_name)
    print("Download complete.")