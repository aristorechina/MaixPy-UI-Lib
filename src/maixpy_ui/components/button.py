# -*- coding: utf-8 -*-
__author__ = 'Aristore'

import maix.image as image
import maix.touchscreen as touchscreen
import maix.display as display
from typing import Callable, Sequence

class Button:
    """创建一个可交互的按钮组件。

    该组件可以响应触摸事件，并在按下时改变外观，释放时执行回调函数。
    """

    def _normalize_color(self, color: Sequence[int] | None):
        """将元组颜色转换为 maix.image.Color 对象。"""
        if color is None:
            return None
        if isinstance(color, tuple):
            if len(color) == 3:
                return image.Color.from_rgb(color[0], color[1], color[2])
            else:
                raise ValueError("颜色元组必须是 3 个元素的 RGB 格式。")
        return color

    def __init__(self, rect: Sequence[int], label: str, callback: Callable | None, bg_color: Sequence[int] | None=(50, 50, 50),
                 pressed_color: Sequence[int] | None=(0, 120, 220), text_color: Sequence[int]=(255, 255, 255),
                 border_color: Sequence[int]=(200, 200, 200), border_thickness: int=2,
                 text_scale: float=1.5, font: str | None=None, align_h: str='center',
                 align_v: str='center'):
        """初始化一个按钮。

        Args:
            rect (Sequence[int]): 按钮的位置和尺寸 `[x, y, w, h]`。
            label (str): 按钮上显示的文本。
            callback (callable | None): 当按钮被点击时调用的函数。
            bg_color (Sequence[int] | None): 背景颜色 (R, G, B)。
            pressed_color (Sequence[int] | None): 按下状态的背景颜色 (R, G, B)。
            text_color (Sequence[int]): 文本颜色 (R, G, B)。
            border_color (Sequence[int]): 边框颜色 (R, G, B)。
            border_thickness (int): 边框厚度（像素）。
            text_scale (float): 文本的缩放比例。
            font (str | None, optional): 使用的字体文件路径。默认为 None。
            align_h (str): 水平对齐方式 ('left', 'center', 'right')。
            align_v (str): 垂直对齐方式 ('top', 'center', 'bottom')。

        Raises:
            ValueError: 如果 `rect` 不是包含四个整数的列表。
            TypeError: 如果 `callback` 不是一个可调用对象。
        """
        if not all(isinstance(i, int) for i in rect) or len(rect) != 4:
            raise ValueError("rect 必须是包含四个整数 [x, y, w, h] 的列表")
        if callback is not None and not callable(callback):
            raise TypeError("callback 必须是一个可调用的函数")
        self.rect, self.label, self.callback = rect, label, callback
        self.text_scale = text_scale
        self.font = font
        self.border_thickness = border_thickness
        self.align_h, self.align_v = align_h, align_v
        self.bg_color = self._normalize_color(bg_color)
        self.pressed_color = self._normalize_color(pressed_color)
        self.text_color = self._normalize_color(text_color)
        self.border_color = self._normalize_color(border_color)
        self.is_pressed = False
        self.click_armed = False
        self.disp_rect = [0, 0, 0, 0]

    def _is_in_rect(self, x: int, y: int, rect: list[int]):
        """检查坐标 (x, y) 是否在指定的矩形区域内。"""
        return rect[0] < x < rect[0] + rect[2] and \
               rect[1] < y < rect[1] + rect[3]

    def draw(self, img: image.Image):
        """在指定的图像上绘制按钮。

        Args:
            img (maix.image.Image): 将要绘制按钮的目标图像。
        """
        current_bg_color = self.pressed_color if self.is_pressed else self.bg_color
        if current_bg_color is not None:
            img.draw_rect(*self.rect, color=current_bg_color, thickness=-1)
        if self.border_thickness > 0:
            img.draw_rect(
                *self.rect,
                color=self.border_color,
                thickness=self.border_thickness)

        font_arg = self.font if self.font is not None else ""
        text_size = image.string_size(
            self.label, scale=self.text_scale, font=font_arg)

        if self.align_h == 'center':
            text_x = self.rect[0] + (self.rect[2] - text_size[0]) // 2
        elif self.align_h == 'left':
            text_x = self.rect[0] + self.border_thickness + 5
        else:
            text_x = self.rect[0] + self.rect[2] - text_size[0] - \
                     self.border_thickness - 5

        if self.align_v == 'center':
            text_y = self.rect[1] + (self.rect[3] - text_size[1]) // 2
        elif self.align_v == 'top':
            text_y = self.rect[1] + self.border_thickness + 5
        else:
            text_y = self.rect[1] + self.rect[3] - text_size[1] - \
                     self.border_thickness - 5

        img.draw_string(
            text_x, text_y, self.label, color=self.text_color,
            scale=self.text_scale, font=font_arg)

    def handle_event(self, x: int, y: int, pressed: bool | int, img_w: int, img_h: int, disp_w: int, disp_h: int):
        """处理触摸事件并更新按钮状态。

        Args:
            x (int): 触摸点的 X 坐标。
            y (int): 触摸点的 Y 坐标。
            pressed (bool | int): 触摸屏是否被按下。
            img_w (int): 图像缓冲区的宽度。
            img_h (int): 图像缓冲区的高度。
            disp_w (int): 显示屏的宽度。
            disp_h (int): 显示屏的高度。
        """
        self.disp_rect = image.resize_map_pos(
            img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *self.rect)
        is_hit = self._is_in_rect(x, y, self.disp_rect)
        if pressed:
            if is_hit:
                if not self.click_armed:
                    self.click_armed = True
                self.is_pressed = True
            else:
                self.is_pressed = False
                self.click_armed = False
        else:
            if self.click_armed and is_hit:
                if self.callback is not None:
                    self.callback()
            self.is_pressed = False
            self.click_armed = False


class ButtonManager:
    """管理一组按钮的事件处理和绘制。"""

    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display):
        """初始化按钮管理器。

        Args:
            ts (maix.touchscreen.TouchScreen): 触摸屏设备实例。
            disp (maix.display.Display): 显示设备实例。
        """
        self.ts = ts
        self.disp = disp
        self.buttons = []

    def add_button(self, button: Button):
        """向管理器中添加一个按钮。

        Args:
            button (Button): 要添加的 Button 实例。

        Raises:
            TypeError: 如果添加的对象不是 Button 类的实例。
        """
        if isinstance(button, Button):
            self.buttons.append(button)
        else:
            raise TypeError("只能添加 Button 类的实例")

    def handle_events(self, img: image.Image):
        """处理所有受管按钮的事件并进行绘制。

        Args:
            img (maix.image.Image): 绘制按钮的目标图像。
        """
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for btn in self.buttons:
            btn.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h)
            btn.draw(img)