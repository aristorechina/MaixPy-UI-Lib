"""
MaixPy-UI-Lib: A lightweight UI component library for MaixPy

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

from .components import (
    Button, ButtonManager,
    Slider, SliderManager,
    Switch, SwitchManager,
    Checkbox, CheckboxManager,
    RadioButton, RadioManager
)

from .core import (
    Page,
    UIManager,
    ResolutionAdapter
)

__version__ = "2.3"
__author__ = "Aristore, levi_jia, HYKMAX"
__license__ = "Apache-2.0"

__all__ = [
    "Button", "Slider", "Switch", "Checkbox", "RadioButton",
    "ButtonManager", "SliderManager", "SwitchManager", "CheckboxManager", "RadioManager",
    "Page", "UIManager", "ResolutionAdapter"
]