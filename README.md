# MaixPy-UI-Lib：一款为 MaixPy 开发的轻量级 UI 组件库

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/aristorechina/MaixPy-UI-Lib/blob/main/LICENSE) [![Version](https://img.shields.io/badge/version-2.1-brightgreen.svg)](https://github.com/aristorechina/MaixPy-UI-Lib)

本项目是一款为 MaixPy 开发的轻量级 UI 组件库，遵循 `Apache 2.0` 协议。

欢迎给本项目提pr，要是觉得好用的话请给本项目点个star⭐

---

## 🖼️功能展示

以下画面均截取自本项目的 `main.py`

![button](https://raw.githubusercontent.com/aristorechina/MaixPy-UI-Lib/main/pics/button.jpg)

![switch](https://raw.githubusercontent.com/aristorechina/MaixPy-UI-Lib/main/pics/switch.jpg)

![slider](https://raw.githubusercontent.com/aristorechina/MaixPy-UI-Lib/main/pics/slider.jpg)

![radiobutton](https://raw.githubusercontent.com/aristorechina/MaixPy-UI-Lib/main/pics/radiobutton.jpg)

![checkbox](https://raw.githubusercontent.com/aristorechina/MaixPy-UI-Lib/main/pics/checkbox.jpg)

---

## 📦 安装

将仓库下的 `ui.py` 与程序置于同一目录下即可。

---

## 🚀快速上手

克隆本仓库并运行整个项目即可了解所有组件的大致作用，仓库中的 `main.py` 即为 demo。

---

# 📖组件详解

## 1. 按钮 (Button)
按钮是最基本的交互组件，用于触发一个操作。

### 使用方式
创建一个 ButtonManager 实例。
创建 Button 实例，定义其矩形区域、标签文本和回调函数。
使用 manager.add_button() 将按钮实例添加到管理器中。
在主循环中，调用 manager.handle_events(img) 来处理触摸事件并绘制按钮。

### 示例
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

### Button 类
创建一个可交互的按钮组件。该组件可以响应触摸事件，并在按下时改变外观，释放时执行回调函数。

#### 构造函数: __init__
| 参数             | 类型                    | 描述                                       | 默认值          |
| ---------------- | ----------------------- | ------------------------------------------ | --------------- |
| rect             | Sequence[int]           | 按钮的位置和尺寸 [x, y, w, h]。必需。      | -               |
| label            | str                     | 按钮上显示的文本。必需。                   | -               |
| callback         | `Callable \| None`      | 当按钮被点击时调用的函数。必需。           | -               |
| bg_color         | `Sequence[int] \| None` | 背景颜色 (R, G, B)。                       | (50, 50, 50)    |
| pressed_color    | `Sequence[int] \| None` | 按下状态的背景颜色 (R, G, B)。             | (0, 120, 220)   |
| text_color       | Sequence[int]           | 文本颜色 (R, G, B)。                       | (255, 255, 255) |
| border_color     | Sequence[int]           | 边框颜色 (R, G, B)。                       | (200, 200, 200) |
| border_thickness | int                     | 边框厚度（像素）。                         | 2               |
| text_scale       | float                   | 文本的缩放比例。                           | 1.5             |
| font             | `str \| None`           | 使用的字体文件路径。                       | None            |
| align_h          | str                     | 水平对齐方式 ('left', 'center', 'right')。 | 'center'        |
| align_v          | str                     | 垂直对齐方式 ('top', 'center', 'bottom')。 | 'center'        |

#### 方法 (Methods)
| 方法              | 参数                                                         | 描述                         |
| ----------------- | ------------------------------------------------------------ | ---------------------------- |
| draw(img)         | img (maix.image.Image): 将要绘制按钮的目标图像。             | 在指定的图像上绘制按钮。     |
| handle_event(...) | x (int): 触摸点的 X 坐标。<br>y (int): 触摸点的 Y 坐标。<br>pressed (`bool \| int`): 触摸屏是否被按下。<br>img_w (int): 图像缓冲区的宽度。<br>img_h (int): 图像缓冲区的高度。<br>disp_w (int): 显示屏的宽度。<br>disp_h (int): 显示屏的高度。 | 处理触摸事件并更新按钮状态。 |

### ButtonManager 类
管理一组按钮的事件处理和绘制。

#### 构造函数: __init__
| 参数 | 类型                    | 描述                   |
| ---- | ----------------------- | ---------------------- |
| ts   | touchscreen.TouchScreen | 触摸屏设备实例。必需。 |
| disp | display.Display         | 显示设备实例。必需。   |

#### 方法 (Methods)
| 方法               | 参数                                         | 描述                               |
| ------------------ | -------------------------------------------- | ---------------------------------- |
| add_button(button) | button (Button): 要添加的 Button 实例。      | 向管理器中添加一个按钮。           |
| handle_events(img) | img (maix.image.Image): 绘制按钮的目标图像。 | 处理所有受管按钮的事件并进行绘制。 |

## 2. 滑块 (Slider)
滑块允许用户在一个连续的范围内选择一个值。

### 使用方式
创建一个 SliderManager 实例。
创建 Slider 实例，定义其区域、数值范围和回调函数。
使用 manager.add_slider() 添加滑块。
在主循环中，调用 manager.handle_events(img)。

### 示例
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

### Slider 类
创建一个可拖动的滑块组件，用于在一定范围内选择一个值。

#### 构造函数: __init__
| 参数                 | 类型               | 描述                                   | 默认值          |
| -------------------- | ------------------ | -------------------------------------- | --------------- |
| rect                 | Sequence[int]      | 滑块的位置和尺寸 [x, y, w, h]。必需。  | -               |
| scale                | float              | 滑块的整体缩放比例。                   | 1.0             |
| min_val              | int                | 滑块的最小值。                         | 0               |
| max_val              | int                | 滑块的最大值。                         | 100             |
| default_val          | int                | 滑块的默认值。                         | 50              |
| callback             | `Callable \| None` | 值改变时调用的函数，接收新值作为参数。 | None            |
| label                | str                | 滑块上方的标签文本。                   | ""              |
| track_color          | Sequence[int]      | 滑轨背景颜色 (R, G, B)。               | (60, 60, 60)    |
| progress_color       | Sequence[int]      | 滑轨进度条颜色 (R, G, B)。             | (0, 120, 220)   |
| handle_color         | Sequence[int]      | 滑块手柄颜色 (R, G, B)。               | (255, 255, 255) |
| handle_border_color  | Sequence[int]      | 滑块手柄边框颜色 (R, G, B)。           | (100, 100, 100) |
| handle_pressed_color | Sequence[int]      | 按下时手柄颜色 (R, G, B)。             | (220, 220, 255) |
| label_color          | Sequence[int]      | 标签文本颜色 (R, G, B)。               | (200, 200, 200) |
| tooltip_bg_color     | Sequence[int]      | 拖动时提示框背景色 (R, G, B)。         | (0, 0, 0)       |
| tooltip_text_color   | Sequence[int]      | 拖动时提示框文本颜色 (R, G, B)。       | (255, 255, 255) |
| show_tooltip_on_drag | `bool \| int`      | 是否在拖动时显示数值提示框。           | True            |

#### 方法 (Methods)
| 方法              | 参数                                                         | 描述                         |
| ----------------- | ------------------------------------------------------------ | ---------------------------- |
| draw(img)         | img (maix.image.Image): 将要绘制滑块的目标图像。             | 在指定的图像上绘制滑块。     |
| handle_event(...) | x (int): 触摸点的 X 坐标。<br>y (int): 触摸点的 Y 坐标。<br>pressed (`bool \| int`): 触摸屏是否被按下。<br>img_w (int): 图像缓冲区的宽度。<br>img_h (int): 图像缓冲区的高度。<br>disp_w (int): 显示屏的宽度。<br>disp_h (int): 显示屏的高度。 | 处理触摸事件并更新滑块状态。 |

### SliderManager 类
管理一组滑块的事件处理和绘制。

#### 构造函数: __init__
| 参数 | 类型                    | 描述                   |
| ---- | ----------------------- | ---------------------- |
| ts   | touchscreen.TouchScreen | 触摸屏设备实例。必需。 |
| disp | display.Display         | 显示设备实例。必需。   |

#### 方法 (Methods)
| 方法               | 参数                                         | 描述                               |
| ------------------ | -------------------------------------------- | ---------------------------------- |
| add_slider(slider) | slider (Slider): 要添加的 Slider 实例。      | 向管理器中添加一个滑块。           |
| handle_events(img) | img (maix.image.Image): 绘制滑块的目标图像。 | 处理所有受管滑块的事件并进行绘制。 |

## 3. 开关 (Switch)
一个具有"开"和"关"两种状态的切换控件。

### 使用方式
创建一个 SwitchManager 实例。
创建 Switch 实例，定义其位置、初始状态和回调函数。
使用 manager.add_switch() 添加开关。
在主循环中，调用 manager.handle_events(img)。

### 示例
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

### Switch 类
创建一个开关（Switch）组件，用于在开/关两种状态之间切换。

#### 构造函数: __init__
| 参数                   | 类型               | 描述                                                 | 默认值          |
| ---------------------- | ------------------ | ---------------------------------------------------- | --------------- |
| position               | Sequence[int]      | 开关的左上角坐标 [x, y]。必需。                      | -               |
| scale                  | float              | 开关的整体缩放比例。                                 | 1.0             |
| is_on                  | `bool \| int`      | 开关的初始状态，True 为开。                          | False           |
| callback               | `Callable \| None` | 状态切换时调用的函数，接收一个布尔值参数表示新状态。 | None            |
| on_color               | Sequence[int]      | 开启状态下的背景颜色 (R, G, B)。                     | (30, 200, 30)   |
| off_color              | Sequence[int]      | 关闭状态下的背景颜色 (R, G, B)。                     | (100, 100, 100) |
| handle_color           | Sequence[int]      | 手柄的颜色 (R, G, B)。                               | (255, 255, 255) |
| handle_pressed_color   | Sequence[int]      | 按下时手柄的颜色 (R, G, B)。                         | (220, 220, 255) |
| handle_radius_increase | int                | 按下时手柄半径增加量。                               | 2               |

#### 方法 (Methods)
| 方法              | 参数                                                         | 描述                             |
| ----------------- | ------------------------------------------------------------ | -------------------------------- |
| toggle()          | -                                                            | 切换开关的状态，并执行回调函数。 |
| draw(img)         | img (maix.image.Image): 将要绘制开关的目标图像。             | 在指定的图像上绘制开关。         |
| handle_event(...) | x (int): 触摸点的 X 坐标。<br>y (int): 触摸点的 Y 坐标。<br>pressed (`bool \| int`): 触摸屏是否被按下。<br>img_w (int): 图像缓冲区的宽度。<br>img_h (int): 图像缓冲区的高度。<br>disp_w (int): 显示屏的宽度。<br>disp_h (int): 显示屏的高度。 | 处理触摸事件并更新开关状态。     |

### SwitchManager 类
管理一组开关的事件处理和绘制。

#### 构造函数: __init__
| 参数 | 类型                    | 描述                   |
| ---- | ----------------------- | ---------------------- |
| ts   | touchscreen.TouchScreen | 触摸屏设备实例。必需。 |
| disp | display.Display         | 显示设备实例。必需。   |

#### 方法 (Methods)
| 方法               | 参数                                         | 描述                               |
| ------------------ | -------------------------------------------- | ---------------------------------- |
| add_switch(switch) | switch (Switch): 要添加的 Switch 实例。      | 向管理器中添加一个开关。           |
| handle_events(img) | img (maix.image.Image): 绘制开关的目标图像。 | 处理所有受管开关的事件并进行绘制。 |

## 4. 复选框 (Checkbox)
允许用户从一组选项中进行多项选择。

### 使用方式
创建一个 CheckboxManager 实例。
创建多个 Checkbox 实例，每个都有独立的回调和状态。
使用 manager.add_checkbox() 添加它们。
在主循环中，调用 manager.handle_events(img)。

### 示例
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

### Checkbox 类
创建一个复选框（Checkbox）组件，可独立选中或取消。

#### 构造函数: __init__
| 参数              | 类型               | 描述                                                 | 默认值          |
| ----------------- | ------------------ | ---------------------------------------------------- | --------------- |
| position          | Sequence[int]      | 复选框的左上角坐标 [x, y]。必需。                    | -               |
| label             | str                | 复选框旁边的标签文本。必需。                         | -               |
| scale             | float              | 复选框的整体缩放比例。                               | 1.0             |
| is_checked        | `bool \| int`      | 复选框的初始状态，True 为选中。                      | False           |
| callback          | `Callable \| None` | 状态切换时调用的函数，接收一个布尔值参数表示新状态。 | None            |
| box_color         | Sequence[int]      | 未选中时方框的颜色 (R, G, B)。                       | (200, 200, 200) |
| box_checked_color | Sequence[int]      | 选中时方框的颜色 (R, G, B)。                         | (0, 120, 220)   |
| check_color       | Sequence[int]      | 选中标记（对勾）的颜色 (R, G, B)。                   | (255, 255, 255) |
| text_color        | Sequence[int]      | 标签文本的颜色 (R, G, B)。                           | (200, 200, 200) |
| box_thickness     | int                | 方框边框的厚度。                                     | 2               |

#### 方法 (Methods)
| 方法              | 参数                                                         | 描述                               |
| ----------------- | ------------------------------------------------------------ | ---------------------------------- |
| toggle()          | -                                                            | 切换复选框的选中状态，并执行回调。 |
| draw(img)         | img (maix.image.Image): 将要绘制复选框的目标图像。           | 在指定的图像上绘制复选框。         |
| handle_event(...) | x (int): 触摸点的 X 坐标。<br>y (int): 触摸点的 Y 坐标。<br>pressed (`bool \| int`): 触摸屏是否被按下。<br>img_w (int): 图像缓冲区的宽度。<br>img_h (int): 图像缓冲区的高度。<br>disp_w (int): 显示屏的宽度。<br>disp_h (int): 显示屏的高度。 | 处理触摸事件并更新复选框状态。     |

### CheckboxManager 类
管理一组复选框的事件处理和绘制。

#### 构造函数: __init__
| 参数 | 类型                    | 描述                   |
| ---- | ----------------------- | ---------------------- |
| ts   | touchscreen.TouchScreen | 触摸屏设备实例。必需。 |
| disp | display.Display         | 显示设备实例。必需。   |

#### 方法 (Methods)
| 方法                   | 参数                                           | 描述                                 |
| ---------------------- | ---------------------------------------------- | ------------------------------------ |
| add_checkbox(checkbox) | checkbox (Checkbox): 要添加的 Checkbox 实例。  | 向管理器中添加一个复选框。           |
| handle_events(img)     | img (maix.image.Image): 绘制复选框的目标图像。 | 处理所有受管复选框的事件并进行绘制。 |

## 5. 单选框 (RadioButton)
允许用户从一组互斥的选项中只选择一项。

### 使用方式
创建一个 RadioManager 实例。注意：RadioManager 构造时需要接收 default_value 和一个全局 callback。
创建 RadioButton 实例，每个按钮必须有唯一的 value。
使用 manager.add_radio() 添加它们。
在主循环中，调用 manager.handle_events(img)。管理器会自动处理互斥逻辑。

### 示例
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

### RadioButton 类
创建一个单选框（RadioButton）项。通常与 RadioManager 结合使用。

#### 构造函数: __init__
| 参数                  | 类型          | 描述                                  | 默认值          |
| --------------------- | ------------- | ------------------------------------- | --------------- |
| position              | Sequence[int] | 单选框圆圈的左上角坐标 [x, y]。必需。 | -               |
| label                 | str           | 按钮旁边的标签文本。必需。            | -               |
| value                 | any           | 与此单选框关联的唯一值。必需。        | -               |
| scale                 | float         | 组件的整体缩放比例。                  | 1.0             |
| circle_color          | Sequence[int] | 未选中时圆圈的颜色 (R, G, B)。        | (200, 200, 200) |
| circle_selected_color | Sequence[int] | 选中时圆圈的颜色 (R, G, B)。          | (0, 120, 220)   |
| dot_color             | Sequence[int] | 选中时中心圆点的颜色 (R, G, B)。      | (255, 255, 255) |
| text_color            | Sequence[int] | 标签文本的颜色 (R, G, B)。            | (200, 200, 200) |
| circle_thickness      | int           | 圆圈边框的厚度。                      | 2               |

#### 方法 (Methods)
| 方法      | 参数                                               | 描述                       |
| --------- | -------------------------------------------------- | -------------------------- |
| draw(img) | img (maix.image.Image): 将要绘制单选框的目标图像。 | 在指定的图像上绘制单选框。 |

### RadioManager 类
管理一个单选框组，确保只有一个按钮能被选中。

#### 构造函数: __init__
| 参数          | 类型                    | 描述                                               | 默认值 |
| ------------- | ----------------------- | -------------------------------------------------- | ------ |
| ts            | touchscreen.TouchScreen | 触摸屏设备实例。必需。                             | -      |
| disp          | display.Display         | 显示设备实例。必需。                               | -      |
| default_value | any                     | 默认选中的按钮的值。                               | None   |
| callback      | `Callable \| None`      | 选中项改变时调用的函数，接收新选中项的值作为参数。 | None   |

#### 方法 (Methods)
| 方法               | 参数                                             | 描述                             |
| ------------------ | ------------------------------------------------ | -------------------------------- |
| add_radio(radio)   | radio (RadioButton): 要添加的 RadioButton 实例。 | 向管理器中添加一个单选框。       |
| handle_events(img) | img (maix.image.Image): 绘制单选框的目标图像。   | 处理所有单选框的事件并进行绘制。 |

## 6. 分辨率适配器 (ResolutionAdapter)
一个辅助工具类，用于自动适配不同分辨率的屏幕，以保持UI布局的一致性。

### 使用方式
创建一个 ResolutionAdapter 实例，并指定目标屏幕尺寸和可选的设计基础分辨率。
基于您的设计基础分辨率，定义组件的原始 rect、position 等参数。
调用 adapter.scale_rect() 等方法，将原始参数转换为适配后的值。
使用转换后的值来创建您的UI组件。

### 示例
```python
from maix import display, camera, app, touchscreen
from ui import Button, ButtonManager, ResolutionAdapter
import time

# 1. 初始化硬件
disp = display.Display()
ts = touchscreen.TouchScreen()
# cam = camera.Camera(640,480)
cam = camera.Camera(320,240)

# 2. 创建分辨率适配器，并明确指定我们的设计是基于 640x480 的
adapter = ResolutionAdapter(
    display_width=cam.width(), 
    display_height=cam.height(),
    base_width=640,
    base_height=480
)

# 3. 基于 640x480 的画布来定义组件参数
original_rect = [160, 200, 320, 80]
original_font_scale = 3.0 

# 4. 使用适配器转换参数
scaled_rect = adapter.scale_rect(original_rect)
scaled_font_size = adapter.scale_value(original_font_scale) 

# 5. 使用缩放后的值创建组件
btn_manager = ButtonManager(ts, disp)
adapted_button = Button(
    rect=scaled_rect,
    label="Big Button",
    text_scale=scaled_font_size,
    callback=lambda: print("Adapted button clicked!")
)
btn_manager.add_button(adapted_button)

# 6. 主循环
print("ResolutionAdapter example running (640x480 base).")
while not app.need_exit():
    img = cam.read()
    btn_manager.handle_events(img)
    disp.show(img)
    time.sleep(0.02)
```

### ResolutionAdapter 类

#### 构造函数: __init__
| 参数           | 类型 | 描述                     | 默认值 |
| -------------- | ---- | ------------------------ | ------ |
| display_width  | int  | 目标显示屏的宽度。必需。 | -      |
| display_height | int  | 目标显示屏的高度。必需。 | -      |
| base_width     | int  | UI设计的基准宽度。       | 320    |
| base_height    | int  | UI设计的基准高度。       | 240    |

#### 方法 (Methods)
| 方法                      | 参数                                                | 描述                               | 返回值        |
| ------------------------- | --------------------------------------------------- | ---------------------------------- | ------------- |
| scale_position(x, y)      | x (int): 原始 X 坐标。<br>y (int): 原始 Y 坐标。    | 缩放一个坐标点 (x, y)。            | Sequence[int] |
| scale_size(width, height) | width (int): 原始宽度。<br>height (int): 原始高度。 | 缩放一个尺寸 (width, height)。     | Sequence[int] |
| scale_rect(rect)          | rect (list[int]): 原始矩形 [x, y, w, h]。           | 缩放一个矩形。                     | Sequence[int] |
| scale_value(value)        | value (`int \| float`): 原始数值。                  | 缩放一个通用数值，如半径、厚度等。 | float         |

## 7. 页面与 UI 管理器 (Page and UIManager) 
用于构建和管理具有树型层次结构的页面系统（如主菜单、设置页、子菜单等）。

### 使用方式
创建一个全局的 UIManager 实例。
定义继承自 Page 的自定义页面类，并在其中初始化该页面所需的UI组件和逻辑。
使用页面的 add_child() 方法建立父子关系，构建树型页面结构。
使用多种导航方法进行页面切换：
- `navigate_to_child()` - 导航到子页面
- `navigate_to_parent()` - 返回父页面
- `navigate_to_path()` - 按路径导航
- `go_back()` - 基于历史记录返回
在主循环中，持续调用 ui_manager.update(img) 来驱动当前活动页面的更新和绘制。

### 示例（其中功能WIFI蓝牙等功能仅供演示，没有实际功能）
```python
from maix import display, camera, app, touchscreen, image
import sys
sys.path.append(r'/root/modules')
from ui import Page, UIManager, Button, ButtonManager, Switch, SwitchManager
import time

# 1. 初始化硬件
disp = display.Display()
ts = touchscreen.TouchScreen()
cam = camera.Camera()

# 2. 定义一个全局状态字典，用于在页面间共享和持久化数据
APP_STATE = {
    'wifi_enabled': False,
    'bluetooth_enabled': True,
    'display_brightness': 80,
}

# 3. 创建 UI 管理器
ui_manager = UIManager()

# --- 定义页面树结构 ---

# 根页面：主菜单
class MainMenuPage(Page):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "main_menu")
        self.btn_manager = ButtonManager(ts, disp)
        
        # 创建导航按钮
        settings_btn = Button(
            rect=[220, 150, 200, 60],
            label="Settings",
            text_scale=2.0,
            callback=lambda: self.ui_manager.navigate_to_child("settings")
        )
        
        about_btn = Button(
            rect=[220, 230, 200, 60],
            label="About",
            text_scale=2.0,
            callback=lambda: self.ui_manager.navigate_to_child("about")
        )
        
        self.btn_manager.add_button(settings_btn)
        self.btn_manager.add_button(about_btn)

    def on_enter(self): 
        print("Entered Main Menu")
    
    def on_exit(self): 
        print("Exited Main Menu")

    def update(self, img):
        title_color = image.Color(255, 255, 255)
        img.draw_string(20, 20, "Main Menu", scale=2.5, color=title_color)
        img.draw_string(20, 60, f"Path: {' > '.join(self.ui_manager.get_current_path())}", 
                       scale=1.2, color=title_color)
        self.btn_manager.handle_events(img)

# 设置页面
class SettingsPage(Page):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "settings")
        self.btn_manager = ButtonManager(ts, disp)
        self.switch_manager = SwitchManager(ts, disp)

        # 返回按钮
        back_btn = Button(
            rect=[20, 360, 120, 60],
            label="Back",
            text_scale=1.8,
            callback=lambda: self.ui_manager.navigate_to_parent()
        )
        
        # 子页面导航按钮
        wifi_btn = Button(
            rect=[220, 150, 200, 60],
            label="Wi-Fi Settings",
            text_scale=1.5,
            callback=lambda: self.ui_manager.navigate_to_child("wifi_settings")
        )
        
        display_btn = Button(
            rect=[220, 230, 200, 60],
            label="Display Settings",
            text_scale=1.5,
            callback=lambda: self.ui_manager.navigate_to_child("display_settings")
        )

        self.btn_manager.add_button(back_btn)
        self.btn_manager.add_button(wifi_btn)
        self.btn_manager.add_button(display_btn)

        # 蓝牙开关
        bluetooth_switch = Switch(
            position=[280, 300],
            scale=2.0,
            is_on=APP_STATE['bluetooth_enabled'],
            callback=self.on_bluetooth_change
        )
        self.switch_manager.add_switch(bluetooth_switch)

    def on_bluetooth_change(self, is_on):
        APP_STATE['bluetooth_enabled'] = is_on
        print(f"Bluetooth: {'ON' if is_on else 'OFF'}")

    def on_enter(self): 
        print("Entered Settings")
    
    def on_exit(self): 
        print("Exited Settings")

    def update(self, img):
        title_color = image.Color(255, 255, 255)
        img.draw_string(20, 20, "Settings", scale=2.5, color=title_color)
        img.draw_string(20, 60, f"Path: {' > '.join(self.ui_manager.get_current_path())}", 
                       scale=1.2, color=title_color)
        img.draw_string(20, 300, "Bluetooth:", scale=1.5, color=title_color)
        self.btn_manager.handle_events(img)
        self.switch_manager.handle_events(img)

# Wi-Fi 设置子页面
class WiFiSettingsPage(Page):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "wifi_settings")
        self.btn_manager = ButtonManager(ts, disp)
        self.switch_manager = SwitchManager(ts, disp)

        # 导航按钮
        back_btn = Button(
            rect=[20, 360, 120, 60],
            label="Back",
            text_scale=1.8,
            callback=lambda: self.ui_manager.navigate_to_parent()
        )
        
        home_btn = Button(
            rect=[160, 360, 120, 60],
            label="Home",
            text_scale=1.8,
            callback=lambda: self.ui_manager.navigate_to_root()
        )

        self.btn_manager.add_button(back_btn)
        self.btn_manager.add_button(home_btn)

        # Wi-Fi 开关
        wifi_switch = Switch(
            position=[280, 200],
            scale=2.0,
            is_on=APP_STATE['wifi_enabled'],
            callback=self.on_wifi_change
        )
        self.switch_manager.add_switch(wifi_switch)

    def on_wifi_change(self, is_on):
        APP_STATE['wifi_enabled'] = is_on
        print(f"Wi-Fi: {'ON' if is_on else 'OFF'}")

    def on_enter(self): 
        print("Entered Wi-Fi Settings")
    
    def on_exit(self): 
        print("Exited Wi-Fi Settings")

    def update(self, img):
        title_color = image.Color(255, 255, 255)
        img.draw_string(20, 20, "Wi-Fi Settings", scale=2.0, color=title_color)
        img.draw_string(20, 60, f"Path: {' > '.join(self.ui_manager.get_current_path())}", 
                       scale=1.2, color=title_color)
        img.draw_string(20, 200, "Wi-Fi:", scale=1.5, color=title_color)
        
        self.btn_manager.handle_events(img)
        self.switch_manager.handle_events(img)

# 显示设置子页面
class DisplaySettingsPage(Page):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "display_settings")
        self.btn_manager = ButtonManager(ts, disp)

        # 导航按钮
        back_btn = Button(
            rect=[20, 360, 120, 60],
            label="Back",
            text_scale=1.8,
            callback=lambda: self.ui_manager.navigate_to_parent()
        )

        self.btn_manager.add_button(back_btn)

    def on_enter(self): 
        print("Entered Display Settings")
    
    def on_exit(self): 
        print("Exited Display Settings")

    def update(self, img):
        title_color = image.Color(255, 255, 255)
        img.draw_string(20, 20, "Display Settings", scale=2.0, color=title_color)
        img.draw_string(20, 60, f"Path: {' > '.join(self.ui_manager.get_current_path())}", 
                       scale=1.2, color=title_color)
        img.draw_string(20, 150, f"Brightness: {APP_STATE['display_brightness']}%", 
                       scale=1.5, color=title_color)
        self.btn_manager.handle_events(img)

# 关于页面
class AboutPage(Page):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "about")
        self.btn_manager = ButtonManager(ts, disp)

        back_btn = Button(
            rect=[20, 360, 120, 60],
            label="Back",
            text_scale=1.8,
            callback=lambda: self.ui_manager.navigate_to_parent()
        )

        self.btn_manager.add_button(back_btn)

    def on_enter(self): 
        print("Entered About")
    
    def on_exit(self): 
        print("Exited About")

    def update(self, img):
        title_color = image.Color(255, 255, 255)
        img.draw_string(20, 20, "About", scale=2.5, color=title_color)
        img.draw_string(20, 60, f"Path: {' > '.join(self.ui_manager.get_current_path())}", 
                       scale=1.2, color=title_color)
        img.draw_string(20, 150, "App Version: 1.0.0", scale=1.5, color=title_color)
        img.draw_string(20, 180, "Tree-based UI Demo", scale=1.5, color=title_color)
        self.btn_manager.handle_events(img)

# 4. 构建页面树结构
if __name__ == "__main__":
    # 创建所有页面实例
    main_page = MainMenuPage(ui_manager)
    settings_page = SettingsPage(ui_manager)
    wifi_page = WiFiSettingsPage(ui_manager)
    display_page = DisplaySettingsPage(ui_manager)
    about_page = AboutPage(ui_manager)

    # 建立父子关系
    main_page.add_child(settings_page)
    main_page.add_child(about_page)
    settings_page.add_child(wifi_page)
    settings_page.add_child(display_page)

    # 设置根页面
    ui_manager.set_root_page(main_page)

    print("Tree-based page navigation example running.")
    print("Navigate using buttons, notice the path and navigation info!")
    
    while not app.need_exit():
        img = cam.read()
        ui_manager.update(img)
        disp.show(img)
        time.sleep(0.02)

```

### Page 类
页面（Page）的基类，支持树型父子节点结构。每个页面可以有一个父页面和多个子页面，形成树型结构。

#### 构造函数: __init__
| 参数       | 类型      | 描述                                  |
| ---------- | --------- | ------------------------------------- |
| ui_manager | UIManager | 用于页面导航的 UIManager 实例。必需。 |
| name       | str       | 页面的唯一名称标识符。默认为""。      |

#### 属性 (Attributes)
| 属性     | 类型           | 描述                               |
| -------- | -------------- | ---------------------------------- |
| parent   | `Page \| None` | 父页面，如果为 None 则表示根页面。 |
| children | List[Page]     | 子页面列表。                       |

#### 方法 (Methods)
| 方法                     | 参数                                           | 描述                                     | 返回值         |
| ------------------------ | ---------------------------------------------- | ---------------------------------------- | -------------- |
| add_child(child_page)    | child_page (Page): 要添加的子页面实例。        | 添加一个子页面。                         | -              |
| remove_child(child_page) | child_page (Page): 要移除的子页面实例。        | 移除一个子页面。                         | bool           |
| get_child(name)          | name (str): 子页面的名称。                     | 根据名称获取子页面。                     | `Page \| None` |
| get_root()               | -                                              | 获取当前页面的根页面。                   | Page           |
| get_path()               | -                                              | 获取从根页面到当前页面的路径。           | List[str]      |
| get_depth()              | -                                              | 获取当前页面在树中的深度。               | int            |
| find_page_by_path(path)  | path (List[str]): 页面路径。                   | 根据路径查找页面。                       | `Page \| None` |
| on_enter()               | -                                              | 当页面进入视图时调用。子类可重写。       | -              |
| on_exit()                | -                                              | 当页面离开视图时调用。子类可重写。       | -              |
| on_child_enter(child)    | child (Page): 进入视图的子页面。               | 当子页面进入视图时调用。                 | -              |
| on_child_exit(child)     | child (Page): 离开视图的子页面。               | 当子页面离开视图时调用。                 | -              |
| update(img)              | img (maix.image.Image): 用于绘制的图像缓冲区。 | 每帧调用的更新和绘制方法。子类必须重写。 | -              |

### UIManager 类
UI 管理器，基于树型页面结构提供灵活的导航功能。

#### 构造函数: __init__
| 参数      | 类型           | 描述                                   | 默认值 |
| --------- | -------------- | -------------------------------------- | ------ |
| root_page | `Page \| None` | 根页面实例，如果为None则需要后续设置。 | None   |

#### 方法 (Methods)
| 方法                            | 参数                                           | 描述                                           | 返回值         |
| ------------------------------- | ---------------------------------------------- | ---------------------------------------------- | -------------- |
| set_root_page(page)             | page (Page): 新的根页面实例。                  | 设置根页面。                                   | -              |
| get_current_page()              | -                                              | 获取当前活动的页面。                           | `Page \| None` |
| navigate_to_child(child_name)   | child_name (str): 子页面的名称。               | 导航到当前页面的指定子页面。                   | bool           |
| navigate_to_parent()            | -                                              | 导航到当前页面的父页面。                       | bool           |
| navigate_to_root()              | -                                              | 导航到根页面。                                 | bool           |
| navigate_to_path(path)          | path (List[str]): 从根页面开始的绝对路径。     | 根据路径导航到指定页面。                       | bool           |
| navigate_to_relative_path(path) | path (List[str]): 从当前页面开始的相对路径。   | 根据相对路径导航到指定页面。                   | bool           |
| navigate_to_page(target_page)   | target_page (Page): 目标页面实例。             | 直接导航到指定页面。                           | bool           |
| go_back()                       | -                                              | 返回到历史记录中的前一个页面。                 | bool           |
| clear_history()                 | -                                              | 清空导航历史记录。                             | -              |
| get_current_path()              | -                                              | 获取当前页面的完整路径。                       | List[str]      |
| get_navigation_info()           | -                                              | 获取当前导航状态信息。                         | dict           |
| update(img)                     | img (maix.image.Image): 用于绘制的图像缓冲区。 | 更新当前活动页面的状态。应在主循环中每帧调用。 | -              |

#### 导航信息字典结构
`get_navigation_info()` 返回的字典包含以下键值：

| 键               | 类型          | 描述                     |
| ---------------- | ------------- | ------------------------ |
| current_page     | `str \| None` | 当前页面名称             |
| current_path     | List[str]     | 当前页面路径             |
| can_go_back      | bool          | 是否可以基于历史记录返回 |
| can_go_to_parent | bool          | 是否可以返回父页面       |
| history_depth    | int           | 历史记录深度             |
| page_depth       | int           | 当前页面在树中的深度     |

---

## ⚖️许可协议
本项目基于 Apache License, Version 2.0 许可。详细信息请参阅代码文件中的许可证说明。

## 📝更新日志

Version 1.0 (Jul 20, 2025)
- 当前已实现的组件：Button, Slider, Switch, Checkbox, RadioButton。

Version 1.1 (Jul 20, 2025)
- 增加了 ResolutionAdapter 以实现对不同分辨率的 UI 适配（由 @levi_jia 实现）。

Version 1.2 (Jul 20, 2025)
- ResolutionAdapter 增加了自定义基础分辨率的功能（默认仍为 320*240）。
- 更新了 README，增加了对 ResolutionAdapter 的说明。
- 更新了 demo 以支持 ResolutionAdapter。

Version 1.3 (Jul 20, 2025)
- 增加了 UIManager 以实现页面间的导航（进入和返回）功能。
- 使用 UIManager 重构了 demo。

Version 2.0 (Jul 21, 2025)
- 进行了大规模代码重构，以提高可读性和可维护性。
- 为所有类和方法添加了全面的文档字符串，以提供清晰的内联文档。
- 集成了完整的类型注解。
- 完善了 README。

Version 2.1 (Jul 23, 2025)
- 尝试改进Page为树型结构（由 @HYKMAX 实现）。
