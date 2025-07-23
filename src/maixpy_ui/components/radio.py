# -*- coding: utf-8 -*-
__author__ = 'Aristore'

import maix.image as image
import maix.touchscreen as touchscreen
import maix.display as display
from typing import Callable, Sequence

class RadioButton:
    """创建一个单选按钮（RadioButton）项。

    通常与 RadioManager 结合使用，以形成一个单选按钮组。
    """
    BASE_CIRCLE_RADIUS, BASE_TEXT_SCALE, BASE_SPACING = 12, 1.2, 10

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

    def __init__(self, position: Sequence[int], label: str, value, scale: float=1.0,
                 circle_color: Sequence[int]=(200, 200, 200),
                 circle_selected_color: Sequence[int]=(0, 120, 220),
                 dot_color: Sequence[int]=(255, 255, 255),
                 text_color: Sequence[int]=(200, 200, 200), circle_thickness: int=2):
        """初始化一个单选按钮项。

        Args:
            position (Sequence[int]): 单选按钮圆圈的左上角坐标 `[x, y]`。
            label (str): 按钮旁边的标签文本。
            value (any): 与此单选按钮关联的唯一值。
            scale (float): 组件的整体缩放比例。
            circle_color (Sequence[int]): 未选中时圆圈的颜色 (R, G, B)。
            circle_selected_color (Sequence[int]): 选中时圆圈的颜色 (R, G, B)。
            dot_color (Sequence[int]): 选中时中心圆点的颜色 (R, G, B)。
            text_color (Sequence[int]): 标签文本的颜色 (R, G, B)。
            circle_thickness (int): 圆圈边框的厚度。
        """
        self.pos, self.label, self.value, self.scale = position, label, value, scale
        self.is_selected = False
        self.radius = int(self.BASE_CIRCLE_RADIUS * scale)
        self.text_scale = self.BASE_TEXT_SCALE * scale
        self.spacing = int(self.BASE_SPACING * scale)
        self.circle_thickness = int(circle_thickness * scale)
        # Centered touch area around the circle
        self.rect = [self.pos[0], self.pos[1], 2 * self.radius, 2 * self.radius]
        self.circle_color = self._normalize_color(circle_color)
        self.circle_selected_color = self._normalize_color(circle_selected_color)
        self.dot_color = self._normalize_color(dot_color)
        self.text_color = self._normalize_color(text_color)
        self.click_armed = False

    def draw(self, img: image.Image):
        """在指定的图像上绘制单选按钮。

        Args:
            img (maix.image.Image): 将要绘制单选按钮的目标图像。
        """
        center_x, center_y = self.pos[0] + self.radius, self.pos[1] + self.radius
        current_circle_color = self.circle_selected_color if self.is_selected else self.circle_color

        img.draw_circle(center_x, center_y, self.radius, color=current_circle_color, thickness=self.circle_thickness)

        if self.is_selected:
            dot_radius = max(2, self.radius // 2)
            img.draw_circle(center_x, center_y, dot_radius, color=self.dot_color, thickness=-1)

        text_size = image.string_size(self.label, scale=self.text_scale)
        text_x = self.pos[0] + 2 * self.radius + self.spacing
        text_y = center_y - text_size.height() // 2
        img.draw_string(text_x, text_y, self.label, color=self.text_color, scale=self.text_scale)


class RadioManager:
    """管理一个单选按钮组，确保只有一个按钮能被选中。"""

    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display, default_value=None, callback: Callable | None=None):
        """初始化单选按钮管理器。

        Args:
            ts (maix.touchscreen.TouchScreen): 触摸屏设备实例。
            disp (maix.display.Display): 显示设备实例。
            default_value (any, optional): 默认选中的按钮的值。
            callback (callable | None, optional): 选中项改变时调用的函数，
                                           接收新选中项的值作为参数。
        """
        self.ts = ts
        self.disp = disp
        self.radios = []
        self.selected_value = default_value
        self.callback = callback
        self.disp_rects = {}

    def add_radio(self, radio: RadioButton):
        """向管理器中添加一个单选按钮。

        Args:
            radio (RadioButton): 要添加的 RadioButton 实例。

        Raises:
            TypeError: 如果添加的对象不是 RadioButton 类的实例。
        """
        if isinstance(radio, RadioButton):
            self.radios.append(radio)
            if radio.value == self.selected_value:
                radio.is_selected = True
        else:
            raise TypeError("只能添加 RadioButton 类的实例")

    def _select_radio(self, value):
        """选中指定的单选按钮，并取消其他按钮的选中状态。"""
        if self.selected_value != value:
            self.selected_value = value
            for r in self.radios:
                r.is_selected = (r.value == self.selected_value)
            if self.callback:
                self.callback(self.selected_value)

    def _is_in_rect(self, x: int, y: int, rect: Sequence[int]):
        """检查坐标 (x, y) 是否在指定的矩形区域内。"""
        return rect[0] < x < rect[0] + rect[2] and \
               rect[1] < y < rect[1] + rect[3]

    def handle_events(self, img: image.Image):
        """处理所有单选按钮的事件并进行绘制。

        Args:
            img (maix.image.Image): 绘制单选按钮的目标图像。
        """
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()

        for r in self.radios:
            self.disp_rects[r.value] = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *r.rect)

        if pressed:
            for r in self.radios:
                if self._is_in_rect(x, y, self.disp_rects[r.value]) and not r.click_armed:
                    r.click_armed = True
        else:
            for r in self.radios:
                if r.click_armed and self._is_in_rect(x, y, self.disp_rects[r.value]):
                    self._select_radio(r.value)
                r.click_armed = False

        for r in self.radios:
            r.draw(img)