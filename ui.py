"""
MaixPy-UI-Lib: A lightweight UI component library for MaixPy

--------------------------------------------------------------------------
  Author  : Aristore， HYKMAX
  Version : 2.0
  Date    : 2025-07-21
  Web     : https://www.aristore.top/
  Repo    : https://github.com/aristorechina/MaixPy-UI-Lib/
--------------------------------------------------------------------------

Copyright 2025 Aristore

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

CHANGELOG
================================================

Version 1.0 (Jul 20, 2025)
-------------------------------------------------
- 当前已实现的组件：Button, Slider, Switch, Checkbox, RadioButton。

Version 1.1 (Jul 20, 2025)
-------------------------------------------------
- 增加了 ResolutionAdapter 以实现对不同分辨率的 UI 适配（由 @levi_jia 实现）。

Version 1.2 (Jul 20, 2025)
-------------------------------------------------
- ResolutionAdapter 增加了自定义基础分辨率的功能（默认仍为 320*240）。
- 更新了 README，增加了对 ResolutionAdapter 的说明。
- 更新了 demo 以支持 ResolutionAdapter。

Version 1.3 (Jul 20, 2025)
-------------------------------------------------
- 增加了 UIManager 以实现页面间的导航（进入和返回）功能。
- 使用 UIManager 重构了 demo。

Version 2.0 (Jul 21, 2025)
-------------------------------------------------
- 进行了大规模代码重构，以提高可读性和可维护性。
- 为所有类和方法添加了全面的文档字符串，以提供清晰的内联文档。
- 集成了完整的类型注解。
- 完善了 README。

Version 2.1 (Jul 23, 2025)
-------------------------------------------------
- 尝试改进Page为树型结构

"""
import maix.image as image
import maix.touchscreen as touchscreen
import maix.display as display
from typing import Callable, Sequence, List, Optional


# ==============================================================================
# 1. Button Component
# ==============================================================================
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


# ==============================================================================
# 2. Slider Component
# ==============================================================================
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


# ==============================================================================
# 3. Switch Component
# ==============================================================================
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


# ==============================================================================
# 4. Checkbox Component
# ==============================================================================
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


# ==============================================================================
# 5. RadioButton Component
# ==============================================================================
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


# ==============================================================================
# 6. Resolution Adaptation
# ==============================================================================
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


# ==============================================================================
# 7. Page and UIManager (树型结构优化版本)
# ==============================================================================
class Page:
    """页面（Page）的基类，支持树型父子节点结构。

    每个页面可以有一个父页面和多个子页面，形成树型结构。
    这种设计允许更灵活的页面组织和导航。

    Attributes:
        ui_manager (UIManager): 管理此页面的 UIManager 实例。
        name (str): 页面的名称，用于在父页面中唯一标识。
        parent (Page | None): 父页面，如果为 None 则表示根页面。
        children (List[Page]): 子页面列表。
    """

    def __init__(self, ui_manager: 'UIManager', name: str = ""):
        """初始化页面。

        Args:
            ui_manager (UIManager): 用于页面导航的 UIManager 实例。
            name (str): 页面的唯一名称标识符。
        """
        self.ui_manager = ui_manager
        self.name = name
        self.parent = None
        self.children = []

    def add_child(self, child_page: 'Page'):
        """添加一个子页面。

        Args:
            child_page (Page): 要添加的子页面实例。

        Raises:
            ValueError: 如果子页面的名称已存在或为空。
            TypeError: 如果传入的不是 Page 实例。
        """
        if not isinstance(child_page, Page):
            raise TypeError("只能添加 Page 类的实例")
        if not child_page.name:
            raise ValueError("子页面必须有一个非空的名称")
        if self.get_child(child_page.name) is not None:
            raise ValueError(f"名称为 '{child_page.name}' 的子页面已存在")
        
        child_page.parent = self
        self.children.append(child_page)

    def remove_child(self, child_page: 'Page'):
        """移除一个子页面。

        Args:
            child_page (Page): 要移除的子页面实例。

        Returns:
            bool: 如果成功移除则返回 True，否则返回 False。
        """
        if child_page in self.children:
            child_page.parent = None
            self.children.remove(child_page)
            return True
        return False

    def get_child(self, name: str) -> Optional['Page']:
        """根据名称获取子页面。

        Args:
            name (str): 子页面的名称。

        Returns:
            Page | None: 如果找到则返回子页面实例，否则返回 None。
        """
        for child in self.children:
            if child.name == name:
                return child
        return None

    def get_root(self) -> 'Page':
        """获取当前页面的根页面。

        Returns:
            Page: 树结构的根页面。
        """
        current = self
        while current.parent:
            current = current.parent
        return current

    def get_path(self) -> List[str]:
        """获取从根页面到当前页面的路径。

        Returns:
            List[str]: 页面名称的路径列表。
        """
        path = []
        current = self
        while current:
            if current.name:  # 只有非空名称才加入路径
                path.insert(0, current.name)
            current = current.parent
        return path

    def get_depth(self) -> int:
        """获取当前页面在树中的深度。

        Returns:
            int: 页面深度，根页面深度为0。
        """
        depth = 0
        current = self.parent
        while current:
            depth += 1
            current = current.parent
        return depth

    def find_page_by_path(self, path: List[str]) -> Optional['Page']:
        """根据路径查找页面。

        Args:
            path (List[str]): 页面路径，从当前页面开始的相对路径。

        Returns:
            Page | None: 如果找到则返回页面实例，否则返回 None。
        """
        if not path:
            return self
        
        child = self.get_child(path[0])
        if child is None:
            return None
        
        if len(path) == 1:
            return child
        else:
            return child.find_page_by_path(path[1:])

    def on_enter(self):
        """当页面进入视图时调用。

        子类可以重写此方法来实现页面进入时的初始化逻辑。
        """
        pass

    def on_exit(self):
        """当页面离开视图时调用。

        子类可以重写此方法来实现页面退出时的清理逻辑。
        """
        pass

    def on_child_enter(self, child: 'Page'):
        """当子页面进入视图时调用。

        Args:
            child (Page): 进入视图的子页面。
        """
        pass

    def on_child_exit(self, child: 'Page'):
        """当子页面离开视图时调用。

        Args:
            child (Page): 离开视图的子页面。
        """
        pass

    def update(self, img: image.Image):
        """每帧调用的更新和绘制方法。

        子类必须重写此方法以实现页面的UI逻辑和绘制。

        Args:
            img (maix.image.Image): 用于绘制的图像缓冲区。

        Raises:
            NotImplementedError: 如果子类没有实现此方法。
        """
        raise NotImplementedError("每个页面都必须实现 update 方法")


class UIManager:
    """UI 管理器，基于树型页面结构提供灵活的导航功能。

    该管理器支持树型页面结构的导航，包括导航到子页面、返回父页面、
    按路径导航等功能。
    """

    def __init__(self, root_page: Optional[Page] = None):
        """初始化UI管理器。

        Args:
            root_page (Page | None): 根页面实例，如果为None则需要后续设置。
        """
        self.root_page = root_page
        self.current_page = root_page
        self.navigation_history = []  # 用于记录导航历史
        
        if root_page:
            root_page.on_enter()

    def set_root_page(self, page: Page):
        """设置根页面。

        Args:
            page (Page): 新的根页面实例。
        """
        if self.current_page:
            self.current_page.on_exit()
        
        self.root_page = page
        self.current_page = page
        self.navigation_history.clear()
        
        if page:
            page.on_enter()

    def get_current_page(self) -> Optional[Page]:
        """获取当前活动的页面。

        Returns:
            Page | None: 当前页面实例，如果没有则返回 None。
        """
        return self.current_page

    def navigate_to_child(self, child_name: str) -> bool:
        """导航到当前页面的指定子页面。

        Args:
            child_name (str): 子页面的名称。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.current_page:
            return False
        
        child = self.current_page.get_child(child_name)
        if child:
            # 记录导航历史
            self.navigation_history.append(self.current_page)
            
            # 通知当前页面和父页面
            self.current_page.on_exit()
            self.current_page.on_child_enter(child)
            
            # 切换页面
            self.current_page = child
            child.on_enter()
            
            return True
        return False

    def navigate_to_parent(self) -> bool:
        """导航到当前页面的父页面。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.current_page or not self.current_page.parent:
            return False
        
        parent = self.current_page.parent
        
        # 通知相关页面
        parent.on_child_exit(self.current_page)
        self.current_page.on_exit()
        
        # 从历史记录中移除（如果存在）
        if self.navigation_history and self.navigation_history[-1] == parent:
            self.navigation_history.pop()
        
        # 切换页面
        self.current_page = parent
        parent.on_enter()
        
        return True

    def navigate_to_root(self) -> bool:
        """导航到根页面。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.root_page:
            return False
        
        return self.navigate_to_page(self.root_page)

    def navigate_to_path(self, path: List[str]) -> bool:
        """根据路径导航到指定页面。

        Args:
            path (List[str]): 从根页面开始的绝对路径。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.root_page or not path:
            return False
        
        target_page = self.root_page.find_page_by_path(path)
        if target_page:
            return self.navigate_to_page(target_page)
        return False

    def navigate_to_relative_path(self, path: List[str]) -> bool:
        """根据相对路径导航到指定页面。

        Args:
            path (List[str]): 从当前页面开始的相对路径。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.current_page:
            return False
        
        target_page = self.current_page.find_page_by_path(path)
        if target_page:
            return self.navigate_to_page(target_page)
        return False

    def navigate_to_page(self, target_page: Page) -> bool:
        """直接导航到指定页面。

        Args:
            target_page (Page): 目标页面实例。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not target_page:
            return False
        
        if self.current_page:
            # 记录当前页面到历史（如果不是返回操作）
            if (not self.navigation_history or 
                self.navigation_history[-1] != target_page):
                self.navigation_history.append(self.current_page)
            
            self.current_page.on_exit()
        
        self.current_page = target_page
        target_page.on_enter()
        
        return True

    def go_back(self) -> bool:
        """返回到历史记录中的前一个页面。

        Returns:
            bool: 如果返回成功则返回 True，否则返回 False。
        """
        if not self.navigation_history:
            return False
        
        previous_page = self.navigation_history.pop()
        
        if self.current_page:
            self.current_page.on_exit()
        
        self.current_page = previous_page
        previous_page.on_enter()
        
        return True

    def clear_history(self):
        """清空导航历史记录。"""
        self.navigation_history.clear()

    def get_current_path(self) -> List[str]:
        """获取当前页面的完整路径。

        Returns:
            List[str]: 当前页面的路径。
        """
        if self.current_page:
            return self.current_page.get_path()
        return []

    def get_navigation_info(self) -> dict:
        """获取当前导航状态信息。

        Returns:
            dict: 包含当前页面、路径、历史等信息的字典。
        """
        return {
            'current_page': self.current_page.name if self.current_page else None,
            'current_path': self.get_current_path(),
            'can_go_back': len(self.navigation_history) > 0,
            'can_go_to_parent': (self.current_page and 
                                self.current_page.parent is not None),
            'history_depth': len(self.navigation_history),
            'page_depth': (self.current_page.get_depth() 
                          if self.current_page else 0)
        }

    def update(self, img: image.Image):
        """更新当前活动页面的状态。

        此方法应在主循环中每帧调用，它会调用当前页面的 `update` 方法。

        Args:
            img (maix.image.Image): 用于绘制的图像缓冲区。
        """
        if self.current_page:
            self.current_page.update(img)
