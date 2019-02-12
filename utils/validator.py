import jsonschema
import json


def assert_valid_config(instance_name, schema_name):
    jsonschema.validate(json.load(open(instance_name, 'r')), json.load(open(schema_name, 'r')))
