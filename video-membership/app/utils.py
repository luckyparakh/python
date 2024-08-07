import json
from pydantic import BaseModel, error_wrappers
def valid_schema_data_or_error(raw_dict: dict, Schema: BaseModel):
    data = {}
    errors = []
    error_str = None
    try:
        clean_data = Schema(**raw_dict)
        data = clean_data.model_dump()
    except error_wrappers.ValidationError as e:
        error_str = e.json()
    
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc": "non_field error", "msg": "unknown error"}]
    return data, errors