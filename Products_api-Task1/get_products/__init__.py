import azure.functions as func
import json
from azure.cosmos import CosmosClient, exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        product_id = req.route_params.get("id")
        if not product_id:
            return func.HttpResponse("Missing product id", status_code=400)

        client = CosmosClient.from_connection_string("<AccountEndpoint=https://charithacosmo.documents.azure.com:443/;AccountKey=MlAuO6TSD4nRZByCmCflN5sdJ6AE3BLHEhd6oCNNGgFjI7TyqPIBFINtITDUCbI8RRp1xRIEVrQ5ACDbnQhCwg==;>")
        database = client.get_database_client("ProductsDB")
        container = database.get_container_client("Products")

        try:
            product = container.read_item(item=product_id, partition_key=product_id)
            return func.HttpResponse(json.dumps(product), status_code=200, mimetype="application/json")
        except exceptions.CosmosResourceNotFoundError:
            return func.HttpResponse("Product not found", status_code=404)

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
