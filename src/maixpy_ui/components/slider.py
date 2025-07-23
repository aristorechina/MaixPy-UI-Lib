# -*- coding: utf-8 -*-
__author__ = 'Aristore'

import maix.image as image
import maix.touchscreen as touchscreen
import maix.display as display
from typing import Callable, Sequence

class Slider:
    """创建一个可拖动的滑块组件，用于在一定范围内选择一个值。"""
    BASE_HANDLE_RADIUS = 10
    BASE_HANDLE_BORDER_THICKNESS = 2
    BASE_HANDLE_PRESSED_RADIUS_INCREASE = 3
    BASE_TRACK_HEIGHT = 6
    BASE_LABEL_SCALE = 1.2
    BASE_TOOLTIP_SCALE = 1.2
    BASE_TOUCH_PADDING_Y = 10

    def _normalize_color(self, color: Sequence[int] | None):
        """将元组颜色转换为 maix.image.Color 对象。"""
        if color is None:
            return None
        if isinstance(color, tuple):
            if len(color) == 3:
                return image.Color.from_rgb(color[0], color[1], color[2])
            else:
                raise ValueError("颜色元组必须是 3 个元素的 RGB 格式")
        return color

    def __init__(self, rect: Sequence[int], scale: float=1.0, min_val: int=0, max_val: int=100, default_val: int=50,
                 callback: Callable | None=None, label: str="", track_color: Sequence[int]=(60, 60, 60),
                 progress_color: Sequence[int]=(0, 120, 220), handle_color: Sequence[int]=(255, 255, 255),
                 handle_border_color: Sequence[int]=(100, 100, 100),
                 handle_pressed_color: Sequence[int]=(220, 220, 255),
                 label_color: Sequence[int]=(200, 200, 200),
                 tooltip_bg_color: Sequence[int]=(0, 0, 0),
                 tooltip_text_color: Sequence[int]=(255, 255, 255),
                 show_tooltip_on_drag: bool | int=True):
        """初始化一个滑块。

        Args:
            rect (Sequence[int]): 滑块的位置和尺寸 `[x, y, w, h]`。
            scale (float): 滑块的整体缩放比例。
            min_val (int): 滑块的最小值。
            max_val (int): 滑块的最大值。
            default_val (int): 滑块的默认值。
            callback (callable | None, optional): 值改变时调用的函数。
            label (str): 滑块上方的标签文本。
            track_color (Sequence[int]): 滑轨背景颜色 (R, G, B)。
            progress_color (Sequence[int]): 滑轨进度条颜色 (R, G, B)。
            handle_color (Sequence[int]): 滑块手柄颜色 (R, G, B)。
            handle_border_color (Sequence[int]): 滑块手柄边框颜色 (R, G, B)。
            handle_pressed_color (Sequence[int]): 按下时手柄颜色 (R, G, B)。
            label_color (Sequence[int]): 标签文本颜色 (R, G, B)。
            tooltip_bg_color (Sequence[int]): 拖动时提示框背景色 (R, G, B)。
            tooltip_text_color (Sequence[int]): 拖动时提示框文本颜色 (R, G, B)。
            show_tooltip_on_drag (bool | int): 是否在拖动时显示数值提示框。

        Raises:
            ValueError: 如果 `rect` 无效，或 `min_val` 不小于 `max_val`，
                        或 `default_val` 不在范围内。
            TypeError: 如果 `callback` 不是可调用对象或 None。
        """
        if not all(isinstance(i, int) for i in rect) or len(rect) != 4:
            raise ValueError("rect 必须是包含四个整数 [x, y, w, h] 的列表")
        if not min_val < max_val:
            raise ValueError("min_val 必须小于 max_val")
        if not min_val <= default_val <= max_val:
            raise ValueError("default_val 必须在 min_val 和 max_val 之间")
        if callback is not None and not callable(callback):
            raise TypeError("callback 必须是一个可调用的函数或 None")

        self.rect = rect
        self.min_val, self.max_val, self.value = min_val, max_val, default_val
        self.callback, self.label, self.scale = callback, label, scale
        self.show_tooltip_on_drag = show_tooltip_on_drag

        # Scale UI elements based on the scale factor
        self.handle_radius = int(self.BASE_HANDLE_RADIUS * scale)
        self.handle_border_thickness = int(self.BASE_HANDLE_BORDER_THICKNESS * scale)
        self.handle_pressed_radius_increase = int(self.BASE_HANDLE_PRESSED_RADIUS_INCREASE * scale)
        self.track_height = int(self.BASE_TRACK_HEIGHT * scale)
        self.label_scale = self.BASE_LABEL_SCALE * scale
        self.tooltip_scale = self.BASE_TOOLTIP_SCALE * scale
        self.touch_padding_y = int(self.BASE_TOUCH_PADDING_Y * scale)

        # Normalize colors
        self.track_color = self._normalize_color(track_color)
        self.progress_color = self._normalize_color(progress_color)
        self.handle_color = self._normalize_color(handle_color)
        self.handle_border_color = self._normalize_color(handle_border_color)
        self.handle_pressed_color = self._normalize_color(handle_pressed_color)
        self.label_color = self._normalize_color(label_color)
        self.tooltip_bg_color = self._normalize_color(tooltip_bg_color)
        self.tooltip_text_color = self._normalize_color(tooltip_text_color)

        self.is_pressed = False
        self.disp_rect = [0, 0, 0, 0]

    def _is_in_rect(self, x: int, y: int, rect: Sequence[int]):
        """检查坐标 (x, y) 是否在指定的矩形区域内。"""
        return rect[0] < x < rect[0] + rect[2] and \
               rect[1] < y < rect[1] + rect[3]

    def draw(self, img: image.Image):
        """在指定的图像上绘制滑块。

        Args:
            img (maix.image.Image): 将要绘制滑块的目标图像。
        """
        track_start_x, track_width, track_center_y = self.rect[0], self.rect[2], self.rect[1] + self.rect[3] // 2
        if track_width <= 0:
            return

        value_fraction = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_center_x = track_start_x + value_fraction * track_width

        if self.label:
            label_size = image.string_size(self.label, scale=self.label_scale)
            label_y = self.rect[1] - label_size.height() - int(5 * self.scale)
            img.draw_string(track_start_x, label_y, self.label, color=self.label_color, scale=self.label_scale)

        track_y = track_center_y - self.track_height // 2
        img.draw_rect(track_start_x, track_y, track_width, self.track_height, color=self.track_color, thickness=-1)

        progress_width = int(value_fraction * track_width)
        if progress_width > 0:
            img.draw_rect(track_start_x, track_y, progress_width, self.track_height, color=self.progress_color, thickness=-1)

        current_radius = self.handle_radius + (self.handle_pressed_radius_increase if self.is_pressed else 0)
        current_handle_color = self.handle_pressed_color if self.is_pressed else self.handle_color

        border_thickness = min(self.handle_border_thickness, current_radius)
        if border_thickness > 0:
            img.draw_circle(
                int(handle_center_x), track_center_y, current_radius,
                color=self.handle_border_color, thickness=-1)
        img.draw_circle(
            int(handle_center_x), track_center_y,
            current_radius - border_thickness,
            color=current_handle_color, thickness=-1)

        if self.is_pressed and self.show_tooltip_on_drag:
            value_text = str(int(self.value))
            text_size = image.string_size(
                value_text, scale=self.tooltip_scale)
            padding = int(5 * self.scale)
            box_w = text_size.width() + 2 * padding
            box_h = text_size.height() + 2 * padding
            box_x = int(handle_center_x - box_w // 2)
            box_y = self.rect[1] - box_h - int(10 * self.scale)
            img.draw_rect(
                box_x, box_y, box_w, box_h,
                color=self.tooltip_bg_color, thickness=-1)
            img.draw_string(
                box_x + padding, box_y + padding, value_text,
                color=self.tooltip_text_color, scale=self.tooltip_scale)

    def handle_event(self, x: int, y: int, pressed: bool | int, img_w: int, img_h: int, disp_w: int, disp_h: int):
        """处理触摸事件并更新滑块状态。

        Args:
            x (int): 触摸点的 X 坐标。
            y (int): 触摸点的 Y 坐标。
            pressed (bool | int): 触摸屏是否被按下。
            img_w (int): 图像缓冲区的宽度。
            img_h (int): 图像缓冲区的高度。
            disp_w (int): 显示屏的宽度。
            disp_h (int): 显示屏的高度。
        """
        touch_rect = [
            self.rect[0], self.rect[1] - self.touch_padding_y,
            self.rect[2], self.rect[3] + 2 * self.touch_padding_y
        ]
        self.disp_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *touch_rect)
        is_hit = self._is_in_rect(x, y, self.disp_rect)

        if self.is_pressed and not pressed:
            self.is_pressed = False
            return

        if (pressed and is_hit) or self.is_pressed:
            self.is_pressed = True
            mapped_track_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *self.rect)
            disp_track_start_x, disp_track_width = mapped_track_rect[0], mapped_track_rect[2]
            if disp_track_width <= 0:
                return

            clamped_x = max(disp_track_start_x, min(x, disp_track_start_x + disp_track_width))
            pos_fraction = (clamped_x - disp_track_start_x) / disp_track_width
            new_value = self.min_val + pos_fraction * (self.max_val - self.min_val)
            new_value_int = int(round(new_value))

            if new_value_int != self.value:
                self.value = new_value_int
                if self.callback:
                    self.callback(self.value)
        else:
            self.is_pressed = False


class SliderManager:
    """管理一组滑块的事件处理和绘制。"""

    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display):
        """初始化滑块管理器。

        Args:
            ts (maix.touchscreen.TouchScreen): 触摸屏设备实例。
            disp (maix.display.Display): 显示设备实例。
        """
        self.ts = ts
        self.disp = disp
        self.sliders = []

    def add_slider(self, slider: Slider):
        """向管理器中添加一个滑块。

        Args:
            slider (Slider): 要添加的 Slider 实例。

        Raises:
            TypeError: 如果添加的对象不是 Slider 类的实例。
        """
        if isinstance(slider, Slider):
            self.sliders.append(slider)
        else:
            raise TypeError("只能添加 Slider 类的实例")

    def handle_events(self, img: image.Image):
        """处理所有受管滑块的事件并进行绘制。

        Args:
            img (maix.image.Image): 绘制滑块的目标图像。
        """
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for s in self.sliders:
            s.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h)
            s.draw(img)