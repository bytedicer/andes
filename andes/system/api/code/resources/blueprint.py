from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.blueprint import BlueprintModel
from util.response import response

class BlueprintList(Resource):
  """API resource to display list of saved blueprints.
  
  Endpoint::
    /blueprints

  """
  @jwt_required()
  def get(self):
    """GET method to retrieve list of saved blueprints

    Headers:
    - `Authorization: JWT <JWT>`

    Returns:
      200 if retrieval of blueprints was successful.

    Example:
      Request:
      GET /blueprints

      Response:
      {
        "status": 201,
        "message": "Blueprints have been retrieved.",
        "error": null,
        "data": {
          "id": 1,
          "name": "foo",
          "description": "bar",
          "image": "hello-world",
          "services: [1,2]
        }
      }

    """
    return response(200, "Blueprints have been retrieved.", None, [blueprint.json() for blueprint in BlueprintModel.query.all()]), 200


class BlueprintCreate(Resource):
  """API resource to create or update blueprints

  Endpoint::
    /blueprints/create   

  """
  parser = reqparse.RequestParser()
  parser.add_argument('name',
                      type = str,
                      required = True,
                      help = "The name of the blueprint is required.")
  parser.add_argument('description',
                      type = str,
                      help = "The description of the blueprint is optional.")
  parser.add_argument('image',
                      type = str,
                      required = True,
                      help = "The image of the blueprint is required.")

  @jwt_required()
  def post(self):
    """POST method to create a new blueprint

    Headers:
    - `Authorization: JWT <JWT>`
    - `Content-Type: application/json`

    Body:
    - name (str)
    - description (str, optional)
    - image (str)

    Returns:
      201 if blueprint has been successfully created, 400 if blueprint with name
      already exists.

    Example:
      Request:
      POST /blueprints/create
      {
        "name": "foo",
        "description": "bar",
        "image": "hello-world"
      }

      Response:
      {
      " status": 201,
        "message": "Blueprint foo has been updated.",
        "error": null,
        "data": {
          "id": 1,
          "name": "foo",
          "description": "bar",
          "image": "hello-world",
          "services: [1,2]
        }
      }

    """
    data = self.parser.parse_args()

    if BlueprintModel.find_by_image(data['image']):
      return response(400, None, f"Blueprint with image {data['image']} already exists.", None), 400

    blueprint = BlueprintModel(name = data['name'],
                               description = data['description'],
                               image = data['image'])

    try:
      blueprint.save_to_db()
    except:
      return response(500, None, f"An error occured while trying to update blueprint {data['name']}.", None), 500

    return response(201, f"Blueprint {data['name']} has been updated.", None, blueprint.json()), 201

  @jwt_required()
  def put(self):
    """PUT method to create or update a blueprint

    Headers:
    - `Authorization: JWT <JWT>`
    - `Content-Type: application/json`

    Body:
    - name (str)
    - description (str, optional)
    - image (str)

    Returns:
      201 if blueprint has been successfully created or updated.

    Example:
      Request:
      PUT /blueprints/create
      {
        "name": "foo",
        "description": "bar",
        "image": "hello-world"
      }

      Response:
      {
      " status": 201,
        "message": "Blueprint foo has been updated.",
        "error": null,
        "data": {
          "id": 1,
          "name": "foo",
          "description": "bar",
          "image": "hello-world",
          "services: [1,2]
        }
      }

    """    
    data = self.parser.parse_args()

    blueprint = BlueprintModel.find_by_image(data['image'])
    if blueprint:
      blueprint.name = data['name']
      blueprint.image = data['image']
      blueprint.description = data['description']
    else:
      blueprint = BlueprintModel(name = data['name'],
                                 description = data['description'],
                                 image = data['image'])

    try:
      blueprint.save_to_db()
    except:
      return response(500, None, f"An error occured while trying to update blueprint {data['name']}.", None), 500

    return response(201, f"Blueprint {data['name']} has been updated.", None, blueprint.json()), 201


class Blueprint(Resource):
  """API resource to retrieve or delete a specific blueprint

  Endpoint::
    /blueprints/<id>

  """
  @jwt_required()
  def get(self, _id):
    """GET method to retrieve a blueprint by ID.

    Headers:
    - `Authorization: JWT <JWT>`

    Returns:
      200 if blueprint has been retrieved successfully, 404 if blueprint with passed ID doesn't exist.

    Example:
      Request:
      GET /blueprints/1

      Response:
      {
        "status": 201,
        "message": "Blueprint foo has been retrieved.",
        "error": null,
        "data": {
          "id": 1,
          "name": "foo",
          "description": "bar",
          "image": "hello-world",
          "services: [1,2]
        }
      }

    """
    try:
      blueprint = BlueprintModel.find_by_id(_id)
    except:
      return {
        'error': f"An error occured while trying to retrieve blueprint."
      }, 500

    if blueprint:
      return response(201, f"Blueprint {blueprint.name} has been retrieved.", None, blueprint.json()), 201

    return {
      'error': f"Blueprint with ID {_id} does not exist."
    }, 400

  @jwt_required()
  def delete(self, _id):
    """DELETE method to delete blueprint by ID.

    Headers:
    - `Authorization: JWT <JWT>`

    Returns:
      200 if blueprint has been deleted successfully, 404 if blueprint with passed ID doesn't exist.

    Example:
      Request:
      GET /blueprints/1
      
      Response:
      {
        "status": 200,
        "message": "Blueprint foo has been deleted.",
        "error": null,
        "data": null
      }

    """
    try:
      blueprint = BlueprintModel.find_by_id(_id)
    except:
      return response(500, None, f"An error occured while trying to delete blueprint {blueprint.name}.", None), 500

    if blueprint:
      try:
        blueprint.delete_from_db()
      except:
        return response(500, None, f"An error occured while trying delete blueprint {data['name']}.", None), 500
      return response(200, f"Blueprint {blueprint.name} has been deleted.", None, None), 200

    return response(404, None, f"Blueprint with id {_id} does not exist.", None), 404
