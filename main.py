from PortalSolverAPI import *

world = World()

door = DoorElement()
door.ColorActivated = FColor(255, 255, 255)
world.Add(door)

button = ButtonElement("123")
button.ColorActivated = FColor(255, 255, 255)
world.Add(button)

world.Connect(button.GetPin(EPin.GetState), door.GetPin(EPin.SetState))

for x in range(0, 2):
    for y in range(0, 2):
        FloorColor = EMaterialAsset.Floor_Black
        if (x + y) % 2 == 0:
            FloorColor = EMaterialAsset.Floor_White

        world.Add(StaticGeometry(FTransform(FVector(x*100, y*100, -200)), EStaticMeshAsset.Plane, FloorColor))

world.Add(StaticGeometry(FTransform(FVector(100, 100, 0)), EStaticMeshAsset.Cube, EMaterialAsset.Wall_White_Medium))

# А затем уже получаем API PortalSolver, передаем туда билдинг мира, и запускаем игру!
api = PortalSolverAPI()
api.Build(world=world)
api.Run()
