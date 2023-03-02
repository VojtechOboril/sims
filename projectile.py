import graphics as g
import time
from numpy import array, append
from math import atan, sqrt, degrees, sin, cos


class Projectile:
    def __init__(self, position:array, speed2d: array):
        self.position = position
        self.speed2d = speed2d

    def next_point(self, step = 1):
        self.position = self.position + (self.speed2d * step)
        self.speed2d[1] -= 10 * step
        return self.position

    def get_position(self):
        return self.position


def setup(name: str, size_x: int, size_y: int):
    window = g.GraphWin(name, size_x, size_y)
    return window

def main():
    window = setup("Test", 800, 800)
    speed = 150
    start_pos = array([0, 0])
    end_pos = array([500, 700])
    all_objects = array([])

    projectile = new_projectile(start_pos, end_pos, speed)
    trajectory(window, projectile, start_pos, end_pos, all_objects, "black", 0.1)

    projectile = new_projectile(start_pos, end_pos, speed, False)
    trajectory(window, projectile, start_pos, end_pos, all_objects, "red", 0.1)


    while True:
        move_all(window)
    window.close()

def move_all(window: g.GraphWin)->None:
    p1 = window.getMouse()
    p2 = window.getMouse()
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    for item in window.items:
        item.move(dx, dy)


def new_projectile(start_pos: array, end_pos: array, speed: int, smaller_angle: bool = True)->Projectile:
    angles = speed_to_angle(start_pos, end_pos, speed)
    if smaller_angle:
        angle = min(angles)
    else:
        angle = max(angles)
    speed2d = array([cos(angle) * speed, sin(angle) * speed])
    projectile = Projectile(start_pos, speed2d)
    return projectile

def speed_to_angle(start: array, end: array, projectile_speed: int):
    dy = end[1] - start[1]
    dx = end[0] - start[0]
    try:
        solution1 = atan(
            (
                projectile_speed**2+sqrt(projectile_speed**4-10*(10*dx**2 + 2*projectile_speed**2 * dy))
            )/
            (
                10*dx
            )
        )
    except ValueError:
        solution1 = 0.0
    try:
        solution2 = atan(
            (
                projectile_speed**2-sqrt(projectile_speed**4-10*(10*dx**2 + 2*projectile_speed**2 * dy))
            )/
            (
                10*dx
            )
        )
    except ValueError:
        solution2 = 0.0
    return(solution1, solution2)

def trajectory(window: g.GraphWin, projectile: Projectile, start: array, end: array, all_objects: array, color: str = "black", step: float = 1)->array:
    start_p = g.Circle(g.Point(start[0], window.getHeight() - start[1]), 5)
    start_p.setFill("blue")
    start_p.draw(window)
    append(all_objects, start_p)

    end_p = g.Circle(g.Point(end[0], window.getHeight()- end[1]), 5)
    end_p.setFill("blue")
    end_p.draw(window)
    append(all_objects, end_p)

    while True:
        position = projectile.next_point(step)
        p = g.Circle(g.Point(position[0], window.getHeight() - position[1]), 3)
        p.setFill(color)
        p.setOutline(color)
        p.draw(window)
        append(all_objects, p)
        if (position[0] > end[0]):
            break

    return all_objects


if __name__ == "__main__":
    main()
