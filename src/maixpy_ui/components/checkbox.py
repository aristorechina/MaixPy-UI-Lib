# -*- coding: utf-8 -*-
__author__ = 'Aristore'

import maix.image as image
import maix.touchscreen as touchscreen
import maix.display as display
from typing import Callable, Sequence

class Checkbox:
    """创建一个复选框（Checkbox）组件，可独立选中或取消。"""
    BASE_BOX_SIZE, BASE_TEXT_SCALE, BASE_SPACING = 25, 1.2, 10

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

    def __init__(self, position: Sequence[int], label: str, scale: float=1.0, is_checked: bool | int=False,
                 callback: Callable | None=None, box_color: Sequence[int]=(200, 200, 200),
                 box_checked_color: Sequence[int]=(0, 120, 220),
                 check_color: Sequence[int]=(255, 255, 255),
                 text_color: Sequence[int]=(200, 200, 200), box_thickness: int=2):
        """初始化一个复选框。

        Args:
            position (Sequence[int]): 复选框的左上角坐标 `[x, y]`。
            label (str): 复选框旁边的标签文本。
            scale (float): 复选框的整体缩放比例。
            is_checked (bool | int): 复选框的初始状态，True 为选中。
            callback (callable | None, optional): 状态切换时调用的函数，
                                           接收一个布尔值参数表示新状态。
            box_color (Sequence[int]): 未选中时方框的颜色 (R, G, B)。
            box_checked_color (Sequence[int]): 选中时方框的颜色 (R, G, B)。
            check_color (Sequence[int]): 选中标记（对勾）的颜色 (R, G, B)。
            text_color (Sequence[int]): 标签文本的颜色 (R, G, B)。
            box_thickness (int): 方框边框的厚度。

        Raises:
            ValueError: 如果 `position` 无效。
            TypeError: 如果 `callback` 不是可调用对象或 None。
        """
        if not isinstance(position, (list, tuple)) or len(position) != 2:
            raise ValueError("position 必须是包含两个整数 [x, y] 的列表或元组")
        if callback is not None and not callable(callback):
            raise TypeError("callback 必须是一个可调用的函数或 None")
        self.pos, self.label, self.scale = position, label, scale
        self.is_checked, self.callback = is_checked, callback
        self.box_size = int(self.BASE_BOX_SIZE * scale)
        self.text_scale = self.BASE_TEXT_SCALE * scale
        self.spacing = int(self.BASE_SPACING * scale)
        self.box_thickness = int(box_thickness * scale)
        touch_padding_y = 5
        # The touchable area for the box
        self.rect = [
            self.pos[0], self.pos[1] - touch_padding_y,
            self.box_size, self.box_size + 2 * touch_padding_y
        ]
        self.box_color = self._normalize_color(box_color)
        self.box_checked_color = self._normalize_color(box_checked_color)
        self.check_color = self._normalize_color(check_color)
        self.text_color = self._normalize_color(text_color)
        self.click_armed = False
        self.disp_rect = [0, 0, 0, 0]

    def _is_in_rect(self, x: int, y: int, rect: Sequence[int]):
        """检查坐标 (x, y) 是否在指定的矩形区域内。"""
        return rect[0] < x < rect[0] + rect[2] and \
               rect[1] < y < rect[1] + rect[3]

    def toggle(self):
        """切换复选框的选中状态，并执行回调。"""
        self.is_checked = not self.is_checked
        if self.callback:
            self.callback(self.is_checked)

    def draw(self, img: image.Image):
        """在指定的图像上绘制复选框。

        Args:
            img (maix.image.Image): 将要绘制复选框的目标图像。
        """
        box_x, box_y = self.pos
        text_size = image.string_size(self.label, scale=self.text_scale)
        total_h = max(self.box_size, text_size.height())
        box_offset_y = (total_h - self.box_size) // 2
        text_offset_y = (total_h - text_size.height()) // 2
        box_draw_y = box_y + box_offset_y
        text_draw_y = box_y + text_offset_y
        text_draw_x = box_x + self.box_size + self.spacing

        current_box_color = self.box_checked_color if self.is_checked else self.box_color
        if self.is_checked:
            img.draw_rect(box_x, box_draw_y, self.box_size, self.box_size, color=current_box_color, thickness=-1)
        img.draw_rect(box_x, box_draw_y, self.box_size, self.box_size, color=current_box_color, thickness=self.box_thickness)

        if self.is_checked:
            # Draw a check mark
            p1 = (box_x + int(self.box_size * 0.2),
                  box_draw_y + int(self.box_size * 0.5))
            p2 = (box_x + int(self.box_size * 0.45),
                  box_draw_y + int(self.box_size * 0.75))
            p3 = (box_x + int(self.box_size * 0.8),
                  box_draw_y + int(self.box_size * 0.25))
            check_thickness = max(1, int(2 * self.scale))
            img.draw_line(p1[0], p1[1], p2[0], p2[1], color=self.check_color, thickness=check_thickness)
            img.draw_line(p2[0], p2[1], p3[0], p3[1], color=self.check_color, thickness=check_thickness)

        img.draw_string(text_draw_x, text_draw_y, self.label, color=self.text_color, scale=self.text_scale)

    def handle_event(self, x: int, y: int, pressed: bool | int, img_w: int, img_h: int, disp_w: int, disp_h: int):
        """处理触摸事件并更新复选框状态。

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
                self.click_armed = True
        else:
            if self.click_armed and is_hit:
                self.toggle()
            self.click_armed = False


class CheckboxManager:
    """管理一组复选框的事件处理和绘制。"""

    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display):
        """初始化复选框管理器。

        Args:
            ts (maix.touchscreen.TouchScreen): 触摸屏设备实例。
            disp (maix.display.Display): 显示设备实例。
        """
        self.ts = ts
        self.disp = disp
        self.checkboxes = []

    def add_checkbox(self, checkbox: Checkbox):
        """向管理器中添加一个复选框。

        Args:
            checkbox (Checkbox): 要添加的 Checkbox 实例。

        Raises:
            TypeError: 如果添加的对象不是 Checkbox 类的实例。
        """
        if isinstance(checkbox, Checkbox):
            self.checkboxes.append(checkbox)
        else:
            raise TypeError("只能添加 Checkbox 类的实例")

    def handle_events(self, img: image.Image):
        """处理所有受管复选框的事件并进行绘制。

        Args:
            img (maix.image.Image): 绘制复选框的目标图像。
        """
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for cb in self.checkboxes:
            cb.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h)
            cb.draw(img)