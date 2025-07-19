from maix import display, camera, app, image, touchscreen
from ui import (Button, ButtonManager, Slider, SliderManager,
                Switch, SwitchManager, Checkbox, CheckboxManager,
                RadioButton, RadioManager)

# ==========================================================
# 1. 全局设置和状态
# ==========================================================
print("Starting comprehensive UI demo with consistent feedback...")
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera(320, 240)
current_page = 'home'

C_WHITE = (255, 255, 255); C_BLACK = (0, 0, 0); C_RED = (200, 30, 30)
C_BLUE = (0, 120, 220); C_GREEN = (30, 200, 30); C_YELLOW = (220, 220, 30)
C_GRAY = (100, 100, 100); C_STATUS_ON = (30, 200, 30); C_STATUS_OFF = (80, 80, 80)

app_state = {
    'slider_color': 128, 'radio_choice': 'B',
    'checkboxes': {'A': False, 'B': True, 'C': False},
    'switches': {'small': False, 'medium': True, 'large': False}
}

# ==========================================================
# 2. 页面切换和回调函数
# ==========================================================
def set_page(page_name):
    def inner_callback(): global current_page; current_page = page_name; print(f"Switching to page: {page_name}")
    return inner_callback

def slider_callback(value): app_state['slider_color'] = value
def radio_callback(value): app_state['radio_choice'] = value
def create_checkbox_callback(key):
    def inner_callback(is_checked): app_state['checkboxes'][key] = is_checked; print(f"Checkbox '{key}' state: {is_checked}")
    return inner_callback

# --- 开关的回调函数 ---
def create_switch_callback(key):
    def inner_callback(is_on):
        app_state['switches'][key] = is_on
        print(f"Switch '{key}' state: {is_on}")
    return inner_callback

# ==========================================================
# 3. UI 组件和管理器初始化
# ==========================================================
back_button = Button(
    rect=[0, 0, 30, 30], label='<', callback=set_page('home'),
    bg_color=C_BLACK, pressed_color=None, text_color=C_WHITE,
    border_thickness=0, text_scale=1.0
)
home_btn_manager = ButtonManager(ts, disp)
home_btn_manager.add_button(Button(rect=[30, 30, 120, 80], label="Switch", callback=set_page('switch_page'), bg_color=None, pressed_color=None, border_color=C_WHITE, text_color=C_WHITE, text_scale=0.8))
home_btn_manager.add_button(Button(rect=[170, 30, 120, 80], label="Slider", callback=set_page('slider_page'), bg_color=C_RED, pressed_color=C_BLUE, border_thickness=0, text_scale=1.0))
home_btn_manager.add_button(Button(rect=[30, 130, 120, 80], label="Radio", callback=set_page('radio_page'), bg_color=C_YELLOW, pressed_color=C_GRAY, border_color=C_GREEN, text_scale=1.2))
home_btn_manager.add_button(Button(rect=[170, 130, 120, 80], label="Checkbox", callback=set_page('checkbox_page'), bg_color=C_GREEN, pressed_color=C_GRAY, border_color=C_YELLOW, text_scale=1.4))

# --- 开关页面 ---
switch_page_manager = SwitchManager(ts, disp)
switch_page_manager.add_switch(Switch(position=[40, 50], scale=0.8, is_on=app_state['switches']['small'], callback=create_switch_callback('small')))
switch_page_manager.add_switch(Switch(position=[40, 100], scale=1.0, is_on=app_state['switches']['medium'], callback=create_switch_callback('medium')))
switch_page_manager.add_switch(Switch(position=[40, 160], scale=1.5, is_on=app_state['switches']['large'], callback=create_switch_callback('large')))

# --- 滑块页面 ---
slider_page_manager = SliderManager(ts, disp)
slider_page_manager.add_slider(Slider(rect=[60, 130, 200, 20], label="Color Value", default_val=app_state['slider_color'], scale=1.0, min_val=0, max_val=255, callback=slider_callback))

# --- 单选框页面 ---
radio_page_manager = RadioManager(ts, disp, default_value=app_state['radio_choice'], callback=radio_callback)
radio_page_manager.add_radio(RadioButton(position=[40, 60], label="Option A", value="A"))
radio_page_manager.add_radio(RadioButton(position=[40, 110], label="Option B", value="B"))
radio_page_manager.add_radio(RadioButton(position=[40, 160], label="Option C", value="C"))

# --- 复选框页面 ---
checkbox_page_manager = CheckboxManager(ts, disp)
checkbox_page_manager.add_checkbox(Checkbox(position=[40, 50], label="Small", scale=0.8, is_checked=app_state['checkboxes']['A'], callback=create_checkbox_callback('A')))
checkbox_page_manager.add_checkbox(Checkbox(position=[40, 100], label="Medium", scale=1.0, is_checked=app_state['checkboxes']['B'], callback=create_checkbox_callback('B')))
checkbox_page_manager.add_checkbox(Checkbox(position=[40, 160], label="Large", scale=1.5, is_checked=app_state['checkboxes']['C'], callback=create_checkbox_callback('C')))

# 预创建颜色对象
title_color = image.Color.from_rgb(*C_WHITE)
status_on_color = image.Color.from_rgb(*C_STATUS_ON)
status_off_color = image.Color.from_rgb(*C_STATUS_OFF)

# ==========================================================
# 4. 主循环
# ==========================================================
while not app.need_exit():
    img = cam.read()
    if current_page == 'home':
        img.draw_string(10, 5, "UI Demo Home", scale=1.5, color=title_color)
        home_btn_manager.handle_events(img)
    else:
        x_touch, y_touch, pressed_touch = ts.read()
        img_w, img_h = img.width(), img.height()
        disp_w, disp_h = disp.width(), disp.height()
        back_button.handle_event(x_touch, y_touch, pressed_touch, img_w, img_h, disp_w, disp_h)
        back_button.draw(img)

        if current_page == 'switch_page':
            img.draw_string(40, 5, "Switch Demo", scale=1.5, color=title_color)
            
            # --- FEEDBACK LOGIC FOR SWITCHES ---
            status_x = 220
            img.draw_string(status_x, 30, "Status", scale=1.0, color=title_color)
            color_s = status_on_color if app_state['switches']['small'] else status_off_color
            img.draw_rect(status_x, 50, 30, 20, color=color_s, thickness=-1)
            color_m = status_on_color if app_state['switches']['medium'] else status_off_color
            img.draw_rect(status_x, 100, 30, 20, color=color_m, thickness=-1)
            color_l = status_on_color if app_state['switches']['large'] else status_off_color
            img.draw_rect(status_x, 160, 30, 20, color=color_l, thickness=-1)

            switch_page_manager.handle_events(img)

        elif current_page == 'slider_page':
            img.draw_string(40, 5, "Slider Demo", scale=1.5, color=title_color)
            color_val = app_state['slider_color']
            preview_color = image.Color.from_rgb(color_val, color_val, color_val)
            img.draw_rect(140, 40, 40, 40, color=preview_color, thickness=-1)
            slider_page_manager.handle_events(img)

        elif current_page == 'radio_page':
            img.draw_string(40, 5, "Radio Button Demo", scale=1.5, color=title_color)
            img.draw_string(200, 110, f"Selected: {app_state['radio_choice']}", color=title_color)
            radio_page_manager.handle_events(img)

        elif current_page == 'checkbox_page':
            img.draw_string(40, 5, "Checkbox Demo", scale=1.5, color=title_color)
            status_x = 260
            img.draw_string(status_x, 30, "Status", scale=1.0, color=title_color)
            color_a = status_on_color if app_state['checkboxes']['A'] else status_off_color
            img.draw_rect(status_x, 55, 30, 20, color=color_a, thickness=-1)
            color_b = status_on_color if app_state['checkboxes']['B'] else status_off_color
            img.draw_rect(status_x, 105, 30, 20, color=color_b, thickness=-1)
            color_c = status_on_color if app_state['checkboxes']['C'] else status_off_color
            img.draw_rect(status_x, 160, 30, 20, color=color_c, thickness=-1)
            checkbox_page_manager.handle_events(img)

    disp.show(img)

print("UI Demo finished.")