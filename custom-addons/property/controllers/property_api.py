import json
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request


def invalid_response(error, status):
    response_body = {
        'error': error,
    }
    return request.make_json_response(response_body, status=status)


def valid_response(data, status):
    response_body = {
        'message': "successful",
        'data': data,
    }
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return invalid_response("Name is required!", status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return valid_response({
                    "message": "Property has been created successfully.",
                    "id": res.id,
                    "name": res.name,
                }, status=201)
        except Exception as error:
            return invalid_response(error, status=400)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return [{
                  "message": "Property has been created successfully."
            }]

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response("ID dose not exist!", status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return valid_response({
                "message": "Property has been updated successfully.",
                "id": property_id.id,
                "name": property_id.name,
            }, status=200)
        except Exception as error:
            return invalid_response(error, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response("ID dose not exist!", status=400)
            return valid_response({
                "id": property_id.id,
                "ref": property_id.ref,
                "name": property_id.name,
                "description": property_id.description,
                "postcode": property_id.postcode,
                "date_availability": property_id.date_availability,
                "expected_selling_date": property_id.expected_selling_date,
            }, status=200)
        except Exception as error:
            return invalid_response(error, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response("ID dose not exist!", status=400)
            property_id.unlink()
            return valid_response({
                "message": "Property has been deleted successfully.",
            }, status=200)
        except Exception as error:
            return invalid_response(error, status=400)

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]
            property_ids = request.env['property'].sudo().search(property_domain)
            if not property_ids:
                return invalid_response("There are not records!", status=400)
            return valid_response([{
                "id": property_id.id,
                "ref": property_id.ref,
                "name": property_id.name,
                "description": property_id.description,
                "postcode": property_id.postcode,
                "date_availability": property_id.date_availability,
                "expected_selling_date": property_id.expected_selling_date,
            } for property_id in property_ids], status=200)
        except Exception as error:
            return invalid_response(error, status=400)
