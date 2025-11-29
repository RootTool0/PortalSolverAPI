from enum import Enum


class EColorPrint:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class FVector:
    def __init__(self, X: float, Y: float, Z: float):
        self.X: float = X
        self.Y: float = Y
        self.Z: float = Z


class FTransform:
    def __init__(self, Location: FVector = FVector(0, 0, 0), Rotation: FVector = FVector(0, 0, 0), Scale: FVector = FVector(1, 1, 1)):
        self.Location: FVector = Location
        self.Rotation: FVector = Rotation  # (pitch, yaw, roll)
        self.Scale: FVector = Scale

    def Pack(self) -> dict:
        return {
            "Location": [self.Location.X, self.Location.Y, self.Location.Z],
            "Rotation": [self.Rotation.X, self.Rotation.Y, self.Rotation.Z],
            "Scale": [self.Scale.X, self.Scale.Y, self.Scale.Z]
        }


class FColor:
    def __init__(self, R: int = 0, G: int = 0, B: int = 0):
        """
        Args:
            R: 0-255
            G: 0-255
            B: 0-255
        """
        self.R: int = R
        self.G: int = G
        self.B: int = B

    def Pack(self) -> int:
        return (self.R << 16) | (self.G << 8) | self.B


class EMaterialAsset(Enum):
    Wall_White_Small = 0
    Wall_White_Medium = 1
    Wall_White_Double = 2
    Wall_White_Big = 3
    Wall_White_AbsoluteScience = 4

    Wall_Black_Small = 5
    Wall_Black_Medium = 6
    Wall_Black_Big = 7

    Floor_White = 8
    Floor_Black = 9


class EStaticMeshAsset(Enum):
    Cube = 0
    Plane = 1
    Face = 2

    O_Inner = 3
    O_Outer = 4

    U_Inner = 5
    U_Outer = 6

    II_Inner = 7
    II_Outer = 8

    Cup_Inner = 9
    Cup_Outer = 10


class EPin(Enum):
    SetState = "SetState"
    GetState = "GetState"


class EPinType(Enum):
    Getter = 0
    Setter = 1


class FPin:
    def __init__(self, ElementName: str, PinName: str, Type: EPinType):
        self.ElementName = ElementName
        self.PinName = PinName
        self.Type = Type

    def GetPin(self) -> str:
        return f"{self.ElementName}::{self.PinName}"

    def GetType(self) -> EPinType:
        return self.Type
