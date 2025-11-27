import azure.functions as func
import json
from azure.cosmos import CosmosClient, exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()

        # Basic validation
        if "id" not in data or "price" not in data:
            return func.HttpResponse("Missing 'id' or 'price'", status_code=400)
        if not isinstance(data["price"], (int, float)):
            return func.HttpResponse("'price' must be numeric", status_code=400)

        # Connect to Cosmos DB
        client = CosmosClient.from_connection_string(
            conn_str=req.params.get("COSMOS_DB_CONNECTION") or "AccountEndpoint=https://charithacosmo.documents.azure.com:443/;AccountKey=MlAuO6TSD4nRZByCmCflN5sdJ6AE3BLHEhd6oCNNGgFjI7TyqPIBFINtITDUCbI8RRp1xRIEVrQ5ACDbnQhCwg==;"
        )
        database = client.get_database_client("ProductsDB")
        container = database.get_container_client("Products")

        # Create product
        container.create_item(body=data)

        return func.HttpResponse(json.dumps(data), status_code=201, mimetype="application/json")

    except exceptions.CosmosResourceExistsError:
        return func.HttpResponse("Product with this id already exists", status_code=400)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
