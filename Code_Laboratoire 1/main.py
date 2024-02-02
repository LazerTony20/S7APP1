# Université de Sherbrooke
# Code préparé par Audrey Corbeil Therrien
# Laboratoire 1 - Interaction avec prolog

from swiplserver import PrologMQI
import os

if __name__ == '__main__':
    os.system("cls")
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            print("============= Checkup =============")
            result = prolog_thread.query("member(X, [first, second, third]).")
            print(result)

        with PrologMQI() as mqi_file:
            print("============= Intro =============")
            with mqi_file.create_thread() as prolog_thread:
                # Load a prolog file
                result = prolog_thread.query("[prolog/parente].")
                print(result)

                # Query the information in the file
                result = prolog_thread.query("homme(X).")
                print("\nVoici la liste des hommes :")
                print(result)

                # Query the information in the file
                result = prolog_thread.query("fils(luc, X).")
                print("\nVoici le parent de luc :")
                print(result)

                # Query the information in the file
                result = prolog_thread.query("enfant(louis, X).")
                print("\nVoici les parents de louis :")
                print(result)

                # Query the information in the file
                result = prolog_thread.query("grandparent(X, louise).")
                print("\nVoici les grand-parents de louise :")
                print(result)

                # Query the information in the file
                result = prolog_thread.query("frere(louis, X).")
                print("\nVoici les freres de louis :")
                print(result)

        with PrologMQI() as mqi_file:
            print("============= NUMERO 1 =============")
            with mqi_file.create_thread() as prolog_thread:
                # Load a prolog file
                result = prolog_thread.query("[prolog/num1].")
                # print(result)

                # Query the information in the file
                result = prolog_thread.query("repas(pate, porc, X).")
                print("\nVoici la sortie de repas(pate, porc, X) :")
                print(result)

                # Query the information in the file
                result = prolog_thread.query("repasLeger(pate, porc, X).")
                print("\nVoici la sortie de repasLeger(pate, porc, X) :")
                print(result)

                # Query the information in the file
                result = prolog_thread.query("repasLeger(X, Y, glace).")
                print("\nVoici la sortie de repasLeger(X, Y, glace) :")
                print(result)
        
        with PrologMQI() as mqi_file:
            print("============= NUMERO 2 =============")
            with mqi_file.create_thread() as prolog_thread:
                # Load a prolog file
                result = prolog_thread.query("[prolog/num2].")
                # print(result)

                # Query the information in the file
                print(prolog_thread.query("un_sur_deux([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],X)."))
                # print("\nVoici la sortie :")
                # print(result)

        with PrologMQI() as mqi_file:
            print("============= NUMERO 3 =============")
            with mqi_file.create_thread() as prolog_thread:
                # Load a prolog file
                print(prolog_thread.query("[prolog/num3]."))

print("\n=======================================")

 
