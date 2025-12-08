from rewardgym.pygame_render.stimuli import (
    BaseText,
    BaseDisplay,
    FormatTextReward,
    TimedAction,
)


def get_pygame_info(action_map=None, window_size=256):
    base_position = (window_size // 2, window_size // 2)

    reward_disp = FormatTextReward(
        "You gain: {0}", 1000, textposition=base_position, target="reward"
    )

    earnings_text = FormatTextReward(
        "You have gained: {0}",
        500,
        textposition=base_position,
        target="total_reward",
    )

    def first_step(stim):
        return [
            BaseDisplay(None, 500),
            BaseText(stim, 1000, textposition=base_position),
            BaseDisplay(None, 500),
            BaseText("x", 100, textposition=base_position),
            TimedAction(500),
        ]

    final_disp = [
        BaseDisplay(None, 500),
        reward_disp,
        earnings_text,
    ]

    pygame_dict = {
        0: {"pygame": first_step("A")},
        1: {"pygame": first_step("B")},
        2: {"pygame": first_step("C")},
        3: {"pygame": first_step("D")},
        4: {"pygame": final_disp},
        5: {"pygame": final_disp},
        6: {"pygame": final_disp},
        7: {"pygame": final_disp},
    }

    return pygame_dict
