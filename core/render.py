from copy import deepcopy

from rewardgym import check_random_state

from rewardgym.stimuli import (
    fixation_cross,
    make_card_stimulus,
    generate_stimulus_properties,
    draw_robot,
    mid_stimuli,
    STIMULUS_DEFAULTS,
)

from rewardgym.render import ImageDefinition
from rewardgym.render.passive_routines import PresentationRoutine, FeedBackRoutine
from rewardgym.render.response_routines import ChangeSceneAfterAction

import string
import pathlib
import math
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def render_letter_to_array(
    letter='A',
    image_size=(128, 128),
    margin_px=10,
    font_path=None,
    font_name='DejaVu Sans',
    outer_color='black',
    inner_color=(128,128,128),
    font_color='white',
    bg_color=(0, 0, 0, 0),  # fully transparent
):
    width, height = image_size
    center = (width // 2, height // 2)
    outer_radius = min(width, height) // 2
    inner_radius = outer_radius - margin_px

    # STEP 1 — Create the base RGBA image with Pillow
    base_img = Image.new('RGBA', image_size, bg_color)
    draw = ImageDraw.Draw(base_img)

    # Draw outer circle
    draw.ellipse(
        [center[0] - outer_radius, center[1] - outer_radius,
         center[0] + outer_radius, center[1] + outer_radius],
        fill=outer_color
    )

    # Draw inner circle
    draw.ellipse(
        [center[0] - inner_radius, center[1] - inner_radius,
         center[0] + inner_radius, center[1] + inner_radius],
        fill=inner_color
    )

    # STEP 2 — Render the letter using matplotlib to a transparent image
    letter_img_size = 512  # render large so scaling looks clean
    fig = plt.figure(figsize=(letter_img_size / 100, letter_img_size / 100), dpi=100)
    canvas = FigureCanvas(fig)

    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, letter_img_size)
    ax.set_ylim(0, letter_img_size)
    ax.axis('off')
    ax.set_facecolor((0, 0, 0, 0))
    # Font setup
    if font_path and os.path.exists(font_path):
        font_prop = FontProperties(fname=font_path)
    else:
        font_prop = FontProperties(family=font_name)

    # Draw text
    ax.text(
        letter_img_size / 2,
        letter_img_size / 2,
        letter,
        fontproperties=font_prop,
        fontsize=letter_img_size * 0.8,  # oversized — we'll scale later
        color=font_color,
        ha='center',
        va='center'
    )

    # Render to buffer
    canvas.draw()
    letter_img_buf = np.asarray(canvas.buffer_rgba()).copy()
    plt.close(fig)

    # Convert to Pillow and crop tight to the letter
    letter_img = Image.fromarray(letter_img_buf)
    letter_bbox = letter_img.getbbox()
    letter_img = letter_img.crop(letter_bbox)

    # STEP 3 — Resize letter image to fit inside inner circle
    max_letter_width = inner_radius * 2 - 2.5 * margin_px
    max_letter_height = inner_radius * 2 - 2.5 * margin_px
    letter_img.thumbnail((max_letter_width, max_letter_height), Image.NEAREST)

    # STEP 4 — Paste letter onto base image (centered)
    paste_x = (width - letter_img.width) // 2
    paste_y = (height - letter_img.height) // 2
    base_img.alpha_composite(letter_img, dest=(paste_x, paste_y))

    return np.array(base_img)[::-1, :] / 255


def get_render_info(
    random_state=None, key_dict={"space": 0}, external_stimuli=None, fullpoints=None, **kwargs
):
    random_state = check_random_state(random_state)

    directory = pathlib.Path(__file__).parents[0].resolve() / "assets"

    robot_fig = directory / "stimuli" / "robot.png"
    light_blue = directory / "stimuli" / "light_blue.png"
    light_red = directory / "stimuli" / "light_red.png"
    factory = directory / "stimuli" / "factory.png"

    robot_fig = robot_fig.as_posix()
    light_blue = light_blue.as_posix()
    light_red = light_red.as_posix()
    factory = factory.as_posix()

    if external_stimuli is None:
        font_path = directory / "BACS2sans.otf"
    else:
        font_path = pathlib.Path(external_stimuli)

    if not font_path.is_file():
        font_path = None
    else:
        try:
            font_path = font_path.as_posix()
        except:
            pass

    letters = list(string.ascii_lowercase)

    robot_labels = random_state.choice(letters, 8, replace=False)

    letter_arrays = [render_letter_to_array(l.upper(), font_path=font_path) for l in robot_labels]

    reward_feedback = FeedBackRoutine(
        duration=1.0, name="reward", bar_total=fullpoints, rl_label="reward"
    )

    stimuli = {"letters": robot_labels.tolist()}

    base_stim = PresentationRoutine(name="fixation", duration=0.3, stimulus_definitions=[
        ImageDefinition(name="fix", autoDraw=True, image=fixation_cross(), pos=(0, 0)),
        ImageDefinition(name="factory", autoDraw=True, image=factory, pos=(0, -3))])

    fix_isi = PresentationRoutine(name="isi", duration=0.3, stimulus_definitions=[
        ImageDefinition(
            name="fix2",
            autoDraw=True,
            image=fixation_cross()
        )
    ])

    def first_step(letter, light):
        return [
            base_stim,
            PresentationRoutine(
                duration=1.3,
                stimulus_definitions=[
                    ImageDefinition(
                        name="robot-body",
                        pos = (0, 0),
                        image = robot_fig
                    ),
                    ImageDefinition(
                        image=letter,
                        pos=(0, 0),
                        name="robot-label"
                    ),
                ],
                name="cue",
                rl_label="obs"
            ),
            ChangeSceneAfterAction(
                name="response",
                rl_label="action",
                duration=1.0,
                key_dict=key_dict,
                stimulus_definitions=[
                    ImageDefinition(
                        name="robot",
                        image=robot_fig,
                        pos=(0, 0)
                    ),
                    ImageDefinition(
                        name="label",
                        image=letter,
                        pos=(0, 0),
                    ),
                    ImageDefinition(
                        name="light",
                        image=light,
                        pos=(0, 0)
                    )
                ],
                timeout_action=1,
                name_timeout="reponse-time-out",
                presentation_settings={
                    "name_before": "target",
                    "name_after": "delay",
                    "duration_after": 0.5,
                    "present_after": True
                },
                draw_stims_after=["robot", "label"]
            )

        ]
    final_step = [
        PresentationRoutine(duration=0.5, name="reward-delay", rl_label=None),
        reward_feedback,
        PresentationRoutine(name="iti", duration=1.0, rl_label='obs'),
    ]

    info_dict = {
        0: {"render": []},
        1: {"render": first_step(letter_arrays[0], light_blue)},
        2: {"render": first_step(letter_arrays[1], light_red)},
        3: {"render": first_step(letter_arrays[2], light_blue)},
        4: {"render": first_step(letter_arrays[3], light_red)},
        5: {"render": first_step(letter_arrays[4], light_blue)},
        6: {"render": first_step(letter_arrays[5], light_red)},
        7: {"render": first_step(letter_arrays[6], light_blue)},
        8: {"render": first_step(letter_arrays[7], light_red)},
        9: {"render": final_step},
        10: {"render": final_step},
        11: {"render": final_step},
        12: {"render": final_step},

    }

    return info_dict, stimuli
