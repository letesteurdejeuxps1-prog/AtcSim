from pages.radar.view.menus.GenericButton import GenericButton


class ClickableButton(GenericButton):

    def __init__(
            self,
            pos_x: int,
            pos_y: int,
            txt: str,
            width: int = 0,
            height: int = 0,
            action=None
    ):
        super().__init__(
            pos_x,
            pos_y,
            txt,
            width,
            height,
            action
        )

        self.selected = False

        # Selected colors
        self.selected_bg_color = (60, 120, 60)
        self.selected_hover_bg_color = (80, 150, 80)
        self.selected_pressed_bg_color = (40, 90, 40)

    def click(self):
        self.selected = not self.selected

        if self.action is not None:
            self.action()

    def get_bg_color(self):

        # Currently being pressed
        if self.pressed:
            if self.selected:
                return self.selected_pressed_bg_color

            return self.pressed_bg_color

        # Hovering
        if self.hovered:
            if self.selected:
                return self.selected_hover_bg_color

            return self.hover_bg_color

        # Normal
        if self.selected:
            return self.selected_bg_color

        return self.bg_color