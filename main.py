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
# cam = camera.Camera(320, 240)
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
def slider_callback(value): app_state['slider_color'] = value
def radio_callback(value): app_state['radio_choice'] = value
def create_checkbox_callback(key):
    def inner_callback(is_checked): app_state['checkboxes'][key] = is_checked; print(f"Checkbox '{key}' state: {is_checked}")
    return inner_callback
def create_switch_callback(key):
    def inner_callback(is_on): app_state['switches'][key] = is_on; print(f"Switch '{key}' state: {is_on}")
    return inner_callback

back_button = Button(rect=adapter.scale_rect([0, 0, 30, 30]), label='<', callback=None, bg_color=C_BLACK, pressed_color=None, text_color=C_WHITE, border_thickness=0, text_scale=adapter.scale_value(1.0))

home_btn_manager = ButtonManager(ts, disp)
home_btn_manager.add_button(Button(rect=adapter.scale_rect([30, 30, 120, 80]), label="Switch", callback=None, bg_color=None, pressed_color=None, border_color=C_WHITE, text_color=C_WHITE, border_thickness=int(adapter.scale_value(2)), text_scale=adapter.scale_value(0.8)))
home_btn_manager.add_button(Button(rect=adapter.scale_rect([170, 30, 120, 80]), label="Slider", callback=None, bg_color=C_RED, pressed_color=C_BLUE, border_thickness=0, text_scale=adapter.scale_value(1.0)))
home_btn_manager.add_button(Button(rect=adapter.scale_rect([30, 130, 120, 80]), label="Radio", callback=None, bg_color=C_YELLOW, pressed_color=C_GRAY, border_color=C_GREEN, border_thickness=int(adapter.scale_value(2)), text_scale=adapter.scale_value(1.2)))
home_btn_manager.add_button(Button(rect=adapter.scale_rect([170, 130, 120, 80]), label="Checkbox", callback=None, bg_color=C_GREEN, pressed_color=C_GRAY, border_color=C_YELLOW, border_thickness=int(adapter.scale_value(2)), text_scale=adapter.scale_value(1.4)))

# --- 开关页面 ---
switch_page_manager = SwitchManager(ts, disp)
switch_page_manager.add_switch(Switch(position=adapter.scale_position(40, 50), scale=adapter.scale_value(0.8), is_on=app_state['switches']['small'], callback=create_switch_callback('small')))
switch_page_manager.add_switch(Switch(position=adapter.scale_position(40, 100), scale=adapter.scale_value(1.0), is_on=app_state['switches']['medium'], callback=create_switch_callback('medium')))
switch_page_manager.add_switch(Switch(position=adapter.scale_position(40, 160), scale=adapter.scale_value(1.5), is_on=app_state['switches']['large'], callback=create_switch_callback('large')))

# --- 滑块页面 ---
slider_page_manager = SliderManager(ts, disp)
slider_page_manager.add_slider(Slider(rect=adapter.scale_rect([60, 130, 200, 20]), label="Color Value", default_val=app_state['slider_color'], scale=adapter.scale_value(1.0), min_val=0, max_val=255, callback=slider_callback))

# --- 单选框页面 ---
radio_page_manager = RadioManager(ts, disp, default_value=app_state['radio_choice'], callback=radio_callback)
radio_page_manager.add_radio(RadioButton(position=adapter.scale_position(40, 60), label="Option A", value="A", scale=adapter.scale_value(1.0)))
radio_page_manager.add_radio(RadioButton(position=adapter.scale_position(40, 110), label="Option B", value="B", scale=adapter.scale_value(1.0)))
radio_page_manager.add_radio(RadioButton(position=adapter.scale_position(40, 160), label="Option C", value="C", scale=adapter.scale_value(1.0)))

# --- 复选框页面 ---
checkbox_page_manager = CheckboxManager(ts, disp)
checkbox_page_manager.add_checkbox(Checkbox(position=adapter.scale_position(40, 50), label="Small", scale=adapter.scale_value(0.8), is_checked=app_state['checkboxes']['A'], callback=create_checkbox_callback('A')))
checkbox_page_manager.add_checkbox(Checkbox(position=adapter.scale_position(40, 100), label="Medium", scale=adapter.scale_value(1.0), is_checked=app_state['checkboxes']['B'], callback=create_checkbox_callback('B')))
checkbox_page_manager.add_checkbox(Checkbox(position=adapter.scale_position(40, 160), label="Large", scale=adapter.scale_value(1.5), is_checked=app_state['checkboxes']['C'], callback=create_checkbox_callback('C')))

# 预创建颜色对象
title_color = image.Color.from_rgb(*C_WHITE)
status_on_color = image.Color.from_rgb(*C_STATUS_ON)
status_off_color = image.Color.from_rgb(*C_STATUS_OFF)

# ==========================================================
# 3. 定义页面类
# ==========================================================
# 优雅地封装到独立的页面类中。每个类负责一个界面的所有绘制和事件处理。

# --- 创建一个通用的“子页面”基类 ---
# 这个类的目的是为了代码复用。
# 所有需要“返回”按钮的页面都可以继承它而不必重复编写处理返回按钮的代码。
class SubPage(Page):
    """
    一个通用的子页面基类，它自动处理“返回”按钮的逻辑
    """
    def handle_back_button(self, img):
        """
        处理和绘制全局的“返回”按钮。
        这个方法应该在所有子页面的 update 方法中被首先调用。
        """
        # 读取当前的触摸事件。注意：每个管理器内部也会读取。
        x_touch, y_touch, pressed_touch = ts.read()
        
        # 获取图像和真实屏幕的尺寸，用于坐标映射。
        img_w, img_h = img.width(), img.height()
        disp_w_actual, disp_h_actual = disp.width(), disp.height()

        # 调用全局 back_button 实例的 handle_event 方法。
        # 它需要知道触摸坐标、画布尺寸和屏幕尺寸，来判断点击是否命中。
        back_button.handle_event(x_touch, y_touch, pressed_touch, img_w, img_h, disp_w_actual, disp_h_actual)
        
        # 将返回按钮绘制到图像上。
        back_button.draw(img)

# --- 主页 ---
class HomePage(Page):
    """
    主页
    """
    def update(self, img):
        """
        HomePage 的核心更新逻辑
        :param img: 当前帧的图像，作为绘制的画布。
        """
        # 1. 绘制此页面的特定内容
        x, y = adapter.scale_position(10, 5)
        img.draw_string(x, y, "UI Demo Home", scale=adapter.scale_value(1.5), color=title_color)
        
        # 2. 调用此页面专属的UI管理器，让它处理自己的按钮
        home_btn_manager.handle_events(img)

# --- 开关页面 ---
class SwitchPage(SubPage):
    """
    开关(Switch)组件的演示页面
    """
    def update(self, img):
        # 1. 首先，调用父类的方法来处理通用的返回按钮
        self.handle_back_button(img)
        
        # 2. 绘制此页面的特定内容
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Switch Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        # 绘制状态反馈矩形
        x_status, y_status = adapter.scale_position(220, 30)
        img.draw_string(x_status, y_status, "Status", scale=adapter.scale_value(1.0), color=title_color)
        colors = [status_on_color if app_state['switches'][k] else status_off_color for k in ['small', 'medium', 'large']]
        rects = [adapter.scale_rect(r) for r in [[220, 50, 30, 20], [220, 100, 30, 20], [220, 160, 30, 20]]]
        for r, c in zip(rects, colors): img.draw_rect(*r, color=c, thickness=-1)
        
        # 3. 调用此页面专属的 SwitchManager 来处理所有开关组件
        switch_page_manager.handle_events(img)

# --- 滑块页面 ---
class SliderPage(SubPage):
    """
    滑块(Slider)组件的演示页面
    """
    def update(self, img):
        # 1. 处理通用的返回按钮
        self.handle_back_button(img)
        
        # 2. 绘制此页面的特定内容
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Slider Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        # 根据全局状态 `app_state` 绘制颜色预览方块
        color_val = app_state['slider_color']
        preview_color = image.Color.from_rgb(color_val, color_val, color_val)
        x_rect, y_rect, w_rect, h_rect = adapter.scale_rect([140, 40, 40, 40])
        img.draw_rect(x_rect, y_rect, w_rect, h_rect, color=preview_color, thickness=-1)
        
        # 3. 调用 SliderManager 来处理滑块
        slider_page_manager.handle_events(img)

# --- 单选框页面 ---
class RadioPage(SubPage):
    """
    单选框(RadioButton)组件的演示页面
    """
    def update(self, img):
        # 1. 处理通用的返回按钮
        self.handle_back_button(img)
        
        # 2. 绘制此页面的特定内容
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Radio Button Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        # 显示当前被选中的选项
        x_text, y_text = adapter.scale_position(200, 110)
        img.draw_string(x_text, y_text, f"Selected: {app_state['radio_choice']}", color=title_color, scale=adapter.scale_value(1.0))
        
        # 3. 调用 RadioManager 来处理单选框组
        radio_page_manager.handle_events(img)

# --- 复选框页面 ---
class CheckboxPage(SubPage):
    """
    复选框(Checkbox)组件的演示页面
    """
    def update(self, img):
        # 1. 处理通用的返回按钮
        self.handle_back_button(img)
        
        # 2. 绘制此页面的特定内容
        x, y = adapter.scale_position(40, 5)
        img.draw_string(x, y, "Checkbox Demo", scale=adapter.scale_value(1.5), color=title_color)
        
        # 绘制状态反馈矩形
        status_x = 260
        x_status, y_status = adapter.scale_position(status_x, 30)
        img.draw_string(x_status, y_status, "Status", scale=adapter.scale_value(1.0), color=title_color)
        colors = [status_on_color if app_state['checkboxes'][k] else status_off_color for k in ['A', 'B', 'C']]
        rects = [adapter.scale_rect(r) for r in [[status_x, 50, 30, 20], [status_x, 105, 30, 20], [status_x, 160, 30, 20]]]
        for r, c in zip(rects, colors): img.draw_rect(*r, color=c, thickness=-1)
        
        # 3. 调用 CheckboxManager 来处理所有复选框
        checkbox_page_manager.handle_events(img)

# ==========================================================
# 4. 初始化页面管理器和页面
# ==========================================================
# 在定义了所有页面类之后，我们需要在这里将它们实例化，并设置好页面之间的“导航”规则。

# --- 步骤 1: 创建一个全局的页面管理器实例 ---
# UIManager 是我们整个UI导航系统的大脑，它将负责跟踪哪个页面是当前活动的。
ui_manager = UIManager()

# --- 步骤 2: 将之前定义的页面类实例化为具体的页面对象 ---
# 我们为每个页面类创建一个对象。每个对象都持有一个对 ui_manager 的引用。
home_page = HomePage(ui_manager)
switch_page = SwitchPage(ui_manager)
slider_page = SliderPage(ui_manager)
radio_page = RadioPage(ui_manager)
checkbox_page = CheckboxPage(ui_manager)

# --- 步骤 3: 设置页面间的导航回调函数 ---
# 这是将所有部分连接起来的关键一步。我们在这里为之前创建的按钮动态地分配行为。
# 我们通过访问 `home_btn_manager.buttons` 列表来获取之前添加的按钮。

# 将主页的 Switch 按钮的点击事件设置为推入“开关页面”
home_btn_manager.buttons[0].callback = lambda: ui_manager.push(switch_page)

# 将主页的 Slider 按钮的点击事件设置为推入“滑块页面”
home_btn_manager.buttons[1].callback = lambda: ui_manager.push(slider_page)

# 将主页的 Radio 按钮的点击事件设置为推入“单选框页面”
home_btn_manager.buttons[2].callback = lambda: ui_manager.push(radio_page)

# 将主页的 Checkbox 按钮的点击事件设置为推入“复选框页面”
home_btn_manager.buttons[3].callback = lambda: ui_manager.push(checkbox_page)

# 将全局的返回按钮的点击事件设置为弹出当前页面，返回到上一页
back_button.callback = lambda: ui_manager.pop()

# --- 步骤 4: 推入初始页面 ---
# 应用程序启动时，将主页 `home_page` 推入栈中，使其成为第一个活动页面。
ui_manager.push(home_page)

# ==========================================================
# 5. 主循环
# ==========================================================
while not app.need_exit():
    img = cam.read()
    ui_manager.update(img)
    disp.show(img)

print("UI Demo finished.")