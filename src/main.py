#----------------------------------------------------
# Création de la fonction factory
#----------------------------------------------------
import numpy as np
from model import RandomNetwork, EisenbergNoeModel
from controller import Simulation
from model.manual_network import ManualNetwork
from view import Visualisation

def create_simulation(simulation_type, network_params, shock_vector):
    """
    Crée une simulation complète en fonction du type spécifié

    Args:
        simulation_type: Type de simulation ("Eisenberg", "SmallWorld", etc.)
        network_params: Paramètres pour la création du réseau
        shock_vector: Vecteur de choc initial

    Returns:
        Une simulation configurée
    """
    # Création du réseau approprié
    if simulation_type == "Eisenberg":
        network = RandomNetwork(
            network_params.get('number_bank', 5),
            network_params.get('probability_of_linking', 0.6)
        )
    elif simulation_type == "SmallWorld":
        # À implémenter plus tard
        raise NotImplementedError("SmallWorldNetwork pas encore implémenté")
    elif simulation_type == "ManualType":
        network = ManualNetwork(network_params["matrix_obligation"],network_params["vector_outside_asset"], network_params["asset"], network_params["vector_outside_liabilities"],
                                network_params["liabilities"], network_params["matrix_relative_liabilities"])
    else:
        raise ValueError(f"Type de simulation inconnu: {simulation_type}")

    # Création et configuration des banques
    for i in range(network.number_bank):
        # Ajouter chaque banque comme observateur du réseau
        network.add_observer(network.banks[i])

    # Création du modèle
    model = EisenbergNoeModel(network)

    # Création de la simulation
    simulation = Simulation("Eisenberg", network, shock_vector)

    # Ajouter une visualisation (optionnel)
    visualization = Visualisation()
    network.add_observer(visualization)

    return simulation, visualization


#----------------------------------------------------
# Exemple d'utilisation avec le main.py modifié
#----------------------------------------------------
if __name__ == "__main__":
    # Paramètres du réseau
    network_params = {
        'number_bank': 5,
        'probability_of_linking': 0.9
    }

    network_parameters_fixed = {
        "matrix_obligation": np.array([
        [0, 180, 0, 0],
        [0, 0, 100, 0],
        [100, 0, 0, 100],
        [150, 0, 0, 0]
    ])
    ,
        "matrix_relative_liabilities": np.array([
        [0, 1/2, 0, 0],
        [0, 0, 1/2, 0],
        [2/5, 0, 0, 2/5],
        [1/2, 0, 0, 0]
    ]),
        "vector_outside_asset": np.array([120, 30, 160, 204]),
        "vector_outside_liabilities": np.array([180, 100, 50, 150]),
        "asset": np.array([250, 180, 100, 100]),
        "liabilities": np.array([180, 100, 200, 150])
    }

    # Vecteur de choc
    shock_vector = np.array([0, 0, 120, 0])

    # Création de la simulation et de la visualisation
    simulation, visualization = create_simulation("ManualType", network_parameters_fixed, shock_vector)

    # Afficher l'état initial
    network = simulation.model.network
    print("État initial:")
    print("Matrice d'obligations:", network.get_matrix_obligation())
    #print("Matrice de vulneralibité relative:", network.get_relative_vulnerabilities())
    print("Valeur nette:", network.get_net_worth())
    #print("Vulnérabilités:", network.get_vulnerabilities())
    print("Vecteur de défaut:", network.get_default_vector())

    # Exécuter la simulation
    vector_payments, shock_measure, default_count, vulnerabilities_measure = simulation.simulate()

    # Afficher l'état final
    print("\nÉtat final:")
    print("Valeur nette:", network.get_net_worth())
    #print("Vulnérabilités:", network.get_vulnerabilities())
    print("Vecteur de défaut:", network.get_default_vector())
    print("Paiements:", vector_payments)
    print("Mesure du choc:", shock_measure)
    print("Nombre de défauts:", default_count)
    #print("Mesure des vulnérabilités:", vulnerabilities_measure)

    # Afficher l'historique
    visualization.plot_history()