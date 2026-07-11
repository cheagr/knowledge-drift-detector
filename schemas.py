KNOWLEDGE_DRIFT_SCHEMA = {

    "type": "object",

    "properties": {

        "executive_summary": {
            "type": "string"
        },

        "knowledge_drifts": {

            "type": "array",

            "items": {

                "type": "object",

                "properties": {

                    "area": {
                        "type": "string"
                    },

                    "severity":{
                        "type":"string"
                    },

                    "confluence": {
                        "type": "string"
                    },

                    "ado": {
                        "type": "string"
                    },

                    "impact": {
                        "type": "string"
                    },
                    "evidence": {

                        "type": "object",

                        "properties": {

                            "confluence": {
                                "type": "string"
                            },

                            "ado": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },

        "manual_review": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "analysis_quality": {
            "type": "object",
            "properties": {
                "confidence": {
                    "type": "string"
                },
                "reason": {
                    "type": "string"
                }
            }
        }
    }
}