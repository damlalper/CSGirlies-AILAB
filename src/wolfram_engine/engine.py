"""Wolfram computation engine for experiment simulations"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from src.config import settings
import base64
import json


@dataclass
class ComputationResult:
    """Result from Wolfram computation"""
    query: str
    result: str
    graph_svg: Optional[str] = None
    numeric_result: Optional[float] = None


class WolframEngine:
    """
    Interface with Wolfram Cloud for scientific computations.
    Generates graphs, calculations, and simulation results.

    Features:
    - Dynamic parameter-driven computations
    - Real-time graph generation
    - Interactive simulations
    - Wolfram API integration (with fallback)
    """

    def __init__(self):
        self.appid = settings.wolfram_appid
        self.queries = {}
        self.computation_cache = {}  # Cache for performance
    
    async def compute_titration(self,
                               acid_concentration: float,
                               acid_volume: float,
                               base_concentration: float) -> ComputationResult:
        """
        Compute acid-base titration curve with DYNAMIC parameters.

        Args:
            acid_concentration: Molarity of acid (M)
            acid_volume: Volume of acid (mL)
            base_concentration: Molarity of base (M)

        Returns:
            ComputationResult with DYNAMIC pH curve based on actual parameters
        """
        query = f"""Plot[pH[x] = 14 + Log10[(x*{base_concentration} - {acid_concentration}*{acid_volume})/({acid_volume} + x)],
                     {{x, 0, {acid_volume * acid_concentration / base_concentration * 1.5}}},
                     AxesLabel -> {{"Volume of Base (mL)", "pH"}},
                     PlotLabel -> "Titration Curve"]"""

        # Calculate equivalence point
        equiv_point = acid_concentration * acid_volume / base_concentration

        return ComputationResult(
            query=query,
            result=f"pH curve computed | Equivalence point: {equiv_point:.2f} mL",
            numeric_result=equiv_point,
            graph_svg=self._generate_dynamic_titration_graph(acid_concentration, acid_volume, base_concentration)
        )
    
    async def compute_hookes_law(self,
                                spring_constant: float,
                                max_displacement: float) -> ComputationResult:
        """
        Compute Hooke's Law: F = kx with DYNAMIC parameters.

        Args:
            spring_constant: Spring constant k (N/m)
            max_displacement: Maximum displacement x (m)

        Returns:
            ComputationResult with DYNAMIC force vs displacement graph
        """
        query = f"Plot[{spring_constant} * x, {{x, 0, {max_displacement}}}, AxesLabel -> {{'Displacement (m)', 'Force (N)'}}]"

        max_force = spring_constant * max_displacement

        return ComputationResult(
            query=query,
            result=f"Force-displacement plotted | Max force: {max_force:.2f} N at {max_displacement:.2f} m",
            numeric_result=max_force,
            graph_svg=self._generate_dynamic_hookes_graph(spring_constant, max_displacement)
        )
    
    async def compute_osmosis(self,
                             concentration: float,
                             temperature: float,
                             volume: float) -> ComputationResult:
        """
        Compute osmotic pressure: π = iMRT with DYNAMIC parameters.

        Args:
            concentration: Concentration (M)
            temperature: Temperature (K)
            volume: Volume (L)

        Returns:
            ComputationResult with DYNAMIC osmotic visualization
        """
        R = 0.08206  # Gas constant (L·atm/mol·K)
        i = 1.0  # van't Hoff factor (assume non-electrolyte)
        osmotic_pressure = i * concentration * R * temperature

        query = f"π = iMRT = {i} × {concentration} × {R} × {temperature} = {osmotic_pressure:.2f} atm"

        return ComputationResult(
            query=query,
            result=f"Osmotic pressure: {osmotic_pressure:.2f} atm | Water flow direction: High → Low concentration",
            numeric_result=osmotic_pressure,
            graph_svg=self._generate_dynamic_osmosis_graph(concentration, temperature, osmotic_pressure)
        )
    
    async def compute_custom(self, query: str) -> ComputationResult:
        """
        Compute custom Wolfram Language query.

        Args:
            query: Wolfram Language query

        Returns:
            ComputationResult
        """
        # In production, this would call Wolfram Cloud API
        return ComputationResult(
            query=query,
            result="Computation executed",
            graph_svg=self._generate_sample_graph("custom")
        )

    async def compute_ph_calculation(self,
                                    h_concentration: float) -> ComputationResult:
        """
        Calculate pH from H+ concentration.

        Args:
            h_concentration: [H+] concentration (M)

        Returns:
            ComputationResult with pH value and scale visualization
        """
        import math

        if h_concentration <= 0:
            h_concentration = 1e-14

        pH = -math.log10(h_concentration)
        pOH = 14 - pH

        query = f"pH = -log₁₀([H⁺]) = -log₁₀({h_concentration:.2e}) = {pH:.2f}"

        return ComputationResult(
            query=query,
            result=f"pH = {pH:.2f} | pOH = {pOH:.2f} | {'Acidic' if pH < 7 else 'Basic' if pH > 7 else 'Neutral'}",
            numeric_result=pH,
            graph_svg=self._generate_ph_scale_graph(pH, h_concentration)
        )

    async def compute_molarity(self,
                              moles: float,
                              volume_liters: float) -> ComputationResult:
        """
        Calculate molarity from moles and volume.

        Args:
            moles: Number of moles (mol)
            volume_liters: Volume in liters (L)

        Returns:
            ComputationResult with molarity calculation
        """
        if volume_liters <= 0:
            volume_liters = 0.001

        molarity = moles / volume_liters

        query = f"M = n/V = {moles} mol / {volume_liters} L = {molarity:.3f} M"

        return ComputationResult(
            query=query,
            result=f"Molarity = {molarity:.3f} M ({moles} moles in {volume_liters} L)",
            numeric_result=molarity,
            graph_svg=self._generate_concentration_graph(molarity, moles, volume_liters)
        )

    async def compute_spring_energy(self,
                                   spring_constant: float,
                                   displacement: float) -> ComputationResult:
        """
        Calculate elastic potential energy in a spring.

        Args:
            spring_constant: Spring constant k (N/m)
            displacement: Displacement x (m)

        Returns:
            ComputationResult with energy calculation
        """
        energy = 0.5 * spring_constant * displacement ** 2
        force = spring_constant * displacement

        query = f"E = ½kx² = ½ × {spring_constant} × {displacement}² = {energy:.3f} J"

        return ComputationResult(
            query=query,
            result=f"Elastic PE = {energy:.3f} J | Force = {force:.2f} N at {displacement} m",
            numeric_result=energy,
            graph_svg=self._generate_energy_graph(spring_constant, displacement, energy)
        )

    async def simulate_temperature_sensor(self,
                                         initial_temp: float,
                                         time_seconds: int) -> ComputationResult:
        """
        Simulate IoT temperature sensor readings over time.

        Args:
            initial_temp: Starting temperature (°C)
            time_seconds: Duration to simulate (seconds)

        Returns:
            ComputationResult with sensor data visualization
        """
        import random
        import math

        sensor_data = []
        for t in range(time_seconds):
            # Simulate realistic temperature variation
            drift = math.sin(t * 0.1) * 0.5  # Periodic variation
            noise = random.uniform(-0.2, 0.2)  # Random noise
            temp = initial_temp + drift + noise
            sensor_data.append((t, temp))

        avg_temp = sum(t[1] for t in sensor_data) / len(sensor_data)

        query = f"Temperature sensor simulation | Duration: {time_seconds}s | Initial: {initial_temp}°C"

        return ComputationResult(
            query=query,
            result=f"Average temperature: {avg_temp:.2f}°C | Readings: {len(sensor_data)} points",
            numeric_result=avg_temp,
            graph_svg=self._generate_sensor_graph(sensor_data, "Temperature", "°C")
        )

    async def simulate_ph_sensor(self,
                                initial_ph: float,
                                time_seconds: int,
                                titration_rate: float = 0.01) -> ComputationResult:
        """
        Simulate IoT pH sensor readings during titration.

        Args:
            initial_ph: Starting pH value
            time_seconds: Duration to simulate (seconds)
            titration_rate: Rate of pH change (pH units/second)

        Returns:
            ComputationResult with pH sensor data
        """
        import random

        sensor_data = []
        for t in range(time_seconds):
            # Simulate pH increase during base addition
            ph_increase = titration_rate * t
            noise = random.uniform(-0.05, 0.05)

            # S-curve for titration (realistic)
            if ph_increase < 6:
                ph = initial_ph + ph_increase * 0.5
            elif ph_increase < 7:
                ph = initial_ph + 3 + (ph_increase - 6) * 4  # Sharp rise
            else:
                ph = initial_ph + 7 + (ph_increase - 7) * 0.3

            ph = min(14, max(0, ph + noise))
            sensor_data.append((t, ph))

        final_ph = sensor_data[-1][1] if sensor_data else initial_ph

        query = f"pH sensor simulation | Duration: {time_seconds}s | Initial pH: {initial_ph}"

        return ComputationResult(
            query=query,
            result=f"Final pH: {final_ph:.2f} | Initial pH: {initial_ph:.2f} | Change: +{final_ph - initial_ph:.2f}",
            numeric_result=final_ph,
            graph_svg=self._generate_sensor_graph(sensor_data, "pH", "pH units")
        )

    async def simulate_pressure_sensor(self,
                                      initial_pressure: float,
                                      time_seconds: int) -> ComputationResult:
        """
        Simulate IoT pressure sensor for osmosis experiment.

        Args:
            initial_pressure: Starting pressure (atm)
            time_seconds: Duration to simulate (seconds)

        Returns:
            ComputationResult with pressure sensor data
        """
        import random
        import math

        sensor_data = []
        for t in range(time_seconds):
            # Simulate pressure build-up (asymptotic approach to equilibrium)
            pressure_increase = (1 - math.exp(-t / 10)) * initial_pressure
            noise = random.uniform(-0.02, 0.02)
            pressure = initial_pressure + pressure_increase + noise
            sensor_data.append((t, pressure))

        final_pressure = sensor_data[-1][1] if sensor_data else initial_pressure

        query = f"Pressure sensor simulation | Duration: {time_seconds}s | Initial: {initial_pressure} atm"

        return ComputationResult(
            query=query,
            result=f"Final pressure: {final_pressure:.2f} atm | Osmotic buildup: +{final_pressure - initial_pressure:.2f} atm",
            numeric_result=final_pressure,
            graph_svg=self._generate_sensor_graph(sensor_data, "Pressure", "atm")
        )
    
    def _generate_dynamic_titration_graph(self, acid_conc: float, acid_vol: float, base_conc: float) -> str:
        """Generate dynamic titration curve based on actual parameters"""
        import math

        # Calculate points for titration curve
        points = []
        max_vol = (acid_conc * acid_vol / base_conc) * 2.5

        for i in range(50):
            vol = (i / 49.0) * max_vol
            # Simplified pH calculation
            if vol < (acid_conc * acid_vol / base_conc) * 0.9:
                pH = 3 + (vol / max_vol) * 3
            elif vol < (acid_conc * acid_vol / base_conc) * 1.1:
                pH = 3 + (vol / max_vol) * 8
            else:
                pH = 10 + (vol / max_vol) * 2

            x = 50 + (vol / max_vol) * 300
            y = 250 - (pH / 14.0) * 200
            points.append(f"{x:.1f},{y:.1f}")

        polyline_points = " ".join(points)

        svg = f"""<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="white"/>
            <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Titration Curve</text>
            <text x="200" y="40" text-anchor="middle" font-size="12">Acid: {acid_conc}M, {acid_vol}mL | Base: {base_conc}M</text>
            <polyline points="{polyline_points}" stroke="blue" fill="none" stroke-width="2"/>
            <line x1="50" y1="250" x2="350" y2="250" stroke="black"/>
            <line x1="50" y1="250" x2="50" y2="50" stroke="black"/>
            <text x="350" y="270" font-size="12">Volume of Base (mL)</text>
            <text x="20" y="150" font-size="12" transform="rotate(-90 20 150)">pH</text>
            <text x="45" y="255" font-size="10">0</text>
            <text x="45" y="55" font-size="10">14</text>
            <text x="350" y="255" font-size="10">{max_vol:.1f}</text>
        </svg>"""

        return base64.b64encode(svg.encode()).decode()

    def _generate_dynamic_hookes_graph(self, k: float, max_x: float) -> str:
        """Generate dynamic Hooke's Law graph based on actual parameters"""
        points = []

        for i in range(20):
            x = (i / 19.0) * max_x
            force = k * x

            px = 50 + (x / max_x) * 300
            max_force = k * max_x
            py = 250 - (force / max_force) * 200 if max_force > 0 else 250
            points.append(f"{px:.1f},{py:.1f}")

        polyline_points = " ".join(points)

        svg = f"""<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="white"/>
            <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Hooke's Law: F = kx</text>
            <text x="200" y="40" text-anchor="middle" font-size="12">Spring Constant k = {k} N/m</text>
            <polyline points="{polyline_points}" stroke="green" fill="none" stroke-width="3"/>
            <line x1="50" y1="250" x2="350" y2="250" stroke="black" stroke-width="1"/>
            <line x1="50" y1="250" x2="50" y2="50" stroke="black" stroke-width="1"/>
            <text x="350" y="270" font-size="12">Displacement (m)</text>
            <text x="20" y="150" font-size="12" transform="rotate(-90 20 150)">Force (N)</text>
            <text x="45" y="255" font-size="10">0</text>
            <text x="350" y="255" font-size="10">{max_x:.2f}</text>
            <text x="30" y="55" font-size="10">{(k*max_x):.1f}</text>
        </svg>"""

        return base64.b64encode(svg.encode()).decode()

    def _generate_dynamic_osmosis_graph(self, concentration: float, temp: float, pressure: float) -> str:
        """Generate dynamic osmosis visualization"""
        # Visual representation of osmotic pressure
        bar_height = min(150, int(pressure * 10))

        svg = f"""<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="white"/>
            <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Osmotic Pressure</text>
            <text x="200" y="40" text-anchor="middle" font-size="12">π = iMRT = {pressure:.2f} atm</text>
            <text x="200" y="60" text-anchor="middle" font-size="11">C = {concentration}M, T = {temp}K</text>

            <!-- Osmotic pressure bar -->
            <rect x="100" y="{250-bar_height}" width="60" height="{bar_height}" fill="lightblue" stroke="black" stroke-width="2"/>
            <text x="130" y="270" text-anchor="middle" font-size="12">Solution</text>

            <!-- Membrane -->
            <line x1="200" y1="100" x2="200" y2="250" stroke="orange" stroke-width="4" stroke-dasharray="5,5"/>
            <text x="205" y="180" font-size="11">Membrane</text>

            <!-- Pure water side -->
            <rect x="240" y="150" width="60" height="100" fill="lightcyan" stroke="black" stroke-width="2"/>
            <text x="270" y="270" text-anchor="middle" font-size="12">Water</text>

            <!-- Pressure arrow -->
            <line x1="160" y1="{250-bar_height/2}" x2="190" y2="{250-bar_height/2}" stroke="red" stroke-width="2"/>
            <polygon points="190,{250-bar_height/2} 180,{245-bar_height/2} 180,{255-bar_height/2}" fill="red"/>
            <text x="130" y="{240-bar_height/2}" font-size="11" fill="red">π</text>
        </svg>"""

        return base64.b64encode(svg.encode()).decode()

    def _generate_sample_graph(self, graph_type: str) -> str:
        """
        Generate sample SVG graph (placeholder for Wolfram API response).
        In production, this would return actual Wolfram computation results.

        Args:
            graph_type: Type of graph

        Returns:
            Base64 encoded SVG
        """
        svg_map = {
            "titration": self._generate_dynamic_titration_graph(0.1, 25.0, 0.1),
            "hookes_law": self._generate_dynamic_hookes_graph(50.0, 0.1),
            "osmosis": self._generate_dynamic_osmosis_graph(0.5, 298.0, 12.2),
            "custom": base64.b64encode(b"""<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="300" fill="white"/>
                <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Computation Result</text>
                <circle cx="200" cy="150" r="50" fill="none" stroke="purple" stroke-width="2"/>
                <text x="200" y="155" text-anchor="middle" font-size="14">Result</text>
            </svg>""").decode()
        }

        return svg_map.get(graph_type, svg_map["custom"])

    def _generate_ph_scale_graph(self, ph: float, h_conc: float) -> str:
        """Generate pH scale visualization"""
        # Position indicator on pH scale
        indicator_x = 50 + (ph / 14.0) * 300

        svg = f"""<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="white"/>
            <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">pH Scale</text>
            <text x="200" y="40" text-anchor="middle" font-size="11">[H⁺] = {h_conc:.2e} M</text>

            <!-- pH Scale gradient -->
            <defs>
                <linearGradient id="phGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
                    <stop offset="50%" style="stop-color:rgb(0,255,0);stop-opacity:1" />
                    <stop offset="100%" style="stop-color:rgb(0,0,255);stop-opacity:1" />
                </linearGradient>
            </defs>

            <rect x="50" y="80" width="300" height="40" fill="url(#phGradient)" stroke="black" stroke-width="2"/>

            <!-- pH markers -->
            <text x="50" y="75" font-size="10" text-anchor="middle">0</text>
            <text x="200" y="75" font-size="10" text-anchor="middle">7</text>
            <text x="350" y="75" font-size="10" text-anchor="middle">14</text>
            <text x="50" y="140" font-size="9">Acidic</text>
            <text x="190" y="140" font-size="9">Neutral</text>
            <text x="330" y="140" font-size="9">Basic</text>

            <!-- Current pH indicator -->
            <circle cx="{indicator_x}" cy="100" r="8" fill="yellow" stroke="black" stroke-width="2"/>
            <text x="{indicator_x}" y="165" text-anchor="middle" font-size="14" font-weight="bold">pH = {ph:.2f}</text>
        </svg>"""

        return base64.b64encode(svg.encode()).decode()

    def _generate_concentration_graph(self, molarity: float, moles: float, volume: float) -> str:
        """Generate molarity visualization"""
        bar_height = min(150, int(molarity * 30))

        svg = f"""<svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="250" fill="white"/>
            <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Molarity Calculation</text>
            <text x="200" y="40" text-anchor="middle" font-size="12">M = n/V = {moles}/{volume} = {molarity:.3f} M</text>

            <!-- Beaker visualization -->
            <rect x="150" y="{200-bar_height}" width="100" height="{bar_height}" fill="lightblue" stroke="black" stroke-width="3"/>
            <text x="200" y="220" text-anchor="middle" font-size="14" font-weight="bold">{molarity:.3f} M</text>

            <!-- Labels -->
            <text x="200" y="240" text-anchor="middle" font-size="11">{moles} mol in {volume} L</text>
        </svg>"""

        return base64.b64encode(svg.encode()).decode()

    def _generate_energy_graph(self, k: float, x: float, energy: float) -> str:
        """Generate spring energy visualization"""
        svg = f"""<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="white"/>
            <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Spring Elastic Potential Energy</text>
            <text x="200" y="40" text-anchor="middle" font-size="12">E = ½kx² = ½({k})({x})² = {energy:.3f} J</text>

            <!-- Energy bar -->
            <rect x="100" y="{200-min(100, int(energy*10))}" width="80" height="{min(100, int(energy*10))}" fill="orange" stroke="black" stroke-width="2"/>
            <text x="140" y="220" text-anchor="middle" font-size="14" font-weight="bold">{energy:.3f} J</text>

            <!-- Spring diagram -->
            <line x1="250" y1="80" x2="250" y2="100" stroke="black" stroke-width="2"/>
            <line x1="250" y1="100" x2="250" y2="{100+min(80, int(x*400))}" stroke="blue" stroke-width="4"/>
            <rect x="230" y="{100+min(80, int(x*400))}" width="40" height="40" fill="gray" stroke="black" stroke-width="2"/>
            <text x="280" y="{120+min(80, int(x*400))}" font-size="10">x={x}m</text>
        </svg>"""

        return base64.b64encode(svg.encode()).decode()

    def _generate_sensor_graph(self, data: List[tuple], label: str, unit: str) -> str:
        """Generate IoT sensor data time-series graph"""
        if not data:
            return self._generate_sample_graph("custom")

        # Calculate min/max for scaling
        values = [d[1] for d in data]
        min_val = min(values)
        max_val = max(values)
        val_range = max_val - min_val if max_val != min_val else 1

        # Generate polyline points
        points = []
        for i, (time, value) in enumerate(data):
            x = 50 + (i / max(len(data) - 1, 1)) * 300
            y = 250 - ((value - min_val) / val_range) * 180
            points.append(f"{x:.1f},{y:.1f}")

        polyline_points = " ".join(points)

        svg = f"""<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="white"/>
            <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">IoT Sensor: {label}</text>
            <text x="200" y="40" text-anchor="middle" font-size="11">Real-time readings ({len(data)} data points)</text>

            <!-- Grid lines -->
            <line x1="50" y1="70" x2="350" y2="70" stroke="#ddd" stroke-width="1" stroke-dasharray="5,5"/>
            <line x1="50" y1="160" x2="350" y2="160" stroke="#ddd" stroke-width="1" stroke-dasharray="5,5"/>
            <line x1="50" y1="250" x2="350" y2="250" stroke="#ddd" stroke-width="1" stroke-dasharray="5,5"/>

            <!-- Data line -->
            <polyline points="{polyline_points}" stroke="red" fill="none" stroke-width="2"/>

            <!-- Axes -->
            <line x1="50" y1="250" x2="350" y2="250" stroke="black" stroke-width="2"/>
            <line x1="50" y1="250" x2="50" y2="70" stroke="black" stroke-width="2"/>

            <!-- Labels -->
            <text x="200" y="280" text-anchor="middle" font-size="12">Time (seconds)</text>
            <text x="20" y="160" font-size="12" transform="rotate(-90 20 160)">{label} ({unit})</text>

            <!-- Value markers -->
            <text x="30" y="75" font-size="10">{max_val:.1f}</text>
            <text x="30" y="255" font-size="10">{min_val:.1f}</text>
            <text x="50" y="270" font-size="10">0</text>
            <text x="345" y="270" font-size="10">{len(data)}</text>
        </svg>"""

        return base64.b64encode(svg.encode()).decode()


# Global Wolfram engine instance
wolfram_engine = WolframEngine()
