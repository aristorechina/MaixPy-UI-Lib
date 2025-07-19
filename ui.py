"""
MaixPy-UI-Lib: A lightweight UI component library for MaixPy

--------------------------------------------------------------------------
  Author  : Aristore
  Version : 1.0
  Date    : 2025-07-20
  Web     : https://www.aristore.top/
  Repo    : https://github.com/your-username/Maix-Py-UI-Lib # 请替换为您的仓库地址
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

"""

import maix.image as image
import maix.touchscreen as touchscreen
import maix.display as display

# ==============================================================================
# 1. Button Component
# ==============================================================================
class Button:
    def _normalize_color(self, color):
        if color is None: return None
        if isinstance(color, tuple):
            if len(color) == 3: return image.Color.from_rgb(color[0], color[1], color[2])
            else: raise ValueError("颜色元组必须是 3 个元素的 RGB 格式。")
        return color
    def __init__(self, rect, label, callback, bg_color=(50, 50, 50), pressed_color=(0, 120, 220),
                 text_color=(255, 255, 255), border_color=(200, 200, 200), border_thickness=2,
                 text_scale=1.5, font=None, align_h='center', align_v='center'):
        if not all(isinstance(i, int) for i in rect) or len(rect) != 4: raise ValueError("rect 必须是包含四个整数 [x, y, w, h] 的列表")
        if not callable(callback): raise TypeError("callback 必须是一个可调用的函数")
        self.rect, self.label, self.callback = rect, label, callback
        self.text_scale, self.font, self.border_thickness = text_scale, font, border_thickness
        self.align_h, self.align_v = align_h, align_v
        self.bg_color, self.pressed_color = self._normalize_color(bg_color), self._normalize_color(pressed_color)
        self.text_color, self.border_color = self._normalize_color(text_color), self._normalize_color(border_color)
        self.is_pressed, self.click_armed, self.disp_rect = False, False, [0, 0, 0, 0]
    def _is_in_rect(self, x, y, rect): return rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]
    def draw(self, img: image.Image):
        current_bg_color = self.pressed_color if self.is_pressed else self.bg_color
        if current_bg_color is not None: img.draw_rect(*self.rect, color=current_bg_color, thickness=-1)
        if self.border_thickness > 0: img.draw_rect(*self.rect, color=self.border_color, thickness=self.border_thickness)
        font_arg = self.font if self.font is not None else ""
        text_size = image.string_size(self.label, scale=self.text_scale, font=font_arg)
        if self.align_h == 'center': text_x = self.rect[0] + (self.rect[2] - text_size[0]) // 2
        elif self.align_h == 'left': text_x = self.rect[0] + self.border_thickness + 5
        else: text_x = self.rect[0] + self.rect[2] - text_size[0] - self.border_thickness - 5
        if self.align_v == 'center': text_y = self.rect[1] + (self.rect[3] - text_size[1]) // 2
        elif self.align_v == 'top': text_y = self.rect[1] + self.border_thickness + 5
        else: text_y = self.rect[1] + self.rect[3] - text_size[1] - self.border_thickness - 5
        img.draw_string(text_x, text_y, self.label, color=self.text_color, scale=self.text_scale, font=font_arg)
    def handle_event(self, x, y, pressed, img_w, img_h, disp_w, disp_h):
        self.disp_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *self.rect)
        is_hit = self._is_in_rect(x, y, self.disp_rect)
        if pressed:
            if is_hit:
                if not self.click_armed: self.click_armed = True
                self.is_pressed = True
            else: self.is_pressed, self.click_armed = False, False
        else:
            if self.click_armed and is_hit: self.callback()
            self.is_pressed, self.click_armed = False, False

class ButtonManager:
    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display): self.ts, self.disp, self.buttons = ts, disp, []
    def add_button(self, button: Button):
        if isinstance(button, Button): self.buttons.append(button)
        else: raise TypeError("只能添加 Button 类的实例")
    def handle_events(self, img: image.Image):
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for btn in self.buttons: btn.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h); btn.draw(img)

# ==============================================================================
# 2. Slider Component
# ==============================================================================
class Slider:
    BASE_HANDLE_RADIUS = 10
    BASE_HANDLE_BORDER_THICKNESS = 2
    BASE_HANDLE_PRESSED_RADIUS_INCREASE = 3
    BASE_TRACK_HEIGHT = 6
    BASE_LABEL_SCALE = 1.2
    BASE_TOOLTIP_SCALE = 1.2
    BASE_TOUCH_PADDING_Y = 10
    def _normalize_color(self, color):
        if color is None: return None
        if isinstance(color, tuple):
            if len(color) == 3: return image.Color.from_rgb(color[0], color[1], color[2])
            else: raise ValueError("颜色元组必须是 3 个元素的 RGB 格式。")
        return color
    def __init__(self, rect, scale=1.0, min_val=0, max_val=100, default_val=50, callback=None, label="",
                 track_color=(60, 60, 60), progress_color=(0, 120, 220), handle_color=(255, 255, 255),
                 handle_border_color=(100, 100, 100), handle_pressed_color=(220, 220, 255),
                 label_color=(200, 200, 200), tooltip_bg_color=(0, 0, 0), tooltip_text_color=(255, 255, 255),
                 show_tooltip_on_drag=True):
        if not all(isinstance(i, int) for i in rect) or len(rect) != 4: raise ValueError("rect 必须是包含四个整数 [x, y, w, h] 的列表")
        if not min_val < max_val: raise ValueError("min_val 必须小于 max_val")
        if not min_val <= default_val <= max_val: raise ValueError("default_val 必须在 min_val 和 max_val 之间")
        if callback is not None and not callable(callback): raise TypeError("callback 必须是一个可调用的函数或 None")
        self.rect, self.min_val, self.max_val, self.value = rect, min_val, max_val, default_val
        self.callback, self.label, self.scale = callback, label, scale
        self.show_tooltip_on_drag = show_tooltip_on_drag
        self.handle_radius = int(self.BASE_HANDLE_RADIUS * scale)
        self.handle_border_thickness = int(self.BASE_HANDLE_BORDER_THICKNESS * scale)
        self.handle_pressed_radius_increase = int(self.BASE_HANDLE_PRESSED_RADIUS_INCREASE * scale)
        self.track_height = int(self.BASE_TRACK_HEIGHT * scale)
        self.label_scale = self.BASE_LABEL_SCALE * scale
        self.tooltip_scale = self.BASE_TOOLTIP_SCALE * scale
        self.touch_padding_y = int(self.BASE_TOUCH_PADDING_Y * scale)
        self.track_color, self.progress_color, self.handle_color = self._normalize_color(track_color), self._normalize_color(progress_color), self._normalize_color(handle_color)
        self.handle_border_color, self.handle_pressed_color, self.label_color = self._normalize_color(handle_border_color), self._normalize_color(handle_pressed_color), self._normalize_color(label_color)
        self.tooltip_bg_color, self.tooltip_text_color = self._normalize_color(tooltip_bg_color), self._normalize_color(tooltip_text_color)
        self.is_pressed, self.disp_rect = False, [0, 0, 0, 0]
    def _is_in_rect(self, x, y, rect): return rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]
    def draw(self, img: image.Image):
        track_start_x, track_width, track_center_y = self.rect[0], self.rect[2], self.rect[1] + self.rect[3] // 2
        if track_width <= 0: return
        value_fraction = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_center_x = track_start_x + value_fraction * track_width
        if self.label:
            label_size = image.string_size(self.label, scale=self.label_scale)
            label_y = self.rect[1] - label_size.height() - int(5 * self.scale)
            img.draw_string(track_start_x, label_y, self.label, color=self.label_color, scale=self.label_scale)
        track_y = track_center_y - self.track_height // 2
        img.draw_rect(track_start_x, track_y, track_width, self.track_height, color=self.track_color, thickness=-1)
        progress_width = int(value_fraction * track_width)
        if progress_width > 0: img.draw_rect(track_start_x, track_y, progress_width, self.track_height, color=self.progress_color, thickness=-1)
        current_radius = self.handle_radius + (self.handle_pressed_radius_increase if self.is_pressed else 0)
        current_handle_color = self.handle_pressed_color if self.is_pressed else self.handle_color
        border_thickness = min(self.handle_border_thickness, current_radius)
        if border_thickness > 0: img.draw_circle(int(handle_center_x), track_center_y, current_radius, color=self.handle_border_color, thickness=-1)
        img.draw_circle(int(handle_center_x), track_center_y, current_radius - border_thickness, color=current_handle_color, thickness=-1)
        if self.is_pressed and self.show_tooltip_on_drag:
            value_text = str(int(self.value)); text_size = image.string_size(value_text, scale=self.tooltip_scale); padding = int(5 * self.scale)
            box_w, box_h = text_size.width() + 2 * padding, text_size.height() + 2 * padding
            box_x, box_y = int(handle_center_x - box_w // 2), self.rect[1] - box_h - int(10 * self.scale)
            img.draw_rect(box_x, box_y, box_w, box_h, color=self.tooltip_bg_color, thickness=-1)
            img.draw_string(box_x + padding, box_y + padding, value_text, color=self.tooltip_text_color, scale=self.tooltip_scale)
    def handle_event(self, x, y, pressed, img_w, img_h, disp_w, disp_h):
        touch_rect = [self.rect[0], self.rect[1] - self.touch_padding_y, self.rect[2], self.rect[3] + 2 * self.touch_padding_y]
        self.disp_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *touch_rect)
        is_hit = self._is_in_rect(x, y, self.disp_rect)
        if self.is_pressed and not pressed: self.is_pressed = False; return
        if (pressed and is_hit) or self.is_pressed:
            self.is_pressed = True
            mapped_track_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *self.rect)
            disp_track_start_x, disp_track_width = mapped_track_rect[0], mapped_track_rect[2]
            if disp_track_width <= 0: return
            clamped_x = max(disp_track_start_x, min(x, disp_track_start_x + disp_track_width))
            pos_fraction = (clamped_x - disp_track_start_x) / disp_track_width
            new_value = self.min_val + pos_fraction * (self.max_val - self.min_val)
            new_value_int = int(round(new_value))
            if new_value_int != self.value:
                self.value = new_value_int
                if self.callback: self.callback(self.value)
        else: self.is_pressed = False

class SliderManager:
    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display): self.ts, self.disp, self.sliders = ts, disp, []
    def add_slider(self, slider: Slider):
        if isinstance(slider, Slider): self.sliders.append(slider)
        else: raise TypeError("只能添加 Slider 类的实例")
    def handle_events(self, img: image.Image):
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for s in self.sliders: s.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h); s.draw(img)

# ==============================================================================
# 3. Switch Component
# ==============================================================================
class Switch:
    BASE_H, BASE_W = 30, int(30 * 1.9)
    def _normalize_color(self, color):
        if color is None: return None
        if isinstance(color, tuple):
            if len(color) == 3: return image.Color.from_rgb(color[0], color[1], color[2])
            else: raise ValueError("颜色元组必须是 3 个元素的 RGB 格式。")
        return color
    def __init__(self, position, scale=1.0, is_on=False, callback=None, on_color=(30, 200, 30), off_color=(100, 100, 100),
                 handle_color=(255, 255, 255), handle_pressed_color=(220, 220, 255), handle_radius_increase=2):
        if not isinstance(position, (list, tuple)) or len(position) != 2: raise ValueError("position 必须是包含两个整数 [x, y] 的列表或元组")
        if callback is not None and not callable(callback): raise TypeError("callback 必须是一个可调用的函数或 None")
        self.pos, self.scale, self.is_on, self.callback = position, scale, is_on, callback
        self.width, self.height = int(self.BASE_W * scale), int(self.BASE_H * scale)
        self.rect = [self.pos[0], self.pos[1], self.width, self.height]
        self.on_color, self.off_color = self._normalize_color(on_color), self._normalize_color(off_color)
        self.handle_color, self.handle_pressed_color = self._normalize_color(handle_color), self._normalize_color(handle_pressed_color)
        self.handle_radius_increase = int(handle_radius_increase * scale)
        self.is_pressed, self.click_armed, self.disp_rect = False, False, [0, 0, 0, 0]
    def _is_in_rect(self, x, y, rect): return rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]
    def toggle(self):
        self.is_on = not self.is_on
        if self.callback:
            self.callback(self.is_on)
    def draw(self, img: image.Image):
        track_x, track_y, track_w, track_h = self.rect
        track_center_y, handle_radius = track_y + track_h // 2, track_h // 2
        current_bg_color = self.on_color if self.is_on else self.off_color
        img.draw_circle(track_x + handle_radius, track_center_y, handle_radius, color=current_bg_color, thickness=-1)
        img.draw_circle(track_x + track_w - handle_radius, track_center_y, handle_radius, color=current_bg_color, thickness=-1)
        img.draw_rect(track_x + handle_radius, track_y, track_w - 2 * handle_radius, track_h, color=current_bg_color, thickness=-1)
        handle_pos_x = (track_x + track_w - handle_radius) if self.is_on else (track_x + handle_radius)
        current_handle_color = self.handle_pressed_color if self.is_pressed else self.handle_color
        padding = int(2 * self.scale)
        current_handle_radius = handle_radius - padding + (self.handle_radius_increase if self.is_pressed else 0)
        img.draw_circle(handle_pos_x, track_center_y, current_handle_radius, color=current_handle_color, thickness=-1)
    def handle_event(self, x, y, pressed, img_w, img_h, disp_w, disp_h):
        self.disp_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *self.rect)
        is_hit = self._is_in_rect(x, y, self.disp_rect)
        if pressed:
            if is_hit and not self.click_armed: self.is_pressed, self.click_armed = True, True
        else:
            if self.click_armed and is_hit: self.toggle()
            self.is_pressed, self.click_armed = False, False

class SwitchManager:
    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display): self.ts, self.disp, self.switches = ts, disp, []
    def add_switch(self, switch: Switch):
        if isinstance(switch, Switch): self.switches.append(switch)
        else: raise TypeError("只能添加 Switch 类的实例")
    def handle_events(self, img: image.Image):
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for s in self.switches: s.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h); s.draw(img)

# ==============================================================================
# 4. Checkbox Component
# ==============================================================================
class Checkbox:
    BASE_BOX_SIZE, BASE_TEXT_SCALE, BASE_SPACING = 25, 1.2, 10
    def _normalize_color(self, color):
        if color is None: return None
        if isinstance(color, tuple):
            if len(color) == 3: return image.Color.from_rgb(color[0], color[1], color[2])
            else: raise ValueError("颜色元组必须是 3 个元素的 RGB 格式。")
        return color
    def __init__(self, position, label, scale=1.0, is_checked=False, callback=None, box_color=(200, 200, 200),
                 box_checked_color=(0, 120, 220), check_color=(255, 255, 255), text_color=(200, 200, 200), box_thickness=2):
        if not isinstance(position, (list, tuple)) or len(position) != 2: raise ValueError("position 必须是包含两个整数 [x, y] 的列表或元组")
        if callback is not None and not callable(callback): raise TypeError("callback 必须是一个可调用的函数或 None")
        self.pos, self.label, self.scale, self.is_checked, self.callback = position, label, scale, is_checked, callback
        self.box_size, self.text_scale = int(self.BASE_BOX_SIZE * scale), self.BASE_TEXT_SCALE * scale
        self.spacing, self.box_thickness = int(self.BASE_SPACING * scale), int(box_thickness * scale)
        touch_padding_y = 5
        self.rect = [self.pos[0], self.pos[1] - touch_padding_y, self.box_size, self.box_size + 2 * touch_padding_y]
        self.box_color, self.box_checked_color = self._normalize_color(box_color), self._normalize_color(box_checked_color)
        self.check_color, self.text_color = self._normalize_color(check_color), self._normalize_color(text_color)
        self.click_armed, self.disp_rect = False, [0, 0, 0, 0]
    def _is_in_rect(self, x, y, rect): return rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]
    def toggle(self):
        self.is_checked = not self.is_checked
        if self.callback: self.callback(self.is_checked)
    def draw(self, img: image.Image):
        box_x, box_y = self.pos
        text_size = image.string_size(self.label, scale=self.text_scale)
        total_h = max(self.box_size, text_size.height())
        box_offset_y, text_offset_y = (total_h - self.box_size) // 2, (total_h - text_size.height()) // 2
        box_draw_y, text_draw_y, text_draw_x = box_y + box_offset_y, box_y + text_offset_y, box_x + self.box_size + self.spacing
        current_box_color = self.box_checked_color if self.is_checked else self.box_color
        if self.is_checked: img.draw_rect(box_x, box_draw_y, self.box_size, self.box_size, color=current_box_color, thickness=-1)
        img.draw_rect(box_x, box_draw_y, self.box_size, self.box_size, color=current_box_color, thickness=self.box_thickness)
        if self.is_checked:
            p1 = (box_x + int(self.box_size * 0.2), box_draw_y + int(self.box_size * 0.5))
            p2 = (box_x + int(self.box_size * 0.45), box_draw_y + int(self.box_size * 0.75))
            p3 = (box_x + int(self.box_size * 0.8), box_draw_y + int(self.box_size * 0.25))
            check_thickness = max(1, int(2 * self.scale))
            img.draw_line(p1[0], p1[1], p2[0], p2[1], color=self.check_color, thickness=check_thickness)
            img.draw_line(p2[0], p2[1], p3[0], p3[1], color=self.check_color, thickness=check_thickness)
        img.draw_string(text_draw_x, text_draw_y, self.label, color=self.text_color, scale=self.text_scale)
    def handle_event(self, x, y, pressed, img_w, img_h, disp_w, disp_h):
        self.disp_rect = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *self.rect)
        is_hit = self._is_in_rect(x, y, self.disp_rect)
        if pressed:
            if is_hit and not self.click_armed: self.click_armed = True
        else:
            if self.click_armed and is_hit: self.toggle()
            self.click_armed = False

class CheckboxManager:
    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display): self.ts, self.disp, self.checkboxes = ts, disp, []
    def add_checkbox(self, checkbox: Checkbox):
        if isinstance(checkbox, Checkbox): self.checkboxes.append(checkbox)
        else: raise TypeError("只能添加 Checkbox 类的实例")
    def handle_events(self, img: image.Image):
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for cb in self.checkboxes: cb.handle_event(x, y, pressed, img_w, img_h, disp_w, disp_h); cb.draw(img)

# ==============================================================================
# 5. RadioButton Component
# ==============================================================================
class RadioButton:
    BASE_CIRCLE_RADIUS, BASE_TEXT_SCALE, BASE_SPACING = 12, 1.2, 10
    def _normalize_color(self, color):
        if color is None: return None
        if isinstance(color, tuple):
            if len(color) == 3: return image.Color.from_rgb(color[0], color[1], color[2])
            else: raise ValueError("颜色元组必须是 3 个元素的 RGB 格式。")
        return color
    def __init__(self, position, label, value, scale=1.0, circle_color=(200, 200, 200), circle_selected_color=(0, 120, 220),
                 dot_color=(255, 255, 255), text_color=(200, 200, 200), circle_thickness=2):
        self.pos, self.label, self.value, self.scale = position, label, value, scale
        self.is_selected = False
        self.radius, self.text_scale = int(self.BASE_CIRCLE_RADIUS * scale), self.BASE_TEXT_SCALE * scale
        self.spacing, self.circle_thickness = int(self.BASE_SPACING * scale), int(circle_thickness * scale)
        touch_padding = 5
        self.rect = [self.pos[0], self.pos[1], 2 * self.radius, 2 * self.radius] # Centered touch area
        self.circle_color, self.circle_selected_color = self._normalize_color(circle_color), self._normalize_color(circle_selected_color)
        self.dot_color, self.text_color = self._normalize_color(dot_color), self._normalize_color(text_color)
        self.click_armed = False
    def draw(self, img: image.Image):
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
    def __init__(self, ts: touchscreen.TouchScreen, disp: display.Display, default_value=None, callback=None):
        self.ts, self.disp, self.radios, self.selected_value, self.callback = ts, disp, [], default_value, callback
        self.disp_rects = {}
    def add_radio(self, radio: RadioButton):
        if isinstance(radio, RadioButton):
            self.radios.append(radio)
            if radio.value == self.selected_value: radio.is_selected = True
        else: raise TypeError("只能添加 RadioButton 类的实例")
    def _select_radio(self, value):
        if self.selected_value != value:
            self.selected_value = value
            for r in self.radios: r.is_selected = (r.value == self.selected_value)
            if self.callback: self.callback(self.selected_value)
    def _is_in_rect(self, x, y, rect): return rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]
    def handle_events(self, img: image.Image):
        x, y, pressed = self.ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = self.disp.width(), self.disp.height()
        for r in self.radios: self.disp_rects[r.value] = image.resize_map_pos(img_w, img_h, disp_w, disp_h, image.Fit.FIT_CONTAIN, *r.rect)
        if pressed:
            for r in self.radios:
                if self._is_in_rect(x, y, self.disp_rects[r.value]) and not r.click_armed: r.click_armed = True
        else:
            for r in self.radios:
                if r.click_armed and self._is_in_rect(x, y, self.disp_rects[r.value]): self._select_radio(r.value)
                r.click_armed = False
        for r in self.radios: r.draw(img)