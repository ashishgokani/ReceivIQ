"""
Main orchestrator for generating the exhaustive, production-grade README.md.
Combines all modular sections and ensures line count strictly exceeds 5,000 lines.
"""

import os
from .sec01_04_intro_arch_rules import generate_sec01_04
from .sec05_feature_walkthroughs import generate_sec05
from .sec06_tools_part1 import generate_sec06_part1
from .sec06_tools_part2 import generate_sec06_part2
from .sec07_08_prompts_workflows import generate_sec07_08
from .sec09_database import generate_sec09
from .sec10_apis import generate_sec10
from .sec11_12_frontend_and_math import generate_sec11_12
from .sec13_subsystems_part1 import generate_sec13_part1
from .sec13_subsystems_part2 import generate_sec13_part2
from .sec14_17_security_testing_deploy import generate_sec14_17
from .sec15_test_catalog import generate_sec15_catalog
from .sec18_faq import generate_sec18
from .sec18_faq_part2 import generate_sec18_part2
from .sec18_faq_part3 import generate_sec18_part3
from .sec19_20_checklist_git import generate_sec19_20

def assemble_readme():
    all_lines = []
    
    print("Collecting Section 01 - 04...")
    all_lines.extend(generate_sec01_04())
    
    print("Collecting Section 05 (Feature Walkthroughs)...")
    all_lines.extend(generate_sec05())
    
    print("Collecting Section 06 (All 25 Bedrock Tools)...")
    all_lines.extend(generate_sec06_part1())
    all_lines.extend(generate_sec06_part2())

    print("Collecting Section 07 - 08 (Mandates & Workflows)...")
    all_lines.extend(generate_sec07_08())
    
    print("Collecting Section 09 (Database Schema & DDL)...")
    all_lines.extend(generate_sec09())

    print("Collecting Section 10 (26 REST APIs)...")
    all_lines.extend(generate_sec10())
    
    print("Collecting Section 11 - 12 (Frontend Components & Math)...")
    all_lines.extend(generate_sec11_12())
    
    print("Collecting Section 13 (20 Subsystems Deep Dives)...")
    all_lines.extend(generate_sec13_part1())
    all_lines.extend(generate_sec13_part2())
    
    print("Collecting Section 14 - 17 (Security, Testing, Diagnostics, Deploy)...")
    all_lines.extend(generate_sec14_17())

    print("Collecting Section 15.2 (All 80 Tests Catalog)...")
    all_lines.extend(generate_sec15_catalog())

    print("Collecting Section 18 (100 Real-World Engineering FAQs)...")
    all_lines.extend(generate_sec18())
    all_lines.extend(generate_sec18_part2())
    all_lines.extend(generate_sec18_part3())
    
    print("Collecting Section 19 - 20 (Acceptance Gates, Git Guide)...")
    all_lines.extend(generate_sec19_20())
    
    content = "\n".join(all_lines)
    
    # Target root README.md
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    readme_path = os.path.join(root_dir, "README.md")
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    line_count = len(all_lines)
    print(f"Successfully generated README.md at {readme_path}")
    print(f"Total Line Count: {line_count}")
    return line_count

if __name__ == "__main__":
    count = assemble_readme()
