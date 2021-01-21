# -*- coding: utf-8 -*-
from .constants import InputButtons


class InputUtils:
    NumericButtonsSequence = [
        InputButtons.BTN_1,
        InputButtons.BTN_2,
        InputButtons.BTN_3,
        InputButtons.BTN_4,
        InputButtons.BTN_5,
        InputButtons.BTN_6,
        InputButtons.BTN_7,
        InputButtons.BTN_8,
        InputButtons.BTN_9,
        InputButtons.BTN_0,
    ]

    @staticmethod
    def get_numeric_button_index(btn):
        value = None
        try:
            value = InputUtils.NumericButtonsSequence.index(btn)
        except IndexError:
            pass
        except ValueError:
            pass

        return value
