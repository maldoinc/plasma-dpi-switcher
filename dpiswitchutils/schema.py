SCHEMA = {
    "type": "object",
    "required": ["version", "profiles"],
    "properties": {
        "version": {
            "type": "string",
            "enum": ["1.0"]
        },
        "profiles": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "description", "scaling", "cursor", "panels", "widgets"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": ["string", "null"]},
                    "scaling": {"type": "number"},
                    "cursor": {
                        "type": "object",
                        "required": ["size"],
                        "properties": {
                            "size": {
                                "type": "integer",
                                "minimum": 0
                            }
                        }
                    },
                    "panels": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["groups", "thickness"],
                            "properties": {
                                "groups": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "thickness": {
                                    "type": "integer",
                                    "minimum": 0
                                }
                            }
                        }
                    },
                    "widgets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["groups", "key", "value"],
                            "properties": {
                                "groups": {
                                    "type": "array",
                                    "items": {
                                        "type": ["string", "integer"]
                                    }
                                },
                                "key": {
                                    "type": ["string", "integer"]
                                },
                                "value": {
                                    "type": ["boolean", "string", "number", "integer"]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
