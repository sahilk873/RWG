#builtin
from typing import List, Union
from enum import Enum

#external
from pydantic import BaseModel

class MetadataType(str, Enum):
    PERSON = "Person"
    PLACE = "Place"
    EVENT = "Event"
    RELATIONSHIP = "Relationship"

class PersonMetadata(BaseModel):
    type: MetadataType = MetadataType.PERSON
    name: str
    birth_date: str
    death_date: str
    role: str
    contribution: str

class PlaceMetadata(BaseModel):
    type: MetadataType = MetadataType.PLACE
    name: str
    location: str
    significance: str

class EventMetadata(BaseModel):
    type: MetadataType = MetadataType.EVENT
    name: str
    date: str
    location: str
    outcome: str
    significance: str

class RelationshipMetadata(BaseModel):
    type: MetadataType = MetadataType.RELATIONSHIP
    relationship_type: str
    entity1_id: str
    entity2_id: str

class RelationshipModel(BaseModel):
    id: str
    metadata: RelationshipMetadata
    text_snippet: str

class FinalEntity(BaseModel):
    id: str
    metadata: Union[PersonMetadata, PlaceMetadata, EventMetadata]
    text_snippet: str

class EntitiesResponseModel(BaseModel):
    entities: List[FinalEntity]
    relationships: List[RelationshipModel]

class FinalRelationship(BaseModel):
    id: str
    metadata: RelationshipMetadata
    text_snippet: str
    embedding: List[float]

class EntityMetadata(BaseModel):
    entity1_id: str
    entity2_id: str
    relationship: str
