from ui.gui.maps.big_map.sprites.entity import Entity


class Element(Entity):
    def __init__(self, sprite_image, isometry, coef=1, x: callable = None, y: callable = None):
        """
        Sprite permettant de dessiner un élément sur la maps

        :param sprite_image: Image du sprite
        :param isometry: Objet Isometry permettant de convertir les coordonnées réelle en isometrique
        :param coef: Coef multiplicateur de l'image
        :param x: Fonction retournant la position x du sprite (version normale, c'est à dire x au sens de la maps et pas au sens isométrique)
        :param y: Fonction retournant la position y du sprite (version normale, c'est à dire y au sens de la maps et pas au sens isométrique)
        """
        super().__init__(sprite_image, isometry, x, y)
        self.coef = coef
