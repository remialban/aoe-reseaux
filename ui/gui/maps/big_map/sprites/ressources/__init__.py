from core import Building
from core.resources_points import ResourcePoint
from ui.gui.maps.big_map.sprites.element import Element


class Resource(Element):
    def __init__(self, resource: ResourcePoint|Building, image, isometry, coef=1):
        self.resource = resource
        self.coef = coef

        super().__init__(image, isometry, coef, x=resource.get_position().get_x, y=resource.get_position().get_y)

        if isinstance(self.resource, Building):
            self.x = lambda: resource.get_position().get_x() + resource.get_width() - 1
            self.y = lambda: resource.get_position().get_y() + resource.get_height() - 1

        self.update_offset()

    def get_image_width(self):
        width = super().get_image_width() * self.coef

        if isinstance(self.resource, Building):
            return width * self.resource.get_width()

        return width
