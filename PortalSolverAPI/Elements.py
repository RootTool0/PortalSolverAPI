from .Types import *
from typing import Dict


class StaticGeometry:
    Transform: FTransform
    StaticMeshAssetID: EStaticMeshAsset
    MaterialAssetID: EMaterialAsset

    def __init__(self, Transform: FTransform = FTransform(), StaticMeshAssetID: EStaticMeshAsset = EStaticMeshAsset.Plane, MaterialAssetID: EMaterialAsset = EMaterialAsset.Wall_White_Small):
        self.Transform = Transform
        self.StaticMeshAssetID = StaticMeshAssetID
        self.MaterialAssetID = MaterialAssetID


class BaseElement:
    Name: str
    Transform: FTransform
    _Pins: Dict[EPin, FPin]

    def __init__(self, Name: str = "ElementName", Transform: FTransform = FTransform()):
        self.Name = Name
        self.Transform = Transform

    def GetPin(self, Pin: EPin):
        if Pin not in self._Pins:
            raise ValueError(f"{Pin} is not a valid pin for element {self.__class__.__name__} with name '{self.Name}'")
        return self._Pins[Pin]


# Elements


'''
Progress: 2/20

[-] AntiExpropriationFieldElement
[-] ButtonElement
[-] CubeDropperElement
[-] CubeElement
[+] DoorElement
[-] FaithPlateElement
[-] IndicatorElement
[-] LaserCubeElement
[-] LaserRelayElement
[-] LaserRXElement
[-] LaserTXElement
[-] PanelElement
[-] PedestalButtonElement
[-] SolverButtonElement
[-] SolverGunPedestalElement
[-] StairsElement
[-] TriggerElement
[-] WeightCubeElement
[-] WindowElement
[-] WireElement
'''


class DoorElement(BaseElement):
    bState: bool
    ColorActivated: FColor
    ColorDeactivated: FColor

    def __init__(self, Name: str = "ElementName", Transform: FTransform = FTransform()):
        super().__init__(Name, Transform)
        self.bState = False
        self.ColorActivated = FColor(255, 203, 89)
        self.ColorDeactivated = FColor(89, 255, 255)

        self._Pins = {EPin.SetState: FPin(Name, "SetState", EPinType.Setter)}


class ButtonElement(BaseElement):
    ColorActivated: FColor
    ColorDeactivated: FColor

    def __init__(self, Name: str = "ElementName", Transform: FTransform = FTransform()):
        super().__init__(Name, Transform)
        self.ColorActivated = FColor(255, 203, 89)
        self.ColorDeactivated = FColor(89, 255, 255)

        self._Pins = {EPin.GetState: FPin(Name, "GetState", EPinType.Getter)}
