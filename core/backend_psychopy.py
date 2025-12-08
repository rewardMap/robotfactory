from copy import deepcopy

from rewardgym import check_random_state
from rewardgym.psychopy_render import (
    ImageStimulus,
    FeedBackStimulus,
    ActionStimulus,
    BaseStimulus,
    LingeringAction
)
from rewardgym.stimuli import (
    fixation_cross,
    make_card_stimulus,
    generate_stimulus_properties,
    draw_robot,
    mid_stimuli,
    STIMULUS_DEFAULTS,
)

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


def get_psychopy_info(
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

    reward_feedback = FeedBackStimulus(
        1.0, text="{0}", target="reward", name="reward", bar_total=fullpoints, rl_label="reward"
    )

    stimuli = {"letters": letters}

    base_stim = ImageStimulus(
        image_paths=[fixation_cross(), factory], duration=0.3, name="fixation", autodraw=True,
        positions=[(0, 0), (0, -3)]
    )

    fix_isi = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.3, name="isi", autodraw=False
    )

    def first_step(letter, light):
        return [
            base_stim,
            ImageStimulus(
                duration=1.3,
                image_paths=[robot_fig, letter],
                positions=[(0, 0), (0, 0)],
                name="cue",
                rl_label="obs"
            ),
            LingeringAction(
                duration=1.0,
                duration_phase1=0.0,
                duration_phase2=0.5,
                rl_label="action",
                key_dict=key_dict,
                name="response",
                name_phase1="target",
                name_phase2="delay",
                timeout_action=1,
                name_timeout="response-time-out",
                positions_phase1=((0, 0), (0, 0), (0, 0)),
                positions_phase2=((0, 0), (0, 0)),
                images_phase1=[robot_fig, letter, light],
                images_phase2=[robot_fig, letter],
                rl_label_phase1=None,
                rl_label_phase2="obs",
            )
        ]

    final_step = [
        BaseStimulus(duration=0.5, name="reward-delay", rl_label="obs"),
        reward_feedback,
        BaseStimulus(name="iti", duration=1.0),
    ]

    info_dict = {
        0: {"psychopy": []},
        1: {"psychopy": first_step(letter_arrays[0], light_blue)},
        2: {"psychopy": first_step(letter_arrays[1], light_red)},
        3: {"psychopy": first_step(letter_arrays[2], light_blue)},
        4: {"psychopy": first_step(letter_arrays[3], light_red)},
        5: {"psychopy": final_step},
        6: {"psychopy": final_step},
        7: {"psychopy": final_step},
        8: {"psychopy": final_step},
        9: {"psychopy": first_step(letter_arrays[4], light_blue)},
        10: {"psychopy": first_step(letter_arrays[5], light_red)},
        11: {"psychopy": first_step(letter_arrays[6], light_blue)},
        12: {"psychopy": first_step(letter_arrays[7], light_red)},
    }

    return info_dict, stimuli
