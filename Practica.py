from datetime import date, datetime
from abc import ABC, abstractmethod
import tkinter as tk

class creaModel():
    def __init__(self, controller):
        self._controller = controller
        self._root = tk.Tk()
        self._root.title("vista")
        self._
        self._bt1 = tk.Radiobutton(self._root, text="Cotxe")
        self._bt2 = tk.Radiobutton(self._root, text="Moto")
class Subministrador():
    def __init__(self, nom:str, CIF:str, adreca:str, pais:str):
        self._nom = nom
        self._CIF = CIF
        self._adreca = adreca
        self._pais = pais
    @property
    def CIF(self)->str:
        return self._CIF
   
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
    def nom(self)->str:
        return self._nom
    @property
    def subministrador(self)->Subministrador:
        return self._subministrador
   
class InventariPeces():
    def __init__(self, dataUltimaRevisio:date):
        self._dataUltimaRevisio = dataUltimaRevisio
        self._peces = {}
    def afegirPeca(self, peca:Peca, quantitat:int):
        if peca in self._peces:
            self._peces[peca] += quantitat
        else:
            self._peces[peca] = quantitat
    def numExistenciesPeca(self, codiPeca:str)->int:
        for peca, existencia in self._peces.items():
            if peca.codi == codiPeca:
                return existencia;
        return 0
    def pecesProveidor(self, CIF:str)->list:
        peces_proveidor = []
        for peca in self._peces.keys():
            if peca.subministrador.CIF == CIF:
                peces_proveidor.append(peca);
        return peces_proveidor

class ModelVehicle(ABC):
    def __init__(self, nomModel:str, electric:bool, cilindrada:int, peces:dict=None):
        self._nomModel = nomModel
        self._electric = electric
        self._cilindrada = cilindrada
        if peces is None:
            self._peces = {}
        else:
            self._peces = peces
    def pecesNecessaries(self)->dict:
        return self._peces
    def afegirPeca(self, peca: Peca, quantitat: int, opcional: bool = False, posicio: int = 0) -> None:
        self._peces[peca] = [quantitat, opcional, posicio]
    @property
    def peces(self):
        return self._peces
    @abstractmethod
    def etiquetaDeContaminacio(self)->str:
        pass
    @abstractmethod
    def numeroDeRodes(self)->int:
        pass
   
   
class ModelCotxe(ModelVehicle):
    def __init__(self, nomModel:str, electric:bool, cilindrada:int, numeroDePortes:int, tipusCanviMarxes:str, tipusCombustible:str, peces:dict=None):
        super().__init__(nomModel, electric, cilindrada, peces)
        self._numeroDePortes = numeroDePortes
        self._tipusCanviMarxes = tipusCanviMarxes
        self._tipusCombustible = tipusCombustible
    def numeroDeRodes(self)->int:
        return 4
    def etiquetaDeContaminacio(self)->str:
        if self._electric == True:
            return ("0Emissions")
        elif self._tipusCombustible == "gasolina":
            return ("B")
        else:
            return ("C")
       
   
class ModelMoto(ModelVehicle):
    def __init__(self, nomModel:str, electric:bool, cilindrada:int, tipusRodes:str, carnetNecessari:str, peces:dict=None):
        super().__init__(nomModel, electric, cilindrada, peces)
        self._tipusRodes = tipusRodes
        self._carnetNecessari = carnetNecessari
    def numeroDeRodes(self)->int:
        return 2
    def etiquetaDeContaminacio(self)->str:
        if self._electric == True:
            return ("0Emissions")
        else:
            return ("B")
   
class VehicleProduit():
    def __init__(self, numeroSerie:str, color:str, dataProduccio:date, model:ModelVehicle):
        self._numeroSerie = numeroSerie
        self._color = color
        self._dataProduccio = dataProduccio
        self._model = model
    @property
    def model(self)->ModelVehicle:
        return self._model
    @property
    def dataProduccio(self)->date:
        return self._dataProduccio
   
class RegistreProduccio():
    def __init__(self, dataIniciRegistre:date):
        self._dataIniciRegistre = dataIniciRegistre
        self._vehiclesProduits = []
    def afegirVehicle(self, vehicle_produit:VehicleProduit)->None:
        self._vehiclesProduits.append(vehicle_produit)
    def nVehiclesProduïts(self, model:ModelVehicle, dataInici:date, dataFi:date)->int:
        contador = 0
        for vehicle in self._vehiclesProduits:
            if vehicle.model == model and vehicle.dataProduccio < dataFi and vehicle.dataProduccio > dataInici:
                contador += 1
        return contador
   
class LiniaProduccioVehicle():
    num_serie = 0
    def __init__(self, id_linia:str):
        self._id_linia = id_linia
       
    def produirVehicle(self, model:ModelVehicle, color:str, data_produccio:datetime=None)->VehicleProduit:
        if data_produccio is None:
            data_produccio = datetime.now()
        vehicle = VehicleProduit(str(LiniaProduccioVehicle.num_serie), color, data_produccio, model)
        LiniaProduccioVehicle.num_serie += 1
        return vehicle
   
class Fabrica():
    def __init__(self, marca:str):
        self._marca = marca
        self._subministradors = []
        self._modelsDisponibles = []
        self._linies = [LiniaProduccioVehicle("L1")]
        self._registre = RegistreProduccio(datetime.now())
        self._inventari = InventariPeces(datetime.now())
    def afegirModelCotxe(self, nom:str, electric:bool, cilindrada:int, numPortes:int, tipusCanvi:str, tipusCombustible:str)->bool:
        nou_cotxe = ModelCotxe(nom, electric, cilindrada, numPortes, tipusCanvi, tipusCombustible)
        self._modelsDisponibles.append(nou_cotxe)
        return True
    def afegirModelMoto(self, nom:str, electric:bool, cilindrada:int, tipusRodes:str, carnetNecessari:str)->bool:
        nova_moto = ModelMoto(nom, electric, cilindrada, tipusRodes, carnetNecessari )
        self._modelsDisponibles.append(nova_moto)
        return True
    def seleccionarLiniaProduccio(self)->LiniaProduccioVehicle:
        return self._linies[0]
    def produirVehicle(self, model:ModelVehicle, color:str, data_produccio:datetime=None)->VehicleProduit:
        if self.esPossibleProduir(model):
            linia = self.seleccionarLiniaProduccio()
            vehicle = linia.produirVehicle(model, color, data_produccio)
            self._registre.afegirVehicle(vehicle)
            for peca, llista in model.peces.items():
                self._inventari.afegirPeca(peca, -1*llista[0])
            print("Vehicle produït")
            return vehicle
        else:
            print("No s'ha pogut produir el vehicle")
            return None
    def esPossibleProduir(self, model:ModelVehicle)->bool:
        peces_necessaries = model.pecesNecessaries()
        for peca, llista in peces_necessaries.items():
            quantitat_necessaria = llista[0]
            codi_peca = peca.codi
            quantitat_disponible = self._inventari.numExistenciesPeca(codi_peca)
            if quantitat_disponible < quantitat_necessaria:
                return False
        return True
           
if __name__ == "__main__":
    fabrica = Fabrica("Honda")
    prov_michelin = Subministrador("Michelin", "11111111C", "c/ Tour Eiffel sn", "Paris, França")
    prov_sporting = Subministrador("Sporting Wheels", "22222222C", "c/ Big Ben sn", "Londres, Anglaterra")
    prov_handlebar = Subministrador("Handle BarBikes", "33333333C", "c/ Tower Bridge sn", "Londres, Anglaterra")
    prov_gearbox = Subministrador("GearBox", "444444444C", "c/ Trafalgar Square sn", "Londres, Anglaterra")
    prov_titanium = Subministrador("Titanium", "555555555C", "c/ Muralla Xinesa sn", "Xangai, Xina")
    prov_aed = Subministrador("AED", "666666666C", "c/ de la boira 5", "Vic, Catalunya")
    prov_honda = Subministrador("HondaMotors", "777777777C", "c/ Mont Fuji", "Tokio, Japó")

    p0001 = Peca("0001", "Roda davantera de cotxe", "Roda", prov_michelin)
    p0002 = Peca("0002", "Roda posterior de cotxe", "Roda", prov_michelin)
    p0003 = Peca("0003", "Roda davantera de moto", "Roda", prov_michelin)
    p0004 = Peca("0004", "Roda posterior de moto", "Roda", prov_michelin)
    p0005 = Peca("0005", "Volant de cotxe", "Direcció", prov_sporting)
    p0006 = Peca("0006", "Manillar de moto", "Direcció", prov_handlebar)
    p0007 = Peca("0007", "Caixa de canvis de cotxe", "Transmissió", prov_gearbox)
    p0008 = Peca("0008", "Caixa de canvis de cotxe elèctric", "Transmissió", prov_gearbox)
    p0009 = Peca("0009", "Bateria de Liti per cotxe", "Energia", prov_titanium)
    p0010 = Peca("0010", "Bateria de Liti per moto", "Energia", prov_titanium)
    p0011 = Peca("0011", "Carburador de cotxe", "Motor", prov_aed)
    p0012 = Peca("0012", "Carburador de moto", "Motor", prov_aed)
    p0013 = Peca("0013", "Motor de cotxe de combustió", "Motor", prov_honda)
    p0014 = Peca("0014", "Motor de moto de combustió", "Motor", prov_honda)
    p0015 = Peca("0015", "Motor de cotxe elèctric", "Motor", prov_honda)
    p0016 = Peca("0016", "Motor de moto elèctric", "Motor", prov_honda)

    dades_inventari = [
        (p0001, 40), (p0002, 45), (p0003, 10), (p0004, 10),
        (p0005, 25), (p0006, 8), (p0007, 27), (p0008, 15),
        (p0009, 12), (p0010, 21), (p0011, 17), (p0012, 7),
        (p0013, 5), (p0014, 15), (p0015, 25), (p0016, 35)
    ]
    for peca, quantitat in dades_inventari:
        fabrica._inventari.afegirPeca(peca, quantitat)
