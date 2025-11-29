from typing import List, Union, Tuple
from .Elements import *


class World:
    Name: str
    Description: str
    Elements: List[Union[StaticGeometry, BaseElement]]
    Connections: List[Tuple[str, str]]

    def __init__(self, Name: str = "", Description: str = ""):
        self.Name = Name
        self.Description = Description
        self.Elements = []
        self.Connections = []

    def Add(self, Element: Union[StaticGeometry, BaseElement]):
        self._ValidateElementTypes(Element)
        self.Elements.append(Element)

    def Connect(self, ElementFrom, ElementTo):
        if ElementFrom.GetType() != EPinType.Getter:
            raise ValueError(f"{EColorPrint.ERROR}[ERROR] Pin '{ElementFrom.GetPin()}' is not a Getter. Only Getter pins can be used as source in connection.")

        if ElementTo.GetType() != EPinType.Setter:
            raise ValueError(f"{EColorPrint.ERROR}[ERROR] Pin '{ElementTo.GetPin()}' is not a Setter. Only Setter pins can receive a connection.")

        self.Connections.append((ElementFrom.GetPin(), ElementTo.GetPin()))

    def Build(self) -> dict:
        Result = {
            "StaticMeshes": [],
            "Elements": {},
            "Connections": []
        }

        for i, Element in enumerate(self.Elements):
            if isinstance(Element, BaseElement):
                if Element.Name in Result["Elements"]:
                    raise TypeError(f"Duplicate element name '{Element.Name}' found at index {i}.")

                Result["Elements"][Element.Name] = Builder.BuildElement(Element)
                continue

            if isinstance(Element, StaticGeometry):
                Result["StaticMeshes"].append(Builder.BuildStaticMesh(Element))
                continue

            raise TypeError(f"Unsupported element type '{type(Element).__name__}' at index {i}.")

        for Connection in self.Connections:
            Result["Connections"].append(Connection)

        # DEBUG:
        import json
        print(json.dumps(Result, indent=2))

        return Result

    @staticmethod
    def _ValidateElementTypes(Element):
        """Checks that all fields match the annotations"""
        ClassAnnotations = Element.__class__.__annotations__

        for FieldName, ExpectedType in ClassAnnotations.items():
            if hasattr(Element, FieldName):
                actual_value = getattr(Element, FieldName)
                if not isinstance(actual_value, ExpectedType):
                    raise TypeError(f"Field '{FieldName}' should be {ExpectedType}, but got {type(actual_value)}")


class Builder:
    @staticmethod
    def BuildStaticMesh(Geometry: StaticGeometry) -> dict:
        return {
            "Transform": Geometry.Transform.Pack(),
            "StaticMeshAssetID": Builder._PackValue(Geometry.StaticMeshAssetID),
            "MaterialAssetID": Builder._PackValue(Geometry.MaterialAssetID)
        }

    @staticmethod
    def BuildElement(Element: BaseElement) -> dict:
        Properties = {}
        for FieldName, FieldValue in vars(Element).items():
            if FieldName not in ["Name", "Transform", "Pins"] and not FieldName.startswith('_'):
                Properties[FieldName] = Builder._PackValue(FieldValue)

        return {
            # "Name": Element.Name,
            "Transform": Element.Transform.Pack(),
            "Class": Element.__class__.__name__,
            "Properties": Properties
        }

    @staticmethod
    def _PackValue(Value) -> int:
        ValueType = type(Value)

        if ValueType == bool: return 1 if Value else 0
        if ValueType == FColor: return Value.Pack()
        if isinstance(Value, Enum): return Value.value

        raise TypeError(f"Unsupported type for packing: {ValueType}")
