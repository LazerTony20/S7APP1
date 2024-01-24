# Université de Sherbrooke
# Code préparé par Audrey Corbeil Therrien
# Laboratoire 1 - Interaction avec prolog

from swiplserver import PrologMQI

from Maze import Maze

class UnlockDoor:
    def unlockDoor(doorInfo):
        with PrologMQI() as mqi:
            with PrologMQI() as mqi_file:
                with mqi_file.create_thread() as prolog_thread:
                    if(doorInfo):
                        result = prolog_thread.query("[prolog/door].")
                        result = prolog_thread.query("ouvrirPorte("+str(doorInfo)+", Cle).")
                        return result[0]["Cle"]


