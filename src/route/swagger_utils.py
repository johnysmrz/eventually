acl_responses = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "code": "AUTHENTICATION_FAILED",
                    "message": "Token was not provided",
                    "request_id": "622b9af1-dfff-445b-8787-84634efe9150",
                }
            }
        },
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "code": "ACL_NOT_ALLOWED",
                    "message": "Current user have not ACL_MANAGEMENT",
                    "request_id": "15c17fa1-ed8f-4dcf-ad81-03cc0d7dfc83",
                }
            }
        },
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {
                    "code": "FUCK...",
                    "message": "aaaaa bbb cccc",
                    "request_id": "e3ccbe05-e8ab-4cdf-b2bc-c8c8af77eb69",
                }
            }
        },
    },
}
