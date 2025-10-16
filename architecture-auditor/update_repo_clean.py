# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Script to update repository with v2.0 improvements
Clean version without special characters for Windows compatibility
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Execute a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("="*60)
    print("UPDATING ARCHITECTURE AUDITOR REPOSITORY v2.0")
    print("="*60)
    
    # Check we're in the correct directory
    current_dir = Path.cwd()
    if not (current_dir / "auditor_clean.py").exists():
        print("[ERROR] Run this script from the architecture-auditor/ directory")
        sys.exit(1)
    
    print("[OK] Correct directory detected")
    
    # Check git
    success, _, _ = run_command("git --version")
    if not success:
        print("[ERROR] Git is not installed or not in PATH")
        sys.exit(1)
    
    print("[OK] Git available")
    
    # Check repository status
    success, output, _ = run_command("git status --porcelain")
    if not success:
        print("[ERROR] Not a valid git repository")
        sys.exit(1)
    
    # Show new/modified files
    if output.strip():
        print("\nNew/modified files:")
        for line in output.strip().split('\n'):
            print(f"  {line}")
    
    # Confirm update
    print(f"\nFiles to add to repository:")
    new_files = [
        "auditor_clean.py",
        "audit_runner_clean.py", 
        "improvement_guide.py",
        "detailed_report.html",
        "audit_report_LOCAL-RAG-JJ.json",
        "EXAMPLES.md",
        "CHANGELOG_v2.md",
        "install.bat",
        "install_improved.sh",
        "update_repo_clean.py"
    ]
    
    for file in new_files:
        if (current_dir / file).exists():
            print(f"  [OK] {file}")
        else:
            print(f"  [SKIP] {file} (not found)")
    
    # Confirm
    response = input(f"\nContinue with repository update? (y/N): ")
    if response.lower() != 'y':
        print("[CANCEL] Update cancelled")
        sys.exit(0)
    
    # Add files
    print("\nAdding files...")
    
    # Add specific files
    files_to_add = []
    for file in new_files:
        if (current_dir / file).exists():
            files_to_add.append(file)
    
    # Add modified existing files
    existing_files = ["README.md", "QUICK_START.md", "requirements.txt"]
    for file in existing_files:
        if (current_dir / file).exists():
            files_to_add.append(file)
    
    for file in files_to_add:
        success, _, error = run_command(f"git add {file}")
        if success:
            print(f"  [OK] {file}")
        else:
            print(f"  [ERROR] {file}: {error}")
    
    # Commit
    print("\nCreating commit...")
    commit_message = """feat: Architecture Auditor v2.0 - Major improvements

New Features:
- auditor_clean.py: Windows-compatible version without special characters
- audit_runner_clean.py: Intelligent project type detection
- Automatic detection for: web_app, api_rest, rag_app, microservice
- Project-specific scoring weights and recommendations
- Improved installation scripts for Windows/Linux/Mac

Enhanced Analysis:
- Context-aware recommendations based on project type
- Better code quality analysis for Python projects
- Specific patterns detection (MVC, Repository, Factory, etc.)
- Weighted scoring system per project type

Documentation:
- EXAMPLES.md: Comprehensive usage examples
- CHANGELOG_v2.md: Detailed version history
- Updated README.md and QUICK_START.md
- HTML report generation with detailed analysis

Technical Improvements:
- Better error handling and logging
- JSON structured output with metadata
- CI/CD integration examples (GitHub Actions, Azure DevOps)
- Pre-commit hooks and automation scripts
- Clean encoding without special characters for Windows compatibility

Tested with LOCAL-RAG-JJ project:
- Automatic detection as rag_app
- RAG-specific recommendations (Factory for LLMs, Repository for docs)
- Improved scoring: 37.5/100 with contextual weights"""

    success, _, error = run_command(f'git commit -m "{commit_message}"')
    if success:
        print("  [OK] Commit created successfully")
    else:
        print(f"  [ERROR] Commit error: {error}")
        return
    
    # Show commit information
    success, output, _ = run_command("git log --oneline -1")
    if success:
        print(f"  Commit: {output.strip()}")
    
    # Ask about push
    print(f"\nPush to remote repository? (y/N): ")
    response = input()
    
    if response.lower() == 'y':
        print("Pushing...")
        
        # Check remote
        success, output, _ = run_command("git remote -v")
        if not success or not output.strip():
            print("[ERROR] No remote repository configured")
            print("Configure remote with: git remote add origin <URL>")
            return
        
        # Push
        success, output, error = run_command("git push")
        if success:
            print("  [OK] Push completed successfully")
        else:
            print(f"  [ERROR] Push error: {error}")
            print("You may need to configure upstream: git push -u origin main")
    
    # Create tag for version
    print(f"\nCreate tag v2.0.0? (y/N): ")
    response = input()
    
    if response.lower() == 'y':
        success, _, error = run_command("git tag -a v2.0.0 -m 'Architecture Auditor v2.0.0 - Major improvements'")
        if success:
            print("  [OK] Tag v2.0.0 created")
            
            # Push tag
            success, _, error = run_command("git push origin v2.0.0")
            if success:
                print("  [OK] Tag sent to remote repository")
            else:
                print(f"  [ERROR] Error sending tag: {error}")
        else:
            print(f"  [ERROR] Error creating tag: {error}")
    
    print("\n" + "="*60)
    print("UPDATE COMPLETED")
    print("="*60)
    print("\nSummary of changes:")
    print("  • Windows-compatible auditor (no special characters)")
    print("  • Automatic project type detection")
    print("  • Type-specific recommendations")
    print("  • Complete documentation with examples")
    print("  • Improved installation scripts")
    print("  • CI/CD integration (GitHub Actions, Azure DevOps)")
    
    print("\nNext steps:")
    print("  1. Test installation: install.bat (Windows) or ./install.sh (Linux)")
    print("  2. Run examples: python audit_runner_clean.py <project>")
    print("  3. Review documentation: README.md, EXAMPLES.md")
    print("  4. Share with community")
    
    print(f"\nUseful links:")
    print("  • Repository: https://github.com/juanjovip2490/architecture-auditor")
    print("  • Issues: https://github.com/juanjovip2490/architecture-auditor/issues")
    print("  • Documentation: README.md")

if __name__ == "__main__":
    main()