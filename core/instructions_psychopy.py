try:
    from psychopy.visual import ImageStim, TextBox2
except ModuleNotFoundError:
    try:
        from rewardgym.psychopy_render.psychopy_stubs import ImageStim, TextBox2
    except ModuleNotFoundError:
        from ....psychopy_render.psychopy_stubs import ImageStim, TextBox2
try:
    from ....stimuli import (
        fixation_cross,
        lose_cross,
        win_cross,
        zero_cross,
        draw_robot,
        mid_stimuli,
    )

except ImportError:
    from rewardgym.stimuli import (
        fixation_cross,
        lose_cross,
        win_cross,
        zero_cross,
        draw_robot,
        mid_stimuli,
    )
import json
import pathlib

from .backend_psychopy import render_letter_to_array

instructions_path = (
    pathlib.Path(__file__).parent.resolve() / "assets" / "instructions_en.json"
)
instructions = json.loads(instructions_path.read_text())


def instructions_psychopy():

    directory = pathlib.Path(__file__).parents[0].resolve() / "assets"

    robot_fig = directory / "stimuli" / "robot.png"
    light_blue = directory / "stimuli" / "light_blue.png"
    light_red = directory / "stimuli" / "light_red.png"

    robot_fig = robot_fig.as_posix()
    light_blue = light_blue.as_posix()
    light_red = light_red.as_posix()

    font_path = directory / "BACS2sans.otf"

    if not font_path.is_file():
        font_path = None
    else:
        try:
            font_path = font_path.as_posix()
        except:
            pass


    robot_labels = ["1", "2", "3", "4"]

    letter_arrays = [render_letter_to_array(l.upper(), font_path=font_path) for l in robot_labels]


    def part_0(win, instructions):
        part_0_0 = TextBox2(
            win=win,
            text=instructions["0.0"] + "\n\n" + instructions["0.1"],
            letterHeight=28,
            pos=(0, 150),
        )

        part_0_0.draw()


    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["1.0"],
            letterHeight=28,
            pos=(0, 200),
        )

        robot_img = ImageStim(win=win, image=robot_fig, pos=(0, 0), size=(300, 300))
        robot_img.draw()
        part_1_0.draw()

    def part_2(win, instructions):
        part_2_0 = TextBox2(
            win=win,
            text=instructions["2.0"],
            letterHeight=28,
            pos=(0, 200),
        )

        robot_img = ImageStim(win=win, image=robot_fig, pos=(0, 0), size=(300, 300))
        letter = ImageStim(win, image=letter_arrays[0], pos=(0, 0), size=(96, 96))
        robot_img.draw()
        letter.draw()
        part_2_0.draw()


    def part_3(win, instructions):
        part_3_0 = TextBox2(
            win=win,
            text=instructions["3.0"] + "\n\n\n" + instructions["3.1"] + "\n\n" + instructions["3.2"],
            letterHeight=28,
            pos=(0, 175),
        )

        part_3_0.draw()

    def part_4(win, instructions):
        part_4_0 = TextBox2(
            win=win,
            text=instructions["4.0"],
            letterHeight=28,
            pos=(0, 175),
        )

        part_4_0.draw()

    def part_5(win, instructions):
        part_5_0 = TextBox2(
            win=win,
            text=instructions["5.0"],
            letterHeight=28,
            pos=(0, 250),
        )

        part_5_1 = TextBox2(
            win=win,
            text=instructions["5.1"],
            letterHeight=28,
            pos=(-200, 175),
        )

        part_5_2 = TextBox2(
            win=win,
            text=instructions["5.2"],
            letterHeight=28,
            pos=(0, 175),
        )

        part_5_3 = TextBox2(
            win=win,
            text=instructions["5.3"],
            letterHeight=28,
            pos=(200, 175),
        )


        robot_img = ImageStim(win=win, image=robot_fig, pos=(-200, 0), size=(300, 300))
        robot_img2 = ImageStim(win=win, image=robot_fig, pos=(200, 0), size=(300, 300))

        blue = ImageStim(win=win, image=light_blue, pos=(-200, 0), size=(300, 300))
        red = ImageStim(win=win, image=light_red, pos=(200, 0), size=(300, 300))

        robot_img.draw()
        robot_img2.draw()
        blue.draw()
        red.draw()

        part_5_0.draw()
        part_5_1.draw()
        part_5_2.draw()
        part_5_3.draw()


    def part_6(win, instructions):
        part_6_0 = TextBox2(
            win=win,
            text=instructions["6.0"],
            letterHeight=28,
            pos=(0, 250),
        )


        robot_img = ImageStim(win=win, image=robot_fig, pos=(0, 0), size=(300, 300))

        blue = ImageStim(win=win, image=light_blue, pos=(0, 0), size=(300, 300))

        robot_img.draw()
        blue.draw()

        part_6_0.draw()

    def part_7(win, instructions):
        part_7_0 = TextBox2(
            win=win,
            text=instructions["7.0"],
            letterHeight=28,
            pos=(0, 250),
        )


        robot_img = ImageStim(win=win, image=robot_fig, pos=(0, 0), size=(300, 300))

        blue = ImageStim(win=win, image=light_red, pos=(0, 0), size=(300, 300))

        robot_img.draw()
        blue.draw()

        part_7_0.draw()

    def part_8(win, instructions):
        part_8_0 = TextBox2(
            win=win,
            text=instructions["8.0"],
            letterHeight=28,
            pos=(0, 150),
        )

        part_8_0.draw()


    def part_9(win, instructions):
        part_9_0 = TextBox2(
            win=win,
            text=instructions["9.0"] + "\n\n\n" + instructions["9.1"],
            letterHeight=28,
            pos=(0, 150),
        )

        part_9_0.draw()


    def part_10(win, instructions):
        part_10_0 = TextBox2(
            win=win,
            text=instructions["10.0"],
            letterHeight=28,
            pos=(0, 150),
        )

        part_10_0.draw()


    def part_11(win, instructions):
        part_11_0 = TextBox2(
            win=win,
            text=instructions["11.0"],
            letterHeight=28,
            pos=(0, 150),
        )

        part_11_0.draw()


    return [part_0, part_1, part_2, part_3, part_4, part_5,part_6,part_7,part_8,part_9,part_10,part_11], instructions
