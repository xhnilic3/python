#!/usr/bin/python3
# vim: tabstop=4 shiftwidth=4 expandtab
from random import random, seed
from PIL import Image, ImageDraw

SAMPLE_WIDTH = 32

COLOR_TOP = (255, 0, 0)
COLOR_BUTT = (0, 255, 0)
COLOR_GRID = (0, 0, 0)

PICTURE_WIDHT = 3840
PICTURE_HEIGHT = 2160

COLUMN_COUNT = SAMPLE_WIDTH
COLUMN_HEIGHT = 18

FILENAME_FORMAT = "{:s}_{:06d}.jpg"


def visualization(filename_base, animation_length):
    column_width = PICTURE_WIDHT // COLUMN_COUNT
    cell_height = PICTURE_HEIGHT // COLUMN_HEIGHT

    def render_frame(sample, number):
        def get_cell_color(_, y, value):
            def get_gradient(a, b, y):
                c = (
                    int(((b[0] - a[0]) * y)),
                    int(((b[1] - a[1]) * y)),
                    int(((b[2] - a[2]) * y)))

                return (
                    (c[0] + a[0]),
                    (c[1] + a[1]),
                    (c[2] + a[2]))

            def darken(color):
                return (color[0] // 2, color[1] // 2, color[2] // 2)

            dark = value > (y * cell_height / PICTURE_HEIGHT)
            color_base = get_gradient(COLOR_TOP, COLOR_BUTT, y / COLUMN_HEIGHT)
            return darken(color_base) if dark else color_base

        im = Image.new("RGB", (PICTURE_WIDHT, PICTURE_HEIGHT))
        imdr = ImageDraw.Draw(im)

        for column in range(COLUMN_COUNT):
            value = sample[column]

            for cell in range(COLUMN_HEIGHT):
                x0 = (column * column_width)
                x1 = x0 + column_width
                y0 = (cell * cell_height)
                y1 = y0 + cell_height
                fill = get_cell_color(column, cell, value)

                imdr.rectangle(
                    [x0, y0, x1, y1],
                    fill=fill,
                    outline=COLOR_GRID)

        filename = FILENAME_FORMAT.format(filename_base, number)
        print("Saving {:s}".format(filename))
        im.save(filename)

    def next_sample(prev_sample):
        for i in range(SAMPLE_WIDTH):
            prev_sample[i] = max(0, min(1, prev_sample[i] + (random()-0.5)/5))
        return prev_sample

    current_sample = [random() for _ in range(SAMPLE_WIDTH)]

    for i in range(animation_length):
        render_frame(current_sample, i)
        current_sample = next_sample(current_sample)


def main():
    seed(42)
    visualization("animace/frame", 100)


if __name__ == "__main__":
    main()
