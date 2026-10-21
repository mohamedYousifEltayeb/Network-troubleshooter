def get_base_context(devices = None):

    return {
        "username": "Alice",
        "companyname": "Canar Telecom",
        "devices":devices or [],
    }
