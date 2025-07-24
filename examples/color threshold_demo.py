from maix import camera, image, touchscreen, display
import cv2
import numpy as np
from maixpy_ui import Page, UIManager, Button, ButtonManager, Slider, SliderManager, Switch, SwitchManager, ResolutionAdapter

class ColorMode:
    HSV = 0
    LAB = 1

class ValueMode:
    Min = 0
    Max = 1

class MainMenuPage(Page):
    """主菜单页面"""
    
    def __init__(self, ui_manager, ts, disp, name="main_menu"):
        super().__init__(ui_manager, name)
        
        # 使用传入的硬件设备实例
        self.ts = ts
        self.disp = disp
        
        # 分辨率适配器
        self.adapter = ResolutionAdapter(
            self.disp.width(), self.disp.height(), 640, 480)
        
        # 创建组件管理器
        self.button_manager = ButtonManager(self.ts, self.disp)
        
        # UI组件
        self.buttons = {}
        
        # 初始化UI
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI组件"""
        button_height = 80
        button_width = 200
        start_y = 100
        spacing = 20
        
        # 颜色阈值调整按钮
        self.buttons['threshold'] = Button(
            rect=self.adapter.scale_rect([220, start_y, button_width, button_height]),
            label="Color Threshold",
            callback=lambda: self.ui_manager.navigate_to_child("threshold"),
            text_scale=1.2
        )
        self.button_manager.add_button(self.buttons['threshold'])
        
        # 设置页面按钮
        self.buttons['settings'] = Button(
            rect=self.adapter.scale_rect([220, start_y + button_height + spacing, button_width, button_height]),
            label="Settings",
            callback=lambda: self.ui_manager.navigate_to_child("settings"),
            text_scale=1.2
        )
        self.button_manager.add_button(self.buttons['settings'])
        
        # 帮助页面按钮
        self.buttons['help'] = Button(
            rect=self.adapter.scale_rect([220, start_y + 2*(button_height + spacing), button_width, button_height]),
            label="Help",
            callback=lambda: self.ui_manager.navigate_to_child("help"),
            text_scale=1.2
        )
        self.button_manager.add_button(self.buttons['help'])
    
    def on_enter(self):
        """进入主菜单时的处理"""
        print("Entered Main Menu")
    
    def update(self, img_buffer):
        """页面更新函数"""
        # 创建背景图像
        img_buffer.draw_rect(0, 0, 640, 480, image.COLOR_BLACK, -1)
        
        # 绘制标题
        img_buffer.draw_string(200, 30, "Vision Tool Menu", image.COLOR_WHITE, scale=2.0)
        
        # 显示当前路径信息
        path_str = " -> ".join(self.get_path()) if self.get_path() else "Root"
        img_buffer.draw_string(10, 10, f"Path: {path_str}", image.COLOR_GRAY, scale=1.0)
        
        # 处理UI组件
        self.button_manager.handle_events(img_buffer)
        
        # 显示图像
        self.disp.show(img_buffer)


class SettingsPage(Page):
    """设置页面"""
    
    def __init__(self, ui_manager, ts, disp, name="settings"):
        super().__init__(ui_manager, name)
        
        self.ts = ts
        self.disp = disp
        
        self.adapter = ResolutionAdapter(
            self.disp.width(), self.disp.height(), 640, 480)
        
        self.button_manager = ButtonManager(self.ts, self.disp)
        self.slider_manager = SliderManager(self.ts, self.disp)
        self.switch_manager = SwitchManager(self.ts, self.disp)
        
        # 设置状态
        self.settings = {
            'brightness': 50,
            'contrast': 50,
            'auto_save': False,
            'debug_mode': False
        }
        
        self.buttons = {}
        self.sliders = {}
        self.switches = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI组件"""
        # 返回按钮
        self.buttons['back'] = Button(
            rect=self.adapter.scale_rect([10, 10, 80, 40]),
            label="Back",
            callback=lambda: self.ui_manager.navigate_to_parent(),
            text_scale=1.0
        )
        self.button_manager.add_button(self.buttons['back'])
        
        # 亮度滑动条
        self.sliders['brightness'] = Slider(
            rect=self.adapter.scale_rect([200, 100, 300, 30]),
            scale=self.adapter.scale_value(1.0),
            min_val=0,
            max_val=100,
            default_val=self.settings['brightness'],
            callback=lambda value: self._on_brightness_changed(value),
            label="Brightness"
        )
        self.slider_manager.add_slider(self.sliders['brightness'])
        
        # 对比度滑动条
        self.sliders['contrast'] = Slider(
            rect=self.adapter.scale_rect([200, 150, 300, 30]),
            scale=self.adapter.scale_value(1.0),
            min_val=0,
            max_val=100,
            default_val=self.settings['contrast'],
            callback=lambda value: self._on_contrast_changed(value),
            label="Contrast"
        )
        self.slider_manager.add_slider(self.sliders['contrast'])
        
        # 自动保存开关
        self.switches['auto_save'] = Switch(
            position=self.adapter.scale_position(150, 200),
            scale=self.adapter.scale_value(1.0),
            is_on=self.settings['auto_save'],
            callback=lambda state: self._on_auto_save_changed(state)
        )
        self.switch_manager.add_switch(self.switches['auto_save'])
        
        # 调试模式开关
        self.switches['debug'] = Switch(
            position=self.adapter.scale_position(150, 250),
            scale=self.adapter.scale_value(1.0),
            is_on=self.settings['debug_mode'],
            callback=lambda state: self._on_debug_changed(state)
        )
        self.switch_manager.add_switch(self.switches['debug'])
    
    def _on_brightness_changed(self, value):
        self.settings['brightness'] = value
    
    def _on_contrast_changed(self, value):
        self.settings['contrast'] = value
    
    def _on_auto_save_changed(self, state):
        self.settings['auto_save'] = state
    
    def _on_debug_changed(self, state):
        self.settings['debug_mode'] = state
    
    def on_enter(self):
        print("Entered Settings Page")
    
    def update(self, img_buffer):
        """页面更新函数"""
        img_buffer.draw_rect(0, 0, 640, 480, image.COLOR_BLACK, -1)
        
        # 绘制标题
        img_buffer.draw_string(250, 30, "Settings", image.COLOR_WHITE, scale=1.8)
        
        # 显示当前路径
        path_str = " -> ".join(self.get_path())
        img_buffer.draw_string(10, 450, f"Path: {path_str}", image.COLOR_GRAY, scale=0.8)
        
        # 绘制标签
        img_buffer.draw_string(50, 210, "Auto Save:", image.COLOR_WHITE, scale=1.2)
        img_buffer.draw_string(50, 260, "Debug Mode:", image.COLOR_WHITE, scale=1.2)
        
        # 显示当前设置值
        img_buffer.draw_string(400, 350, f"Brightness: {self.settings['brightness']}", 
                              image.COLOR_GREEN, scale=1.0)
        img_buffer.draw_string(400, 370, f"Contrast: {self.settings['contrast']}", 
                              image.COLOR_GREEN, scale=1.0)
        img_buffer.draw_string(400, 390, f"Auto Save: {'ON' if self.settings['auto_save'] else 'OFF'}", 
                              image.COLOR_GREEN, scale=1.0)
        img_buffer.draw_string(400, 410, f"Debug: {'ON' if self.settings['debug_mode'] else 'OFF'}", 
                              image.COLOR_GREEN, scale=1.0)
        
        # 处理UI组件
        self.button_manager.handle_events(img_buffer)
        self.slider_manager.handle_events(img_buffer)
        self.switch_manager.handle_events(img_buffer)
        
        self.disp.show(img_buffer)


class HelpPage(Page):
    """帮助页面"""
    
    def __init__(self, ui_manager, ts, disp, name="help"):
        super().__init__(ui_manager, name)
        
        self.ts = ts
        self.disp = disp
        
        self.adapter = ResolutionAdapter(
            self.disp.width(), self.disp.height(), 640, 480)
        
        self.button_manager = ButtonManager(self.ts, self.disp)
        self.buttons = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI组件"""
        # 返回按钮
        self.buttons['back'] = Button(
            rect=self.adapter.scale_rect([10, 10, 80, 40]),
            label="Back",
            callback=lambda: self.ui_manager.navigate_to_parent(),
            text_scale=1.0
        )
        self.button_manager.add_button(self.buttons['back'])
        
        # 返回主菜单按钮
        self.buttons['home'] = Button(
            rect=self.adapter.scale_rect([100, 10, 80, 40]),
            label="Home",
            callback=lambda: self.ui_manager.navigate_to_root(),
            text_scale=1.0
        )
        self.button_manager.add_button(self.buttons['home'])
    
    def on_enter(self):
        print("Entered Help Page")
    
    def update(self, img_buffer):
        """页面更新函数"""
        img_buffer.draw_rect(0, 0, 640, 480, image.COLOR_BLACK, -1)
        
        # 绘制标题
        img_buffer.draw_string(280, 30, "Help", image.COLOR_WHITE, scale=1.8)
        
        # 显示当前路径
        path_str = " -> ".join(self.get_path())
        img_buffer.draw_string(10, 450, f"Path: {path_str}", image.COLOR_GRAY, scale=0.8)
        
        # 显示深度信息
        img_buffer.draw_string(10, 430, f"Depth: {self.get_depth()}", image.COLOR_GRAY, scale=0.8)
        
        # 帮助内容
        help_text = [
            "Vision Tool Help",
            "",
            "Color Threshold:",
            "- Switch between LAB/HSV modes",
            "- Adjust min/max values for each channel",
            "- Toggle binary view",
            "",
            "Settings:",
            "- Adjust brightness and contrast",
            "- Enable/disable auto save",
            "- Toggle debug mode",
            "",
            "Navigation:",
            "- Use Back button to return",
            "- Use Home button to go to main menu"
        ]
        
        y_pos = 80
        for line in help_text:
            if line == "":
                y_pos += 10
            else:
                scale = 1.2 if line.endswith(":") else 1.0
                color = image.COLOR_YELLOW if line.endswith(":") else image.COLOR_WHITE
                img_buffer.draw_string(50, y_pos, line, color, scale=scale)
                y_pos += 20
        
        # 处理UI组件
        self.button_manager.handle_events(img_buffer)
        
        self.disp.show(img_buffer)


class ColorThresholdPage(Page):
    """颜色阈值调整页面"""
    
    def __init__(self, ui_manager, ts, disp, name="threshold"):
        super().__init__(ui_manager, name)
        
        # 初始化硬件设备 - 只有摄像头需要在这个页面单独创建
        self.cam = camera.Camera(640, 480)
        self.ts = ts
        self.disp = disp
        
        # 分辨率适配器
        self.adapter = ResolutionAdapter(
            self.disp.width(), self.disp.height(), 640, 480)
        
        # 创建组件管理器
        self.button_manager = ButtonManager(self.ts, self.disp)
        self.slider_manager = SliderManager(self.ts, self.disp)
        self.switch_manager = SwitchManager(self.ts, self.disp)
        
        # 应用状态
        self.context = {
            'color_mode': ColorMode.LAB,
            'value_mode': ValueMode.Min,
            'current_ch': 1,
            'disp_binary': False,
            'threshold_lab': [0, 100, -128, 127, -128, 127],
            'threshold_hsv': [0, 180, 0, 255, 0, 255]
        }
        
        # UI组件
        self.buttons = {}
        self.sliders = {}
        self.switches = {}
        
        # 初始化UI
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI组件"""
        # 按钮尺寸计算
        button_height = 480 // 7  # 为返回按钮留出空间
        button_width = 80
        
        # 返回按钮
        self.buttons['back'] = Button(
            rect=self.adapter.scale_rect([0, 0, button_width, button_height//2]),
            label="Back",
            callback=lambda: self.ui_manager.navigate_to_parent(),
            text_scale=0.8
        )
        self.button_manager.add_button(self.buttons['back'])
        
        # 模式切换按钮
        self.buttons['mode'] = Button(
            rect=self.adapter.scale_rect([0, button_height//2, button_width, button_height]),
            label="LAB",
            callback=lambda: self._on_mode_button_pressed(),
            text_scale=1.0
        )
        self.button_manager.add_button(self.buttons['mode'])
        
        # 通道按钮
        self.buttons['ch1'] = Button(
            rect=self.adapter.scale_rect([0, button_height//2 + button_height, button_width, button_height]),
            label="L Min",
            callback=lambda: self._on_ch1_button_pressed(),
            text_scale=1.0
        )
        self.button_manager.add_button(self.buttons['ch1'])
        
        self.buttons['ch2'] = Button(
            rect=self.adapter.scale_rect([0, button_height//2 + 2*button_height, button_width, button_height]),
            label="A Min",
            callback=lambda: self._on_ch2_button_pressed(),
            text_scale=1.0
        )
        self.button_manager.add_button(self.buttons['ch2'])
        
        self.buttons['ch3'] = Button(
            rect=self.adapter.scale_rect([0, button_height//2 + 3*button_height, button_width, button_height]),
            label="B Min",
            callback=lambda: self._on_ch3_button_pressed(),
            text_scale=1.0
        )
        self.button_manager.add_button(self.buttons['ch3'])
        
        # 二值化开关
        self.switches['binary'] = Switch(
            position=self.adapter.scale_position(5, button_height//2 + 4*button_height + 15),
            scale=self.adapter.scale_value(1.0),
            callback=lambda state: self._on_binary_switch_changed(state)
        )
        self.switch_manager.add_switch(self.switches['binary'])
        
        # 滑动条
        self.sliders['threshold'] = Slider(
            rect=self.adapter.scale_rect([100, 420, 400, 40]),
            scale=self.adapter.scale_value(1.0),
            min_val=0,
            max_val=100,
            default_val=0,
            callback=lambda value: self._on_slider_changed(value),
            label="L Min"
        )
        self.slider_manager.add_slider(self.sliders['threshold'])
    
    def _on_mode_button_pressed(self):
        """模式按钮回调"""
        if self.context['color_mode'] == ColorMode.LAB:
            self.context['color_mode'] = ColorMode.HSV
            self.buttons['mode'].label = 'HSV'
            self.buttons['ch1'].label = 'H Min'
            self.buttons['ch2'].label = 'S Min'
            self.buttons['ch3'].label = 'V Min'
            self.sliders['threshold'].label = 'H Min'
        else:
            self.context['color_mode'] = ColorMode.LAB
            self.buttons['mode'].label = 'LAB'
            self.buttons['ch1'].label = 'L Min'
            self.buttons['ch2'].label = 'A Min'
            self.buttons['ch3'].label = 'B Min'
            self.sliders['threshold'].label = 'L Min'
        
        self.context['current_ch'] = 1
        self.context['value_mode'] = ValueMode.Min
        self._update_slider_value()
    
    def _on_ch1_button_pressed(self):
        """通道1按钮回调"""
        self.context['current_ch'] = 1
        if self.context['value_mode'] == ValueMode.Min:
            self.context['value_mode'] = ValueMode.Max
            if self.context['color_mode'] == ColorMode.LAB:
                self.buttons['ch1'].label = 'L Max'
                self.sliders['threshold'].label = 'L Max'
            else:
                self.buttons['ch1'].label = 'H Max'
                self.sliders['threshold'].label = 'H Max'
        else:
            self.context['value_mode'] = ValueMode.Min
            if self.context['color_mode'] == ColorMode.LAB:
                self.buttons['ch1'].label = 'L Min'
                self.sliders['threshold'].label = 'L Min'
            else:
                self.buttons['ch1'].label = 'H Min'
                self.sliders['threshold'].label = 'H Min'
        self._update_slider_value()
    
    def _on_ch2_button_pressed(self):
        """通道2按钮回调"""
        self.context['current_ch'] = 2
        if self.context['value_mode'] == ValueMode.Min:
            self.context['value_mode'] = ValueMode.Max
            if self.context['color_mode'] == ColorMode.LAB:
                self.buttons['ch2'].label = 'A Max'
                self.sliders['threshold'].label = 'A Max'
            else:
                self.buttons['ch2'].label = 'S Max'
                self.sliders['threshold'].label = 'S Max'
        else:
            self.context['value_mode'] = ValueMode.Min
            if self.context['color_mode'] == ColorMode.LAB:
                self.buttons['ch2'].label = 'A Min'
                self.sliders['threshold'].label = 'A Min'
            else:
                self.buttons['ch2'].label = 'S Min'
                self.sliders['threshold'].label = 'S Min'
        self._update_slider_value()
    
    def _on_ch3_button_pressed(self):
        """通道3按钮回调"""
        self.context['current_ch'] = 3
        if self.context['value_mode'] == ValueMode.Min:
            self.context['value_mode'] = ValueMode.Max
            if self.context['color_mode'] == ColorMode.LAB:
                self.buttons['ch3'].label = 'B Max'
                self.sliders['threshold'].label = 'B Max'
            else:
                self.buttons['ch3'].label = 'V Max'
                self.sliders['threshold'].label = 'V Max'
        else:
            self.context['value_mode'] = ValueMode.Min
            if self.context['color_mode'] == ColorMode.LAB:
                self.buttons['ch3'].label = 'B Min'
                self.sliders['threshold'].label = 'B Min'
            else:
                self.buttons['ch3'].label = 'V Min'
                self.sliders['threshold'].label = 'V Min'
        self._update_slider_value()
    
    def _on_binary_switch_changed(self, state):
        """二值化开关回调"""
        self.context['disp_binary'] = state
    
    def _on_slider_changed(self, value):
        """滑动条回调"""
        if self.context['color_mode'] == ColorMode.LAB:
            if self.context['value_mode'] == ValueMode.Min:
                if self.context['current_ch'] == 1:
                    self.context['threshold_lab'][0] = value
                elif self.context['current_ch'] == 2:
                    self.context['threshold_lab'][2] = int(-128 + value * 255 / 100)
                elif self.context['current_ch'] == 3:
                    self.context['threshold_lab'][4] = int(-128 + value * 255 / 100)
            else:
                if self.context['current_ch'] == 1:
                    self.context['threshold_lab'][1] = value
                elif self.context['current_ch'] == 2:
                    self.context['threshold_lab'][3] = int(-128 + value * 255 / 100)
                elif self.context['current_ch'] == 3:
                    self.context['threshold_lab'][5] = int(-128 + value * 255 / 100)
        else:
            if self.context['value_mode'] == ValueMode.Min:
                if self.context['current_ch'] == 1:
                    self.context['threshold_hsv'][0] = int(value / 100 * 180)
                elif self.context['current_ch'] == 2:
                    self.context['threshold_hsv'][2] = int(value / 100 * 255)
                elif self.context['current_ch'] == 3:
                    self.context['threshold_hsv'][4] = int(value / 100 * 255)
            else:
                if self.context['current_ch'] == 1:
                    self.context['threshold_hsv'][1] = int(value / 100 * 180)
                elif self.context['current_ch'] == 2:
                    self.context['threshold_hsv'][3] = int(value / 100 * 255)
                elif self.context['current_ch'] == 3:
                    self.context['threshold_hsv'][5] = int(value / 100 * 255)
    
    def _update_slider_value(self):
        """更新滑动条的值"""
        if self.context['color_mode'] == ColorMode.LAB:
            if self.context['value_mode'] == ValueMode.Min:
                if self.context['current_ch'] == 1:
                    self.sliders['threshold'].value = self.context['threshold_lab'][0]
                elif self.context['current_ch'] == 2:
                    self.sliders['threshold'].value = int((self.context['threshold_lab'][2] + 128) / 255 * 100)
                elif self.context['current_ch'] == 3:
                    self.sliders['threshold'].value = int((self.context['threshold_lab'][4] + 128) / 255 * 100)
            else:
                if self.context['current_ch'] == 1:
                    self.sliders['threshold'].value = self.context['threshold_lab'][1]
                elif self.context['current_ch'] == 2:
                    self.sliders['threshold'].value = int((self.context['threshold_lab'][3] + 128) / 255 * 100)
                elif self.context['current_ch'] == 3:
                    self.sliders['threshold'].value = int((self.context['threshold_lab'][5] + 128) / 255 * 100)
        else:
            if self.context['value_mode'] == ValueMode.Min:
                if self.context['current_ch'] == 1:
                    self.sliders['threshold'].value = int(self.context['threshold_hsv'][0] / 180 * 100)
                elif self.context['current_ch'] == 2:
                    self.sliders['threshold'].value = int(self.context['threshold_hsv'][2] / 255 * 100)
                elif self.context['current_ch'] == 3:
                    self.sliders['threshold'].value = int(self.context['threshold_hsv'][4] / 255 * 100)
            else:
                if self.context['current_ch'] == 1:
                    self.sliders['threshold'].value = int(self.context['threshold_hsv'][1] / 180 * 100)
                elif self.context['current_ch'] == 2:
                    self.sliders['threshold'].value = int(self.context['threshold_hsv'][3] / 255 * 100)
                elif self.context['current_ch'] == 3:
                    self.sliders['threshold'].value = int(self.context['threshold_hsv'][5] / 255 * 100)
    
    def rgb_to_hsv(self, r, g, b):
        """RGB转HSV"""
        bgr_pixel = np.uint8([[[b, g, r]]])
        hsv_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)
        h, s, v = hsv_pixel[0][0]
        return h, s, v
    
    def rgb_to_lab(self, r, g, b):
        """RGB转LAB"""
        bgr_pixel = np.uint8([[[b, g, r]]])
        lab_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2LAB)
        l, a, b = lab_pixel[0][0]
        l = int(l * (100 / 255))
        a = a - 128
        b = b - 128
        return l, a, b
    
    def on_enter(self):
        """进入页面时的处理"""
        print("Entered Color Threshold Page")
    
    def on_exit(self):
        """退出页面时的处理"""
        print("Exited Color Threshold Page")
    
    def update(self, img_buffer):
        """页面更新函数"""
        # 1. 获取摄像头图像
        img = self.cam.read()
        
        # 2. 根据颜色模式进行阈值处理
        if self.context['color_mode'] == ColorMode.LAB:
            # LAB模式处理
            blobs = img.find_blobs(
                thresholds=[self.context['threshold_lab']], 
                pixels_threshold=500
            )
            for blob in blobs:
                img.draw_rect(blob[0], blob[1], blob[2], blob[3], image.COLOR_BLUE)
            
            if self.context['disp_binary']:
                img = img.binary([self.context['threshold_lab']])
        else:
            # HSV模式处理
            frame = image.image2cv(img, ensure_bgr=False, copy=False)
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            
            lower = np.array([
                self.context['threshold_hsv'][0], 
                self.context['threshold_hsv'][2], 
                self.context['threshold_hsv'][4]
            ])
            upper = np.array([
                self.context['threshold_hsv'][1], 
                self.context['threshold_hsv'][3], 
                self.context['threshold_hsv'][5]
            ])
            mask = cv2.inRange(hsv, lower, upper)
            
            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            if self.context['disp_binary']:
                img = image.cv2image(mask, bgr=False, copy=False)
            else:
                img = image.cv2image(frame, bgr=False, copy=False)
        
        # 3. 显示颜色信息（如果不是二值化模式）
        if not self.context['disp_binary']:
            pixel_x = 640 // 2
            pixel_y = 480 // 2
            pixel = img.get_pixel(pixel_x, pixel_y, True)
            
            if self.context['color_mode'] == ColorMode.LAB:
                value_l, value_a, value_b = self.rgb_to_lab(pixel[0], pixel[1], pixel[2])
                img.draw_string(
                    100, 10, 
                    'Color:{:4d},{:4d},{:4d}'.format(value_l, value_a, value_b), 
                    image.COLOR_BLUE,
                    scale=1.2
                )
                img.draw_string(
                    100, 30, 
                    'Thresh:{:3d},{:3d},{:3d},{:3d},{:3d},{:3d}'.format(
                        self.context['threshold_lab'][0],
                        self.context['threshold_lab'][1], 
                        self.context['threshold_lab'][2],
                        self.context['threshold_lab'][3],
                        self.context['threshold_lab'][4],
                        self.context['threshold_lab'][5]
                    ), 
                    image.COLOR_BLUE,
                    scale=1.0
                )
            else:
                value_h, value_s, value_v = self.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
                img.draw_string(
                    100, 10, 
                    'Color:{:4d},{:4d},{:4d}'.format(value_h, value_s, value_v), 
                    image.COLOR_BLUE,
                    scale=1.2
                )
                img.draw_string(
                    100, 30, 
                    'Thresh:{:3d},{:3d},{:3d},{:3d},{:3d},{:3d}'.format(
                        self.context['threshold_hsv'][0],
                        self.context['threshold_hsv'][1],
                        self.context['threshold_hsv'][2],
                        self.context['threshold_hsv'][3],
                        self.context['threshold_hsv'][4],
                        self.context['threshold_hsv'][5]
                    ), 
                    image.COLOR_BLUE,
                    scale=1.0
                )
            
            img.draw_cross(pixel_x, pixel_y, image.COLOR_BLUE, 8)
        
        # 4. 绘制导航信息
        path_str = " -> ".join(self.get_path())
        img.draw_string(100, 460, f"Path: {path_str}", image.COLOR_GRAY, scale=0.8)
        
        # 5. 处理UI组件事件和绘制
        self.button_manager.handle_events(img)
        self.slider_manager.handle_events(img)
        self.switch_manager.handle_events(img)
        
        # 6. 显示图像
        self.disp.show(img)


def main():
    """主函数"""
    print("=== Vision Tool Started ===")
    print("Initializing hardware...")
    
    try:
        # 首先初始化硬件设备（单例模式）
        ts = touchscreen.TouchScreen()
        disp = display.Display()
        print(f"Display initialized: {disp.width()}x{disp.height()}")
        
        # 创建UI管理器
        ui_manager = UIManager()
        
        # 创建主菜单页面（根页面）
        main_menu = MainMenuPage(ui_manager, ts, disp, "main_menu")
        
        # 创建子页面
        threshold_page = ColorThresholdPage(ui_manager, ts, disp, "threshold")
        settings_page = SettingsPage(ui_manager, ts, disp, "settings")
        help_page = HelpPage(ui_manager, ts, disp, "help")
        
        # 建立页面树型结构
        main_menu.add_child(threshold_page)
        main_menu.add_child(settings_page)
        main_menu.add_child(help_page)
        
        # 设置根页面
        ui_manager.set_root_page(main_menu)
        
        print("Tree Structure:")
        print("Main Menu (Root)")
        print("├── Color Threshold")
        print("├── Settings") 
        print("└── Help")
        print("\nStarting main loop...")
        
        # 主循环
        while True:
            img_buffer = image.Image(640, 480)
            ui_manager.update(img_buffer)
                
    except Exception as e:
        print(f"Error: {e}")
        print("Hardware initialization failed, check device connections")
    except KeyboardInterrupt:
        print("\nProgram exited")
        print("Navigation demo completed")


if __name__ == '__main__':
    main()
