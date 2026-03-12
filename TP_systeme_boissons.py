
#  SYSTÈME DE BOISSONS D'UN CAFÉ — Programmation Orientée Objet

from abc import ABC, abstractmethod      # pour créer des classes abstraites
from dataclasses import dataclass        # pour créer facilement la classe Client

# PARTIE 1 — Classe abstraite Boisson
class Boisson(ABC):
    """Classe de base pour toutes les boissons"""
    @abstractmethod
    def cout(self):
        pass

    @abstractmethod
    def description(self):
        pass

    def afficher_commande(self):
        print(f"Commande : {self.description()}")
        print(f"Prix     : {self.cout():.2f}€")

    # Permet de combiner deux boissons avec l'opérateur +
    def __add__(self, autre_boisson):
        boisson_self = self
        boisson_autre = autre_boisson

        class BoissonCombinee(Boisson):
            def cout(self):
                return boisson_self.cout() + boisson_autre.cout()
            def description(self):
                return boisson_self.description() + " + " + boisson_autre.description()

        return BoissonCombinee()
    
# PARTIE 2 — Boissons de base
class Cafe(Boisson):
    """Représente un café simple"""
    def cout(self):
        return 2.0
    def description(self):
        return "Café simple"

class The(Boisson):
    """Représente un thé"""
    def cout(self):
        return 1.5
    def description(self):
        return "Thé"

# PARTIE 3 — Décorateurs (ingrédients supplémentaires)
class DecorateurBoisson(Boisson):
    """Classe de base pour les ingrédients"""
    def __init__(self, boisson):
        self._boisson = boisson

class Lait(DecorateurBoisson):
    """Ajoute du lait à la boisson"""
    def cout(self):
        return self._boisson.cout() + 0.5
    def description(self):
        return self._boisson.description() + ", Lait"

class Sucre(DecorateurBoisson):
    """Ajoute du sucre"""
    def cout(self):
        return self._boisson.cout() + 0.2
    def description(self):
        return self._boisson.description() + ", Sucre"

class Caramel(DecorateurBoisson):
    """Ajoute du caramel"""
    def cout(self):
        return self._boisson.cout() + 0.7
    def description(self):
        return self._boisson.description() + ", Caramel"

# PARTIE 4 — Classe Client
@dataclass
class Client:
    """Stocke les infos du client"""
    nom: str
    numero: int
    points_fidelite: int

# PARTIE 5 — Gestion des commandes

class Commande:
    """Une commande appartient à un client et contient des boissons"""
    def __init__(self, client):
        self.client = client
        self.boissons = []

    def ajouter_boisson(self, boisson):
        self.boissons.append(boisson)

    def prix_total(self):
        total = 0
        for boisson in self.boissons:
            total += boisson.cout()
        return total

    def afficher(self):
        print("=" * 40)
        print(f"  Client  : {self.client.nom} (n°{self.client.numero})")
        print("  Boissons commandées :")
        for boisson in self.boissons:
            print(f"    → {boisson.description()} : {boisson.cout():.2f}€")
        print(f"  TOTAL   : {self.prix_total():.2f}€")
        print("=" * 40)

# PARTIE 6 — Types de commandes
class CommandeSurPlace(Commande):
    """Commande consommée dans le café"""
    def afficher(self):
        print(" COMMANDE SUR PLACE")
        super().afficher()
        print("  Service à table. Bonne dégustation !")

class CommandeEmporter(Commande):
    """Commande à emporter"""
    def afficher(self):
        print(" COMMANDE À EMPORTER")
        super().afficher()
        print("  Votre commande sera prête dans quelques minutes.")

# PARTIE 7 — Programme de fidélité

class Fidelite:
    """Gestion des points de fidélité : 1 point par euro dépensé"""
    def ajouter_points(self, client, montant):
        points_gagnes = int(montant)
        client.points_fidelite += points_gagnes
        print(f" {points_gagnes} points ajoutés à {client.nom}")
        print(f"  Total points : {client.points_fidelite} pts")

class CommandeFidele(Commande, Fidelite):
    """Commande avec programme fidélité intégré"""
    def valider(self):
        self.afficher()
        print("\n  Programme fidélité :")
        self.ajouter_points(self.client, self.prix_total())

if __name__ == "__main__":

    print("\n" + "=" * 50)
    print("   BIENVENUE AU CAFÉ POO ")
    print("=" * 50)

    client1 = Client(nom="Fatima ", numero=101, points_fidelite=0)
    print(f"\nNouveau client enregistré : {client1}")

    # Test boisson avec ingrédients
    print("\n--- Test boisson avec ingrédients ---")
    boisson = Cafe()
    boisson = Lait(boisson)
    boisson = Sucre(boisson)
    boisson.afficher_commande()

    # Test combinaison de boissons
    print("\n--- Test combinaison de boissons ---")
    cafe = Cafe()
    the = The()
    menu = cafe + the
    menu.afficher_commande()

    # Commande sur place
    print("\n--- Commande sur place ---")
    boisson1 = Lait(Cafe())
    boisson2 = Caramel(The())
    cmd_sur_place = CommandeSurPlace(client1)
    cmd_sur_place.ajouter_boisson(boisson1)
    cmd_sur_place.ajouter_boisson(boisson2)
    cmd_sur_place.afficher()

    # Commande à emporter
    print("\n--- Commande à emporter ---")
    boisson3 = Sucre(Lait(Cafe()))
    cmd_emporter = CommandeEmporter(client1)
    cmd_emporter.ajouter_boisson(boisson3)
    cmd_emporter.afficher()

    # Commande avec fidélité
    print("\n--- Commande avec programme fidélité ---")
    client2 = Client(nom="Mohamed", numero=202, points_fidelite=10)
    boisson_fid1 = Caramel(Lait(Cafe()))
    boisson_fid2 = The()
    cmd_fidele = CommandeFidele(client2)
    cmd_fidele.ajouter_boisson(boisson_fid1)
    cmd_fidele.ajouter_boisson(boisson_fid2)
    cmd_fidele.valider()
    print(f"\nClient après validation : {client2}")

# PARTIE 8 — Questions de réflexion

# Q1 : Quelle partie permet d'ajouter facilement de nouveaux ingrédients ?
# → Le patron Décorateur (classe DecorateurBoisson)
#   Exemple : pour ajouter "Vanille", il suffit de créer une classe Vanille(DecorateurBoisson)
#     class Vanille(DecorateurBoisson):
#         def cout(self):
#             return self._boisson.cout() + 0.6
#         def description(self):
#             return self._boisson.description() + ", Vanille"

# Q2 : Pour ajouter le chocolat chaud, que faut-il faire ?
# → Créer une nouvelle classe qui hérite de Boisson
#     class ChocolatChaud(Boisson):
#         def cout(self):
#             return 3.0
#         def description(self):
#             return "Chocolat chaud"

# Q3 : Pourquoi séparer les responsabilités entre plusieurs classes ?
# → Chaque classe a un rôle unique (SRP - Single Responsibility Principle)
#   - Boisson → concept de boisson
#   - DecorateurBoisson → ingrédients
#   - Commande → gestion de la commande
#   - Fidelite → gestion des points
#   - Client → stocke les infos du client
# Cela rend le code plus clair, modifiable et sans bugs