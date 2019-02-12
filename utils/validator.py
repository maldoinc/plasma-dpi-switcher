import jsonschema
import json


def validate_json(instance_name, schema_name):
    try:
        jsonschema.validate(json.load(open(instance_name, 'r')), json.load(open(schema_name, 'r')))
    except Exception as e:
        print("[ERR] [Schema Validation] {}".format(e))
