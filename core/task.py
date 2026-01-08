import pathlib
from typing import Literal, Union

import numpy as np

from rewardgym import check_random_state
from rewardgym.reward_classes import PseudoRandomReward
from rewardgym.tasks.yaml_tools import load_task_from_yaml


def get_task(
    render_backend: Literal["pygame", "psychopy"] = None,
    random_state: Union[int, np.random.Generator] = 1000,
    key_dict=None,
):
    random_state = check_random_state(random_state)
    yaml_file = pathlib.Path(__file__).parents[1].resolve() / "task.yaml"
    info_dict, environment_graph = load_task_from_yaml(yaml_file)

    reward_structure = {
        11: PseudoRandomReward(reward_list=[-5, -5, -1, -1, -1, -1, -1, -1, -1, -1], random_state=random_state),
        12: PseudoRandomReward(
            reward_list=[-5, -5, -5, -5, -5, -5, -5, -5, -1, -1], random_state=random_state
        ),
        9: PseudoRandomReward(reward_list=[5, 5, 5, 5, 5, 5, 5, 5, 1, 1], random_state=random_state),
        10: PseudoRandomReward(reward_list=[1, 1, 1, 1, 1, 1, 1, 1, 5, 5], random_state=random_state),
    }

    info_dict.update(
        {"position": {1: "go-win", 2: "go-punish", 3: "nogo-win", 4: "nogo-punish",
                      5: "go-win", 6: "go-punish", 7: "nogo-win", 8: "nogo-punish"}}
    )

    if render_backend == "pygame":
        from .backend_pygame import get_pygame_info

        pygame_dict = get_pygame_info()
        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from .backend_psychopy import get_psychopy_info

        if key_dict is None:
            key_dict = {"space": 0}

        psychopy_dict, _ = get_psychopy_info(random_state=random_state, key_dict=key_dict)
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict
