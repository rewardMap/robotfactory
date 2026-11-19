import json
import pathlib

from rewardgym.render.routines.passive_routines import InstructionRoutine
from rewardgym.render.stimulus_definitions import (
    ImageDefinition,
    TextDefinition,
)
from rewardgym.utils import NameCounter

from .render import render_letter_to_array

instructions_path = (
    pathlib.Path(__file__).parent.resolve() / "assets" / "instructions_en.json"
)
instructions = json.loads(instructions_path.read_text())


def get_instructions():
    name = NameCounter()

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
        font_path = pathlib.Path(font_path).as_posix()


    robot_labels = ["1", "2", "3", "4"]

    letter_arrays = [render_letter_to_array(l.upper(), font_path=font_path) for l in robot_labels]


    part_0_0 = TextDefinition(
        name=name.name,
        text=instructions["0.0"] + "\n\n" + instructions["0.1"],
        height=28,
        pos=(0, 150),
    )

    part_0 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_0_0],
    )


    part_1_0 = TextDefinition(
        name=name.name,
        text=instructions["1.0"],
        height=28,
        pos=(0, 200),
    )

    robot_img = ImageDefinition(name=name.name, image=robot_fig, pos=(0, 0), size=(300, 300))

    part_1 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_1_0, robot_img],
    )
    part_2_0 = TextDefinition(
        name=name.name,
        text=instructions["2.0"],
        height=28,
        pos=(0, 200),
    )

    robot_img = ImageDefinition(name=name.name, image=robot_fig, pos=(0, 0), size=(300, 300))
    letter = ImageDefinition(name=name.name, image=letter_arrays[0], pos=(0, 0), size=(96, 96))

    part_2 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_2_0, robot_img, letter],
    )

    part_3_0 = TextDefinition(
        name=name.name,
        text=instructions["3.0"] + "\n\n\n" + instructions["3.1"] + "\n\n" + instructions["3.2"],
        height=28,
        pos=(0, 175),
    )

    part_3 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_3_0],
    )
    part_4_0 = TextDefinition(
        name=name.name,
        text=instructions["4.0"],
        height=28,
        pos=(0, 175),
    )

    part_4 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_4_0],
    )

    part_5_0 = TextDefinition(
        name=name.name,
        text=instructions["5.0"],
        height=28,
        pos=(0, 250),
    )

    part_5_1 = TextDefinition(
        name=name.name,
        text=instructions["5.1"],
        height=28,
        pos=(-200, 175),
    )

    part_5_2 = TextDefinition(
        name=name.name,
        text=instructions["5.2"],
        height=28,
        pos=(0, 175),
    )

    part_5_3 = TextDefinition(
        name=name.name,
        text=instructions["5.3"],
        height=28,
        pos=(200, 175),
    )


    robot_img = ImageDefinition(name=name.name, image=robot_fig, pos=(-200, 0), size=(300, 300))
    robot_img2 = ImageDefinition(name=name.name, image=robot_fig, pos=(200, 0), size=(300, 300))

    blue = ImageDefinition(name=name.name, image=light_blue, pos=(-200, 0), size=(300, 300))
    red = ImageDefinition(name=name.name, image=light_red, pos=(200, 0), size=(300, 300))

    part_5 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[robot_img, robot_img2, blue, red, part_5_0, part_5_1, part_5_2, part_5_3],
    )
    part_6_0 = TextDefinition(
        name=name.name,
        text=instructions["6.0"],
        height=28,
        pos=(0, 250),
    )


    robot_img = ImageDefinition(name=name.name, image=robot_fig, pos=(0, 0), size=(300, 300))

    blue = ImageDefinition(name=name.name, image=light_blue, pos=(0, 0), size=(300, 300))

    part_6 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[robot_img, blue, part_6_0],
    )
    part_7_0 = TextDefinition(
        name=name.name,
        text=instructions["7.0"],
        height=28,
        pos=(0, 250),
    )


    robot_img = ImageDefinition(name=name.name, image=robot_fig, pos=(0, 0), size=(300, 300))

    blue = ImageDefinition(name=name.name, image=light_red, pos=(0, 0), size=(300, 300))

    part_7 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[robot_img, blue, part_7_0],
    )

    part_8_0 = TextDefinition(
        name=name.name,
        text=instructions["8.0"],
        height=28,
        pos=(0, 150),
    )

    part_8 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_8_0],
    )

    part_9_0 = TextDefinition(
        name=name.name,
        text=instructions["9.0"] + "\n\n\n" + instructions["9.1"],
        height=28,
        pos=(0, 150),
    )

    part_9 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_9_0],
    )

    part_10_0 = TextDefinition(
        name=name.name,
        text=instructions["10.0"],
        height=28,
        pos=(0, 150),
    )

    part_10 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_10_0],
    )

    part_11_0 = TextDefinition(
        name=name.name,
        text=instructions["11.0"],
        height=28,
        pos=(0, 150),
    )
    part_11 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_11_0],
    )

    return [part_0, part_1, part_2, part_3, part_4, part_5,part_6,part_7,part_8,part_9,part_10,part_11], instructions
