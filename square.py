import time

from simple_airsim.api import coordinate_system
from simple_airsim.api.drone import Drone
from simple_airsim.api.gui_manager import GUIManager
from simple_airsim.api.manager import Manager


def loop(drone: Drone):
    battery = 100
    drone.takeoff(True)
    while True:
        print(battery)
        lidarsData = drone.get_lidars()
        while lidarsData["right"] > 0.5:
            drone.move_by(0.1, 1, 0, False)
            lidarsData = drone.get_lidars()

        if lidarsData["front"] > 1.0:
            drone.move_by(1, 0, 0, False)
            time.sleep(0.1)
            lidarsData = drone.get_lidars()
        elif lidarsData["right"] < 0.8:
            drone.turn_by(0, 0, -80, False)
            time.sleep(0.3)
            lidarsData = drone.get_lidars()
        elif lidarsData["left"] < 0.8:
            drone.turn_by(0, 0, 80, False)
            time.sleep(0.3)
            lidarsData = drone.get_lidars()

        if lidarsData["down"] < 0.5:
            battery = battery - 1
            drone.move_by(0, 1, 0, False)
            time.sleep(0.3)
            lidarsData = drone.get_lidars()

        if battery < 50:
            drone.land(True)

        time.sleep(0.1)


if __name__ == '__main__':
    with Manager(coordinate_system.AIRSIM, method=loop) as man:
        with GUIManager(man, 10, 10, 10, 3) as gui:
            gui.start()
