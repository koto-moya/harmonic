from pydantic import BaseModel, field_validator
from typing import List, Optional, Tuple, Any
import numpy as np

class AssetPayload(BaseModel):
    type: str  # "chart", "table", "custom", etc.
    enable_mouseover: bool = True

class ChartAssetPayload(AssetPayload):
    type: str = "chart"  # "chart", "table", "custom", etc.
    title: str = None
    x_values: Optional[Any] = None  # Will store numpy array or list
    y_label_left: str = None
    y_label_right: Optional[str] = None
    multi_line: bool = False
    dual_axis: bool = False
    y_values_right: Optional[Any] = None  
    y_values_left: Optional[Any]= None  
    left_units: str = None
    right_units: Optional[str] = None
    is_datetime: bool = False
    width: int = 780
    height: int = 420

    model_config = {
        "arbitrary_types_allowed": True  # Allow numpy arrays
    }
    
    