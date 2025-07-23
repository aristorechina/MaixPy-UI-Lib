# -*- coding: utf-8 -*-
__author__ = 'Aristore'

import maix.image as image
import maix.touchscreen as touchscreen
import maix.display as display
from typing import Callable, Sequence

class Switch:
    """创建一个开关（Switch）组件，用于在开/关两种状态之间切换。"""
    BASE_H, BASE_W = 30, int(30 * 1.9)

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

    def __init__(self, position: Sequence[int], scale: float=1.0, is_on: bool | int=False, callback: Callable | None=None,
                 on_color: Sequence[int]=(30, 200, 30), off_color: Sequence[int]=(100, 100, 100),
                 handle_color: Sequence[int]=(255, 255, 255),
                 handle_pressed_color: Sequence[int]=(220, 220, 255),
                 handle_radius_increase: int=2):
        """初始化一个开关组件。

        Args:
            position (Sequence[int]): 开关的左上角坐标 `[x, y]`。
            scale (float): 开关的整体缩放比例。
            is_on (bool | int): 开关的初始状态，True 为开，False 为关。
            callback (callable | None, optional): 状态切换时调用的函数，
                                           接收一个布尔值参数表示新状态。
            on_color (Sequence[int]): 开启状态下的背景颜色 (R, G, B)。
            off_color (Sequence[int]): 关闭状态下的背景颜色 (R, G, B)。
            handle_color (Sequence[int]): 手柄的颜色 (R, G, B)。
            handle_pressed_color (Sequence[int]): 按下时手柄的颜色 (R, G, B)。
            handle_radius_increase (int): 按下时手柄半径增加量。

        Raises:
            ValueError: 如果 `position` 不是包含两个整数的列表或元组。
            TypeError: 如果 `callback` 不是可调用对象或 None。
        """
        if not isinstance(position, (list, tuple)) or len(position) != 2:
            raise ValueError("position 必须是包含两个整数 [x, y] 的列表或元组")
        if callback is not None and not callable(callback):
            raise TypeError("callback 必须是一个可调用的函数或 None")
        self.pos, self.scale, self.is_on, self.callback = position, scale, is_on, callback
        self.width = int(self.BASE_W * scale)
        self.height = int(self.BASE_H * scale)
        self.rect = [self.pos[0], self.pos[1], self.width, self.height]
        self.on_color = self._normalize_color(on_color)
        self.off_color = self._normalize_color(off_color)
        self.handle_color = self._normalize_color(handle_color)
        self.handle_pressed_color = self._normalize_color(handle_pressed_color)
        self.handle_radius_increase = int(handle_radius_increase * scale)
        self.is_pressed = False
        self.click_armed = False
        self.disp_rect = [0, 0, 0, 0]

    def _is_in_rect(self, x: int, y: int, rect: Sequence[int]):
        """检查坐标 (x, y) 是否在指定的矩形区域内。"""
        return rect[0] < x < rect[0] + rect[2] and \
               rect[1] < y < rect[1] + rect[3]

    def toggle(self):
        """切换开关的状态，并执行回调函数。"""
        self.is_on = not self.is_on
        if self.callback:
            self.callback(self.is_on)

    def draw(self, img: image.Image):
        """在指定的图像上绘制开关。

        Args:
            img (maix.image.Image): 将要绘制开关的目标图像。
        """
        track_x, track_y, track_w, track_h = self.rect
        track_center_y = track_y + track_h // 2
        handle_radius = track_h // 2
        current_bg_color = self.on_color if self.is_on else self.off_color

        # Draw rounded track
        img.draw_circle(track_x + handle_radius, track_center_y, handle_radius, color=current_bg_color, thickness=-1)
        img.draw_circle(track_x + track_w - handle_radius, track_center_y, handle_radius, color=current_bg_color, thickness=-1)
        img.draw_rect(track_x + handle_radius, track_y, track_w - 2 * handle_radius, track_h, color=current_bg_color, thickness=-1)

        # Draw handle
        handle_pos_x = (track_x + track_w - handle_radius) if self.is_on else (track_x + handle_radius)
        current_handle_color = self.handle_pressed_color if self.is_pressed else self.handle_color
        padding = int(2 * self.scale)
        current_handle_radius = handle_radius - padding + (self.handle_radius_increase if self.is_pressed else 0)
        img.draw_circle(handle_pos_x, track_center_y, current_handle_radius, color=current_handle_color, thickness=-1)

    def handle_event(self, x: int, y: int, pressed: bool | int, img_w: int, img_h: int, disp_w: int, disp_h: int):
        """处理触摸事件并更新开关状态。

        Args:
            x (int): 触摸点的 X 坐标。
            y (int): 触摸点的 Y 坐标。
            pressed (bool | int): 触摸屏是否被按下。
            img_w (int): 图像缓冲区的宽度。
            img_h (int): 图像缓冲区的高度。
            disp_w (int): 显示屏的宽度。
            disp_h (int): 显示屏的高度。
        """
        self.disp_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *self.rect)
        is_hit = self._is_in_rect(x, y, self.disp_rect)

        if pressed:
            if is_hit and not self.click_armed:
                self.is_pressed = True
                self.click_armed = True
        else:
            if self.click_armed and is_hit:
                self.toggle()
            self.is_pressed, self.click_armed = False, False


class SwitchManager:
    """管理一组开关的事件处理和绘制。"""

    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display):
        """初始化开关管理器。

        Args:
            ts (maix.touchscreen.TouchScreen): 触摸屏设备实例。
            disp (maix.display.Display): 显示设备实例。
        """
        self.ts = ts
        self.disp = disp
        self.switches = []

    def add_switch(self, switch: Switch):
        """向管理器中添加一个开关。

        Args:
            switch (Switch): 要添加的 Switch 实例。

        Raises:
            TypeError: 如果添加的对象不是 Switch 类的实例。
        """
        if isinstance(switch, Switch):
            self.switches.append(switch)
        else:
            raise TypeError("只能添加 Switch 类的实例")

    def handle_events(self, img: image.Image):
        """处理所有受管开关的事件并进行绘制。

        Args:
            img (maix.image.Image): 绘制开关的目标图像。
        """
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for s in self.switches:
            s.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h)
            s.draw(img)