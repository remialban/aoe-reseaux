import queue
import socket
import threading
import time
import json
import errno
import time
import traceback
from copy import deepcopy

from keyboard.mouse import get_position

from core.position import Position
from core.resources_points.mine import Mine
from core.resources_points.wood import Wood
from core.units.swordsman import Swordsman
from core.units.villager import Villager
from core.units.archer import Archer
from core.units.horse_man import Horseman

from core.map import Map

from core.buildings.farm import Farm
from core.buildings.house import House
from core.buildings.town_center import TownCenter
from core.buildings.barracks import Barracks
from core.buildings.archery_range import ArcheryRange
from core.buildings.keep import Keep
from core.buildings.stable import Stable
from core.buildings.camp import Camp


from core.resources_points import ResourcePoint
from core.resource import Resource

from core.players import Player
from core.players.ai import AI
from network.state import State
from tests.test_position import position
from tests.test_resource import resource


class Receiver:
    ui=None
    sock=None

    data = queue.Queue()

    @staticmethod
    def init(ui):
        Receiver.ui =ui
        # Définir l'adresse IP et le port du serveur
        HOST = '127.0.0.1'  # Adresse du serveur
        PORT = 5000  # Port à utiliser

        # Créer un socket UDP
        Receiver.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Receiver.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        # Lier le socket à l'adresse et au port
        Receiver.sock.bind((HOST, PORT))

        # Rendre le socket non bloquant
        Receiver.sock.setblocking(False)

        #print(f"Serveur en attente de données sur {HOST}:{PORT}...")


    @staticmethod
    def event_manager(ui):
        #if Receiver.sock is None:
        #    Receiver.init(ui)
        while True:
            try:
                # Réception de données (non bloquante)
                try:
                    data, addr = Receiver.sock.recvfrom(1024)  # Taille maximale des données reçues : 1024 octets
                    if data:
                        data = data.decode('utf-8')
                        print(f"Reçu {data} de {addr}")

                        # Traiter les données reçues (exemple : action du joueur)
                        #threading.Thread(target=message_pick_up, args=(Receiver.ui, data)).start()
                        message_pick_up(Receiver.ui, data)

                        #message_pick_up(Receiver.ui,data)
                except BlockingIOError:
                    # Si aucune donnée n'est reçue, ignorer l'erreur
                    pass


            except socket.error as e:
                # Gérer les erreurs réseau
                if e.errno == errno.ECONNREFUSED:
                    print("La connexion a été refusée. Vérifiez si le serveur est en ligne.")
                else:
                    print(f"Erreur de socket : {e}")

            time.sleep(0.01)  # Petite pause pour éviter la surcharge CPU

    @staticmethod
    def process_message(ui):


        game = ui.get_game()
        map = game.get_map()

        for i in range(50):
            if Receiver.data.empty():
                break
            response = Receiver.data.get()
            try:
                if response["class"] == "Keep":
                    continue

                print(response)
                class_name = response["class"]
                class__ = globals()[class_name]

                if response["operation"] == "add":
                    argument = response["args"]
                    print(response)
                    if response["type"] == "resources_point":
                        position = Position(argument[0][0], argument[0][1])
                        if class_name == "Mine":
                            resources = Mine(position)
                        else:
                            resources = Wood(position)

                        resources.id = response["id"]
                        map.add_resource_point(resources)

                    elif response["type"] == "player":
                        player = Player(argument[0], argument[1])
                        game.get_players().add(player)
                        player.id = response["id"]
                    else:
                        print("message building ", response, class_name, class__)
                        instance = class__(
                            position=Position(argument[0][0], argument[0][1]),
                            player=get_player_by_id(argument[1], ui)

                        )
                        print(instance)
                        instance.id = response["id"]

                        if response["type"] == "unit":
                            map.add_unit(instance)
                        else:
                            map.add_building(instance)


                elif response["operation"] == "edit":
                    if response["type"] == "resources_point":
                        instance = get_resources_by_id(response["id"], ui)

                    elif response["type"] == "unit":
                        instance = get_unit_by_id(response["id"], ui)


                    elif response["type"] == "building":
                        instance = get_building_by_id(response["id"], ui)

                    elif response["type"] == "player":
                        instance = get_player_by_id(response["id"], ui)

                    t = type(getattr(instance, response["property"]))

                    value = response["value"]

                    if t == Resource:
                        value = Resource(value[0], value[1], value[2])

                    elif t == Position:
                        value = Position(value[0], value[1])

                    setattr(instance, response['property'], value)


                else:
                    print("remove")
                    if response["type"] == "resource_point":

                        instance = get_resources_by_id(response["id"], ui)
                        map.remove_resource_point(instance)

                    elif response["type"] == "building":
                        instance = get_building_by_id(response["id"], ui)
                        map.remove_building(instance)

                    else:
                        print("remove d'une unité")
                        instance = get_unit_by_id(response["id"], ui)
                        print("instance remove : ", instance)
                        map.remove_unit(instance)

            except Exception as e:
                print(e)


def message_pick_up(ui,data):
    game = ui.get_game()
    map = game.get_map()

    response = json.loads(data)

    for event in response:
        Receiver.data.put(event)


def get_player_by_id(id,ui):
    game=ui.get_game()
    map= game.get_map()
    for player in game.get_players() :
        if player.id ==id:
            return player


def get_unit_by_id(id,ui):
    game=ui.get_game()
    map= game.get_map()
    for unit in map.units :
        if unit.id ==id:
            return unit

def get_building_by_id(id,ui):
    game=ui.get_game()
    map= game.get_map()
    for building in map.buildings :
        if building.id ==id:
            return building

def get_resources_by_id(id,ui):
    game=ui.get_game()
    map= game.get_map()
    for resources in map.resources :
        if resources.id ==id:
            return resources


def get_resources_by_position(position,ui):
    game=ui.get_game()
    map = game.get_map()
    for resources in map.resources :
        if resources.__position ==position:
            return resources


