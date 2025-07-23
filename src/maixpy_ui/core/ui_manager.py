# -*- coding: utf-8 -*-
__author__ = 'HYKMAX'

import maix.image as image
from typing import List, Optional

class Page:
    """页面（Page）的基类，支持树型父子节点结构。

    每个页面可以有一个父页面和多个子页面，形成树型结构。
    这种设计允许更灵活的页面组织和导航。

    Attributes:
        ui_manager (UIManager): 管理此页面的 UIManager 实例。
        name (str): 页面的名称，用于在父页面中唯一标识。
        parent (Page | None): 父页面，如果为 None 则表示根页面。
        children (List[Page]): 子页面列表。
    """

    def __init__(self, ui_manager: 'UIManager', name: str = ""):
        """初始化页面。

        Args:
            ui_manager (UIManager): 用于页面导航的 UIManager 实例。
            name (str): 页面的唯一名称标识符。
        """
        self.ui_manager = ui_manager
        self.name = name
        self.parent = None
        self.children = []

    def add_child(self, child_page: 'Page'):
        """添加一个子页面。

        Args:
            child_page (Page): 要添加的子页面实例。

        Raises:
            ValueError: 如果子页面的名称已存在或为空。
            TypeError: 如果传入的不是 Page 实例。
        """
        if not isinstance(child_page, Page):
            raise TypeError("只能添加 Page 类的实例")
        if not child_page.name:
            raise ValueError("子页面必须有一个非空的名称")
        if self.get_child(child_page.name) is not None:
            raise ValueError(f"名称为 '{child_page.name}' 的子页面已存在")
        
        child_page.parent = self
        self.children.append(child_page)

    def remove_child(self, child_page: 'Page'):
        """移除一个子页面。

        Args:
            child_page (Page): 要移除的子页面实例。

        Returns:
            bool: 如果成功移除则返回 True，否则返回 False。
        """
        if child_page in self.children:
            child_page.parent = None
            self.children.remove(child_page)
            return True
        return False

    def get_child(self, name: str) -> Optional['Page']:
        """根据名称获取子页面。

        Args:
            name (str): 子页面的名称。

        Returns:
            Page | None: 如果找到则返回子页面实例，否则返回 None。
        """
        for child in self.children:
            if child.name == name:
                return child
        return None

    def get_root(self) -> 'Page':
        """获取当前页面的根页面。

        Returns:
            Page: 树结构的根页面。
        """
        current = self
        while current.parent:
            current = current.parent
        return current

    def get_path(self) -> List[str]:
        """获取从根页面到当前页面的路径。

        Returns:
            List[str]: 页面名称的路径列表。
        """
        path = []
        current = self
        while current:
            if current.name:  # 只有非空名称才加入路径
                path.insert(0, current.name)
            current = current.parent
        return path

    def get_depth(self) -> int:
        """获取当前页面在树中的深度。

        Returns:
            int: 页面深度，根页面深度为0。
        """
        depth = 0
        current = self.parent
        while current:
            depth += 1
            current = current.parent
        return depth

    def find_page_by_path(self, path: List[str]) -> Optional['Page']:
        """根据路径查找页面。

        Args:
            path (List[str]): 页面路径，从当前页面开始的相对路径。

        Returns:
            Page | None: 如果找到则返回页面实例，否则返回 None。
        """
        if not path:
            return self
        
        child = self.get_child(path[0])
        if child is None:
            return None
        
        if len(path) == 1:
            return child
        else:
            return child.find_page_by_path(path[1:])

    def on_enter(self):
        """当页面进入视图时调用。

        子类可以重写此方法来实现页面进入时的初始化逻辑。
        """
        pass

    def on_exit(self):
        """当页面离开视图时调用。

        子类可以重写此方法来实现页面退出时的清理逻辑。
        """
        pass

    def on_child_enter(self, child: 'Page'):
        """当子页面进入视图时调用。

        Args:
            child (Page): 进入视图的子页面。
        """
        pass

    def on_child_exit(self, child: 'Page'):
        """当子页面离开视图时调用。

        Args:
            child (Page): 离开视图的子页面。
        """
        pass

    def update(self, img: image.Image):
        """每帧调用的更新和绘制方法。

        子类必须重写此方法以实现页面的UI逻辑和绘制。

        Args:
            img (maix.image.Image): 用于绘制的图像缓冲区。

        Raises:
            NotImplementedError: 如果子类没有实现此方法。
        """
        raise NotImplementedError("每个页面都必须实现 update 方法")


class UIManager:
    """UI 管理器，基于树型页面结构提供灵活的导航功能。

    该管理器支持树型页面结构的导航，包括导航到子页面、返回父页面、
    按路径导航等功能。
    """

    def __init__(self, root_page: Optional[Page] = None):
        """初始化UI管理器。

        Args:
            root_page (Page | None): 根页面实例，如果为None则需要后续设置。
        """
        self.root_page = root_page
        self.current_page = root_page
        self.navigation_history = []  # 用于记录导航历史
        
        if root_page:
            root_page.on_enter()

    def set_root_page(self, page: Page):
        """设置根页面。

        Args:
            page (Page): 新的根页面实例。
        """
        if self.current_page:
            self.current_page.on_exit()
        
        self.root_page = page
        self.current_page = page
        self.navigation_history.clear()
        
        if page:
            page.on_enter()

    def get_current_page(self) -> Optional[Page]:
        """获取当前活动的页面。

        Returns:
            Page | None: 当前页面实例，如果没有则返回 None。
        """
        return self.current_page

    def navigate_to_child(self, child_name: str) -> bool:
        """导航到当前页面的指定子页面。

        Args:
            child_name (str): 子页面的名称。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.current_page:
            return False
        
        child = self.current_page.get_child(child_name)
        if child:
            # 记录导航历史
            self.navigation_history.append(self.current_page)
            
            # 通知当前页面和父页面
            self.current_page.on_exit()
            self.current_page.on_child_enter(child)
            
            # 切换页面
            self.current_page = child
            child.on_enter()
            
            return True
        return False

    def navigate_to_parent(self) -> bool:
        """导航到当前页面的父页面。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.current_page or not self.current_page.parent:
            return False
        
        parent = self.current_page.parent
        
        # 通知相关页面
        parent.on_child_exit(self.current_page)
        self.current_page.on_exit()
        
        # 从历史记录中移除（如果存在）
        if self.navigation_history and self.navigation_history[-1] == parent:
            self.navigation_history.pop()
        
        # 切换页面
        self.current_page = parent
        parent.on_enter()
        
        return True

    def navigate_to_root(self) -> bool:
        """导航到根页面。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.root_page:
            return False
        
        return self.navigate_to_page(self.root_page)

    def navigate_to_path(self, path: List[str]) -> bool:
        """根据路径导航到指定页面。

        Args:
            path (List[str]): 从根页面开始的绝对路径。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.root_page or not path:
            return False
        
        target_page = self.root_page.find_page_by_path(path)
        if target_page:
            return self.navigate_to_page(target_page)
        return False

    def navigate_to_relative_path(self, path: List[str]) -> bool:
        """根据相对路径导航到指定页面。

        Args:
            path (List[str]): 从当前页面开始的相对路径。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not self.current_page:
            return False
        
        target_page = self.current_page.find_page_by_path(path)
        if target_page:
            return self.navigate_to_page(target_page)
        return False

    def navigate_to_page(self, target_page: Page) -> bool:
        """直接导航到指定页面。

        Args:
            target_page (Page): 目标页面实例。

        Returns:
            bool: 如果导航成功则返回 True，否则返回 False。
        """
        if not target_page:
            return False
        
        if self.current_page:
            # 记录当前页面到历史（如果不是返回操作）
            if (not self.navigation_history or 
                self.navigation_history[-1] != target_page):
                self.navigation_history.append(self.current_page)
            
            self.current_page.on_exit()
        
        self.current_page = target_page
        target_page.on_enter()
        
        return True

    def go_back(self) -> bool:
        """返回到历史记录中的前一个页面。

        Returns:
            bool: 如果返回成功则返回 True，否则返回 False。
        """
        if not self.navigation_history:
            return False
        
        previous_page = self.navigation_history.pop()
        
        if self.current_page:
            self.current_page.on_exit()
        
        self.current_page = previous_page
        previous_page.on_enter()
        
        return True

    def clear_history(self):
        """清空导航历史记录。"""
        self.navigation_history.clear()

    def get_current_path(self) -> List[str]:
        """获取当前页面的完整路径。

        Returns:
            List[str]: 当前页面的路径。
        """
        if self.current_page:
            return self.current_page.get_path()
        return []

    def get_navigation_info(self) -> dict:
        """获取当前导航状态信息。

        Returns:
            dict: 包含当前页面、路径、历史等信息的字典。
        """
        return {
            'current_page': self.current_page.name if self.current_page else None,
            'current_path': self.get_current_path(),
            'can_go_back': len(self.navigation_history) > 0,
            'can_go_to_parent': (self.current_page and 
                                self.current_page.parent is not None),
            'history_depth': len(self.navigation_history),
            'page_depth': (self.current_page.get_depth() 
                          if self.current_page else 0)
        }

    def update(self, img: image.Image):
        """更新当前活动页面的状态。

        此方法应在主循环中每帧调用，它会调用当前页面的 `update` 方法。

        Args:
            img (maix.image.Image): 用于绘制的图像缓冲区。
        """
        if self.current_page:
            self.current_page.update(img)
