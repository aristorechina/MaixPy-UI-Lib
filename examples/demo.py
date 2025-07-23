# -*- coding: utf-8 -*-
__author__ = 'Aristore'

from maix import display, camera, app, image, touchscreen
from maixpy_ui import (Button, ButtonManager, Slider, SliderManager,
                Switch, SwitchManager, Checkbox, CheckboxManager,
                RadioButton, RadioManager, ResolutionAdapter,
                Page, UIManager)

# ==========================================================
# 1. 全局设置和状态
# ==========================================================
print("Starting comprehensive UI demo...")

disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera(640, 480)
# cam = camera.Camera(320,240) # demo 是为 640*480 分辨率准备的，将上一行注释并取消本行注释即可体验 ResolutionAdapter 的效果

# 创建分辨率适配器
# 它可以将我们在一个固定设计分辨率（如此处的640x480）下定义的UI坐标和尺寸
# 自动缩放到摄像头的实际输出分辨率，确保UI在不同分辨率下都能正确显示。
disp_w, disp_h = cam.width(), cam.height()
adapter = ResolutionAdapter(disp_w, disp_h)

# 全局颜色常量
C_WHITE = (255, 255, 255); C_BLACK = (0, 0, 0); C_RED = (200, 30, 30)
C_BLUE = (0, 120, 220); C_GREEN = (30, 200, 30); C_YELLOW = (220, 220, 30)
C_GRAY = (100, 100, 100); C_STATUS_ON = (30, 200, 30); C_STATUS_OFF = (80, 80, 80)

# 全局应用状态字典
app_state = {
    'slider_color': 128, 'radio_choice': 'B',
    'checkboxes': {'A': False, 'B': True, 'C': False},
    'switches': {'small': False, 'medium': True, 'large': False}
}

# ==========================================================
# 2. 回调函数和UI组件初始化
# ==========================================================
# 创建所有UI组件实例和它们被操作时触发的回调函数。
# 注意：此时按钮的回调函数（callback）暂时都设为 None，我们将在第4部分统一设置导航逻辑。

# --- 定义回调函数 ---
def slider_callback(value): app_state['slider_color'] = value
def radio_callback(value): app_state['radio_choice'] = value
# 使用闭包为每个复选框/开关创建独立的回调函数
def create_checkbox_callback(key):
    def inner_callback(is_checked): app_state['checkboxes'][key] = is_checked; print(f"Checkbox '{key}' state: {is_checked}")
    return inner_callback
def create_switch_callback(key):
    def inner_callback(is_on): app_state['switches'][key] = is_on; print(f"Switch '{key}' state: {is_on}")
    return inner_callback

# --- 创建UI组件和管理器 ---
# 全局返回按钮，所有子页面都会共用这一个实例
back_button = Button(rect=adapter.scale_rect([0, 0, 30, 30]), label='<', callback=None, bg_color=C_BLACK, pressed_color=None, text_color=C_WHITE, border_thickness=0, text_scale=adapter.scale_value(1.0))

# 主页的按钮管理器和按钮
home_btn_manager = ButtonManager(ts, disp)
home_btn_manager.add_button(Button(rect=adapter.scale_rect([30, 30, 120, 80]), label="Switch", callback=None, border_color=C_WHITE, text_color=C_WHITE, border_thickness=int(adapter.scale_value(2)), text_scale=adapter.scale_value(0.8)))
home_btn_manager.add_button(Button(rect=adapter.scale_rect([170, 30, 120, 80]), label="Slider", callback=None, bg_color=C_RED, pressed_color=C_BLUE, border_thickness=0, text_scale=adapter.scale_value(1.0)))
home_btn_manager.add_button(Button(rect=adapter.scale_rect([30, 130, 120, 80]), label="Radio", callback=None, bg_color=C_YELLOW, pressed_color=C_GRAY, border_color=C_GREEN, border_thickness=int(adapter.scale_value(2)), text_scale=adapter.scale_value(1.2)))
home_btn_manager.add_button(Button(rect=adapter.scale_rect([170, 130, 120, 80]), label="Checkbox", callback=None, bg_color=C_GREEN, pressed_color=C_GRAY, border_color=C_YELLOW, border_thickness=int(adapter.scale_value(2)), text_scale=adapter.scale_value(1.4)))

# 各个子页面的UI管理器
switch_page_manager = SwitchManager(ts, disp)
switch_page_manager.add_switch(Switch(position=adapter.scale_position(40, 50), scale=adapter.scale_value(0.8), is_on=app_state['switches']['small'], callback=create_switch_callback('small')))
switch_page_manager.add_switch(Switch(position=adapter.scale_position(40, 100), scale=adapter.scale_value(1.0), is_on=app_state['switches']['medium'], callback=create_switch_callback('medium')))
switch_page_manager.add_switch(Switch(position=adapter.scale_position(40, 160), scale=adapter.scale_value(1.5), is_on=app_state['switches']['large'], callback=create_switch_callback('large')))

slider_page_manager = SliderManager(ts, disp)
slider_page_manager.add_slider(Slider(rect=adapter.scale_rect([60, 130, 200, 20]), label="Color Value", default_val=app_state['slider_color'], scale=adapter.scale_value(1.0), min_val=0, max_val=255, callback=slider_callback))

radio_page_manager = RadioManager(ts, disp, default_value=app_state['radio_choice'], callback=radio_callback)
radio_page_manager.add_radio(RadioButton(position=adapter.scale_position(40, 60), label="Option A", value="A", scale=adapter.scale_value(1.0)))
radio_page_manager.add_radio(RadioButton(position=adapter.scale_position(40, 110), label="Option B", value="B", scale=adapter.scale_value(1.0)))
radio_page_manager.add_radio(RadioButton(position=adapter.scale_position(40, 160), label="Option C", value="C", scale=adapter.scale_value(1.0)))

checkbox_page_manager = CheckboxManager(ts, disp)
checkbox_page_manager.add_checkbox(Checkbox(position=adapter.scale_position(40, 50), label="Small", scale=adapter.scale_value(0.8), is_checked=app_state['checkboxes']['A'], callback=create_checkbox_callback('A')))
checkbox_page_manager.add_checkbox(Checkbox(position=adapter.scale_position(40, 100), label="Medium", scale=adapter.scale_value(1.0), is_checked=app_state['checkboxes']['B'], callback=create_checkbox_callback('B')))
checkbox_page_manager.add_checkbox(Checkbox(position=adapter.scale_position(40, 160), label="Large", scale=adapter.scale_value(1.5), is_checked=app_state['checkboxes']['C'], callback=create_checkbox_callback('C')))

# 预创建颜色对象，可以轻微提升绘制性能
title_color = image.Color.from_rgb(*C_WHITE)
status_on_color = image.Color.from_rgb(*C_STATUS_ON)
status_off_color = image.Color.from_rgb(*C_STATUS_OFF)

# ==========================================================
# 3. 定义页面类
# ==========================================================
# 这里的页面类都继承自 maixpy_ui.Page。

# --- 创建一个通用的“子页面”基类 ---
# 这个类的目的是为了代码复用，
# 它继承自 maixpy_ui.Page 并添加了处理“返回”按钮的通用逻辑。
# 所有需要“返回”按钮的页面都可以继承它，而无需重复编写代码。
class SubPage(Page):
    """一个通用的子页面基类，它自动处理“返回”按钮的逻辑。"""
    def __init__(self, ui_manager: UIManager, name: str):
        # 必须调用父类的 __init__ 方法，传递 ui_manager 和页面名称
        super().__init__(ui_manager, name)

    def handle_back_button(self, img):
        """处理和绘制全局的“返回”按钮。"""
        x_touch, y_touch, pressed_touch = ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w_actual, disp_h_actual = disp.width(), disp.height()
        back_button.handle_event(x_touch, y_touch, pressed_touch, img_w, img_h, disp_w_actual, disp_h_actual)
        back_button.draw(img)

# --- 主页 ---
class HomePage(Page):
    """主页。作为所有其他页面的父节点。"""
    def __init__(self, ui_manager: UIManager, name: str):
        super().__init__(ui_manager, name)
    
    def update(self, img):
        """主页的绘制和事件处理。"""
        x, y = adapter.scale_position(10, 5)
        img.draw_string(x, y, "UI Demo Home", scale=adapter.scale_value(1.5), color=title_color)
        # 调用主页专属的按钮管理器，让它处理按钮的事件和绘制
        home_btn_manager.handle_events(img)

# --- 开关页面 ---
class SwitchPage(SubPage):
    """开关(Switch)组件的演示页面。"""
    def __init__(self, ui_manager: UIManager, name: str):
        super().__init__(ui_manager, name)

    def update(self, img):
        # 首先，调用基类方法来处理通用的返回按钮
        self.handle_back_button(img)
        # 接着，绘制此页面的特定内容
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Switch Demo", scale=adapter.scale_value(1.5), color=title_color)
        x_status, y_status = adapter.scale_position(220, 30)
        img.draw_string(x_status, y_status, "Status", scale=adapter.scale_value(1.0), color=title_color)
        colors = [status_on_color if app_state['switches'][k] else status_off_color for k in ['small', 'medium', 'large']]
        rects = [adapter.scale_rect(r) for r in [[220, 50, 30, 20], [220, 100, 30, 20], [220, 160, 30, 20]]]
        for r, c in zip(rects, colors): img.draw_rect(*r, color=c, thickness=-1)
        # 最后，调用此页面专属的 SwitchManager
        switch_page_manager.handle_events(img)

# --- 其他子页面定义（与SwitchPage结构类似，保持简洁）---
class SliderPage(SubPage):
    def __init__(self, ui_manager: UIManager, name: str): super().__init__(ui_manager, name)
    def update(self, img):
        self.handle_back_button(img)
        img.draw_string(*adapter.scale_position(40, 5), "Slider Demo", scale=adapter.scale_value(1.5), color=title_color)
        color_val = app_state['slider_color']
        preview_color = image.Color.from_rgb(color_val, color_val, color_val)
        img.draw_rect(*adapter.scale_rect([140, 40, 40, 40]), color=preview_color, thickness=-1)
        slider_page_manager.handle_events(img)

class RadioPage(SubPage):
    def __init__(self, ui_manager: UIManager, name: str): super().__init__(ui_manager, name)
    def update(self, img):
        self.handle_back_button(img)
        img.draw_string(*adapter.scale_position(40, 5), "Radio Button Demo", scale=adapter.scale_value(1.5), color=title_color)
        img.draw_string(*adapter.scale_position(200, 110), f"Selected: {app_state['radio_choice']}", color=title_color, scale=adapter.scale_value(1.0))
        radio_page_manager.handle_events(img)

class CheckboxPage(SubPage):
    def __init__(self, ui_manager: UIManager, name: str): super().__init__(ui_manager, name)
    def update(self, img):
        self.handle_back_button(img)
        img.draw_string(*adapter.scale_position(40, 5), "Checkbox Demo", scale=adapter.scale_value(1.5), color=title_color)
        status_x = 260
        img.draw_string(*adapter.scale_position(status_x, 30), "Status", scale=adapter.scale_value(1.0), color=title_color)
        colors = [status_on_color if app_state['checkboxes'][k] else status_off_color for k in ['A', 'B', 'C']]
        rects = [adapter.scale_rect(r) for r in [[status_x, 50, 30, 20], [status_x, 105, 30, 20], [status_x, 160, 30, 20]]]
        for r, c in zip(rects, colors): img.draw_rect(*r, color=c, thickness=-1)
        checkbox_page_manager.handle_events(img)

# ==========================================================
# 4. 初始化页面管理器和页面
# ==========================================================
# --- 步骤 1: 创建一个全局的页面管理器实例 ---
# UIManager 是整个UI导航系统的大脑，负责跟踪和切换当前活动的页面。
ui_manager = UIManager()

# --- 步骤 2: 将页面类实例化为具体的页面对象 ---
# 每个页面都需要一个对 ui_manager 的引用和一个在父页面中唯一的 'name'。
# 这个 'name' 是新导航系统用来查找和切换页面的关键标识符。
home_page = HomePage(ui_manager, name="home")
switch_page = SwitchPage(ui_manager, name="switch_demo")
slider_page = SliderPage(ui_manager, name="slider_demo")
radio_page = RadioPage(ui_manager, name="radio_demo")
checkbox_page = CheckboxPage(ui_manager, name="checkbox_demo")

# --- 步骤 3: 构建页面树形结构 ---
# 我们将所有演示页面添加为 home_page 的子页面，形成一个以 "home" 为根的树状结构。
# 当我们调用 ui_manager.navigate_to_child() 时，它会在此结构中查找对应的子页面。
home_page.add_child(switch_page)
home_page.add_child(slider_page)
home_page.add_child(radio_page)
home_page.add_child(checkbox_page)

# --- 步骤 4: 设置页面间的导航回调函数 ---
# 这里我们将主页按钮的点击事件（callback）与 UIManager 的导航方法关联起来。
# 我们现在使用的是 ui_manager.navigate_to_child("页面名称")。
home_btn_manager.buttons[0].callback = lambda: ui_manager.navigate_to_child("switch_demo")
home_btn_manager.buttons[1].callback = lambda: ui_manager.navigate_to_child("slider_demo")
home_btn_manager.buttons[2].callback = lambda: ui_manager.navigate_to_child("radio_demo")
home_btn_manager.buttons[3].callback = lambda: ui_manager.navigate_to_child("checkbox_demo")

# 对于返回按钮，我们使用 go_back() 方法。
# 这个方法会利用 UIManager 内置的导航历史记录返回到上一个访问的页面。
back_button.callback = lambda: ui_manager.go_back()

# --- 步骤 5: 设置根页面，启动UI管理器 ---
# 在所有页面和导航规则设置完毕后，我们通过 set_root_page() 告诉 UIManager
# 哪个页面是应用程序的入口。管理器将从这个页面开始运行和显示。
ui_manager.set_root_page(home_page)

# ==========================================================
# 5. 主循环
# ==========================================================
while not app.need_exit():
    img = cam.read()
    ui_manager.update(img)
    disp.show(img)

print("UI Demo finished.")