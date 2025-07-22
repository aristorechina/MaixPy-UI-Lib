# -*- coding: utf-8 -*-
import sys
sys.path.append(r'/root/modules')
from maix import display, camera, app, image, touchscreen
from ui import (Button, ButtonManager, Slider, SliderManager,
                Switch, SwitchManager, Checkbox, CheckboxManager,
                RadioButton, RadioManager, ResolutionAdapter,
                Page, UIManager)

# ==========================================================
# 1. 全局设置和状态
# ==========================================================
print("Starting comprehensive UI demo with consistent feedback...")
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera(640, 480)

# 获取摄像头实际分辨率并创建适配器
disp_w, disp_h = cam.width(), cam.height()
adapter = ResolutionAdapter(disp_w, disp_h)

# 颜色和应用状态
C_WHITE = (255, 255, 255); C_BLACK = (0, 0, 0); C_RED = (200, 30, 30)
C_BLUE = (0, 120, 220); C_GREEN = (30, 200, 30); C_YELLOW = (220, 220, 30)
C_GRAY = (100, 100, 100); C_STATUS_ON = (30, 200, 30); C_STATUS_OFF = (80, 80, 80)

app_state = {
    'slider_color': 128, 'radio_choice': 'B',
    'checkboxes': {'A': False, 'B': True, 'C': False},
    'switches': {'small': False, 'medium': True, 'large': False}
}

# ==========================================================
# 2. 回调函数和UI组件初始化
# ==========================================================
def slider_callback(value): 
    app_state['slider_color'] = value

def radio_callback(value): 
    app_state['radio_choice'] = value

def create_checkbox_callback(key):
    def inner_callback(is_checked): 
        app_state['checkboxes'][key] = is_checked
        print(f"Checkbox '{key}' state: {is_checked}")
    return inner_callback

def create_switch_callback(key):
    def inner_callback(is_on): 
        app_state['switches'][key] = is_on
        print(f"Switch '{key}' state: {is_on}")
    return inner_callback

# 创建返回按钮
back_button = Button(
    rect=adapter.scale_rect([0, 0, 30, 30]), 
    label='<', 
    callback=None,  # 稍后设置
    bg_color=C_BLACK, 
    pressed_color=None, 
    text_color=C_WHITE, 
    border_thickness=0, 
    text_scale=adapter.scale_value(1.0)
)

# 创建主页按钮管理器
home_btn_manager = ButtonManager(ts, disp)
home_btn_manager.add_button(Button(
    rect=adapter.scale_rect([30, 30, 120, 80]), 
    label="Switch", 
    callback=None,  # 稍后设置
    bg_color=None, 
    pressed_color=None, 
    border_color=C_WHITE, 
    text_color=C_WHITE, 
    border_thickness=int(adapter.scale_value(2)), 
    text_scale=adapter.scale_value(0.8)
))
home_btn_manager.add_button(Button(
    rect=adapter.scale_rect([170, 30, 120, 80]), 
    label="Slider", 
    callback=None,  # 稍后设置
    bg_color=C_RED, 
    pressed_color=C_BLUE, 
    border_thickness=0, 
    text_scale=adapter.scale_value(1.0)
))
home_btn_manager.add_button(Button(
    rect=adapter.scale_rect([30, 130, 120, 80]), 
    label="Radio", 
    callback=None,  # 稍后设置
    bg_color=C_YELLOW, 
    pressed_color=C_GRAY, 
    border_color=C_GREEN, 
    border_thickness=int(adapter.scale_value(2)), 
    text_scale=adapter.scale_value(1.2)
))
home_btn_manager.add_button(Button(
    rect=adapter.scale_rect([170, 130, 120, 80]), 
    label="Checkbox", 
    callback=None,  # 稍后设置
    bg_color=C_GREEN, 
    pressed_color=C_GRAY, 
    border_color=C_YELLOW, 
    border_thickness=int(adapter.scale_value(2)), 
    text_scale=adapter.scale_value(1.4)
))

# 初始化各个页面管理器
switch_page_manager = SwitchManager(ts, disp)
switch_page_manager.add_switch(Switch(
    position=adapter.scale_position(40, 50), 
    scale=adapter.scale_value(0.8), 
    is_on=app_state['switches']['small'], 
    callback=create_switch_callback('small')
))
switch_page_manager.add_switch(Switch(
    position=adapter.scale_position(40, 100), 
    scale=adapter.scale_value(1.0), 
    is_on=app_state['switches']['medium'], 
    callback=create_switch_callback('medium')
))
switch_page_manager.add_switch(Switch(
    position=adapter.scale_position(40, 160), 
    scale=adapter.scale_value(1.5), 
    is_on=app_state['switches']['large'], 
    callback=create_switch_callback('large')
))

slider_page_manager = SliderManager(ts, disp)
slider_page_manager.add_slider(Slider(
    rect=adapter.scale_rect([60, 130, 200, 20]), 
    label="Color Value", 
    default_val=app_state['slider_color'], 
    scale=adapter.scale_value(1.0), 
    min_val=0, 
    max_val=255, 
    callback=slider_callback
))

radio_page_manager = RadioManager(ts, disp, default_value=app_state['radio_choice'], callback=radio_callback)
radio_page_manager.add_radio(RadioButton(
    position=adapter.scale_position(40, 60), 
    label="Option A", 
    value="A", 
    scale=adapter.scale_value(1.0)
))
radio_page_manager.add_radio(RadioButton(
    position=adapter.scale_position(40, 110), 
    label="Option B", 
    value="B", 
    scale=adapter.scale_value(1.0)
))
radio_page_manager.add_radio(RadioButton(
    position=adapter.scale_position(40, 160), 
    label="Option C", 
    value="C", 
    scale=adapter.scale_value(1.0)
))

checkbox_page_manager = CheckboxManager(ts, disp)
checkbox_page_manager.add_checkbox(Checkbox(
    position=adapter.scale_position(40, 50), 
    label="Small", 
    scale=adapter.scale_value(0.8), 
    is_checked=app_state['checkboxes']['A'], 
    callback=create_checkbox_callback('A')
))
checkbox_page_manager.add_checkbox(Checkbox(
    position=adapter.scale_position(40, 100), 
    label="Medium", 
    scale=adapter.scale_value(1.0), 
    is_checked=app_state['checkboxes']['B'], 
    callback=create_checkbox_callback('B')
))
checkbox_page_manager.add_checkbox(Checkbox(
    position=adapter.scale_position(40, 160), 
    label="Large", 
    scale=adapter.scale_value(1.5), 
    is_checked=app_state['checkboxes']['C'], 
    callback=create_checkbox_callback('C')
))

# 预创建颜色对象
title_color = image.Color.from_rgb(*C_WHITE)
status_on_color = image.Color.from_rgb(*C_STATUS_ON)
status_off_color = image.Color.from_rgb(*C_STATUS_OFF)

# ==========================================================
# 3. 定义页面类
# ==========================================================
class SubPage(Page):
    """
    一个通用的子页面基类，它自动处理"返回"按钮的逻辑
    """
    def handle_back_button(self, img):
        """
        处理和绘制全局的"返回"按钮
        """
        x_touch, y_touch, pressed_touch = ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w_actual, disp_h_actual = disp.width(), disp.height()
        
        back_button.handle_event(x_touch, y_touch, pressed_touch, img_w, img_h, disp_w_actual, disp_h_actual)
        back_button.draw(img)

class HomePage(Page):
    """
    主页
    """
    def update(self, img):
        """
        HomePage 的核心更新逻辑
        """
        x, y = adapter.scale_position(10, 5)
        img.draw_string(x, y, "UI Demo Home", scale=adapter.scale_value(1.5), color=title_color)
        home_btn_manager.handle_events(img)

class SwitchPage(SubPage):
    """
    开关(Switch)组件的演示页面
    """
    def update(self, img):
        self.handle_back_button(img)
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Switch Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        x_status, y_status = adapter.scale_position(220, 30)
        img.draw_string(x_status, y_status, "Status", scale=adapter.scale_value(1.0), color=title_color)
        colors = [status_on_color if app_state['switches'][k] else status_off_color for k in ['small', 'medium', 'large']]
        rects = [adapter.scale_rect(r) for r in [[220, 50, 30, 20], [220, 100, 30, 20], [220, 160, 30, 20]]]
        for r, c in zip(rects, colors): 
            img.draw_rect(*r, color=c, thickness=-1)
        
        switch_page_manager.handle_events(img)

class SliderPage(SubPage):
    """
    滑块(Slider)组件的演示页面
    """
    def update(self, img):
        self.handle_back_button(img)
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Slider Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        color_val = app_state['slider_color']
        preview_color = image.Color.from_rgb(color_val, color_val, color_val)
        x_rect, y_rect, w_rect, h_rect = adapter.scale_rect([140, 40, 40, 40])
        img.draw_rect(x_rect, y_rect, w_rect, h_rect, color=preview_color, thickness=-1)
        
        slider_page_manager.handle_events(img)

class RadioPage(SubPage):
    """
    单选框(RadioButton)组件的演示页面
    """
    def update(self, img):
        self.handle_back_button(img)
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Radio Button Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        x_text, y_text = adapter.scale_position(200, 110)
        img.draw_string(x_text, y_text, f"Selected: {app_state['radio_choice']}", color=title_color, scale=adapter.scale_value(1.0))
        
        radio_page_manager.handle_events(img)

class CheckboxPage(SubPage):
    """
    复选框(Checkbox)组件的演示页面
    """
    def update(self, img):
        self.handle_back_button(img)
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Checkbox Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        status_x = 260
        x_status, y_status = adapter.scale_position(status_x, 30)
        img.draw_string(x_status, y_status, "Status", scale=adapter.scale_value(1.0), color=title_color)
        colors = [status_on_color if app_state['checkboxes'][k] else status_off_color for k in ['A', 'B', 'C']]
        rects = [adapter.scale_rect(r) for r in [[status_x, 50, 30, 20], [status_x, 105, 30, 20], [status_x, 160, 30, 20]]]
        for r, c in zip(rects, colors): 
            img.draw_rect(*r, color=c, thickness=-1)
        
        checkbox_page_manager.handle_events(img)

# ==========================================================
# 4. 初始化UI管理器（使用新的树型结构）
# ==========================================================
ui_manager = UIManager()

# 创建页面实例
home_page = HomePage(ui_manager, "home")
switch_page = SwitchPage(ui_manager, "switch")
slider_page = SliderPage(ui_manager, "slider")
radio_page = RadioPage(ui_manager, "radio")
checkbox_page = CheckboxPage(ui_manager, "checkbox")

# 建立页面树结构 - 将所有子页面添加到主页下
home_page.add_child(switch_page)
home_page.add_child(slider_page)
home_page.add_child(radio_page)
home_page.add_child(checkbox_page)

# 设置页面间的导航回调函数
home_btn_manager.buttons[0].callback = lambda: ui_manager.navigate_to_child("switch")
home_btn_manager.buttons[1].callback = lambda: ui_manager.navigate_to_child("slider")
home_btn_manager.buttons[2].callback = lambda: ui_manager.navigate_to_child("radio")
home_btn_manager.buttons[3].callback = lambda: ui_manager.navigate_to_child("checkbox")

back_button.callback = lambda: ui_manager.navigate_to_parent()

# 设置根页面并开始
ui_manager.set_root_page(home_page)

# ==========================================================
# 5. 主循环
# ==========================================================
while not app.need_exit():
    img = cam.read()
    ui_manager.update(img)
    disp.show(img)

print("UI Demo finished.")
