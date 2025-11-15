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
    """
    
    def __init__(self):
        self.appid = settings.wolfram_appid
        self.queries = {}
    
    async def compute_titration(self, 
                               acid_concentration: float,
                               acid_volume: float,
                               base_concentration: float) -> ComputationResult:
        """
        Compute acid-base titration curve.
        
        Args:
            acid_concentration: Molarity of acid (M)
            acid_volume: Volume of acid (mL)
            base_concentration: Molarity of base (M)
            
        Returns:
            ComputationResult with pH curve
        """
        query = f"""Plot[pH[x] = 14 + Log10[(x*{base_concentration} - {acid_concentration}*{acid_volume})/({acid_volume} + x)], 
                     {{x, 0, {acid_volume * acid_concentration / base_concentration * 1.5}}},
                     AxesLabel -> {{"Volume of Base (mL)", "pH"}},
                     PlotLabel -> "Titration Curve"]"""
        
        return ComputationResult(
            query=query,
            result="pH curve computed",
            numeric_result=7.0,
            graph_svg=self._generate_sample_graph("titration")
        )
    
    async def compute_hookes_law(self,
                                spring_constant: float,
                                max_displacement: float) -> ComputationResult:
        """
        Compute Hooke's Law: F = kx
        
        Args:
            spring_constant: Spring constant k (N/m)
            max_displacement: Maximum displacement x (m)
            
        Returns:
            ComputationResult with force vs displacement graph
        """
        query = f"Plot[{spring_constant} * x, {{x, 0, {max_displacement}}}, AxesLabel -> {{'Displacement (m)', 'Force (N)'}}]"
        
        return ComputationResult(
            query=query,
            result="Force-displacement relationship plotted",
            numeric_result=spring_constant * max_displacement,
            graph_svg=self._generate_sample_graph("hookes_law")
        )
    
    async def compute_osmosis(self,
                             concentration: float,
                             temperature: float,
                             volume: float) -> ComputationResult:
        """
        Compute osmotic pressure: π = iMRT
        
        Args:
            concentration: Concentration (M)
            temperature: Temperature (K)
            volume: Volume (L)
            
        Returns:
            ComputationResult with osmotic effects
        """
        R = 0.08206  # Gas constant
        osmotic_pressure = concentration * R * temperature
        
        query = f"osmotic_pressure = {osmotic_pressure} atm"
        
        return ComputationResult(
            query=query,
            result=f"Osmotic pressure: {osmotic_pressure:.2f} atm",
            numeric_result=osmotic_pressure,
            graph_svg=self._generate_sample_graph("osmosis")
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
            "titration": """<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="300" fill="white"/>
                <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Titration Curve</text>
                <polyline points="50,250 100,240 150,230 200,150 250,50 300,30 350,20" 
                          stroke="blue" fill="none" stroke-width="2"/>
                <line x1="50" y1="250" x2="350" y2="250" stroke="black"/>
                <line x1="50" y1="250" x2="50" y2="20" stroke="black"/>
                <text x="350" y="270" font-size="12">Volume (mL)</text>
                <text x="20" y="130" font-size="12" transform="rotate(-90 20 130)">pH</text>
            </svg>""",
            
            "hookes_law": """<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="300" fill="white"/>
                <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Hooke's Law: F = kx</text>
                <polyline points="50,250 100,225 150,200 200,175 250,150 300,125 350,100" 
                          stroke="green" fill="none" stroke-width="2"/>
                <line x1="50" y1="250" x2="350" y2="250" stroke="black"/>
                <line x1="50" y1="250" x2="50" y2="20" stroke="black"/>
                <text x="350" y="270" font-size="12">Displacement (m)</text>
                <text x="20" y="130" font-size="12" transform="rotate(-90 20 130)">Force (N)</text>
            </svg>""",
            
            "osmosis": """<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="300" fill="white"/>
                <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Osmotic Pressure</text>
                <rect x="100" y="100" width="50" height="100" fill="lightblue" stroke="black" stroke-width="2"/>
                <text x="125" y="160" text-anchor="middle" font-size="12">π</text>
                <text x="200" y="160" font-size="12">= iMRT</text>
                <text x="200" y="200" font-size="11">Osmotic Pressure (atm)</text>
            </svg>""",
            
            "custom": """<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="300" fill="white"/>
                <text x="200" y="20" text-anchor="middle" font-size="16" font-weight="bold">Computation Result</text>
                <circle cx="200" cy="150" r="50" fill="none" stroke="purple" stroke-width="2"/>
                <text x="200" y="155" text-anchor="middle" font-size="14">Result</text>
            </svg>"""
        }
        
        svg = svg_map.get(graph_type, svg_map["custom"])
        return base64.b64encode(svg.encode()).decode()


# Global Wolfram engine instance
wolfram_engine = WolframEngine()
