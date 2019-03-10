SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "required": [
        "version",
        "profiles"
    ],
    "properties": {
        "version": {
            "$id": "#/properties/version",
            "type": "string",
            "enum": ["1.0"],
            "pattern": "^(.*)$"
        },
        "profiles": {
            "$id": "#/properties/profiles",
            "type": "array",
            "items": {
                "$id": "#/properties/profiles/items",
                "type": "object",
                "required": [
                    "name",
                    "description",
                    "scaling",
                    "cursor",
                    "panels",
                    "widgets"
                ],
                "properties": {
                    "name": {
                        "$id": "#/properties/profiles/items/properties/name",
                        "type": "string",
                        "pattern": "^(.*)$"
                    },
                    "description": {
                        "$id": "#/properties/profiles/items/properties/description",
                        "type": ["string", "null"],
                        "pattern": "^(.*)$"
                    },
                    "scaling": {
                        "$id": "#/properties/profiles/items/properties/scaling",
                        "type": "number"
                    },
                    "cursor": {
                        "$id": "#/properties/profiles/items/properties/cursor",
                        "type": "object",
                        "required": [
                            "size"
                        ],
                        "properties": {
                            "size": {
                                "$id": "#/properties/profiles/items/properties/cursor/properties/size",
                                "type": "integer",
                                "enum": [
                                    24,
                                    36,
                                    48
                                ]
                            }
                        }
                    },
                    "panels": {
                        "$id": "#/properties/profiles/items/properties/panels",
                        "type": "array",
                        "items": {
                            "$id": "#/properties/profiles/items/properties/panels/items",
                            "type": "object",
                            "required": [
                                "groups",
                                "thickness"
                            ],
                            "properties": {
                                "groups": {
                                    "$id": "#/properties/profiles/items/properties/panels/items/properties/groups",
                                    "type": "array",
                                    "items": {
                                        "$id": "#/properties/profiles/items/properties/panels/items/properties/groups"
                                               "/items",
                                        "type": "string",
                                        "pattern": "^(.*)$"
                                    }
                                },
                                "thickness": {
                                    "$id": "#/properties/profiles/items/properties/panels/items/properties/thickness",
                                    "type": "integer",
                                    "minimum": 0
                                }
                            }
                        }
                    },
                    "widgets": {
                        "$id": "#/properties/profiles/items/properties/widgets",
                        "type": "array",
                        "items": {
                            "$id": "#/properties/profiles/items/properties/widgets/items",
                            "type": "object",
                            "required": [
                                "groups",
                                "key",
                                "value"
                            ],
                            "properties": {
                                "groups": {
                                    "$id": "#/properties/profiles/items/properties/widgets/items/properties/groups",
                                    "type": "array",
                                    "items": {
                                        "$id": "#/properties/profiles/items/properties/widgets/items/properties"
                                               "/groups/items",
                                        "type": [
                                            "string",
                                            "integer"
                                        ],
                                        "pattern": "^(.*)$"
                                    }
                                },
                                "key": {
                                    "$id": "#/properties/profiles/items/properties/widgets/items/properties/key",
                                    "type": [
                                        "string",
                                        "integer"
                                    ],
                                    "pattern": "^(.*)$"
                                },
                                "value": {
                                    "$id": "#/properties/profiles/items/properties/widgets/items/properties/value",
                                    "type": [
                                        "boolean",
                                        "string",
                                        "number",
                                        "integer"
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}