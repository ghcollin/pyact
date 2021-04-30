from typing import Dict, Callable, List, Union
from .context import Context

JSON = Dict
PyactApp = Callable[[Context], JSON]
ChildList = List[Union[str, PyactApp]]