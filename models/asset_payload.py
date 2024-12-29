from pydantic import BaseModel, field_validator
from typing import List, Optional, Tuple, Any
import numpy as np

class AssetPayload(BaseModel):
    type: str  # "chart", "table", "custom", etc.
    x_values: Optional[Any] = None  # Will store numpy array
    data_series: Optional[List[Tuple[Any, str, str]]] = None  # (data, label, units)
    is_datetime: bool = False
    enable_mouseover: bool = True

    model_config = {
        "arbitrary_types_allowed": True  # Allow numpy arrays
    }
    
    @field_validator('x_values')
    def validate_x_values(cls, v):
        if v is not None and not isinstance(v, np.ndarray):
            raise ValueError('x_values must be a numpy array')
        return v
    
    @field_validator('data_series')
    def validate_data_series(cls, v):
        if v is not None:
            for item in v:
                if not isinstance(item[0], np.ndarray):
                    raise ValueError('data series values must be numpy arrays')
        return v
