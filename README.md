# MaixPy-UI-Lib：一款为 MaixPy 开发的轻量级 UI 组件库

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/aristorechina/MaixPy-UI-Lib/blob/main/LICENSE) [![Version](https://img.shields.io/badge/version-2.3-brightgreen.svg)](https://github.com/aristorechina/MaixPy-UI-Lib)

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

`pip install maixpy-ui-lib`

---

## 🚀快速上手

您可以通过运行仓库中的示例程序 `examples/demo.py` 来快速熟悉本项目的基本功能和使用方法。

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
from maixpy_ui import Button, ButtonManager
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

#### `Button` 类
创建一个可交互的按钮组件。该组件可以响应触摸事件，并在按下时改变外观，释放时执行回调函数。

##### 构造函数: `__init__`
|        参数        |          类型          |                    描述                     |      默认值       |
| :----------------: | :--------------------: | :-----------------------------------------: | :---------------: |
|       `rect`       |    `Sequence[int]`     | 按钮的位置和尺寸 `[x, y, w, h]`。**必需**。 |         -         |
|      `label`       |         `str`          |        按钮上显示的文本。**必需**。         |         -         |
|     `callback`     |   `Callable | None`    |    当按钮被点击时调用的函数。**必需**。     |         -         |
|     `bg_color`     | `Sequence[int] | None` |            背景颜色 (R, G, B)。             |  `(50, 50, 50)`   |
|  `pressed_color`   | `Sequence[int] | None` |       按下状态的背景颜色 (R, G, B)。        |  `(0, 120, 220)`  |
|    `text_color`    |    `Sequence[int]`     |            文本颜色 (R, G, B)。             | `(255, 255, 255)` |
|   `border_color`   |    `Sequence[int]`     |            边框颜色 (R, G, B)。             | `(200, 200, 200)` |
| `border_thickness` |         `int`          |             边框厚度（像素）。              |        `2`        |
|    `text_scale`    |        `float`         |              文本的缩放比例。               |       `1.5`       |
|       `font`       |      `str | None`      |            使用的字体文件路径。             |      `None`       |
|     `align_h`      |         `str`          | 水平对齐方式 ('left', 'center', 'right')。  |    `'center'`     |
|     `align_v`      |         `str`          | 垂直对齐方式 ('top', 'center', 'bottom')。  |    `'center'`     |

##### 方法 (Methods)
|        方法         |                             参数                             |             描述             |
| :-----------------: | :----------------------------------------------------------: | :--------------------------: |
|     `draw(img)`     |     `img` (`maix.image.Image`): 将要绘制按钮的目标图像。     |   在指定的图像上绘制按钮。   |
| `handle_event(...)` | `x` (`int`): 触摸点的 X 坐标。<br>`y` (`int`): 触摸点的 Y 坐标。<br>`pressed` (`bool|int`): 触摸屏是否被按下。<br>`img_w` (`int`): 图像缓冲区的宽度。<br>`img_h` (`int`): 图像缓冲区的高度。<br>`disp_w` (`int`): 显示屏的宽度。<br>`disp_h` (`int`): 显示屏的高度。 | 处理触摸事件并更新按钮状态。 |

#### `ButtonManager` 类
管理一组按钮的事件处理和绘制。

##### 构造函数: `__init__`
| 参数   | 类型                      | 描述             |
| :----: | :-----------------------: | :--------------: |
| `ts`   | `touchscreen.TouchScreen` | 触摸屏设备实例。**必需**。 |
| `disp` | `display.Display`         | 显示设备实例。**必需**。   |

##### 方法 (Methods)
|         方法         |                       参数                       |                描述                |
| :------------------: | :----------------------------------------------: | :--------------------------------: |
| `add_button(button)` |   `button` (`Button`): 要添加的 Button 实例。    |      向管理器中添加一个按钮。      |
| `handle_events(img)` | `img` (`maix.image.Image`): 绘制按钮的目标图像。 | 处理所有受管按钮的事件并进行绘制。 |

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
from maixpy_ui import Slider, SliderManager
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

#### `Slider` 类
创建一个可拖动的滑块组件，用于在一定范围内选择一个值。

##### 构造函数: `__init__`
|          参数          |       类型        |                    描述                     |      默认值       |
| :--------------------: | :---------------: | :-----------------------------------------: | :---------------: |
|         `rect`         |  `Sequence[int]`  | 滑块的位置和尺寸 `[x, y, w, h]`。**必需**。 |         -         |
|        `scale`         |      `float`      |            滑块的整体缩放比例。             |       `1.0`       |
|       `min_val`        |       `int`       |               滑块的最小值。                |        `0`        |
|       `max_val`        |       `int`       |               滑块的最大值。                |       `100`       |
|     `default_val`      |       `int`       |               滑块的默认值。                |       `50`        |
|       `callback`       | `Callable | None` |   值改变时调用的函数，接收新值作为参数。    |      `None`       |
|        `label`         |       `str`       |            滑块上方的标签文本。             |       `""`        |
|     `track_color`      |  `Sequence[int]`  |          滑轨背景颜色 (R, G, B)。           |  `(60, 60, 60)`   |
|    `progress_color`    |  `Sequence[int]`  |         滑轨进度条颜色 (R, G, B)。          |  `(0, 120, 220)`  |
|     `handle_color`     |  `Sequence[int]`  |          滑块手柄颜色 (R, G, B)。           | `(255, 255, 255)` |
| `handle_border_color`  |  `Sequence[int]`  |        滑块手柄边框颜色 (R, G, B)。         | `(100, 100, 100)` |
| `handle_pressed_color` |  `Sequence[int]`  |         按下时手柄颜色 (R, G, B)。          | `(220, 220, 255)` |
|     `label_color`      |  `Sequence[int]`  |          标签文本颜色 (R, G, B)。           | `(200, 200, 200)` |
|   `tooltip_bg_color`   |  `Sequence[int]`  |       拖动时提示框背景色 (R, G, B)。        |    `(0, 0, 0)`    |
|  `tooltip_text_color`  |  `Sequence[int]`  |      拖动时提示框文本颜色 (R, G, B)。       | `(255, 255, 255)` |
| `show_tooltip_on_drag` |   `bool | int`    |        是否在拖动时显示数值提示框。         |      `True`       |

##### 方法 (Methods)
|        方法         |                             参数                             |             描述             |
| :-----------------: | :----------------------------------------------------------: | :--------------------------: |
|     `draw(img)`     |     `img` (`maix.image.Image`): 将要绘制滑块的目标图像。     |   在指定的图像上绘制滑块。   |
| `handle_event(...)` | `x` (`int`): 触摸点的 X 坐标。<br>`y` (`int`): 触摸点的 Y 坐标。<br>`pressed` (`bool|int`): 触摸屏是否被按下。<br>`img_w` (`int`): 图像缓冲区的宽度。<br>`img_h` (`int`): 图像缓冲区的高度。<br>`disp_w` (`int`): 显示屏的宽度。<br>`disp_h` (`int`): 显示屏的高度。 | 处理触摸事件并更新滑块状态。 |

#### `SliderManager` 类
管理一组滑块的事件处理和绘制。

##### 构造函数: `__init__`
| 参数   | 类型                      | 描述             |
| :----: | :-----------------------: | :--------------: |
| `ts`   | `touchscreen.TouchScreen` | 触摸屏设备实例。**必需**。 |
| `disp` | `display.Display`         | 显示设备实例。**必需**。   |

##### 方法 (Methods)
|         方法         |                       参数                       |                描述                |
| :------------------: | :----------------------------------------------: | :--------------------------------: |
| `add_slider(slider)` |   `slider` (`Slider`): 要添加的 Slider 实例。    |      向管理器中添加一个滑块。      |
| `handle_events(img)` | `img` (`maix.image.Image`): 绘制滑块的目标图像。 | 处理所有受管滑块的事件并进行绘制。 |

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
from maixpy_ui import Switch, SwitchManager
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

#### `Switch` 类
创建一个开关（Switch）组件，用于在开/关两种状态之间切换。

##### 构造函数: `__init__`
|           参数           |       类型        |                         描述                         |      默认值       |
| :----------------------: | :---------------: | :--------------------------------------------------: | :---------------: |
|        `position`        |  `Sequence[int]`  |        开关的左上角坐标 `[x, y]`。**必需**。         |         -         |
|         `scale`          |      `float`      |                 开关的整体缩放比例。                 |       `1.0`       |
|         `is_on`          |   `bool | int`    |             开关的初始状态，True 为开。              |      `False`      |
|        `callback`        | `Callable | None` | 状态切换时调用的函数，接收一个布尔值参数表示新状态。 |      `None`       |
|        `on_color`        |  `Sequence[int]`  |           开启状态下的背景颜色 (R, G, B)。           |  `(30, 200, 30)`  |
|       `off_color`        |  `Sequence[int]`  |           关闭状态下的背景颜色 (R, G, B)。           | `(100, 100, 100)` |
|      `handle_color`      |  `Sequence[int]`  |                手柄的颜色 (R, G, B)。                | `(255, 255, 255)` |
|  `handle_pressed_color`  |  `Sequence[int]`  |             按下时手柄的颜色 (R, G, B)。             | `(220, 220, 255)` |
| `handle_radius_increase` |       `int`       |                按下时手柄半径增加量。                |        `2`        |

##### 方法 (Methods)
|        方法         |                             参数                             |               描述               |
| :-----------------: | :----------------------------------------------------------: | :------------------------------: |
|     `toggle()`      |                              -                               | 切换开关的状态，并执行回调函数。 |
|     `draw(img)`     |     `img` (`maix.image.Image`): 将要绘制开关的目标图像。     |     在指定的图像上绘制开关。     |
| `handle_event(...)` | `x` (`int`): 触摸点的 X 坐标。<br>`y` (`int`): 触摸点的 Y 坐标。<br>`pressed` (`bool|int`): 触摸屏是否被按下。<br>`img_w` (`int`): 图像缓冲区的宽度。<br>`img_h` (`int`): 图像缓冲区的高度。<br>`disp_w` (`int`): 显示屏的宽度。<br>`disp_h` (`int`): 显示屏的高度。 |   处理触摸事件并更新开关状态。   |

#### `SwitchManager` 类
管理一组开关的事件处理和绘制。

##### 构造函数: `__init__`
| 参数   | 类型                      | 描述             |
| :----: | :-----------------------: | :--------------: |
| `ts`   | `touchscreen.TouchScreen` | 触摸屏设备实例。**必需**。 |
| `disp` | `display.Display`         | 显示设备实例。**必需**。   |

##### 方法 (Methods)
|         方法         |                       参数                       |                描述                |
| :------------------: | :----------------------------------------------: | :--------------------------------: |
| `add_switch(switch)` |   `switch` (`Switch`): 要添加的 Switch 实例。    |      向管理器中添加一个开关。      |
| `handle_events(img)` | `img` (`maix.image.Image`): 绘制开关的目标图像。 | 处理所有受管开关的事件并进行绘制。 |

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
from maixpy_ui import Checkbox, CheckboxManager
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

#### `Checkbox` 类
创建一个复选框（Checkbox）组件，可独立选中或取消。

##### 构造函数: `__init__`
|        参数         |       类型        |                         描述                         |      默认值       |
| :-----------------: | :---------------: | :--------------------------------------------------: | :---------------: |
|     `position`      |  `Sequence[int]`  |       复选框的左上角坐标 `[x, y]`。**必需**。        |         -         |
|       `label`       |       `str`       |           复选框旁边的标签文本。**必需**。           |         -         |
|       `scale`       |      `float`      |                复选框的整体缩放比例。                |       `1.0`       |
|    `is_checked`     |   `bool | int`    |           复选框的初始状态，True 为选中。            |      `False`      |
|     `callback`      | `Callable | None` | 状态切换时调用的函数，接收一个布尔值参数表示新状态。 |      `None`       |
|     `box_color`     |  `Sequence[int]`  |            未选中时方框的颜色 (R, G, B)。            | `(200, 200, 200)` |
| `box_checked_color` |  `Sequence[int]`  |             选中时方框的颜色 (R, G, B)。             |  `(0, 120, 220)`  |
|    `check_color`    |  `Sequence[int]`  |          选中标记（对勾）的颜色 (R, G, B)。          | `(255, 255, 255)` |
|    `text_color`     |  `Sequence[int]`  |              标签文本的颜色 (R, G, B)。              | `(200, 200, 200)` |
|   `box_thickness`   |       `int`       |                   方框边框的厚度。                   |        `2`        |

##### 方法 (Methods)
|        方法         |                             参数                             |                描述                |
| :-----------------: | :----------------------------------------------------------: | :--------------------------------: |
|     `toggle()`      |                              -                               | 切换复选框的选中状态，并执行回调。 |
|     `draw(img)`     |    `img` (`maix.image.Image`): 将要绘制复选框的目标图像。    |     在指定的图像上绘制复选框。     |
| `handle_event(...)` | `x` (`int`): 触摸点的 X 坐标。<br>`y` (`int`): 触摸点的 Y 坐标。<br>`pressed` (`bool|int`): 触摸屏是否被按下。<br>`img_w` (`int`): 图像缓冲区的宽度。<br>`img_h` (`int`): 图像缓冲区的高度。<br>`disp_w` (`int`): 显示屏的宽度。<br>`disp_h` (`int`): 显示屏的高度。 |   处理触摸事件并更新复选框状态。   |

#### `CheckboxManager` 类
管理一组复选框的事件处理和绘制。

##### 构造函数: `__init__`
| 参数   | 类型                      | 描述             |
| :----: | :-----------------------: | :--------------: |
| `ts`   | `touchscreen.TouchScreen` | 触摸屏设备实例。**必需**。 |
| `disp` | `display.Display`         | 显示设备实例。**必需**。   |

##### 方法 (Methods)
|           方法           |                        参数                        |                 描述                 |
| :----------------------: | :------------------------------------------------: | :----------------------------------: |
| `add_checkbox(checkbox)` | `checkbox` (`Checkbox`): 要添加的 Checkbox 实例。  |      向管理器中添加一个复选框。      |
|   `handle_events(img)`   | `img` (`maix.image.Image`): 绘制复选框的目标图像。 | 处理所有受管复选框的事件并进行绘制。 |

---

### 5. 单选框 (RadioButton)

允许用户从一组互斥的选项中只选择一项。

#### 使用方式
1.  创建一个 `RadioManager` 实例。**注意**：`RadioManager` 构造时需要接收 `default_value` 和一个全局 `callback`。
2.  创建 `RadioButton` 实例，每个按钮必须有唯一的 `value`。
3.  使用 `manager.add_radio()` 添加它们。
4.  在主循环中，调用 `manager.handle_events(img)`。管理器会自动处理互斥逻辑。

#### 示例
```python
from maix import display, camera, app, touchscreen, image
from maixpy_ui import RadioButton, RadioManager
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

#### `RadioButton` 类
创建一个单选框（RadioButton）项。通常与 `RadioManager` 结合使用。

##### 构造函数: `__init__`
| 参数                    | 类型            | 描述                              | 默认值            |
| :---------------------: | :-------------: | :-------------------------------: | :---------------: |
| `position`              | `Sequence[int]` | 单选框圆圈的左上角坐标 `[x, y]`。**必需**。 | -               |
| `label`                 | `str`           | 按钮旁边的标签文本。**必需**。              | -               |
| `value`                 | `any`           | 与此单选框关联的唯一值。**必需**。          | -               |
| `scale`                 | `float`         | 组件的整体缩放比例。              | `1.0`             |
| `circle_color`          | `Sequence[int]` | 未选中时圆圈的颜色 (R, G, B)。    | `(200, 200, 200)` |
| `circle_selected_color` | `Sequence[int]` | 选中时圆圈的颜色 (R, G, B)。      | `(0, 120, 220)`   |
| `dot_color`             | `Sequence[int]` | 选中时中心圆点的颜色 (R, G, B)。  | `(255, 255, 255)` |
| `text_color`            | `Sequence[int]` | 标签文本的颜色 (R, G, B)。        | `(200, 200, 200)` |
| `circle_thickness`      | `int`           | 圆圈边框的厚度。                  | `2`               |

##### 方法 (Methods)
|    方法     |                          参数                          |            描述            |
| :---------: | :----------------------------------------------------: | :------------------------: |
| `draw(img)` | `img` (`maix.image.Image`): 将要绘制单选框的目标图像。 | 在指定的图像上绘制单选框。 |

#### `RadioManager` 类
管理一个单选框组，确保只有一个按钮能被选中。

##### 构造函数: `__init__`
|      参数       |           类型            |                        描述                        | 默认值 |
| :-------------: | :-----------------------: | :------------------------------------------------: | :----: |
|      `ts`       | `touchscreen.TouchScreen` |             触摸屏设备实例。**必需**。             |   -    |
|     `disp`      |     `display.Display`     |              显示设备实例。**必需**。              |   -    |
| `default_value` |           `any`           |                默认选中的按钮的值。                | `None` |
|   `callback`    |     `Callable | None`     | 选中项改变时调用的函数，接收新选中项的值作为参数。 | `None` |

##### 方法 (Methods)
|         方法         |                         参数                         |               描述               |
| :------------------: | :--------------------------------------------------: | :------------------------------: |
|  `add_radio(radio)`  | `radio` (`RadioButton`): 要添加的 RadioButton 实例。 |    向管理器中添加一个单选框。    |
| `handle_events(img)` |  `img` (`maix.image.Image`): 绘制单选框的目标图像。  | 处理所有单选框的事件并进行绘制。 |

---

### 6. 分辨率适配器 (ResolutionAdapter)

一个辅助工具类，用于自动适配不同分辨率的屏幕，以保持UI布局的一致性。

#### 使用方式

1.  创建一个 `ResolutionAdapter` 实例，并指定目标屏幕尺寸和可选的设计基础分辨率。
2.  基于您的设计基础分辨率，定义组件的原始 `rect`、`position` 等参数。
3.  调用 `adapter.scale_rect()` 等方法，将原始参数转换为适配后的值。
4.  使用转换后的值来创建您的UI组件。

#### 示例

```python
from maix import display, camera, app, touchscreen
from maixpy_ui import Button, ButtonManager, ResolutionAdapter
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

#### `ResolutionAdapter` 类

##### 构造函数: `__init__`
|       参数       | 类型  |             描述             | 默认值 |
| :--------------: | :---: | :--------------------------: | :----: |
| `display_width`  | `int` | 目标显示屏的宽度。**必需**。 |   -    |
| `display_height` | `int` | 目标显示屏的高度。**必需**。 |   -    |
|   `base_width`   | `int` |      UI设计的基准宽度。      | `320`  |
|  `base_height`   | `int` |      UI设计的基准高度。      | `240`  |

##### 方法 (Methods)
|            方法             |                            参数                             |                描述                |     返回值      |
| :-------------------------: | :---------------------------------------------------------: | :--------------------------------: | :-------------: |
|   `scale_position(x, y)`    |  `x` (`int`): 原始 X 坐标。<br>`y` (`int`): 原始 Y 坐标。   |      缩放一个坐标点 (x, y)。       | `Sequence[int]` |
| `scale_size(width, height)` | `width` (`int`): 原始宽度。<br>`height` (`int`): 原始高度。 |   缩放一个尺寸 (width, height)。   | `Sequence[int]` |
|     `scale_rect(rect)`      |       `rect` (`list[int]`): 原始矩形 `[x, y, w, h]`。       |           缩放一个矩形。           | `Sequence[int]` |
|    `scale_value(value)`     |              `value` (`int|float`): 原始数值。              | 缩放一个通用数值，如半径、厚度等。 |     `float`     |

### 7. 页面与 UI 管理器 (Page and UIManager)

用于构建多页面应用，并管理页面间的树型导航。

#### 使用方式
1.  创建一个全局的 `UIManager` 实例。
2.  定义继承自 `Page` 的自定义页面类，并在构造函数中为页面命名。
3.  在父页面中，创建子页面的实例，并使用 `parent.add_child()` 方法来构建页面树。
4.  使用 `ui_manager.set_root_page()` 设置应用的根页面。
5.  在页面内部，通过 `self.ui_manager` 调用导航方法，如 `navigate_to_child()`、`navigate_to_parent()`、`navigate_to_root()` 等。
6.  在主循环中，持续调用 `ui_manager.update(img)` 来驱动当前活动页面的更新和绘制。

#### 示例

```python
from maix import display, camera, app, touchscreen, image
from maixpy_ui import Page, UIManager, Button, ButtonManager
import time

# --------------------------------------------------------------------------
# 1. 初始化硬件 & 全局资源
# --------------------------------------------------------------------------
disp = display.Display()
ts = touchscreen.TouchScreen()
screen_w, screen_h = disp.width(), disp.height()
cam = camera.Camera(screen_w, screen_h)

# 预创建颜色对象
COLOR_WHITE = image.Color(255, 255, 255)
COLOR_GREY = image.Color(150, 150, 150)
COLOR_GREEN = image.Color(30, 200, 30)
COLOR_BLUE = image.Color(0, 120, 220)

def get_background():
    if cam:
        img = cam.read()
        if img: return img
    return image.new(size=(screen_w, screen_h), color=(10, 20, 30))

# --------------------------------------------------------------------------
# 2. 定义页面类
# --------------------------------------------------------------------------

class BasePage(Page):
    """一个包含通用功能的页面基类，例如绘制调试信息"""
    def draw_path_info(self, img: image.Image):
        """在屏幕右下角绘制当前的导航路径"""
        info = self.ui_manager.get_navigation_info()
        path_str = " > ".join(info['current_path'])
        
        # 计算文本尺寸
        text_scale = 1.0
        text_size = image.string_size(path_str, scale=text_scale)
        
        # 计算绘制位置（右下角，留出一些边距）
        padding = 10
        text_x = screen_w - text_size.width() - padding
        text_y = screen_h - text_size.height() - padding
        
        # 绘制文本
        img.draw_string(text_x, text_y, path_str, scale=text_scale, color=COLOR_GREY)
        
    def update(self, img: image.Image):
        """子类应该重写此方法，并在末尾调用 super().update(img) 来绘制调试信息"""
        self.draw_path_info(img)

class PageA1(BasePage):
    """最深层的页面"""
    def __init__(self, ui_manager):
        super().__init__(ui_manager, name="page_a1")
        self.btn_manager = ButtonManager(ts, disp)
        self.btn_manager.add_button(Button([40, 150, 400, 80], "Back to Parent (-> Page A)", lambda: self.ui_manager.navigate_to_parent()))
        self.btn_manager.add_button(Button([40, 250, 400, 80], "Go Back in History", lambda: self.ui_manager.go_back()))
        self.btn_manager.add_button(Button([40, 350, 400, 80], "Go to Root (Home)", lambda: self.ui_manager.navigate_to_root(), bg_color=COLOR_GREEN))

    def update(self, img):
        img.draw_string(20, 20, "Page A.1 (Deepest)", scale=2.0, color=COLOR_WHITE)
        history = self.ui_manager.navigation_history
        prev_page_name = history[-1].name if history else "None"
        img.draw_string(20, 80, f"'Go Back' will return to '{prev_page_name}'.", scale=1.2, color=COLOR_GREY)
        self.btn_manager.handle_events(img)
        super().update(img) # 调用基类的方法来绘制路径信息

class PageA(BasePage):
    """中间层页面 A"""
    def __init__(self, ui_manager):
        super().__init__(ui_manager, name="page_a")
        self.btn_manager = ButtonManager(ts, disp)
        self.btn_manager.add_button(Button([80, 150, 350, 80], "Go to Page A.1", lambda: self.ui_manager.navigate_to_child("page_a1")))
        self.btn_manager.add_button(Button([20, 400, 250, 80], "Back to Parent", lambda: self.ui_manager.navigate_to_parent()))
        self.add_child(PageA1(self.ui_manager))

    def update(self, img):
        img.draw_string(20, 20, "Page A", scale=2.5, color=COLOR_WHITE)
        self.btn_manager.handle_events(img)
        super().update(img)

class PageB(BasePage):
    """中间层页面 B"""
    def __init__(self, ui_manager):
        super().__init__(ui_manager, name="page_b")
        self.btn_manager = ButtonManager(ts, disp)
        self.btn_manager.add_button(Button([80, 150, 350, 80], "Jump to Page A.1 by Path", lambda: self.ui_manager.navigate_to_path(["page_a", "page_a1"])))
        self.btn_manager.add_button(Button([20, 400, 250, 80], "Back to Parent", lambda: self.ui_manager.navigate_to_parent()))

    def update(self, img):
        img.draw_string(20, 20, "Page B", scale=2.5, color=COLOR_WHITE)
        img.draw_string(20, 80, "From here, we'll jump to A.1.", scale=1.2, color=COLOR_GREY)
        img.draw_string(20, 110, "This will make 'Go Back' and 'Back to Parent' different on the next page.", scale=1.2, color=COLOR_GREY)
        self.btn_manager.handle_events(img)
        super().update(img)

class RootPage(BasePage):
    """根页面"""
    def __init__(self, ui_manager):
        super().__init__(ui_manager, name="root")
        self.btn_manager = ButtonManager(ts, disp)
        self.btn_manager.add_button(Button([80, 150, 350, 80], "Path 1: Go to Page A", lambda: self.ui_manager.navigate_to_child("page_a")))
        self.btn_manager.add_button(Button([80, 300, 350, 80], "Path 2: Go to Page B", lambda: self.ui_manager.navigate_to_child("page_b")))
        self.add_child(PageA(self.ui_manager))
        self.add_child(PageB(self.ui_manager))

    def update(self, img):
        img.draw_string(20, 20, "Root Page (Home)", scale=2.5, color=COLOR_WHITE)
        img.draw_string(20, 80, "Try both paths to see how 'Go Back' behaves differently.", scale=1.2, color=COLOR_GREY)
        self.btn_manager.handle_events(img)
        super().update(img) # 调用基类的方法来绘制路径信息

# --------------------------------------------------------------------------
# 3. 主程序逻辑
# --------------------------------------------------------------------------
if __name__ == "__main__":
    ui_manager = UIManager()
    root_page = RootPage(ui_manager)
    ui_manager.set_root_page(root_page)

    print("Navigation demo with persistent path display running.")

    while not app.need_exit():
        img = get_background()
        ui_manager.update(img)
        disp.show(img)
        time.sleep(0.02)
```

#### `Page` 类
页面（Page）的基类，支持树型父子节点结构。所有具体的UI页面都应继承此类。

##### 构造函数: `__init__`
|    参数    |    类型     |                     描述                      | 默认值 |
| :--------: | :---------: | :-------------------------------------------: | :----: |
| `ui_manager` | `UIManager` |      用于页面导航的 UIManager 实例。**必需**。      |   -    |
|   `name`   |    `str`    | 页面的唯一名称标识符，用于在父页面中查找。 |  `""`  |

##### 方法 (Methods)
|        方法         |                      参数                      |                           描述                           |      返回值      |
| :-----------------: | :--------------------------------------------: | :------------------------------------------------------: | :--------------: |
| `add_child(page)`   |      `page` (`Page`): 要添加的子页面实例。       |   将一个页面添加为当前页面的子节点，以构建页面树。   |        -         |
| `remove_child(page)` |     `page` (`Page`): 要移除的子页面实例。      |                     从当前页面移除一个子节点。                     |      `bool`      |
| `get_child(name)`   |           `name` (`str`): 子页面的名称。           |            根据名称获取子页面，用于自定义导航逻辑。            |  `Page \| None`  |
|     `on_enter()`      |                       -                        |     当页面进入视图时调用。子类可重写以实现初始化逻辑。     |        -         |
|      `on_exit()`      |                       -                        |     当页面离开视图时调用。子类可重写以实现清理逻辑。     |        -         |
| `on_child_enter()`  |      `child` (`Page`): 进入视图的子页面。      |   当此页面的一个子页面进入视图时调用。父页面可重写。   |        -         |
| `on_child_exit()`   |      `child` (`Page`): 离开视图的子页面。      |   当此页面的一个子页面离开视图时调用。父页面可重写。   |        -         |
|     `update(img)`     | `img` (`maix.image.Image`): 用于绘制的图像缓冲区。 | 每帧调用的更新和绘制方法。**子类必须重写此方法**。 |        -         |

#### `UIManager` 类
UI 管理器，基于树型页面结构提供灵活的导航功能。

##### 构造函数: `__init__`
|   参数    |    类型     |             描述             | 默认值 |
| :-------: | :---------: | :--------------------------: | :----: |
| `root_page` | `Page | None` | 根页面实例，如果为None则需要后续设置。 | `None` |

##### 方法 (Methods)
|           方法           |                            参数                            |                             描述                             |      返回值      |
| :----------------------: | :--------------------------------------------------------: | :----------------------------------------------------------: | :--------------: |
|   `set_root_page(page)`    |            `page` (`Page`): 新的根页面实例。             |           设置或重置UI管理器的根页面，并清空历史。           |        -         |
|   `get_current_page()`   |                             -                              |                     获取当前活动的页面。                     |  `Page \| None`  |
| `navigate_to_child(name)`  |               `name` (`str`): 子页面的名称。               |             导航到当前页面的指定名称的子页面。             |      `bool`      |
|  `navigate_to_parent()`  |                             -                              |                 导航到当前页面的父页面。                 |      `bool`      |
|   `navigate_to_root()`   |                             -                              |                 直接导航到树的根页面。                 |      `bool`      |
|  `navigate_to_path(path)`  | `path` (`List[str]`): 从根页面开始的绝对路径。 |                   根据绝对路径导航到指定页面。                   |      `bool`      |
|       `go_back()`        |                             -                              |             返回到导航历史记录中的前一个页面。             |      `bool`      |
|    `get_navigation_info()`     |                             -                              | 获取包含当前路径、历史深度等信息的字典，用于调试或显示。 |      `dict`      |
|      `update(img)`       |     `img` (`maix.image.Image`): 用于绘制的图像缓冲区。     |     更新当前活动页面的状态。此方法应在主循环中每帧调用。     |        -         |
---

## ⚖️许可协议

本项目基于 **Apache License, Version 2.0** 许可。详细信息请参阅代码文件中的许可证说明。
