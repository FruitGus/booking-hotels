from pydantic import BaseModel, ConfigDict


class FacilitiesAddRequest(BaseModel):
    title: str


class Facility(FacilitiesAddRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)