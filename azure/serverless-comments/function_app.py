import azure.functions as func
import logging
import os
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

table_service = TableService(account_name='your_account_name', account_key='your_account_key')
table_name = os.getenv('TABLE_NAME')

@app.route(route="CommentHttpTrigger")
def CommentHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    method = req.params.get('method')

    if method == 'create':
        comment = Entity()
        comment.PartitionKey = req.params.get('post_id')
        comment.RowKey = req.params.get('comment_id')
        comment.text = req.params.get('comment_text')

        table_service.insert_entity(table_name, comment)

        return func.HttpResponse("Comment created", status_code=200)

    elif method == 'read':
        post_id = req.params.get('post_id')
        comment_id = req.params.get('comment_id')

        comment = table_service.get_entity(table_name, post_id, comment_id)

        return func.HttpResponse(str(comment), status_code=200)

    elif method == 'update':
        # post_id = req.params.get('post_id')
        # comment_id = req.params.get('comment_id')
        # new_text = req.params.get('new_text')

        # comment = table_service.get_entity(table_name, post_id, comment_id)
        # comment.text = new_text
        # table_service.update_entity(table_name, comment)

        # return func.HttpResponse("Comment updated", status_code=200)
        return func.HttpResponse("Comment update not allowed", status_code=401)

    elif method == 'delete':
        # post_id = req.params.get('post_id')
        # comment_id = req.params.get('comment_id')

        # table_service.delete_entity(table_name, post_id, comment_id)

        # return func.HttpResponse("Comment deleted", status_code=200)
        return func.HttpResponse("Comment delete not allowed", status_code=401)

    else:
        return func.HttpResponse("Invalid method", status_code=400)
