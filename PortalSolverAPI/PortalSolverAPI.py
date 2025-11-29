import requests
from typing import Optional
from .Types import EColorPrint
from .World import World


class PortalSolverAPI:
    def __init__(self, Host: str = 'localhost', Port: int = 20563):
        self.Host: str = Host
        self.Port: int = Port
        self.URL: str = f"http://{Host}:{Port}"

    def Build(self, world: World = None, json: dict = None):
        if world is not None:
            self.Send("/build", world.Build())
            print(f"{EColorPrint.OK_GREEN}[OK] World data successfully builded and sent")
        elif json is not None:
            self.Send("/build", json)
            print(f"{EColorPrint.OK_GREEN}[OK] JSON data successfully sent")
        else:
            print(f"{EColorPrint.WARNING}[WARNING] No \"world\" or \"json\" data to sent")

    def Run(self):
        if self.Send("/run"):
            print(f"{EColorPrint.OK_GREEN}[OK] Portal: Solver runned. Have a nice game!")

    def Send(self, endpoint: str, json: Optional[dict] = None) -> bool:
        try:
            response = requests.post(
                f"{self.URL}{endpoint}",
                json=json,
                timeout=5.0
            )

            if response.status_code == 200 and response.text == "OK":
                return True
            else:
                print(f"{EColorPrint.ERROR}[ERROR] Server error: {response.status_code} - {response.text}")
                return False

        except requests.exceptions.ConnectionError:
            print(f"{EColorPrint.ERROR}[ERROR] Connection failed - is Portal Solver running with Python Editor mode?")
            return False

        except requests.exceptions.Timeout:
            print(f"{EColorPrint.ERROR}[ERROR] Request timeout - game might be busy")
            return False

        except Exception as e:
            print(f"{EColorPrint.ERROR}[ERROR] Unexpected error: {e}")
            return False
