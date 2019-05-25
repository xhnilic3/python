#!/usr/bin/python3
# vim: tabstop=4 shiftwidth=4 expandtab
from random import randint, seed
import math




class SVGTurtle:
    class Saver:
        SVG_START = "<svg width='100%' height='100%' xmlns='http://www.w3.org/2000/svg' xmlns:xlink= 'http://www.w3.org/1999/xlink'>\n"
        SVG_LINE = "\t<line x1='{}' y1='{}' x2='{}' y2='{}' style='stroke: {}; stroke-width:2' />\n"
        SVG_END = "\n</svg>"

        def __init__(self, filename):
            self._filename = filename
            self._f = open(filename, "w")
            self._f.write(SVGTurtle.Saver.SVG_START)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self._f.write(SVGTurtle.Saver.SVG_END)
            self._f.close()

        def _parse_turtle(self, turtle):
            svg = ""
            for x1, y1, x2, y2, col in turtle.lines:
                svg += SVGTurtle.Saver.SVG_LINE.format(x1, y1, x2, y2, col)
            return svg

        def append_turtle(self, turtle):
            parsed = self._parse_turtle(turtle)
            self._f.write(parsed)

    def __init__(self):
        self.x = 50
        self.y = 50
        self.heading = 0
        self.lines = []
        self.color = "black"

    def left(self, angle):
        self.heading -= angle

    def right(self, angle):
        self.heading += angle

    def forward(self, d):
        nx = self.x + d * math.cos(self.heading * math.pi / 180)
        ny = self.y + d * math.sin(self.heading * math.pi / 180)
        self.lines.append((self.x, self.y, nx, ny, self.color))
        self.x, self.y = nx, ny

    def back(self, d):
        self.heading += 180
        self.forward(d)
        self.heading -= 180

    def set_color(self, color):
        self.color = color

    def random_step(self, distance):
        self.right(randint(0, 360))
        self.forward(distance)

    def regular_n_gon(self, num_sides, radius):
        angle = 360 / num_sides
        side = (math.cos(math.radians(90 - angle / 2)) * radius) * 2

        for _ in range(num_sides):
            self.forward(side)
            self.left(angle)

    def turn_to(self, turtle):
        x2 = turtle.x
        y2 = turtle.y
        x1 = self.x
        y1 = self.y

        if x2 - x1 == 0:
            gradient = 0
        else:
            gradient = (y2 - y1) / (x2 - x1)

        self.heading = math.degrees(math.atan(gradient))
        if x2 < x1:
            self.heading += 180

    def connect(self, turtle):
        self.turn_to(turtle)
        distance = math.sqrt((turtle.x - self.x)**2 + (turtle.y - self.y)**2)
        self.forward(distance)

    def connect_and_back(self, turtle):
        last = self.heading
        distance = math.sqrt((turtle.x - self.x)**2 + (turtle.y - self.y)**2)
        self.connect(turtle)
        self.back(distance)
        self.heading = last


NUM_STEPS = 20
RADIUS = 250
ENEMY_SPEED_MULT = 1.2


def run_forest_run(svgfilename):
    '''
    Pronasledovatele se budou pohybovat 1,2 krat rychleji nez nahanena zelva.
    '''

    def find_distance(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def coordinates(angle, distance):
        x = distance * math.sin(angle)
        y = distance * math.cos(angle)
        return [x, y]

    def caught(counter):
        for turtle in turtles:
            if len(turtle) > 1:
                counter += 1
        if counter == len(turtles):
            return False
        return True

    t1 = SVGTurtle()
    t1.set_color("red")
    t1.x = 265
    t1.y = 200

    turtles = [[SVGTurtle()] for _ in range(20)]
    hunter_color = 255 - int(255 / len(turtles))
    angle = 0
    for turtle in turtles:
        turtle[0].x = coordinates(angle, 250)[0] + t1.x
        turtle[0].y = coordinates(angle, 250)[1] + t1.y
        angle += 360 / len(turtles)
        turtle[0].set_color("#{:02x}{:02x}FF".format(hunter_color, hunter_color))
        hunter_color -= int(255 / len(turtles))

    t1.left(180)
    t1.forward(125)
    t1.left(180)

    chase = True
    distance = RADIUS / NUM_STEPS
    counter = 0
    while chase:
        for _ in range(NUM_STEPS):
            t1.forward(distance)
            for turtle in turtles:
                if find_distance(turtle[0], t1) < distance * ENEMY_SPEED_MULT:
                    if not len(turtle) > 1:
                        turtle.append(1)
                    continue
                else:
                    turtle[0].turn_to(t1)
                    turtle[0].forward(distance * ENEMY_SPEED_MULT)
        chase = caught(counter)

    with SVGTurtle.Saver(svgfilename) as save:
        for t in [[t1]] + turtles:
            save.append_turtle(t[0])


def main():
    seed(42)
    # visualization("animace", 100)
    run_forest_run("svg/svg_turtle.svg")
    # lorem_ipsum("dlouhy_textovy_soubor.txt", 500)


if __name__ == "__main__":
    main()
