from datetime import date, datetime
from abc import ABC, abstractmethod

class Peca():
    def __init__(self, codi:str, nom:str, descripcio:str, subministrador:Subministrador):
        self._codi = codi
        self._nom = nom
        self._descripcio = descripcio
        self._subministrador = subministrador
    @property
    def codi(self)->str:
        return self._codi
    @property
    def subministrador(self)->Subministrador:
        return self._subministrador
class Subministrador():
    def __init__(self, nom:str, CIF:str, adreca:str, pais:str):
        self._nom = nom
        self._CIF = CIF
        self._adreca = adreca
        self._pais = pais
class InventariPeces():
    def __init__(self, data_ultima_revisio:date, peces:dict = {}):
        self._data_ultima_revisio = data_ultima_revisio
        self._peces = peces
    def existencia_peca(self, codi:str)->int:
        for peca, existencia in self._peces.values():
            if peca.codi == codi:
                return existencia;
        return 0
    def peces_proveidor(self, CIF:str)->list:
        peces_proveidor = []
        for peca in self._peces.keys():
            if peca.proveidor == CIF:
                peces_proveidor.append(peca);
        return peces_proveidor

class ModelVehicle(ABC):
    # Mirar funcions
    def __init__(self, nom_model:str, electric:bool, cilindrada:int, peces:dict):
        self._nom_model = nom_model
        self._electric = electric
        self._cilindrada = cilindrada
        """
        El diccionari amb les peces tindra com a key un objecte del tipus peca
        i com a valors tindra una llista amb quantitat:int, opcional:bool i posicio:int
        """
        self._peces = peces
    def peces_necessaries(self)->dict:
        return self._peces
    @abstractmethod
    def etiqueta_contaminacio(self)->str:...
    @abstractmethod
    def numero_rodes(self)->int:...
class ModelCotxe(ModelVehicle):
    def __init__(self, nom_model:str, electric:bool, cilindrada:int, peces:dict, num_portes:int, tipus_canvi:str, tipus_combustible:str):
        super().__init__(nom_model, electric, cilindrada, peces)
        self._num_portes = num_portes
        self._tipus_canvi = tipus_canvi
        self._tipus_combustible = tipus_combustible
    def numero_rodes(self)->int:
        return 4
class ModelMoto(ModelVehicle):
    def __init__(self, nom_model:str, electric:bool, cilindrada:int, peces:dict, tipus_rodes:str, carnet_necessari:str):
        super().__init__(nom_model, electric, cilindrada, peces)
        self._tipus_rodes = tipus_rodes
        self._carnet_necessari = carnet_necessari
    def numero_rodes(self)->int:
        return 2
class VehicleProduit():
    def __init__(self, num_serie:str, color:str, data_produccio:date, model:ModelVehicle):
        self._num_serie = num_serie
        self._color = color
        self._data_produccio = data_produccio
        self._model = model
    @property
    def model(self)->ModelVehicle:
        return self._model
    @property
    def data_produccio(self)->date:
        return self._data_produccio
class RegistreProduccio():
    def __init__(self, inici_registre:date):
        self._inici_registre = inici_registre
        self._vehicles_produits = []
    def afegir_vehicle(self, vehicle_produit:VehicleProduit)->None:
        self._vehicles_produits.append(vehicle_produit)
    def num_vehicles_produits(self, model:ModelVehicle, inici:date, fi:date)->int:
        contador = 0
        for vehicle in self._vehicles_produits:
            if vehicle.model == model and vehicle.data_produccio < fi and vehicle.data_produccio > inici:
                contador += 1
        return contador
# class LiniaProduccioVehicle():
#     def __init__(self, id_linia:int)