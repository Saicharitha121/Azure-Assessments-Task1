import os
from azure.cosmos import CosmosClient

def get_cosmos_container():
    connection_string = os.environ.get("COSMOS_DB_CONNECTION")
    database_name = os.environ.get("COSMOS_DB_DATABASE")
    container_name = os.environ.get("COSMOS_DB_CONTAINER")

    client = CosmosClient.from_connection_string(connection_string)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container
