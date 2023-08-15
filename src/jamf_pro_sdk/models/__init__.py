from pydantic import BaseModel as PydanticBaseModel

# Removes the docstring from the __init__ of the BaseModel for Sphinx documentation.


class BaseModel(PydanticBaseModel):
    def __init__(self, **kwargs):
        """"""
        super().__init__(**kwargs)
