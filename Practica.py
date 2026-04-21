from datetime import date, datetime
from abc import ABC, abstractmethod

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
       
    def produirVehicle(self, model:ModelVehicle, color:str, data_produccio: datetime = None)->VehicleProduit:
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
    def produirVehicle(self, model:ModelVehicle, color:str, data_produccio: datetime = None)->VehicleProduit:
        if self.esPossibleProduir(model):
            linia = self.seleccionarLiniaProduccio()
            vehicle = linia.produirVehicle(model, color, data_produccio)
            self._registre.afegirVehicle(vehicle)
            return vehicle
        else:
            print("No s'ha pogut produïr el vehicle")
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
    prov_michelin = Subministrador("Michelin", "11111111C", "c/ Tour Eiffel sn", "Paris")
    prov_sporting = Subministrador("Sporting Wheels", "22222222C", "c/ Big Ben sn", "Londres")
    prov_handlebar = Subministrador("Handle BarBikes", "33333333C", "c/ Tower Bridge sn", "Londres")
    prov_gearbox = Subministrador("GearBox", "444444444C", "c/ Trafalgar Square sn", "Londres")
    prov_titanium = Subministrador("Titanium", "555555555C", "c/ Muralla Xinesa sn", "Xangai")
    prov_honda = Subministrador("HondaMotors", "666666666C", "c/ Mont Fuji", "Japó")

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
    p0011 = Peca("0011", "Carburador de cotxe", "Motor", prov_honda)
    p0012 = Peca("0012", "Carburador de moto", "Motor", prov_honda)
    p0013 = Peca("0013", "Motor de cotxe de combustió", "Motor", prov_honda)
    p0014 = Peca("0014", "Motor de moto de combustió", "Motor", prov_honda)
    p0015 = Peca("0015", "Motor de cotxe elèctric", "Motor", prov_honda)
    p0016 = Peca("0016", "Motor de moto elèctric", "Motor", prov_honda)

    dades_inventari = [
        (p0001, 18), (p0002, 18), (p0003, 10), (p0004, 10),
        (p0005, 5), (p0006, 8), (p0007, 7), (p0008, 15),
        (p0009, 12), (p0010, 21), (p0011, 17), (p0012, 7),
        (p0013, 5), (p0014, 15), (p0015, 25), (p0016, 35)
    ]
    for peca, quantitat in dades_inventari:
        fabrica._inventari.afegirPeca(peca, quantitat)

    print("\n 1. Afegir un nou model de vehicle")
   
    fabrica.afegirModelCotxe("Honda Civic", True, 0, 5, "Automàtic", "elèctric")
    civic_elec = fabrica._modelsDisponibles[-1]
    civic_elec.afegirPeca(p0001, 2)
    civic_elec.afegirPeca(p0002, 2)
    civic_elec.afegirPeca(p0005, 1)
    civic_elec.afegirPeca(p0008, 1)
    civic_elec.afegirPeca(p0009, 1)
    civic_elec.afegirPeca(p0015, 1)

    fabrica.afegirModelCotxe("Honda Civic", False, 1500, 5, "Manual", "gasolina")
    civic_gas = fabrica._modelsDisponibles[-1]
    civic_gas.afegirPeca(p0001, 2)
    civic_gas.afegirPeca(p0002, 2)
    civic_gas.afegirPeca(p0005, 1)
    civic_gas.afegirPeca(p0007, 1)
    civic_gas.afegirPeca(p0011, 1)
    civic_gas.afegirPeca(p0013, 1)

    fabrica.afegirModelCotxe("Honda HR-V", False, 2000, 5, "Automàtic", "gasolina")
    hrv_comb = fabrica._modelsDisponibles[-1]
    hrv_comb.afegirPeca(p0001, 2)
    hrv_comb.afegirPeca(p0002, 2)
    hrv_comb.afegirPeca(p0005, 1)
    hrv_comb.afegirPeca(p0007, 1)
    hrv_comb.afegirPeca(p0011, 1)
    hrv_comb.afegirPeca(p0013, 1)

    fabrica.afegirModelMoto("Honda CBR", True, 0, "Carretera", "A2")
    cbr_elec = fabrica._modelsDisponibles[-1]
    cbr_elec.afegirPeca(p0003, 1)
    cbr_elec.afegirPeca(p0004, 1)
    cbr_elec.afegirPeca(p0006, 1)
    cbr_elec.afegirPeca(p0010, 1)
    cbr_elec.afegirPeca(p0016, 1)

    fabrica.afegirModelMoto("Honda CRM 75", False, 75, "Muntanya", "A1")
    crm75_comb = fabrica._modelsDisponibles[-1]
    crm75_comb.afegirPeca(p0003, 1)
    crm75_comb.afegirPeca(p0004, 1)
    crm75_comb.afegirPeca(p0006, 1)
    crm75_comb.afegirPeca(p0012, 1)
    crm75_comb.afegirPeca(p0014, 1)
   
    print("Models afegits correctament.")


    print("\n 2. Produir un nou vehicle")
   
    data1 = datetime(2026, 3, 10)
    for i in range(10):
        fabrica.produirVehicle(civic_elec, "Blanc", data_produccio=data1)
       
    data2 = datetime(2026, 3, 12)
    for j in range(10):
        fabrica.produirVehicle(civic_gas, "Blau", data_produccio=data2)
       
    print("Vehicles produïts i registrats.")


    print("\n 3. Consulta de si una peça està disponible")
   
    estoc_0001 = fabrica._inventari.numExistenciesPeca("0001")
   
    print("Estoc disponible de la peça 0001 (Roda davantera cotxe):", estoc_0001)
   
    peces_gearbox = fabrica._inventari.pecesProveidor("444444444C")
    noms_gearbox = [p.nom for p in peces_gearbox]  
    print("Peces disponibles del subministrador GearBox:", noms_gearbox)

    print("\n 4. Producció en un interval de dates")
   
    inici_mes = datetime(2026, 3, 1)
    fi_mes = datetime(2026, 3, 31)
   
    produits_civic_gas = fabrica._registre.nVehiclesProduïts(civic_gas, inici_mes, fi_mes)
    print("Honda Civic de combustió produïts durant el març de 2026:", produits_civic_gas)


    print("\n 5. Saber si és possible produir un vehicle")
   
    possible_produir = fabrica.esPossibleProduir(civic_gas)
    if possible_produir:
        print("És possible produir un altre Honda Civic de combustió?: Sí")
    else:
        print("És possible produir un altre Honda Civic de combustió?: No")
