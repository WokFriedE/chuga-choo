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
    
    allowable_stress: float = 70 # MPa (140 for Wrought Iron, 200 for Stainless Steel)
    pipe_thickness: float = 0.001
    
    # 6000 Tons
    train_mass = 6000 * 907.2
    
    exhaust_rate: float = 10 # kg / s
    
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
    
    furnace_lit = False
    exhaust_open = False
    
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
        if not self.furnace_lit:
            return 0
        air_mass_flow = 50 # kg / s
        coal_mass_flow = air_mass_flow / self.train_data.air_fuel_ratio # kg / s
        return min(coal_mass_flow*self.timestep, self.furnace_coal_kg)
    
    def step(self):
        if self.furnace_panel_open:
            self.furnace_air_kg = (self.train_data.boiler_volume - self.coal_volume) * 1.225
        else:
            new_air = self.timestep * (self.speed_train / 3.6) * (np.pi * self.train_data.intake_pipe_radius ** 2) * 1.225
            self.furnace_air_kg = min(self.furnace_air_kg + new_air, self.train_data.boiler_volume)
        if self.furnace_coal_kg == 0:
            self.furnace_lit = False
        # --- FURNACE ---
        fuel_used_kg = self.fuel_used_kg()
        self.furnace_coal_kg -= fuel_used_kg
        self.furnace_air_kg -= fuel_used_kg * self.train_data.air_fuel_ratio
        furnace_energy_MJ = self.train_data.boiler_efficiency * fuel_used_kg * 25 # 25 MJ / kg
        
        furnace_heat_loss_MJ = (1 - self.train_data.boiler_efficiency) * fuel_used_kg * 25
        self.temp_engine += 1e6 * furnace_heat_loss_MJ / self.train_data.heat_capacity

        
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
        engine_energy_MJ = min(self.train_data.engine_efficiency * furnace_energy_MJ, energy_diff_MJ / self.train_data.engine_efficiency)
        
        engine_energy_MJ = -engine_energy_MJ if speed_diff_ms < 0 else energy_diff_MJ
        friction_energy = 0.3 * (self.train_data.train_mass * 9.8) * self.speed_train * self.timestep
        
        dv = np.sign(engine_energy_MJ - friction_energy) * np.sqrt((2*abs(engine_energy_MJ - friction_energy)) / self.train_data.train_mass)
        self.speed_train += dv
        
        steam_used_kg = engine_energy_MJ / (enthalpy_diff_MJ * self.train_data.engine_efficiency)
        self.kg_boiler_to_engine = max(self.kg_boiler_to_engine - steam_used_kg, 0)
        self.kg_engine_to_cond += steam_used_kg
        self.temp_engine += 1e6 * self.train_data.engine_heat_loss * engine_energy_MJ / self.train_data.heat_capacity
        engine_energy_MJ *= self.train_data.engine_efficiency
        # Convective Heat Transfer: 50 W/m^2
        # Atmospheric Air Temp: 20C
        self.temp_engine -= 50 * (np.pi * self.train_data.intake_pipe_radius ** 2) * (self.temp_engine - 20)
        # --- CONDENSER ---
        if self.exhaust_open:
            self.kg_engine_to_cond -= self.train_data.exhaust_rate
        condenser_transfer = min(self.kg_engine_to_cond, self.train_data.condenser_rate * self.timestep)
        self.kg_engine_to_cond = max(self.kg_engine_to_cond - condenser_transfer, 0)
        self.kg_cond_to_boiler += condenser_transfer        
        # --- METRICS ---
        ideal_gas_const = 8.3145
        steam_mol_kg = 55.5
        water_mol_kg = 1
        
        vol_cond_to_boiler = (np.pi * (self.train_data.rad_cond_to_boiler ** 2)) * self.train_data.len_cond_to_boiler
        vol_boiler_to_engine = (np.pi * (self.train_data.rad_boiler_to_engine ** 2)) * self.train_data.len_boiler_to_engine
        vol_engine_to_cond = (np.pi * (self.train_data.rad_engine_to_cond ** 2)) * self.train_data.len_engine_to_cond
        
        pressure_cond_to_boiler = (self.kg_cond_to_boiler * water_mol_kg) * ideal_gas_const * (60 + 273.15) / vol_cond_to_boiler
        pressure_boiler_to_engine = (self.kg_boiler_to_engine * steam_mol_kg) * ideal_gas_const * (100 + 273.15) / vol_boiler_to_engine
        pressure_engine_to_cond = (self.kg_engine_to_cond * steam_mol_kg) * ideal_gas_const * (100 + 273.15) / vol_engine_to_cond
        
        return {
            'Cond-Boiler Pipe Burst': pressure_cond_to_boiler > self.train_data.allowable_stress,
            'Boiler-Engine Pipe Burst': pressure_boiler_to_engine > self.train_data.allowable_stress,
            'Engine-Cond Pipe Burst': pressure_engine_to_cond > self.train_data.allowable_stress,
            'Engine Overheating': self.temp_engine > 215,
            'Engine Exploded': self.temp_engine > 250,
            
            'Engine Temperature': self.temp_engine,
            'Cond-Boiler Pressure': pressure_cond_to_boiler,
            'Boiler-Engine Pressure': pressure_boiler_to_engine,
            'Engine-Cond Pressure': pressure_engine_to_cond,
            'Speed': self.speed_train
        }
        
    def actions(self):
        return [
            'Coal',
            
        ]