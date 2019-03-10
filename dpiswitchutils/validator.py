import jsonschema
import json


def assert_valid_config(instance_name, schema):
    jsonschema.validate(json.load(open(instance_name, 'r')), schema)
