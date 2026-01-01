#!/usr/bin/env python3
"""
Cross-Domain Innovation Engine
Author: Pranay M.

System that identifies technologies, concepts, and methods in one field
that could revolutionize another unrelated field.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                💡 CROSS-DOMAIN INNOVATION ENGINE 💡                            ║
║                    Revolutionary Technology Transfer Platform                  ║
║                           Author: Pranay M.                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Technology Scanner", "tech_scan", "Scan technologies across domains"),
    "2": ("Analogy Finder", "analogy", "Find analogies between fields"),
    "3": ("Transfer Assessor", "transfer", "Assess transfer potential"),
    "4": ("Innovation Generator", "innovate", "Generate cross-domain innovations"),
    "5": ("Feasibility Analyzer", "feasibility", "Analyze implementation feasibility"),
    "6": ("Impact Predictor", "impact", "Predict innovation impact"),
    "7": ("Patent Analyzer", "patent", "Analyze patent landscapes"),
    "8": ("Collaboration Matcher", "collab", "Match potential collaborators"),
    "9": ("Roadmap Builder", "roadmap", "Build innovation roadmaps"),
    "10": ("Innovation Dashboard", "dashboard", "View innovation opportunities dashboard")
}

SYSTEM_PROMPTS = {
    "tech_scan": """You are an expert in technology scouting across all domains.

For each technology scan, identify:

1. **Emerging Technologies**: Cutting-edge developments
2. **Breakthrough Methods**: Novel approaches, techniques
3. **Successful Solutions**: What's working in each field
4. **Underlying Principles**: Core concepts and mechanisms
5. **Maturity Assessment**: Development stage
6. **Transfer Potential**: Applicability to other domains

Scan technologies across diverse domains.""",

    "analogy": """You are an expert in analogical reasoning and cross-domain thinking.

For each analogy finding request, discover:

1. **Structural Analogies**: Similar underlying structures
2. **Functional Analogies**: Similar functions, purposes
3. **Process Analogies**: Similar methods, workflows
4. **Problem Analogies**: Similar challenges solved
5. **Analogy Strength**: How strong the parallel is
6. **Transfer Insights**: What can be learned

Find analogies between different fields.""",

    "transfer": """You are an expert in technology transfer and adaptation.

For each transfer assessment, evaluate:

1. **Compatibility Analysis**: How technology fits new domain
2. **Adaptation Requirements**: Modifications needed
3. **Barrier Identification**: Obstacles to transfer
4. **Enabler Identification**: Factors supporting transfer
5. **Success Probability**: Likelihood of successful transfer
6. **Resource Estimate**: What transfer requires

Assess cross-domain transfer potential.""",

    "innovate": """You are an expert in innovation and creative problem-solving.

For each innovation generation, create:

1. **Innovation Concept**: New application of existing technology
2. **Value Proposition**: Benefits in new domain
3. **Differentiation**: How it's better than existing solutions
4. **Technical Approach**: How to implement
5. **Use Cases**: Specific applications
6. **Development Path**: How to realize the innovation

Generate cross-domain innovation concepts.""",

    "feasibility": """You are an expert in innovation feasibility analysis.

For each feasibility analysis, evaluate:

1. **Technical Feasibility**: Can it be built?
2. **Economic Feasibility**: Does it make financial sense?
3. **Market Feasibility**: Is there demand?
4. **Resource Feasibility**: Are resources available?
5. **Regulatory Feasibility**: Legal/regulatory barriers
6. **Timeline Assessment**: How long to implement

Analyze innovation implementation feasibility.""",

    "impact": """You are an expert in technology impact assessment.

For each impact prediction, analyze:

1. **Direct Impact**: Immediate effects in target domain
2. **Indirect Impact**: Secondary effects
3. **Disruption Potential**: How disruptive could this be
4. **Value Creation**: Economic and social value
5. **Risk Assessment**: Potential negative impacts
6. **Long-term Implications**: Future trajectory

Predict cross-domain innovation impact.""",

    "patent": """You are an expert in patent analysis and IP strategy.

For each patent analysis, examine:

1. **Patent Landscape**: Existing patents in space
2. **White Spaces**: Unpatented opportunities
3. **Freedom to Operate**: FTO assessment
4. **Patent Strategy**: How to protect innovation
5. **Prior Art**: Relevant existing IP
6. **Licensing Opportunities**: Potential partnerships

Analyze patent landscapes for innovations.""",

    "collab": """You are an expert in research collaboration and partnerships.

For each collaboration matching, identify:

1. **Potential Partners**: Organizations with relevant expertise
2. **Complementary Capabilities**: What each brings
3. **Collaboration Models**: Partnership structures
4. **Alignment Assessment**: Goal and culture fit
5. **Value Distribution**: How value would be shared
6. **Engagement Approach**: How to initiate collaboration

Match potential innovation collaborators.""",

    "roadmap": """You are an expert in innovation roadmapping and planning.

For each roadmap, develop:

1. **Vision Statement**: End state description
2. **Milestone Definition**: Key achievements
3. **Phase Planning**: Development stages
4. **Resource Planning**: Requirements by phase
5. **Risk Mitigation**: Handling uncertainties
6. **Success Metrics**: How to measure progress

Build innovation development roadmaps.""",

    "dashboard": """You are an expert in innovation portfolio management.

For each dashboard, generate:

1. **Opportunity Inventory**: Identified innovations
2. **Transfer Pipeline**: Technologies being transferred
3. **Feasibility Status**: Viability assessments
4. **Impact Projections**: Expected outcomes
5. **Resource Allocation**: Investment priorities
6. **Priority Actions**: Next steps

View innovation opportunities dashboard."""
}

def get_multiline_input(prompt_text):
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

def display_menu():
    console.print(BANNER, style="bold blue")
    table = Table(title="💡 Innovation Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=42)
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_module(module_key):
    name, key, desc = MODULES[module_key]
    console.print(Panel(f"💡 {name}", style="bold green"))
    user_input = get_multiline_input(f"Describe your {name.lower()} request:")
    with console.status(f"[bold green]Processing {name}..."):
        response = query_llama(SYSTEM_PROMPTS[key], user_input)
    console.print(Panel(Markdown(response), title=f"💡 {name} Results", border_style="green"))

def main():
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Cross-Domain Innovation Engine![/yellow]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        try:
            run_module(choice)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
