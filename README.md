# MaixPy-UI-Lib：一款为 MaixPy 开发的轻量级 UI 组件库

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/aristorechina/MaixPy-UI-Lib/blob/main/LICENSE)[![Version](https://img.shields.io/badge/version-1.0-brightgreen.svg)](https://github.com/aristorechina/MaixPy-UI-Lib)

本项目是一款为 MaixPy 开发的轻量级 UI 组件库，遵循 `Apache 2.0` 协议。

欢迎给本项目提pr，要是觉得好用的话请给本项目点个star⭐

---

## 📦 安装

将仓库下的 `ui.py` 与程序置于同一目录下即可。

---

## 🚀快速上手

克隆本仓库并运行整个项目即可了解所有组件的大致作用，仓库中的 `main.py` 即为 demo。

---

## 📖组件详解

### 1. 按钮 (Button)

按钮是最基本的交互组件，用于触发一个操作。

#### 使用方式
1.  创建一个 `ButtonManager` 实例。
2.  创建 `Button` 实例，定义其矩形区域、标签文本和回调函数。
3.  使用 `manager.add_button()` 将按钮实例添加到管理器中。
4.  在主循环中，调用 `manager.handle_events(img)` 来处理触摸事件并绘制按钮。

#### 示例

```python
from maix import display, camera, app, touchscreen, image
from ui import Button, ButtonManager
import time

# 1. 初始化硬件
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera()

# 2. 定义回调函数
# 当按钮被点击时，这个函数会被调用
def on_button_click():
    print("Hello, World! The button was clicked.")
    # 你可以在这里执行任何操作，比如切换页面、拍照等

# 3. 初始化UI
# 创建一个按钮管理器
btn_manager = ButtonManager(ts, disp)

# 创建一个按钮实例
# rect: [x, y, 宽度, 高度]
# label: 按钮上显示的文字
# callback: 点击时调用的函数
hello_button = Button(
    rect=[240, 200, 160, 80],
    label="Click Me",
    text_scale=2.0,
    callback=on_button_click,
    bg_color=(0, 120, 220),       # 蓝色背景
    pressed_color=(0, 80, 180),   # 按下时深蓝色
    text_color=(255, 255, 255)    # 白色文字
)

# 将按钮添加到管理器
btn_manager.add_button(hello_button)

# 4. 主循环
print("Button example running. Press the button on the screen.")
while not app.need_exit():
    img = cam.read()
    
    # 在每一帧中，让管理器处理事件并绘制按钮
    btn_manager.handle_events(img)
    
    disp.show(img)
    time.sleep(0.02) # 降低CPU使用率
```

#### `Button` 构造函数参数详解
| 参数 | 类型 | 描述 | 默认值 |
| :--: | :--: | :--: | :--: |
| `rect` | `list` | `[x, y, w, h]` 定义按钮位置和大小。**必需**。 | - |
| `label` | `str` | 按钮上显示的文本。**必需**。 | - |
| `callback` | `function` | 点击时调用的函数。**必需**。 | - |
| `bg_color` | `tuple/None` | `(r, g, b)` 背景颜色。`None` 为透明。 | `(50, 50, 50)` |
| `pressed_color`| `tuple/None` | `(r, g, b)` 按下时的背景颜色。 | `(0, 120, 220)` |
| `text_color` | `tuple` | `(r, g, b)` 文本颜色。 | `(255, 255, 255)` |
| `border_color`| `tuple` | `(r, g, b)` 边框颜色。 | `(200, 200, 200)` |
| `border_thickness`| `int` | 边框厚度。`0` 为无边框。 | `2` |
| `text_scale` | `float` | 文本缩放比例。 | `1.5` |
| `align_h` | `str` | 水平对齐：`'center'`, `'left'`, `'right'`。 | `'center'` |
| `align_v` | `str` | 垂直对齐：`'center'`, `'top'`, `'bottom'`。 | `'center'` |

---

### 2. 滑块 (Slider)

滑块允许用户在一个连续的范围内选择一个值。

#### 使用方式
1.  创建一个 `SliderManager` 实例。
2.  创建 `Slider` 实例，定义其区域、数值范围和回调函数。
3.  使用 `manager.add_slider()` 添加滑块。
4.  在主循环中，调用 `manager.handle_events(img)`。

#### 示例
```python
from maix import display, camera, app, touchscreen, image
from ui import Slider, SliderManager
import time

# 1. 初始化硬件
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera()

# 全局变量，用于存储滑块的值
current_brightness = 128 

# 2. 定义回调函数
# 当滑块的值改变时，这个函数会被调用
def on_slider_update(value):
    global current_brightness
    current_brightness = value
    print(f"Slider value updated to: {value}")

# 3. 初始化UI
slider_manager = SliderManager(ts, disp)

brightness_slider = Slider(
    rect=[50, 230, 540, 20],
    scale=2.0,
    min_val=0,
    max_val=255,
    default_val=current_brightness,
    callback=on_slider_update,
    label="Slider"
)

slider_manager.add_slider(brightness_slider)

# 4. 主循环
print("Slider example running. Drag the slider.")
title_color = image.Color.from_rgb(255, 255, 255)

while not app.need_exit():
    img = cam.read()
    
    # 实时显示滑块的值
    img.draw_string(20, 20, f"Value: {current_brightness}", scale=2.0, color=title_color)
    
    # 处理滑块事件并绘制
    slider_manager.handle_events(img)
    
    disp.show(img)
    time.sleep(0.02)
```
#### `Slider` 构造函数参数详解

| 参数 | 类型 | 描述 | 默认值 |
| :--: | :--: | :--: | :--: |
| `rect` | `list` | `[x, y, w, h]` 定义滑块轨道位置和触摸区域。**必需**。 | - |
| `scale` | `float` | 整体缩放因子。影响轨道高度、手柄大小和文字等所有视觉元素。 | `1.0` |
| `min_val` | `int` | 滑块的最小值。 | `0` |
| `max_val` | `int` | 滑块的最大值。 | `100` |
| `default_val`| `int` | 滑块的初始值。 | `50` |
| `callback` | `function` | 拖动时调用的函数，会传入当前值 `value`。 | `None` |
| `label` | `str` | 显示在滑块上方的标签文本。 | `""` |
| `track_color`| `tuple` | `(r, g, b)` 轨道背景色。 | `(60, 60, 60)` |
| `progress_color`| `tuple` | `(r, g, b)` 轨道进度条颜色。 | `(0, 120, 220)` |
| `handle_color`| `tuple` | `(r, g, b)` 未按下时手柄的颜色。 | `(255, 255, 255)` |
| `handle_border_color` | `tuple` | `(r, g, b)` 手柄的边框颜色。 | `(100, 100, 100)` |
| `handle_pressed_color`| `tuple` | `(r, g, b)` 按下时手柄的颜色。 | `(220, 220, 255)` |
| `label_color` | `tuple` | `(r, g, b)` 标签文本的颜色。 | `(200, 200, 200)` |
| `tooltip_bg_color` | `tuple` | `(r, g, b)` 拖动时数值提示框的背景色。 | `(0, 0, 0)` |
| `tooltip_text_color` | `tuple` | `(r, g, b)` 拖动时数值提示框的文本颜色。 | `(255, 255, 255)` |
| `show_tooltip_on_drag`| `bool`| 拖动时是否显示当前值的提示框。 | `True` |

---

### 3. 开关 (Switch)

一个具有“开”和“关”两种状态的切换控件。

#### 使用方式
1.  创建一个 `SwitchManager` 实例。
2.  创建 `Switch` 实例，定义其位置、初始状态和回调函数。
3.  使用 `manager.add_switch()` 添加开关。
4.  在主循环中，调用 `manager.handle_events(img)`。

#### 示例
```python
from maix import display, camera, app, touchscreen, image
from ui import Switch, SwitchManager
import time

# 1. 初始化硬件
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera()

# 全局变量，用于存储开关状态
is_light_on = False

# 2. 定义回调函数
def on_switch_toggle(is_on):
    global is_light_on
    is_light_on = is_on
    status = "ON" if is_on else "OFF"
    print(f"Switch toggled. Light is now {status}.")

# 3. 初始化UI
switch_manager = SwitchManager(ts, disp)

light_switch = Switch(
    position=[280, 190],
    scale=2.0,
    is_on=is_light_on,
    callback=on_switch_toggle
)

switch_manager.add_switch(light_switch)

# 4. 主循环
print("Switch example running. Tap the switch.")
title_color = image.Color.from_rgb(255, 255, 255)
status_on_color = image.Color.from_rgb(30, 200, 30)
status_off_color = image.Color.from_rgb(80, 80, 80)

while not app.need_exit():
    img = cam.read()
    
    # 根据开关状态显示一个状态指示灯
    status_text = "Light: ON" if is_light_on else "Light: OFF"
    status_color = status_on_color if is_light_on else status_off_color
    img.draw_string(20, 20, status_text, scale=1.5, color=title_color)
    img.draw_rect(310, 280, 50, 50, color=status_color, thickness=-1)
    
    switch_manager.handle_events(img)
    
    disp.show(img)
    time.sleep(0.02)
```

#### `Switch` 构造函数参数详解
| 参数 | 类型 | 描述 | 默认值 |
| :--: | :--: | :--: | :--: |
| `position` | `list/tuple` | `[x, y]` 定义开关左上角位置。**必需**。 | - |
| `scale` | `float` | 开关的整体缩放比例。 | `1.0` |
| `is_on` | `bool` | 初始状态，`True` 为开。 | `False` |
| `callback` | `function` | 切换时调用的函数，会传入新状态 `is_on`。 | `None` |
| `on_color` | `tuple` | `(r, g, b)` “开”状态的背景色。 | `(30, 200, 30)` |
| `off_color` | `tuple` | `(r, g, b)` “关”状态的背景色。 | `(100, 100, 100)`|
| `handle_color`| `tuple` | `(r, g, b)` 手柄颜色。 | `(255, 255, 255)`|

---

### 4. 复选框 (Checkbox)

允许用户从一组选项中进行多项选择。

#### 使用方式
1.  创建一个 `CheckboxManager` 实例。
2.  创建多个 `Checkbox` 实例，每个都有独立的回调和状态。
3.  使用 `manager.add_checkbox()` 添加它们。
4.  在主循环中，调用 `manager.handle_events(img)`。

#### 示例
```python
from maix import display, camera, app, touchscreen, image
from ui import Checkbox, CheckboxManager
import time

# 1. 初始化硬件
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera()

# 全局字典，用于存储每个复选框的状态
options = {'Checkbox A': True, 'Checkbox B': False}

# 2. 定义回调函数 (使用闭包来区分是哪个复选框被点击)
def create_checkbox_callback(key):
    def on_check_change(is_checked):
        options[key] = is_checked
        print(f"Option '{key}' is now {'checked' if is_checked else 'unchecked'}.")
    return on_check_change

# 3. 初始化UI
checkbox_manager = CheckboxManager(ts, disp)

checkbox_a = Checkbox(
    position=[80, 150],
    label="Checkbox A",
    is_checked=options['Checkbox A'],
    callback=create_checkbox_callback('Checkbox A'),
    scale=2.0
)
checkbox_b = Checkbox(
    position=[80, 300],
    label="Checkbox B",
    is_checked=options['Checkbox B'],
    callback=create_checkbox_callback('Checkbox B'),
    scale=2.0
)

checkbox_manager.add_checkbox(checkbox_a)
checkbox_manager.add_checkbox(checkbox_b)

# 4. 主循环
print("Checkbox example running. Tap the checkboxes.")
title_color = image.Color.from_rgb(255, 255, 255)
while not app.need_exit():
    img = cam.read()
    
    # 显示当前状态
    a_status = "ON" if options['Checkbox A'] else "OFF"
    b_status = "ON" if options['Checkbox B'] else "OFF"
    img.draw_string(20, 20, f"Checkbox A: {a_status}, Checkbox B: {b_status}", scale=1.5, color=title_color)
    
    checkbox_manager.handle_events(img)
    
    disp.show(img)
    time.sleep(0.02)
```

#### `Checkbox` 构造函数参数详解
| 参数 | 类型 | 描述 | 默认值 |
| :--: | :--: | :--: | :--: |
| `position` | `list/tuple` | `[x, y]` 定义方框左上角位置。**必需**。 | - |
| `label` | `str` | 旁边的说明文字。**必需**。 | - |
| `scale` | `float` | 整体缩放比例。 | `1.0` |
| `is_checked` | `bool` | 初始选中状态。 | `False` |
| `callback` | `function` | 状态改变时调用的函数，传入新状态 `is_checked`。 | `None` |
| `box_color` | `tuple` | `(r, g, b)` 未选中时方框颜色。 | `(200, 200, 200)`|
| `box_checked_color`| `tuple` | `(r, g, b)` 选中时方框背景色。 | `(0, 120, 220)` |
| `check_color` | `tuple` | `(r, g, b)` 选中时“对勾”的颜色。 | `(255, 255, 255)`|
| `text_color` | `tuple` | `(r, g, b)` 标签文本颜色。 | `(200, 200, 200)`|

---

### 5. 单选按钮 (RadioButton)

允许用户从一组互斥的选项中只选择一项。

#### 使用方式
1.  创建一个 `RadioManager` 实例。**注意**：`RadioManager` 构造时需要接收 `default_value` 和一个全局 `callback`。
2.  创建 `RadioButton` 实例，每个按钮必须有唯一的 `value`。
3.  使用 `manager.add_radio()` 添加它们。
4.  在主循环中，调用 `manager.handle_events(img)`。管理器会自动处理互斥逻辑。

#### 示例
```python
from maix import display, camera, app, touchscreen, image
from ui import RadioButton, RadioManager
import time

# 1. 初始化硬件
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera()

# 全局变量，存储当前选择的模式
current_mode = None

# 2. 定义回调函数
# 这个回调由 RadioManager 调用，传入被选中项的 value
def on_mode_change(selected_value):
    global current_mode
    current_mode = selected_value
    print(f"Mode changed to: {selected_value}")

# 3. 初始化UI
# 创建 RadioManager，并传入默认值和回调
radio_manager = RadioManager(ts, disp, 
                           default_value=current_mode, 
                           callback=on_mode_change)

# 创建三个 RadioButton 实例，注意它们的 value 是唯一的
radio_a = RadioButton(position=[80, 100], label="Mode A", value="Mode A", scale=2.0)
radio_b = RadioButton(position=[80, 200], label="Mode B", value="Mode B", scale=2.0)
radio_c = RadioButton(position=[80, 300], label="Mode C", value="Mode C", scale=2.0)

# 将它们都添加到管理器中
radio_manager.add_radio(radio_a)
radio_manager.add_radio(radio_b)
radio_manager.add_radio(radio_c)

# 4. 主循环
print("Radio button example running. Select a mode.")
title_color = image.Color.from_rgb(255, 255, 255)
while not app.need_exit():
    img = cam.read()
    
    img.draw_string(20, 20, f"Current: {current_mode}", scale=1.8, color=title_color)
    
    radio_manager.handle_events(img)
    
    disp.show(img)
    time.sleep(0.02)
```

#### `RadioButton` 构造函数参数详解
| 参数 | 类型 | 描述 | 默认值 |
| :--: | :--: | :--: | :--: |
| `position` | `list/tuple` | `[x, y]` 定义圆形区域左上角位置。**必需**。 | - |
| `label` | `str` | 旁边的说明文字。**必需**。 | - |
| `value` | `any` | 代表此选项的唯一值。**必需**。 | - |
| `scale` | `float` | 整体缩放比例。 | `1.0` |
| `circle_color`| `tuple` | `(r, g, b)` 未选中时圆圈颜色。 | `(200, 200, 200)`|
| `circle_selected_color`| `tuple` | `(r, g, b)` 选中时圆圈颜色。 | `(0, 120, 220)` |
| `dot_color` | `tuple` | `(r, g, b)` 选中时中心圆点颜色。 | `(255, 255, 255)`|
| `text_color` | `tuple` | `(r, g, b)` 标签文本颜色。 | `(200, 200, 200)`|

#### `RadioManager` 构造函数参数详解
| 参数 | 类型 | 描述 | 默认值 |
| :--: | :--: | :--: | :--: |
| `ts` | `touchscreen`| 触摸屏实例。**必需**。 | - |
| `disp` | `display` | 显示屏实例。**必需**。 | - |
| `default_value` | `any` | 初始选中的单选按钮的 `value`。 | `None` |
| `callback` | `function` | 选项改变时调用的函数，传入被选中项的 `value`。| `None` |