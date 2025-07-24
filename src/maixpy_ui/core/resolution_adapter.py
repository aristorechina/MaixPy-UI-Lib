# -*- coding: utf-8 -*-
__author__ = 'levi_jia'

from typing import Sequence

class ResolutionAdapter:
    """一个工具类，用于在不同分辨率的屏幕上适配UI元素。

    它将基于一个"基础分辨率"的坐标和尺寸，按比例缩放到"目标显示分辨率"。
    """

    def __init__(self, display_width: int, display_height: int, base_width: int=320, base_height: int=240):
        """初始化分辨率适配器。

        Args:
            display_width (int): 目标显示屏的宽度。
            display_height (int): 目标显示屏的高度。
            base_width (int): UI设计的基准宽度。
            base_height (int): UI设计的基准高度。

        Raises:
            ValueError: 如果基础宽度或高度为零。
        """
        self.display_width = display_width
        self.display_height = display_height
        self.base_width = base_width
        self.base_height = base_height
        if self.base_width == 0 or self.base_height == 0:
            raise ValueError("基础宽度和高度不能为零")
        self.scale_x = display_width / self.base_width
        self.scale_y = display_height / self.base_height

    def scale_position(self, x: int, y: int):
        """缩放一个坐标点 (x, y)。

        Args:
            x (int): 原始 X 坐标。
            y (int): 原始 Y 坐标。

        Returns:
            Sequence[int]: 缩放后的 (x, y) 坐标。
        """
        return int(x * self.scale_x), int(y * self.scale_y)

    def scale_size(self, width: int, height: int):
        """缩放一个尺寸 (width, height)。

        Args:
            width (int): 原始宽度。
            height (int): 原始高度。

        Returns:
            Sequence[int]: 缩放后的 (width, height) 尺寸。
        """
        return int(width * self.scale_x), int(height * self.scale_y)

    def scale_rect(self, rect: Sequence[int]):
        """缩放一个矩形 [x, y, w, h]。

        Args:
            rect (list[int]): 原始矩形 `[x, y, w, h]`。

        Returns:
            Sequence[int]: 缩放后的矩形 (x, y, w, h)。
        """
        x, y, w, h = rect
        return self.scale_position(x, y) + self.scale_size(w, h)

    def scale_value(self, value: int|float):
        """缩放一个通用数值，如半径、厚度等。

        使用 X 和 Y 缩放因子中较大的一个，以保持视觉比例。

        Args:
            value (int|float): 原始数值。

        Returns:
            float: 缩放后的数值。
        """
        return value * max(self.scale_x, self.scale_y)