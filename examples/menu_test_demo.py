#!/usr/bin/env python3
import maix
from maix import app, camera, display, touchscreen, image, time

from typing import Dict, Any, List, Callable

from maixpy_ui import (
    Page, UIManager, Button, ButtonManager,
    ResolutionAdapter
)

class NavigationTracker:
    """Track navigation patterns and statistics"""
    
    def __init__(self):
        self.navigation_log = []
        self.visit_count = {}
        self.max_depth_reached = 0
        self.total_navigations = 0
        self.cross_level_jumps = 0
        self.failed_navigations = 0
    
    def log_navigation(self, from_page: str, to_page: str, nav_type: str, depth: int, success: bool = True):
        """Log a navigation event"""
        self.total_navigations += 1
        if not success:
            self.failed_navigations += 1
            return
            
        self.max_depth_reached = max(self.max_depth_reached, depth)
        
        if nav_type == "cross_level":
            self.cross_level_jumps += 1
        
        self.visit_count[to_page] = self.visit_count.get(to_page, 0) + 1
        
        log_entry = {
            "from": from_page,
            "to": to_page,
            "type": nav_type,
            "depth": depth,
            "timestamp": time.time(),
            "success": success
        }
        self.navigation_log.append(log_entry)
        
        # Keep only last 30 entries for larger screen
        if len(self.navigation_log) > 30:
            self.navigation_log.pop(0)
    
    def get_stats(self):
        """Get navigation statistics"""
        return {
            "total_navigations": self.total_navigations,
            "max_depth": self.max_depth_reached,
            "cross_level_jumps": self.cross_level_jumps,
            "failed_navigations": self.failed_navigations,
            "unique_pages_visited": len(self.visit_count),
            "most_visited": max(self.visit_count.items(), key=lambda x: x[1]) if self.visit_count else ("None", 0)
        }


# Fixed UIManager with corrected path navigation
class FixedUIManager(UIManager):
    """Fixed UI Manager with corrected path navigation logic"""
    
    def navigate_to_path(self, path: List[str]) -> bool:
        """Fixed path navigation - handles both absolute and relative paths"""
        if not path:
            return False
        
        print(f"UIManager: Navigating to path: {path}")
        
        # If path starts with root, remove it for searching
        search_path = path[1:] if path and path[0] == "root" else path
        
        if not search_path:
            # Path was just ["root"], navigate to root
            return self.navigate_to_root()
        
        # Find target page from root
        if self.root_page:
            target_page = self.root_page.find_page_by_path(search_path)
            print(f"UIManager: Found target page: {target_page.name if target_page else 'None'}")
            
            if target_page:
                return self.navigate_to_page(target_page)
        
        print(f"UIManager: Failed to find path: {path}")
        return False
    
    def debug_tree_structure(self, page=None, level=0):
        """Debug method to print tree structure"""
        if page is None:
            page = self.root_page
        
        if page:
            indent = "  " * level
            print(f"{indent}{page.name} (Level {level})")
            for child in page.children:
                self.debug_tree_structure(child, level + 1)


class TestPage(Page):
    """Base test page for navigation testing - with fixed navigation"""
    
    def __init__(self, ui_manager, name: str, ts, disp, level_info: str = ""):
        super().__init__(ui_manager, name)
        self.ts = ts
        self.disp = disp
        self.button_manager = ButtonManager(ts, disp)
        self.level_info = level_info
        self.visit_count = 0
        self.last_nav_result = ""
        self.tracker = ui_manager.tracker if hasattr(ui_manager, 'tracker') else None
        
    def log_navigation(self, to_page: str, nav_type: str, success: bool = True):
        """Log navigation for tracking"""
        if self.tracker:
            self.tracker.log_navigation(self.name, to_page, nav_type, self.get_depth(), success)
        
        # Update UI feedback
        if success:
            self.last_nav_result = f"OK: {nav_type} to {to_page}"
        else:
            self.last_nav_result = f"FAIL: {nav_type} to {to_page}"
        
        print(f"Navigation: {self.last_nav_result}")
    
    def on_enter(self):
        self.visit_count += 1
        print(f"Entered {self.name} (Level {self.get_depth()}) - Visit #{self.visit_count}")
        if self.level_info:
            print(f"  Info: {self.level_info}")
    
    def create_navigation_buttons(self, custom_buttons: List = None):
        """Create navigation buttons optimized for 640x480"""
        button_y = 10
        
        # Standard back button
        if self.parent:
            self.button_manager.add_button(Button(
                [10, button_y, 80, 30], "Back", 
                lambda: self.navigate_with_log("parent", "back"),
                bg_color=(100, 100, 100)
            ))
        
        # Root button (if not already at root)
        if self.get_depth() > 0:
            self.button_manager.add_button(Button(
                [100, button_y, 70, 30], "Root", 
                lambda: self.navigate_with_log("root", "to_root"),
                bg_color=(50, 100, 150)
            ))
        
        # Level navigation buttons for deep pages
        current_depth = self.get_depth()
        if current_depth > 1:
            self.button_manager.add_button(Button(
                [180, button_y, 60, 30], "L1", 
                lambda: self.navigate_to_absolute_level(1),
                bg_color=(150, 100, 50)
            ))
        
        if current_depth > 2:
            self.button_manager.add_button(Button(
                [250, button_y, 60, 30], "L2", 
                lambda: self.navigate_to_absolute_level(2),
                bg_color=(100, 150, 50)
            ))
        
        if current_depth > 3:
            self.button_manager.add_button(Button(
                [320, button_y, 60, 30], "L3", 
                lambda: self.navigate_to_absolute_level(3),
                bg_color=(150, 150, 50)
            ))
        
        # History back button
        self.button_manager.add_button(Button(
            [390, button_y, 100, 30], "History Back", 
            lambda: self.navigate_with_history(),
            bg_color=(100, 50, 150)
        ))
        
        # Debug button
        self.button_manager.add_button(Button(
            [500, button_y, 80, 30], "Debug Tree", 
            lambda: self.debug_tree_structure(),
            bg_color=(150, 50, 50)
        ))
        
        # Custom buttons
        if custom_buttons:
            for btn_data in custom_buttons:
                self.button_manager.add_button(btn_data)
    
    def debug_tree_structure(self):
        """Debug current tree structure"""
        print(f"\n=== Tree Structure from {self.name} ===")
        if hasattr(self.ui_manager, 'debug_tree_structure'):
            self.ui_manager.debug_tree_structure()
        else:
            root = self.get_root()
            self._print_tree(root, 0)
        print("================================\n")
    
    def _print_tree(self, page, level):
        """Helper to print tree structure"""
        indent = "  " * level
        print(f"{indent}{page.name} (Level {level})")
        for child in page.children:
            self._print_tree(child, level + 1)
    
    def navigate_with_log(self, target: str, nav_type: str):
        """Navigate and log the action"""
        success = False
        
        try:
            if target == "parent":
                success = self.ui_manager.navigate_to_parent()
            elif target == "root":
                success = self.ui_manager.navigate_to_root()
            elif target.startswith("level_"):
                level = int(target.split("_")[1])
                success = self.navigate_to_absolute_level(level)
            else:
                # Try child first
                success = self.ui_manager.navigate_to_child(target)
        except Exception as e:
            print(f"Navigation error: {e}")
            success = False
        
        self.log_navigation(target, nav_type, success)
        return success
    
    def navigate_to_absolute_level(self, target_level: int):
        """Navigate to a specific absolute level in the tree"""
        try:
            current_path = self.get_path()
            print(f"Current path: {current_path}, target level: {target_level}")
            
            if target_level >= len(current_path):
                print(f"Cannot navigate to level {target_level}, current depth is {len(current_path)-1}")
                return False
            
            # Build path to target level (0-indexed, but level display is 1-indexed)
            if target_level == 0:
                return self.ui_manager.navigate_to_root()
            else:
                target_path = current_path[:target_level + 1]
                print(f"Navigating to path: {target_path}")
                success = self.ui_manager.navigate_to_path(target_path)
                if success:
                    self.log_navigation(f"level_{target_level}", "to_level", True)
                else:
                    self.log_navigation(f"level_{target_level}", "to_level", False)
                return success
                
        except Exception as e:
            print(f"Error in navigate_to_absolute_level: {e}")
            self.log_navigation(f"level_{target_level}", "to_level", False)
            return False
    
    def navigate_with_history(self):
        """Use history-based navigation"""
        success = self.ui_manager.go_back()
        self.log_navigation("history_back", "history", success)
        return success
    
    def cross_level_jump(self, target_path: List[str], jump_name: str = "cross_jump"):
        """Perform cross-level jump with error handling"""
        try:
            print(f"Attempting cross-level jump to: {target_path}")
            
            # Validate path exists by checking each level
            current = self.get_root()
            search_path = target_path[1:] if target_path[0] == "root" else target_path
            
            print(f"Search path: {search_path}")
            
            # Verify path exists
            for i, page_name in enumerate(search_path):
                child = current.get_child(page_name)
                if child is None:
                    print(f"Path validation failed at level {i}: '{page_name}' not found in {current.name}")
                    print(f"Available children: {[c.name for c in current.children]}")
                    self.log_navigation("failed_jump", "cross_level", False)
                    return False
                current = child
                print(f"Found {page_name} at level {i}")
            
            # Path exists, now navigate
            success = self.ui_manager.navigate_to_path(target_path)
            target_name = target_path[-1] if target_path else "unknown"
            self.log_navigation(target_name, "cross_level", success)
            return success
            
        except Exception as e:
            print(f"Cross-level jump failed: {e}")
            self.log_navigation("failed_jump", "cross_level", False)
            return False
    
    def update(self, img):
        # Page title - larger for 640x480
        title = f"{self.name.replace('_', ' ').title()}"
        img.draw_string(30, 60, title, image.Color.from_rgb(255, 255, 255), scale=2.0)
        
        # Level info
        level_text = f"Level {self.get_depth()}"
        if self.level_info:
            level_text += f" - {self.level_info}"
        img.draw_string(30, 90, level_text, image.Color.from_rgb(200, 200, 200), scale=1.3)
        
        # Visit count and children info
        info_line = f"Visits: {self.visit_count}"
        if self.children:
            info_line += f" | Children: {len(self.children)}"
        img.draw_string(30, 110, info_line, image.Color.from_rgb(150, 255, 150), scale=1.1)
        
        # Last navigation result
        if self.last_nav_result:
            color = image.Color.from_rgb(150, 255, 150) if "OK:" in self.last_nav_result else image.Color.from_rgb(255, 150, 150)
            img.draw_string(30, 130, f"Last Nav: {self.last_nav_result}", color, scale=0.9)
        
        # Path display at bottom
        path_text = " > ".join(self.get_path())
        img.draw_string(10, 450, f"Path: {path_text}", 
                       image.Color.from_rgb(180, 180, 180), scale=0.9)
        
        # Navigation info
        nav_info = self.ui_manager.get_navigation_info()
        info_text = f"Depth: {nav_info['page_depth']} | History: {nav_info['history_depth']} | Can go back: {nav_info['can_go_back']}"
        img.draw_string(10, 470, info_text, image.Color.from_rgb(150, 150, 150), scale=0.8)
        
        # Handle button events
        self.button_manager.handle_events(img)


class RootTestPage(TestPage):
    """Root level page - Level 0"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "root", ts, disp, "Navigation Test Root")
        self.setup_ui()
    
    def setup_ui(self):
        # Main menu buttons - larger for 640x480
        button_width = 200
        button_height = 40
        start_x = 50
        start_y = 160
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Menu Branch A", 
                   lambda: self.navigate_with_log("branch_a", "child")),
            Button([start_x, start_y + spacing, button_width, button_height], "Menu Branch B", 
                   lambda: self.navigate_with_log("branch_b", "child")),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Deep Test Branch", 
                   lambda: self.navigate_with_log("deep_branch", "child")),
            Button([start_x, start_y + spacing*3, button_width, button_height], "Navigation Stats", 
                   lambda: self.navigate_with_log("nav_stats", "child")),
            
            # Cross-level jump buttons - these should now work!
            Button([start_x + 250, start_y, button_width, button_height], "Jump to Level 3", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3"], "deep_jump"),
                   bg_color=(150, 100, 100)),
            Button([start_x + 250, start_y + spacing, button_width, button_height], "Jump to Level 5", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3", "level4", "level5"], "deepest_jump"),
                   bg_color=(200, 100, 100)),
            Button([start_x + 250, start_y + spacing*2, button_width, button_height], "Jump to Sub A1", 
                   lambda: self.cross_level_jump(["root", "branch_a", "sub_a1"], "branch_jump"),
                   bg_color=(100, 150, 100)),
            
            Button([start_x + 100, start_y + spacing*3 + 20, button_width, button_height], "Exit Program", 
                   lambda: app.set_exit_flag(True),
                   bg_color=(200, 50, 50))
        ]
        
        self.create_navigation_buttons(menu_buttons)


class BranchAPage(TestPage):
    """Branch A - Level 1"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "branch_a", ts, disp, "Branch A Menu")
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 180
        button_height = 40
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Sub Menu A1", 
                   lambda: self.navigate_with_log("sub_a1", "child")),
            Button([start_x, start_y + spacing, button_width, button_height], "Sub Menu A2", 
                   lambda: self.navigate_with_log("sub_a2", "child")),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Jump to Branch B", 
                   lambda: self.cross_level_jump(["root", "branch_b"], "cross_branch"),
                   bg_color=(100, 150, 100)),
            Button([start_x, start_y + spacing*3, button_width, button_height], "Jump to Deep Level 4", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3", "level4"], "deep_jump"),
                   bg_color=(150, 100, 150))
        ]
        
        self.create_navigation_buttons(menu_buttons)


class BranchBPage(TestPage):
    """Branch B - Level 1"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "branch_b", ts, disp, "Branch B Menu")
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 180
        button_height = 40
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Sub Menu B1", 
                   lambda: self.navigate_with_log("sub_b1", "child")),
            Button([start_x, start_y + spacing, button_width, button_height], "Sub Menu B2", 
                   lambda: self.navigate_with_log("sub_b2", "child")),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Jump to Branch A", 
                   lambda: self.cross_level_jump(["root", "branch_a"], "cross_branch"),
                   bg_color=(100, 150, 100)),
            Button([start_x, start_y + spacing*3, button_width, button_height], "Jump to Deepest", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3", "level4", "level5"], "deepest_jump"),
                   bg_color=(200, 100, 100))
        ]
        
        self.create_navigation_buttons(menu_buttons)


class SubMenuPage(TestPage):
    """Generic sub menu page - Level 2"""
    
    def __init__(self, ui_manager, name: str, ts, disp, branch_info: str):
        super().__init__(ui_manager, name, ts, disp, f"Sub Menu - {branch_info}")
        self.branch_info = branch_info
        self.action_count = 0
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 180
        button_height = 40
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Test Action 1", 
                   lambda: self.perform_action("Action 1")),
            Button([start_x, start_y + spacing, button_width, button_height], "Test Action 2", 
                   lambda: self.perform_action("Action 2")),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Jump to Other Branch", 
                   lambda: self.jump_to_other_branch(),
                   bg_color=(100, 100, 150)),
            Button([start_x, start_y + spacing*3, button_width, button_height], "Deep Jump Test", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3"], "deep_jump"),
                   bg_color=(150, 100, 150))
        ]
        
        self.create_navigation_buttons(menu_buttons)
    
    def perform_action(self, action):
        self.action_count += 1
        print(f"Performed {action} in {self.name} (count: {self.action_count})")
        self.last_nav_result = f"Action: {action} (#{self.action_count})"
    
    def jump_to_other_branch(self):
        """Jump to the other branch's sub menu"""
        if "sub_a" in self.name:
            # Jump to branch B
            target_path = ["root", "branch_b", "sub_b1"]
        else:
            # Jump to branch A
            target_path = ["root", "branch_a", "sub_a1"]
        
        self.cross_level_jump(target_path, "branch_cross_jump")


class DeepBranchPage(TestPage):
    """Start of deep branch - Level 1"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "deep_branch", ts, disp, "Deep Navigation Test")
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 180
        button_height = 40
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Go to Level 2", 
                   lambda: self.navigate_with_log("level2", "child")),
            Button([start_x, start_y + spacing, button_width, button_height], "Jump to Level 4", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3", "level4"], "skip_jump"),
                   bg_color=(200, 100, 100)),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Jump to Level 5", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3", "level4", "level5"], "deepest_skip"),
                   bg_color=(255, 100, 100)),
            Button([start_x, start_y + spacing*3, button_width, button_height], "Back to Branch A", 
                   lambda: self.cross_level_jump(["root", "branch_a"], "branch_jump"),
                   bg_color=(100, 200, 100))
        ]
        
        self.create_navigation_buttons(menu_buttons)


class Level2Page(TestPage):
    """Deep level 2"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "level2", ts, disp, "Deep Level 2")
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 180
        button_height = 40
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Go to Level 3", 
                   lambda: self.navigate_with_log("level3", "child")),
            Button([start_x, start_y + spacing, button_width, button_height], "Skip to Level 5", 
                   lambda: self.cross_level_jump(["root", "deep_branch", "level2", "level3", "level4", "level5"], "skip_to_end"),
                   bg_color=(150, 150, 100)),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Jump to Sub Menu", 
                   lambda: self.cross_level_jump(["root", "branch_a", "sub_a2"], "to_submenu"),
                   bg_color=(100, 150, 150))
        ]
        
        self.create_navigation_buttons(menu_buttons)


class Level3Page(TestPage):
    """Deep level 3"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "level3", ts, disp, "Deep Level 3")
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 180
        button_height = 40
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Go to Level 4", 
                   lambda: self.navigate_with_log("level4", "child")),
            Button([start_x, start_y + spacing, button_width, button_height], "Jump to Level 1", 
                   lambda: self.navigate_to_absolute_level(1),
                   bg_color=(100, 200, 100)),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Emergency to Root", 
                   lambda: self.navigate_with_log("root", "emergency"),
                   bg_color=(200, 50, 50))
        ]
        
        self.create_navigation_buttons(menu_buttons)


class Level4Page(TestPage):
    """Deep level 4"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "level4", ts, disp, "Deep Level 4")
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 180
        button_height = 40
        spacing = 50
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Go to Level 5", 
                   lambda: self.navigate_with_log("level5", "child")),
            Button([start_x, start_y + spacing, button_width, button_height], "Multi-Jump Test", 
                   lambda: self.multi_jump_sequence(),
                   bg_color=(255, 150, 100)),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Direct to Branch B", 
                   lambda: self.cross_level_jump(["root", "branch_b"], "deep_to_branch"),
                   bg_color=(150, 100, 200))
        ]
        
        self.create_navigation_buttons(menu_buttons)
    
    def multi_jump_sequence(self):
        """Test complex multi-jump sequence"""
        print("Starting multi-jump sequence from Level 4")
        
        # First jump to level 5
        if self.ui_manager.navigate_to_child("level5"):
            self.log_navigation("level5", "multi_jump_step1", True)
        else:
            self.log_navigation("level5", "multi_jump_step1", False)


class Level5Page(TestPage):
    """Deepest level - Level 5"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "level5", ts, disp, "Deepest Level (5)")
        self.test_count = 0
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 160
        button_width = 200
        button_height = 35
        spacing = 45
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Complex Jump Test", 
                   lambda: self.complex_navigation_test(),
                   bg_color=(200, 150, 100)),
            Button([start_x, start_y + spacing, button_width, button_height], "Level Navigation Test", 
                   lambda: self.level_navigation_test(),
                   bg_color=(150, 200, 100)),
            Button([start_x, start_y + spacing*2, button_width, button_height], "Branch Jump Test", 
                   lambda: self.branch_jump_test(),
                   bg_color=(100, 150, 200)),
            Button([start_x, start_y + spacing*3, button_width, button_height], "Emergency Exit", 
                   lambda: self.emergency_exit(),
                   bg_color=(255, 50, 50)),
            
            # Additional test buttons
            Button([start_x + 250, start_y, button_width-50, button_height], "To Level 2", 
                   lambda: self.navigate_to_absolute_level(2),
                   bg_color=(100, 100, 150)),
            Button([start_x + 250, start_y + spacing, button_width-50, button_height], "To Level 1", 
                   lambda: self.navigate_to_absolute_level(1),
                   bg_color=(150, 100, 150)),
            Button([start_x + 250, start_y + spacing*2, button_width-50, button_height], "Clear History", 
                   lambda: self.clear_and_jump(),
                   bg_color=(150, 150, 100))
        ]
        
        self.create_navigation_buttons(menu_buttons)
    
    def complex_navigation_test(self):
        """Test complex navigation from deepest level"""
        self.test_count += 1
        print(f"Complex navigation test #{self.test_count} from level {self.get_depth()}")
        
        # Try to jump to branch A sub menu
        success = self.cross_level_jump(["root", "branch_a", "sub_a1"], "complex_jump")
        if success:
            print("Complex jump successful")
        else:
            print("Complex jump failed")
    
    def level_navigation_test(self):
        """Test level-specific navigation"""
        # Try to go to level 2
        success = self.navigate_to_absolute_level(2)
        if not success:
            print("Level navigation failed, trying alternative")
            # Try direct path navigation
            self.cross_level_jump(["root", "deep_branch", "level2"], "level_alt")
    
    def branch_jump_test(self):
        """Test jumping to different branches"""
        branches = [
            (["root", "branch_a"], "branch_a"),
            (["root", "branch_b"], "branch_b"),
            (["root", "nav_stats"], "nav_stats")
        ]
        
        import random
        target_path, target_name = random.choice(branches)
        print(f"Random branch jump to: {target_name}")
        self.cross_level_jump(target_path, "random_branch_jump")
    
    def clear_and_jump(self):
        """Clear history and jump"""
        self.ui_manager.clear_history()
        self.last_nav_result = "History cleared"
        print("Navigation history cleared from deepest level")
    
    def emergency_exit(self):
        """Emergency exit to root"""
        success = self.ui_manager.navigate_to_root()
        self.log_navigation("root", "emergency_exit", success)
        if success:
            print("Emergency exit to root completed")
        else:
            print("Emergency exit failed!")


class NavigationStatsPage(TestPage):
    """Page to display navigation statistics"""
    
    def __init__(self, ui_manager, ts, disp):
        super().__init__(ui_manager, "nav_stats", ts, disp, "Navigation Statistics")
        self.setup_ui()
    
    def setup_ui(self):
        start_x = 50
        start_y = 350
        button_width = 150
        button_height = 35
        
        menu_buttons = [
            Button([start_x, start_y, button_width, button_height], "Reset Stats", 
                   lambda: self.reset_stats(),
                   bg_color=(200, 100, 100)),
            Button([start_x + 170, start_y, button_width, button_height], "Print Log", 
                   lambda: self.print_navigation_log(),
                   bg_color=(100, 200, 100)),
            Button([start_x + 340, start_y, button_width, button_height], "Test All Jumps", 
                   lambda: self.test_all_navigation(),
                   bg_color=(100, 100, 200))
        ]
        
        self.create_navigation_buttons(menu_buttons)
    
    def reset_stats(self):
        """Reset all navigation statistics"""
        if self.tracker:
            self.tracker.__init__()
            self.last_nav_result = "All stats reset"
            print("All navigation statistics reset")
    
    def print_navigation_log(self):
        """Print recent navigation log"""
        if self.tracker and self.tracker.navigation_log:
            print("\n=== Recent Navigation Log ===")
            for entry in self.tracker.navigation_log[-10:]:  # Last 10 entries
                print(f"{entry['from']} -> {entry['to']} ({entry['type']}) {'✓' if entry['success'] else '✗'}")
            print("=============================\n")
    
    def test_all_navigation(self):
        """Test various navigation patterns"""
        print("Testing all navigation types...")
        test_paths = [
            (["root", "branch_a"], "test_branch_a"),
            (["root", "branch_b", "sub_b1"], "test_sub_b1"),
            (["root", "deep_branch", "level2", "level3"], "test_level3"),
            (["root", "deep_branch", "level2", "level3", "level4", "level5"], "test_deepest")
        ]
        
        for path, test_name in test_paths:
            print(f"Testing path: {path}")
            success = self.ui_manager.navigate_to_path(path)
            self.log_navigation(test_name, "navigation_test", success)
            if success:
                # Come back to stats page
                time.sleep_ms(100)  # Brief pause
                self.ui_manager.navigate_to_path(["root", "nav_stats"])
    
    def update(self, img):
        super().update(img)
        
        # Display current stats
        if self.tracker:
            stats = self.tracker.get_stats()
            
            y_offset = 160
            line_height = 20
            
            stats_lines = [
                f"Total Navigations: {stats['total_navigations']}",
                f"Failed Navigations: {stats['failed_navigations']}",
                f"Max Depth Reached: {stats['max_depth']}",
                f"Cross-Level Jumps: {stats['cross_level_jumps']}",
                f"Unique Pages Visited: {stats['unique_pages_visited']}",
                f"Most Visited: {stats['most_visited'][0]} ({stats['most_visited'][1]}x)"
            ]
            
            for i, line in enumerate(stats_lines):
                img.draw_string(30, y_offset + i * line_height, line, 
                               image.Color.from_rgb(200, 255, 200), scale=1.1)
            
            # Show recent navigation history
            if self.tracker.navigation_log:
                img.draw_string(30, y_offset + len(stats_lines) * line_height + 20, 
                               "Recent Navigations:", 
                               image.Color.from_rgb(255, 255, 200), scale=1.0)
                
                recent_y = y_offset + len(stats_lines) * line_height + 45
                for i, entry in enumerate(self.tracker.navigation_log[-5:]):  # Last 5
                    color = image.Color.from_rgb(150, 255, 150) if entry['success'] else image.Color.from_rgb(255, 150, 150)
                    nav_text = f"{entry['from']} -> {entry['to']} ({'✓' if entry['success'] else '✗'})"
                    img.draw_string(30, recent_y + i * 15, nav_text, color, scale=0.8)


def create_test_menu_tree(ui_manager, ts, disp):
    """Create the complete test menu tree with proper structure"""
    
    print("Creating menu tree structure...")
    
    # Create all pages
    root = RootTestPage(ui_manager, ts, disp)
    
    # Level 1 pages
    branch_a = BranchAPage(ui_manager, ts, disp)
    branch_b = BranchBPage(ui_manager, ts, disp)
    deep_branch = DeepBranchPage(ui_manager, ts, disp)
    nav_stats = NavigationStatsPage(ui_manager, ts, disp)
    
    # Level 2 pages
    sub_a1 = SubMenuPage(ui_manager, "sub_a1", ts, disp, "Branch A1")
    sub_a2 = SubMenuPage(ui_manager, "sub_a2", ts, disp, "Branch A2")
    sub_b1 = SubMenuPage(ui_manager, "sub_b1", ts, disp, "Branch B1")
    sub_b2 = SubMenuPage(ui_manager, "sub_b2", ts, disp, "Branch B2")
    level2 = Level2Page(ui_manager, ts, disp)
    
    # Level 3+ pages (deep branch)
    level3 = Level3Page(ui_manager, ts, disp)
    level4 = Level4Page(ui_manager, ts, disp)
    level5 = Level5Page(ui_manager, ts, disp)
    
    # Build tree structure step by step
    print("Building tree structure...")
    
    # Root children (Level 1)
    root.add_child(branch_a)
    root.add_child(branch_b)
    root.add_child(deep_branch)
    root.add_child(nav_stats)
    print(f"Root now has {len(root.children)} children: {[c.name for c in root.children]}")
    
    # Branch A children (Level 2)
    branch_a.add_child(sub_a1)
    branch_a.add_child(sub_a2)
    print(f"Branch A has {len(branch_a.children)} children: {[c.name for c in branch_a.children]}")
    
    # Branch B children (Level 2)
    branch_b.add_child(sub_b1)
    branch_b.add_child(sub_b2)
    print(f"Branch B has {len(branch_b.children)} children: {[c.name for c in branch_b.children]}")
    
    # Deep branch children (creating a deep hierarchy)
    deep_branch.add_child(level2)
    level2.add_child(level3)
    level3.add_child(level4)
    level4.add_child(level5)
    print(f"Deep branch structure: deep_branch -> level2 -> level3 -> level4 -> level5")
    
    # Verify tree structure
    print("\n=== Final Tree Structure ===")
    def print_tree(page, indent=0):
        spaces = "  " * indent
        print(f"{spaces}{page.name} (children: {len(page.children)})")
        for child in page.children:
            print_tree(child, indent + 1)
    
    print_tree(root)
    print("============================\n")
    
    return root


def main():
    """Main function for navigation testing - FIXED VERSION"""
    print("FIXED Multi-Level Menu Navigation Test (640x480)")
    print("===============================================")
    
    # Initialize hardware for 640x480
    cam = camera.Camera(640, 480)
    disp = display.Display()
    ts = touchscreen.TouchScreen()
    
    # Create navigation tracker
    tracker = NavigationTracker()
    
    # Create FIXED UI manager with tracker
    ui_manager = FixedUIManager()
    ui_manager.tracker = tracker
    
    # Create menu tree
    root_page = create_test_menu_tree(ui_manager, ts, disp)
    ui_manager.set_root_page(root_page)
    
    # Debug: Print the final structure and test a path
    print("Testing path resolution...")
    ui_manager.debug_tree_structure()
    
    test_paths = [
        ["root", "branch_a", "sub_a1"],
        ["root", "deep_branch", "level2", "level3"],
        ["root", "deep_branch", "level2", "level3", "level4", "level5"]
    ]
    
    for path in test_paths:
        target = root_page.find_page_by_path(path[1:])  # Skip 'root'
        print(f"Path {path} -> Found: {target.name if target else 'None'}")
    
    print("\n=== FIXED Features ===")
    print("- Fixed path navigation logic")
    print("- Path validation with detailed error messages")
    print("- Cross-level jumps now working correctly")
    print("- Tree structure verification")
    print("- Debug buttons for troubleshooting")
    print("=====================\n")
    
    # Main loop
    frame_count = 0
    while not app.need_exit():
        img = cam.read()
        
        # Clear background
        img.draw_rect(0, 0, img.width(), img.height(), 
                     image.Color.from_rgb(25, 30, 35), thickness=-1)
        
        # Update current page
        ui_manager.update(img)
        
        # Show frame counter and navigation info (top-left corner)
        nav_info = ui_manager.get_navigation_info()
        frame_info = f"Frame: {frame_count} | History: {nav_info['history_depth']}"
        img.draw_string(5, 5, frame_info, image.Color.from_rgb(120, 120, 120), scale=0.7)
        
        # Display
        disp.show(img)
        frame_count += 1
    
    # Final statistics
    print("\n=== Final Navigation Statistics ===")
    if tracker:
        stats = tracker.get_stats()
        print(f"Total navigations: {stats['total_navigations']}")
        print(f"Failed navigations: {stats['failed_navigations']}")
        success_rate = ((stats['total_navigations'] - stats['failed_navigations']) / max(1, stats['total_navigations']) * 100)
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Maximum depth reached: {stats['max_depth']}")
        print(f"Cross-level jumps: {stats['cross_level_jumps']}")
        print(f"Unique pages visited: {stats['unique_pages_visited']}")
        print(f"Most visited page: {stats['most_visited'][0]} ({stats['most_visited'][1]} times)")
    print("===================================")
    
    print("FIXED navigation test completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
