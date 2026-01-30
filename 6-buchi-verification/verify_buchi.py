"""
Buchi verification of Alice & Bob protocols.
Verifies all 25 (model, property) pairs.
Produces counter-examples in (prefix-trace, cyclic-suffix-trace) form.
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))
sys.path.insert(0, str(Path(__file__).parent.parent / "3-protocols"))

from ab_models_soup import get_model
from isoup import get_isoup_property
from buchi import verify_buchi, format_counter_example


MODEL_NAMES = ["AB1", "AB2", "AB3", "AB4", "AB5"]
PROPERTY_NAMES = ["P1", "P2", "P3", "P4", "P5"]
PROPERTY_DESCRIPTIONS = {
    "P1": "Exclusion (never A.CS & B.CS)",
    "P2": "No deadlock",
    "P3": "At least one in CS (liveness)",
    "P4": "If one wants in, it gets in",
    "P5": "Uncontested progress",
}


def verify_one(model_name, prop_name):
    """Verify a single (model, property) pair."""
    system_ls = get_model(model_name)          # Soup Sem
    property_ls = get_isoup_property(prop_name) # iSoup Sem
    satisfied, ce = verify_buchi(system_ls, property_ls)  # Composition + BFS + cycle
    return satisfied, ce


def run_all_verifications():
    """Run all 25 (model, property) pairs and collect results."""
    results = {}

    for model_name in MODEL_NAMES:
        for prop_name in PROPERTY_NAMES:
            print(f"Verifying {model_name} x {prop_name}...", end=" ", flush=True)
            satisfied, ce = verify_one(model_name, prop_name)
            status = "SATISFIED" if satisfied else "VIOLATED"
            print(status)
            results[(model_name, prop_name)] = (satisfied, ce)

    return results


def print_results_table(results):
    """Print a summary table of all verification results."""
    # Header
    header = f"{'Model':<8}"
    for p in PROPERTY_NAMES:
        header += f" {p:<12}"
    print("\n" + "=" * 70)
    print("BUCHI VERIFICATION RESULTS")
    print("=" * 70)
    print(header)
    print("-" * 70)

    for m in MODEL_NAMES:
        row = f"{m:<8}"
        for p in PROPERTY_NAMES:
            satisfied, _ = results[(m, p)]
            mark = "OK" if satisfied else "FAIL"
            row += f" {mark:<12}"
        print(row)

    print("=" * 70)


def print_counter_examples(results):
    """Print all counter-examples for violated properties."""
    print("\n" + "=" * 70)
    print("COUNTER-EXAMPLES")
    print("=" * 70)

    any_violated = False
    for m in MODEL_NAMES:
        for p in PROPERTY_NAMES:
            satisfied, ce = results[(m, p)]
            if not satisfied:
                any_violated = True
                print(f"\n--- {m} x {p} ({PROPERTY_DESCRIPTIONS[p]}) ---")
                print(format_counter_example(ce))

    if not any_violated:
        print("\nNo violations found - all properties satisfied.")


def generate_markdown(results):
    """Generate VerificationBuchiAliceBob.md content."""
    lines = []
    lines.append("# Verification Buchi - Alice & Bob")
    lines.append("")
    lines.append("## Commande")
    lines.append("```")
    lines.append("cd 6-buchi-verification")
    lines.append("python verify_buchi.py")
    lines.append("```")
    lines.append("")
    lines.append("## Resultats")
    lines.append("")

    # Table header
    header = "| Model |"
    separator = "|-------|"
    for p in PROPERTY_NAMES:
        header += f" {p} |"
        separator += "------|"
    lines.append(header)
    lines.append(separator)

    for m in MODEL_NAMES:
        row = f"| {m} |"
        for p in PROPERTY_NAMES:
            satisfied, _ = results[(m, p)]
            mark = "OK" if satisfied else "FAIL"
            row += f" {mark} |"
        lines.append(row)

    lines.append("")
    lines.append("- **OK** = propriete satisfaite (pas de cycle acceptant)")
    lines.append("- **FAIL** = propriete violee (cycle acceptant trouve)")
    lines.append("")

    # Counter-examples
    lines.append("## Contre-exemples")
    lines.append("")

    any_violated = False
    for m in MODEL_NAMES:
        for p in PROPERTY_NAMES:
            satisfied, ce = results[(m, p)]
            if not satisfied:
                any_violated = True
                lines.append(f"### {m} x {p} - {PROPERTY_DESCRIPTIONS[p]}")
                lines.append("```")
                lines.append(format_counter_example(ce))
                lines.append("```")
                lines.append("")

    if not any_violated:
        lines.append("Aucune violation trouvee.")
        lines.append("")

    # Analysis
    lines.append("## Analyse")
    lines.append("")
    lines.append("### Differences entre les modeles")
    lines.append("")
    lines.append("- **AB1**: Pas de mecanisme de protection. Alice et Bob peuvent entrer en CS simultanement.")
    lines.append("- **AB2**: Utilise des drapeaux. Garantit l'exclusion mutuelle mais peut causer un deadlock (les deux en W avec drapeaux UP).")
    lines.append("- **AB3**: Bob recule si le drapeau d'Alice est leve. Evite le deadlock mais Bob peut etre en famine (starvation).")
    lines.append("- **AB4**: Bob se retire dans un etat R avant de reessayer. Similaire a AB3 avec un etat de repli explicite.")
    lines.append("- **AB5**: Algorithme de Peterson avec variable `turn`. Garantit exclusion mutuelle, absence de deadlock, et equite.")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 70)
    print("BUCHI VERIFICATION - ALICE & BOB PROTOCOLS")
    print("=" * 70)
    print()

    # Run all verifications
    results = run_all_verifications()

    # Print table
    print_results_table(results)

    # Print counter-examples
    print_counter_examples(results)

    # Generate markdown
    md_content = generate_markdown(results)
    md_path = Path(__file__).parent / "VerificationBuchiAliceBob.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\nResults written to: {md_path}")
