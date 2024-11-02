from dataclasses import dataclass
import numpy as np

@dataclass
class TrainInfo():
    engine_mass_kg: float = 200
    J_per_kg_coal: float = 25
    
    air_fuel_ratio: float = 12 # 12:1 to 5:1 by weight
    boiler_volume: float = 10 # m^3, 10-20
    intake_pipe_radius: float = 0.1 # m
    
    boiler_efficiency: float = 0.8
    engine_efficiency: float = 0.2
    engine_heat_loss: float = 0.3
    condenser_rate: float = 2 # kg / s
    
    len_cond_to_boiler: float = 1
    len_boiler_to_engine: float = 1
    len_engine_to_cond: float = 1
    
    rad_cond_to_boiler: float = 0.1
    rad_boiler_to_engine: float = 0.1
    rad_engine_to_cond: float = 0.2
    
    # 6000 Tons
    train_mass = 6000 * 907.2
    
    @property
    def heat_capacity(self):
        # Joule / Celsius
        return 460 * self.engine_mass_kg
    


class TrainSim():
    furnace_coal_kg = 0
    furnace_air_kg = 0
    furnace_panel_open = False
    
    kg_cond_to_boiler = 0
    kg_boiler_to_engine = 0
    kg_engine_to_cond = 0
    
    temp_engine = 20
    
    # km / h
    speed_train = 0
    speed_target = 0
    
    def __init__(self, train_data: TrainInfo, timestep: float = 0.1):
        self.train_data: TrainInfo = train_data
        self.timestep = timestep
    
    @property
    def coal_volume(self):
        return self.furnace_coal_kg / 850
    @property
    def air_volume(self):
        return self.furnace_air_kg / 1.225
    
    def fuel_used_kg(self):
        air_mass_flow = 50 # kg / s
        coal_mass_flow = air_mass_flow / self.train_data.air_fuel_ratio # kg / s
        return min(coal_mass_flow*self.timestep, self.furnace_coal_kg)
    
    def step(self):
        if self.furnace_panel_open:
            self.furnace_air_kg = (self.train_data.boiler_volume - self.coal_volume) * 1.225
        
        # --- FURNACE ---
        fuel_used_kg = self.fuel_used_kg()
        furnace_energy_MJ = self.train_data.boiler_efficiency * fuel_used_kg * 25 # 25 MJ / kg
        temp_diff = 100 - 60 # Assuming that Water is 60C after condenser- if we want more granularity change this
        water_boil_capacity_kg = furnace_energy_MJ / (0.004186 * temp_diff)
        water_boiled = min(self.kg_cond_to_boiler, water_boil_capacity_kg)
        self.kg_cond_to_boiler -= water_boiled
        latent_heat = 2.26  # MJ/kg
        steam_produced_kg = water_boiled / latent_heat  # Convert water boiled to steam
        self.kg_boiler_to_engine += steam_produced_kg
        # --- ENGINE ---
        enthalpy_diff_MJ = 800000 / 1e6
        speed_diff_ms = abs(self.speed_target - self.speed_train) / 3.6
        energy_diff_MJ = (self.train_data.train_mass * (speed_diff_ms ** 2)) / 1e6
        engine_energy = min(self.train_data.engine_efficiency * furnace_energy_MJ, energy_diff_MJ / self.train_data.engine_efficiency)
        
        steam_used_kg = engine_energy / (enthalpy_diff_MJ * self.train_data.engine_efficiency)
        self.kg_boiler_to_engine -= steam_used_kg
        self.kg_engine_to_cond += steam_used_kg
        self.temp_engine += self.train_data.engine_heat_loss * engine_energy / self.train_data.heat_capacity
        engine_energy *= self.train_data.engine_efficiency
        # Convective Heat Transfer: 50 W/m^2
        # Atmospheric Air Temp: 20C
        self.temp_engine -= 50 * (np.pi * self.train_data.intake_pipe_radius ** 2) * (self.temp_engine - 20)
        # --- CONDENSER ---
        condenser_transfer = min(self.kg_engine_to_cond, self.train_data.condenser_rate * self.timestep)
        self.kg_engine_to_cond -= condenser_transfer
        self.kg_cond_to_boiler += condenser_transfer        
        # --- METRICS ---
        
            
        