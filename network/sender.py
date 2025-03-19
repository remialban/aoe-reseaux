from pprint import pprint
from time import sleep

from core.position import Position
from core.resource import Resource
from core.resources_points import ResourcePoint
from core.units import Unit
from core.buildings import Building
from core.players import Player
from core.actions import Action

import socket
import json

class Sender:
    @staticmethod
    def get_type(obj):
        if isinstance(obj, Unit):
            return "unit"
        elif isinstance(obj, Building):
            return "building"
        elif isinstance(obj, Player):
            return "player"
        elif isinstance(obj, ResourcePoint):
            return "resources_point"
        elif isinstance(obj, Action):
            return "action"

    @staticmethod
    def notify_edit(obj, property, value):

        t = value


        if isinstance(t, Position):
            value = [value.get_x(), value.get_y()]
        elif isinstance(t, Resource):
            value = [value.get_wood(), value.get_gold(), value.get_food()]
            #print("dand2")
        elif isinstance(t, Unit) or isinstance(t, Building) or isinstance(t, Player) or isinstance(t, ResourcePoint):
            # print("dans 3")
            # print("VALUE :")
            # print(value)
            # print("END VALUE")
            value = value.id

        print(obj)
        #pprint(obj.__a)
        # print("OBJET A AVNEOYER =================================")
        # print(obj)
        # print(property)
        # print(value)
        # print("==============")
        data = {
            "operation": "edit",
            "type": Sender.get_type(obj),
            "class": obj.__class__.__name__,
            "id": obj.id,
            "property": property,
            "value": value,
        }
        # pprint(data)

        Sender.send_to_C(data)

    @staticmethod
    def get_value(value):
        t = type(value)

        if isinstance(value, Position):
            value = [value.get_x(), value.get_y()]
        elif isinstance(value, Resource):
            value = [value.get_wood(), value.get_gold(), value.get_food()]
        elif isinstance(value, Unit) or isinstance(value, Building) or isinstance(value, Player) or isinstance(value, ResourcePoint):
            value = value.id

        return value

    @staticmethod
    def notify_add(obj):
        print("====== NOUVEL OBJET==========")
        print("-> objet", obj)
        #print("ccccccc")
        property = []
        #print("las bbas")

        if isinstance(obj, Player):
            #print("ici")
            property = [obj.get_name(), obj.get_color(), Sender.get_value(obj.get_stock())]
        elif isinstance(obj, Unit):
            property = [
                Sender.get_value(obj.get_player()),
                Sender.get_value(obj.get_position())
            ]
        elif isinstance(obj, Building):
            property = [
                Sender.get_value(obj.get_position()),
                Sender.get_value(obj.get_player())
            ]
        elif isinstance(obj, ResourcePoint):
            property = [
                Sender.get_value(obj.get_position()),
                Sender.get_value(obj.get_resource())
            ]

        data = {
            "operation": "add",
            "type": Sender.get_type(obj),
            "class": obj.__class__.__name__,
            "id": obj.id,
            "args": property,
        }
        #pprint(data)
        #print("ici")
        Sender.send_to_C(data)

    @staticmethod
    def notify_remove(obj):
        data = {
            "operation": "remove",
            "type": Sender.get_type(obj),
            "class": obj.__class__.__name__,
            "id": obj.id
        }
        Sender.send_to_C(data)

    @staticmethod
    def send_to_C(message):
        # Création du socket UDP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Adresse du serveur (IP et port)
        server_address = ('127.0.0.1', 5000)

        # Envoi des données
        client_socket.sendto((json.dumps(message) + "\n").encode('utf-8'), server_address)

        # Fermeture du socket
        client_socket.close()


