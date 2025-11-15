"""Experiment scenario definitions"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class ExperimentLevel(str, Enum):
    """Difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class ExperimentStep:
    """Single step in an experiment"""
    step_number: int
    title: str
    description: str
    instructions: str
    expected_observation: str
    learning_objectives: List[str]
    tips: List[str] = field(default_factory=list)


@dataclass
class ExperimentScenario:
    """Complete experiment scenario"""
    experiment_id: str
    title: str
    description: str
    subject: str  # physics, chemistry, biology
    level: ExperimentLevel
    duration_minutes: int
    learning_objectives: List[str]
    materials: List[str]
    steps: List[ExperimentStep]
    safety_notes: List[str]
    wolfram_computations: Dict[str, str]  # Computation name -> Wolfram query
    
    def get_step(self, step_number: int) -> ExperimentStep:
        """Get specific step"""
        for step in self.steps:
            if step.step_number == step_number:
                return step
        return None


# Chemistry: Acid-Base Titration
TITRATION_SCENARIO = ExperimentScenario(
    experiment_id="chem_titration",
    title="Acid-Base Titration: Finding Molarity",
    description="Determine the concentration (molarity) of an unknown acid solution using standard base titration.",
    subject="chemistry",
    level=ExperimentLevel.BEGINNER,
    duration_minutes=45,
    learning_objectives=[
        "Understand acid-base neutralization reactions",
        "Learn proper titration technique",
        "Determine unknown solution concentration",
        "Read meniscus correctly",
        "Calculate molarity from experimental data"
    ],
    materials=[
        "Unknown acid solution (~0.1 M HCl)",
        "Standard NaOH solution (0.1 M)",
        "Burette",
        "Erlenmeyer flask",
        "Pipette",
        "Phenolphthalein indicator",
        "Distilled water",
        "Beaker"
    ],
    steps=[
        ExperimentStep(
            step_number=1,
            title="Setup and Calibration",
            description="Prepare apparatus and standardize burette",
            instructions="1. Clean the burette thoroughly\n2. Add NaOH solution\n3. Remove air bubbles\n4. Record initial volume",
            expected_observation="Clear meniscus at starting mark, no air bubbles in tip",
            learning_objectives=["Proper apparatus handling"],
            tips=[
                "Always read from bottom of meniscus",
                "Use distilled water to rinse burette 3 times first"
            ]
        ),
        ExperimentStep(
            step_number=2,
            title="Add Acid and Indicator",
            description="Prepare flask with unknown acid and indicator",
            instructions="1. Pipette 20 mL of unknown acid into flask\n2. Add 2-3 drops of phenolphthalein\n3. Add ~30 mL distilled water",
            expected_observation="Colorless solution (acid in excess of phenolphthalein endpoint)",
            learning_objectives=["Indicator behavior", "Solution preparation"]
        ),
        ExperimentStep(
            step_number=3,
            title="Titration Process",
            description="Slowly add base until endpoint is reached",
            instructions="1. Open burette tap slowly\n2. Swirl flask continuously\n3. When nearing endpoint, add drop by drop\n4. Stop when pale pink color persists for 30 seconds",
            expected_observation="Solution turns from colorless to pale pink (endpoint)",
            learning_objectives=["Titration technique", "Endpoint recognition"]
        ),
        ExperimentStep(
            step_number=4,
            title="Calculate Results",
            description="Use titration data to find acid molarity",
            instructions="Volume of NaOH used × Molarity of NaOH = Moles of NaOH\nMoles of HCl = Moles of NaOH (1:1 ratio)\nMolarity of HCl = Moles HCl / Volume (L)",
            expected_observation="Calculated molarity should be ~0.1 M for the unknown",
            learning_objectives=["Stoichiometry", "Data analysis"]
        )
    ],
    safety_notes=[
        "Wear eye protection at all times",
        "NaOH is caustic - avoid skin contact",
        "Report any spills immediately",
        "Wash hands after experiment"
    ],
    wolfram_computations={
        "pH_curve": "Plot[pH[x] = 14 + Log10[(x*0.1 - 0.1*20)/(20 + x)], {x, 0, 30}, AxesLabel -> {'Volume of NaOH (mL)', 'pH'}, PlotLabel -> 'Titration Curve']"
    }
)


# Physics: Hooke's Law
HOOKES_LAW_SCENARIO = ExperimentScenario(
    experiment_id="phys_hookes_law",
    title="Hooke's Law: Spring Constant Determination",
    description="Experimentally determine the spring constant of a spring using various masses.",
    subject="physics",
    level=ExperimentLevel.BEGINNER,
    duration_minutes=40,
    learning_objectives=[
        "Understand Hooke's Law (F = kx)",
        "Determine spring constant experimentally",
        "Create force vs displacement graphs",
        "Understand linear relationships in physics",
        "Apply mathematical modeling to physical systems"
    ],
    materials=[
        "Spring",
        "Retort stand",
        "Clamp",
        "Ruler or measuring tape (0-50 cm)",
        "Various masses (100g, 200g, 300g, 400g, 500g)",
        "Mass hanger",
        "Paper and pencil"
    ],
    steps=[
        ExperimentStep(
            step_number=1,
            title="Setup the Apparatus",
            description="Mount spring vertically on retort stand",
            instructions="1. Attach spring to clamp\n2. Hang mass hanger (without masses)\n3. Mark initial position with ruler\n4. Record initial position (x₀)",
            expected_observation="Spring hanging vertically with slight stretch from hanger weight",
            learning_objectives=["Apparatus setup"],
            tips=["Ensure spring hangs freely without touching surfaces"]
        ),
        ExperimentStep(
            step_number=2,
            title="Add Masses and Measure",
            description="Add masses incrementally and record displacement",
            instructions="1. Add 100g mass\n2. Wait for spring to stabilize\n3. Record new position\n4. Calculate displacement: Δx = x - x₀\n5. Repeat for 100g, 200g, 300g, 400g, 500g",
            expected_observation="Spring stretches more with each additional mass",
            learning_objectives=["Data collection", "Measurement technique"]
        ),
        ExperimentStep(
            step_number=3,
            title="Calculate Spring Constant",
            description="Use F = kx to find spring constant",
            instructions="For each measurement:\n1. Force (N) = mass (kg) × 9.8 m/s²\n2. Displacement (m) = Δx in meters\n3. Spring constant k = F / Δx (N/m)\n4. Average all k values",
            expected_observation="Consistent k value across all measurements (~200-500 N/m typically)",
            learning_objectives=["Calculations", "Data analysis"]
        ),
        ExperimentStep(
            step_number=4,
            title="Plot Results",
            description="Create force vs displacement graph",
            instructions="1. Plot Force (N) on y-axis\n2. Plot Displacement (m) on x-axis\n3. Should see linear relationship\n4. Slope of line = spring constant k",
            expected_observation="Straight line through origin, slope = k",
            learning_objectives=["Graphical analysis", "Linear relationships"]
        )
    ],
    safety_notes=[
        "Ensure spring is secure before adding masses",
        "Don't exceed maximum displacement",
        "Keep fingers clear of falling masses",
        "Wear shoes to protect feet from dropped weights"
    ],
    wolfram_computations={
        "force_displacement": "Plot[{x, 300*x}, {x, 0, 0.1}, AxesLabel -> {'Displacement (m)', 'Force (N)'}, PlotLabel -> 'Hooke\\'s Law: F = kx']"
    }
)


# Biology: Osmosis and Cell Membrane
OSMOSIS_SCENARIO = ExperimentScenario(
    experiment_id="bio_osmosis",
    title="Osmosis: Water Movement Across Membranes",
    description="Observe and measure water movement across a semipermeable membrane in response to concentration gradients.",
    subject="biology",
    level=ExperimentLevel.INTERMEDIATE,
    duration_minutes=50,
    learning_objectives=[
        "Understand osmosis and osmotic pressure",
        "Observe water movement at cellular level",
        "Understand hypertonic, hypotonic, and isotonic solutions",
        "Model osmotic pressure (π = iMRT)",
        "Apply concepts to real biological systems"
    ],
    materials=[
        "Dialysis tubing or potato cores",
        "Distilled water",
        "Concentrated salt solution (20% NaCl)",
        "Dilute salt solution (5% NaCl)",
        "Measuring cylinder",
        "Ruler",
        "Weighing scale",
        "String",
        "Paper towels"
    ],
    steps=[
        ExperimentStep(
            step_number=1,
            title="Prepare Osmosis Systems",
            description="Create semipermeable membrane systems with different solute concentrations",
            instructions="Setup 3 containers:\nA) Distilled water (hypotonic)\nB) 5% NaCl (isotonic)\nC) 20% NaCl (hypertonic)\nPlace dialysis tubing with 10mL concentrated salt solution in each",
            expected_observation="Three containers with labeled bags of similar initial size",
            learning_objectives=["Solution preparation"],
            tips=["Tie dialysis bags securely to prevent leaks"]
        ),
        ExperimentStep(
            step_number=2,
            title="Initial Measurements",
            description="Record starting mass and volume of each bag",
            instructions="For each bag:\n1. Measure mass with scale\n2. Measure length with ruler\n3. Record observations (appearance, firmness)\n4. Note the time",
            expected_observation="All bags similar size initially, approximately 10mL content",
            learning_objectives=["Data collection", "Baseline establishment"]
        ),
        ExperimentStep(
            step_number=3,
            title="Observation Over Time",
            description="Monitor changes at intervals (30 min, 1 hr, 2 hrs, 24 hrs)",
            instructions="At each time interval:\n1. Remove bag, dry gently with paper towel\n2. Weigh again\n3. Measure length again\n4. Note appearance changes\n5. Return to same container\n6. Record observations",
            expected_observation="Bag A swells (hypotonic), Bag B stable (isotonic), Bag C shrinks (hypertonic)",
            learning_objectives=["Long-term observation", "Pattern recognition"]
        ),
        ExperimentStep(
            step_number=4,
            title="Analyze and Calculate",
            description="Quantify osmosis and calculate osmotic pressure",
            instructions="1. Calculate mass change (%) for each bag\n2. Osmotic pressure π = iMRT\n   where i = van't Hoff factor, M = molarity, R = 0.08206, T = 298K\n3. Plot mass change vs time\n4. Compare theoretical osmotic pressures",
            expected_observation="Quantitative differences between hypertonic and hypotonic systems",
            learning_objectives=["Osmotic pressure calculation", "Data analysis"]
        )
    ],
    safety_notes=[
        "Salt solutions are safe but don't ingest",
        "Wash hands after handling",
        "Use dialysis tubing carefully to avoid tears",
        "Dispose of salt solutions properly"
    ],
    wolfram_computations={
        "osmotic_pressure": "osmotic_pressure[M_, T_] := M * 0.08206 * T; Plot[osmotic_pressure[c, 298], {c, 0, 1}, AxesLabel -> {'Molarity (M)', 'Osmotic Pressure (atm)'}, PlotLabel -> 'Osmotic Pressure: π = MRT']"
    }
)


# Scenario registry
SCENARIOS = {
    "acid_base_titration": TITRATION_SCENARIO,
    "hookes_law": HOOKES_LAW_SCENARIO,
    "osmosis": OSMOSIS_SCENARIO
}


def get_scenario(experiment_id: str) -> ExperimentScenario:
    """Get experiment scenario by ID"""
    return SCENARIOS.get(experiment_id)


def list_scenarios() -> Dict[str, ExperimentScenario]:
    """List all available scenarios"""
    return SCENARIOS
