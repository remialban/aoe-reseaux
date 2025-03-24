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
    data_to_send = list()
    client_socket = None
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

        #print(obj)
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
        # print("====== NOUVEL OBJET==========")
        # print("-> objet", obj)
        #print("ccccccc")
        property = []
        #print("las bbas")

        if isinstance(obj, Player):
            #print("ici")
            property = [obj.get_name(), obj.get_color(), Sender.get_value(obj.get_stock())]
        elif isinstance(obj, Unit):
            property = [
                Sender.get_value(obj.get_position()),
                Sender.get_value(obj.get_player())
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
        print(data)
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
        if Sender.client_socket is None:
            # Création du socket UDP
            Sender.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        n = 1
        if message["operation"] == "add" and message["type"] == "building":
            n = 10

        for _ in range(1):
            # print(message)
            # # Création du socket UDP
            # print("⁼====================== CREATION CLINET SOCKET ===========================")
            # client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if message["operation"] == "add" and message["type"] == "building":
                print(message)

            # Adresse du serveur (IP et port)
            server_address = ('127.0.0.1', 5001)

            Sender.data_to_send.append(message)

            if len(Sender.data_to_send) > 5:

                Sender.client_socket.sendto((json.dumps(Sender.data_to_send)).encode('utf-8'), server_address)
                Sender.data_to_send = list()

            # Envoi des données
            #Sender.client_socket.sendto(().encode('utf-8'), server_address)

            # # Fermeture du socket
            # client_socket.close()

            return

    @staticmethod
    def ask_property(player,obj):
        data = {
            "operation": "ask_property",
            "type": Sender.get_type(obj),
            "class": obj.__class__.__name__,
            "id": obj.id,
            "arg" : player.id #joueur voulant obtenir la propriété de l'objet
        }
        Sender.send_to_C(data)

    @staticmethod
    def give_property(obj):
        data = {
            "operation": "give_property",
            "type": Sender.get_type(obj),
            "class": obj.__class__.__name__,
            "id": obj.id,
        }
        Sender.send_to_C(data)