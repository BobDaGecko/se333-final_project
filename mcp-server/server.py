#!/usr/bin/env python3
"""
MCP Server for Intelligent Test Generation and Coverage Analysis
Implements tools for automated JUnit test generation, Maven execution,
coverage analysis, and Git automation.
"""

import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Software-Testing-Agent")

# ============================================================================
# Configuration
# ============================================================================

BENCHMARK_PATH = Path(__file__).parent.parent / "supplementals" / "benchmark-codebase"
COVERAGE_REPORT_PATH = BENCHMARK_PATH / "target" / "site" / "jacoco" / "jacoco.xml"


# ============================================================================
# Basic Calculator Tool (Phase 1)
# ============================================================================


@mcp.tool()
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Args:
        expression: A mathematical expression string (e.g., "2 + 2", "sqrt(16)")

    Returns:
        The result of the evaluation as a string
    """
    import math

    try:
        # Allow common math functions
        safe_dict = {
            "sqrt": math.sqrt,
            "pow": math.pow,
            "abs": abs,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "exp": math.exp,
        }
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


# ============================================================================
# Maven & Test Execution Tools (Phase 2)
# ============================================================================


@mcp.tool()
def run_maven_tests(project_path: Optional[str] = None) -> str:
    """
    Execute Maven tests on the specified project and generate JaCoCo coverage report.
    Tests will continue even if some fail to ensure coverage report generation.

    Args:
        project_path: Path to the Maven project (defaults to benchmark-codebase)

    Returns:
        Output from Maven test execution including test results
    """
    if project_path is None:
        project_path = str(BENCHMARK_PATH)

    try:
        # Run Maven clean test with test failure ignore, then generate JaCoCo report
        # This ensures coverage report is generated even when tests fail
        result = subprocess.run(
            ["mvn", "clean", "test", "-Dmaven.test.failure.ignore=true"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300,
        )

        # Generate JaCoCo report separately
        jacoco_result = subprocess.run(
            ["mvn", "jacoco:report"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )

        output = f"Maven Test Execution\n{'=' * 60}\n"
        output += f"Test Exit Code: {result.returncode}\n"
        output += f"JaCoCo Exit Code: {jacoco_result.returncode}\n\n"

        output += "TEST STDOUT:\n" + (
            result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout
        )

        if result.returncode != 0:
            output += "\n\nTEST STDERR:\n" + (
                result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr
            )

        output += "\n\nJACOCO REPORT:\n" + (
            jacoco_result.stdout[-1000:]
            if len(jacoco_result.stdout) > 1000
            else jacoco_result.stdout
        )

        return output
    except subprocess.TimeoutExpired:
        return "Error: Maven test execution timed out after 5 minutes"
    except Exception as e:
        return f"Error running Maven tests: {e}"


@mcp.tool()
def analyze_coverage() -> str:
    """
    Parse JaCoCo coverage report and provide detailed analysis.

    Returns:
        Detailed coverage statistics including line, branch, and method coverage
    """
    try:
        if not COVERAGE_REPORT_PATH.exists():
            return "Error: Coverage report not found. Run 'run_maven_tests' first."

        tree = ET.parse(COVERAGE_REPORT_PATH)
        root = tree.getroot()

        output = "JaCoCo Coverage Analysis\n" + "=" * 60 + "\n\n"

        # Overall coverage
        for counter in root.findall(".//counter"):
            counter_type = counter.get("type")
            missed = int(counter.get("missed", 0))
            covered = int(counter.get("covered", 0))
            total = missed + covered

            if total > 0:
                percentage = (covered / total) * 100
                output += (
                    f"{counter_type:12} | Covered: {covered:5} | Missed: {missed:5} | "
                )
                output += f"Total: {total:5} | Coverage: {percentage:6.2f}%\n"

        # Package-level analysis
        output += "\n" + "Package-Level Coverage\n" + "-" * 60 + "\n"

        for package in root.findall(".//package"):
            package_name = package.get("name", "").replace("/", ".")

            line_counter = package.find(".//counter[@type='LINE']")
            if line_counter is not None:
                missed = int(line_counter.get("missed", 0))
                covered = int(line_counter.get("covered", 0))
                total = missed + covered

                if total > 0:
                    percentage = (covered / total) * 100
                    output += f"\n{package_name}\n"
                    output += (
                        f"  Line Coverage: {percentage:6.2f}% ({covered}/{total})\n"
                    )

        return output
    except Exception as e:
        return f"Error analyzing coverage: {e}"


@mcp.tool()
def identify_uncovered_code() -> str:
    """
    Identify specific classes and methods with low or no coverage.

    Returns:
        List of uncovered code segments with recommendations
    """
    try:
        if not COVERAGE_REPORT_PATH.exists():
            return "Error: Coverage report not found. Run 'run_maven_tests' first."

        tree = ET.parse(COVERAGE_REPORT_PATH)
        root = tree.getroot()

        output = "Uncovered Code Analysis\n" + "=" * 60 + "\n\n"
        uncovered_items = []

        for package in root.findall(".//package"):
            package_name = package.get("name", "").replace("/", ".")

            for cls in package.findall(".//class"):
                class_name = cls.get("name", "").split("/")[-1]

                for method in cls.findall(".//method"):
                    method_name = method.get("name", "")

                    line_counter = method.find(".//counter[@type='LINE']")
                    if line_counter is not None:
                        missed = int(line_counter.get("missed", 0))
                        covered = int(line_counter.get("covered", 0))
                        total = missed + covered

                        if total > 0:
                            coverage = (covered / total) * 100
                            if coverage < 50:  # Focus on methods with < 50% coverage
                                uncovered_items.append(
                                    {
                                        "package": package_name,
                                        "class": class_name,
                                        "method": method_name,
                                        "coverage": coverage,
                                        "lines_missed": missed,
                                    }
                                )

        # Sort by coverage (lowest first)
        uncovered_items.sort(key=lambda x: x["coverage"])

        output += f"Found {len(uncovered_items)} methods with <50% coverage\n\n"
        output += "Top Priority Methods to Test:\n" + "-" * 60 + "\n"

        for i, item in enumerate(uncovered_items[:20], 1):  # Show top 20
            output += f"\n{i}. {item['package']}.{item['class']}.{item['method']}\n"
            output += f"   Coverage: {item['coverage']:.1f}% | Lines Missed: {item['lines_missed']}\n"

        if len(uncovered_items) > 20:
            output += f"\n... and {len(uncovered_items) - 20} more methods\n"

        return output
    except Exception as e:
        return f"Error identifying uncovered code: {e}"


# ============================================================================
# Git Automation Tools (Phase 3)
# ============================================================================


@mcp.tool()
def git_status(repo_path: Optional[str] = None) -> str:
    """
    Get current Git repository status.

    Args:
        repo_path: Path to Git repository (defaults to project root)

    Returns:
        Git status information including staged changes and conflicts
    """
    if repo_path is None:
        repo_path = str(Path(__file__).parent.parent)

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"Error getting git status: {result.stderr}"

        output = "Git Repository Status\n" + "=" * 60 + "\n\n"

        if not result.stdout.strip():
            output += "Working tree clean - no changes to commit\n"
        else:
            lines = result.stdout.strip().split("\n")
            staged = [l for l in lines if l[0] in ["A", "M", "D", "R"]]
            unstaged = [l for l in lines if l[1] in ["M", "D"]]
            untracked = [l for l in lines if l.startswith("??")]
            conflicts = [l for l in lines if l.startswith("UU")]

            if staged:
                output += f"Staged Changes ({len(staged)}):\n"
                for line in staged:
                    output += f"  {line}\n"
                output += "\n"

            if unstaged:
                output += f"Unstaged Changes ({len(unstaged)}):\n"
                for line in unstaged:
                    output += f"  {line}\n"
                output += "\n"

            if untracked:
                output += f"Untracked Files ({len(untracked)}):\n"
                for line in untracked:
                    output += f"  {line}\n"
                output += "\n"

            if conflicts:
                output += f"CONFLICTS ({len(conflicts)}):\n"
                for line in conflicts:
                    output += f"  {line}\n"
                output += "\n"

        return output
    except Exception as e:
        return f"Error executing git status: {e}"


@mcp.tool()
def git_add_all(repo_path: Optional[str] = None) -> str:
    """
    Stage all changes, excluding build artifacts and temporary files.

    Args:
        repo_path: Path to Git repository (defaults to project root)

    Returns:
        Confirmation of staged files
    """
    if repo_path is None:
        repo_path = str(Path(__file__).parent.parent)

    try:
        # Add all files
        result = subprocess.run(
            ["git", "add", "-A"], cwd=repo_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            return f"Error staging files: {result.stderr}"

        # Get status to confirm
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        staged_files = [
            l
            for l in status_result.stdout.strip().split("\n")
            if l and l[0] in ["A", "M", "D", "R"]
        ]

        output = "Git Add All\n" + "=" * 60 + "\n\n"
        output += f"Successfully staged {len(staged_files)} file(s)\n\n"

        if staged_files:
            output += "Staged files:\n"
            for line in staged_files[:30]:  # Limit display
                output += f"  {line}\n"

            if len(staged_files) > 30:
                output += f"  ... and {len(staged_files) - 30} more files\n"

        return output
    except Exception as e:
        return f"Error staging files: {e}"


@mcp.tool()
def git_commit(message: str, repo_path: Optional[str] = None) -> str:
    """
    Create a Git commit with the specified message.

    Args:
        message: Commit message
        repo_path: Path to Git repository (defaults to project root)

    Returns:
        Commit confirmation with hash
    """
    if repo_path is None:
        repo_path = str(Path(__file__).parent.parent)

    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"Error creating commit: {result.stderr}"

        output = "Git Commit\n" + "=" * 60 + "\n\n"
        output += result.stdout

        return output
    except Exception as e:
        return f"Error creating commit: {e}"


@mcp.tool()
def git_push(
    remote: str = "origin",
    branch: Optional[str] = None,
    repo_path: Optional[str] = None,
) -> str:
    """
    Push commits to remote repository.

    Args:
        remote: Remote name (default: origin)
        branch: Branch name (defaults to current branch)
        repo_path: Path to Git repository (defaults to project root)

    Returns:
        Push confirmation
    """
    if repo_path is None:
        repo_path = str(Path(__file__).parent.parent)

    try:
        # Get current branch if not specified
        if branch is None:
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
            )
            branch = branch_result.stdout.strip()

        # Push to remote
        result = subprocess.run(
            ["git", "push", remote, branch],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"Error pushing to remote: {result.stderr}"

        output = "Git Push\n" + "=" * 60 + "\n\n"
        output += f"Successfully pushed to {remote}/{branch}\n\n"
        output += result.stdout if result.stdout else result.stderr

        return output
    except Exception as e:
        return f"Error pushing to remote: {e}"


@mcp.tool()
def git_pull_request(
    title: str, body: str, base: str = "main", repo_path: Optional[str] = None
) -> str:
    """
    Create a pull request (requires GitHub CLI).

    Args:
        title: PR title
        body: PR description
        base: Base branch (default: main)
        repo_path: Path to Git repository (defaults to project root)

    Returns:
        Pull request URL
    """
    if repo_path is None:
        repo_path = str(Path(__file__).parent.parent)

    try:
        # Check if gh CLI is available
        check_result = subprocess.run(["which", "gh"], capture_output=True)

        if check_result.returncode != 0:
            return (
                "Error: GitHub CLI (gh) not found. Install from https://cli.github.com/"
            )

        # Create PR
        result = subprocess.run(
            ["gh", "pr", "create", "--base", base, "--title", title, "--body", body],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"Error creating pull request: {result.stderr}"

        output = "Pull Request Created\n" + "=" * 60 + "\n\n"
        output += result.stdout

        return output
    except Exception as e:
        return f"Error creating pull request: {e}"


# ============================================================================
# Test Generation Tool (Phase 2 & 4)
# ============================================================================


@mcp.tool()
def analyze_java_class(class_path: str) -> str:
    """
    Analyze a Java class file and extract method signatures for test generation.

    Args:
        class_path: Relative path to Java source file from benchmark-codebase/src/main/java

    Returns:
        Analysis of class structure including methods, fields, and recommendations
    """
    try:
        full_path = BENCHMARK_PATH / "src" / "main" / "java" / class_path

        if not full_path.exists():
            return f"Error: File not found at {full_path}"

        with open(full_path, "r") as f:
            content = f.read()

        output = f"Java Class Analysis: {class_path}\n" + "=" * 60 + "\n\n"

        # Simple pattern matching for methods (basic implementation)
        import re

        # Extract package
        package_match = re.search(r"package\s+([\w.]+);", content)
        if package_match:
            output += f"Package: {package_match.group(1)}\n\n"

        # Extract class name
        class_match = re.search(r"public\s+(?:final\s+)?class\s+(\w+)", content)
        if class_match:
            output += f"Class: {class_match.group(1)}\n\n"

        # Extract public methods
        method_pattern = r"public\s+(?:static\s+)?(?:<[^>]+>\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)"
        methods = re.findall(method_pattern, content)

        if methods:
            output += "Public Methods:\n" + "-" * 60 + "\n"
            for return_type, method_name, params in methods:
                output += f"\n  {return_type} {method_name}({params})\n"

        output += "\n\nTest Generation Recommendations:\n" + "-" * 60 + "\n"
        output += f"- Found {len(methods)} public methods to test\n"
        output += "- Consider edge cases: null inputs, empty strings, boundary values\n"
        output += "- Test exception handling where applicable\n"
        output += "- Verify return values and state changes\n"

        return output
    except Exception as e:
        return f"Error analyzing Java class: {e}"


@mcp.tool()
def generate_test_template(class_path: str, method_name: str) -> str:
    """
    Generate a JUnit test template for a specific method.

    Args:
        class_path: Relative path to Java source file
        method_name: Name of the method to test

    Returns:
        JUnit test template code
    """
    try:
        # Extract class name from path
        class_name = class_path.split("/")[-1].replace(".java", "")
        test_class_name = f"{class_name}Test"

        # Extract package from path
        package_parts = class_path.split("/")[:-1]
        if package_parts:
            package = ".".join(package_parts)
        else:
            package = "org.apache.commons.lang3"

        template = f"""package {package};

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Test class for {class_name}.{method_name}
 * Generated by MCP Testing Agent
 */
public class {test_class_name} {{

    @Test
    public void test{method_name.capitalize()}Normal() {{
        // TODO: Test normal case
        fail("Test not implemented");
    }}

    @Test
    public void test{method_name.capitalize()}EdgeCase() {{
        // TODO: Test edge cases (null, empty, boundary values)
        fail("Test not implemented");
    }}

    @Test(expected = Exception.class)
    public void test{method_name.capitalize()}Exception() {{
        // TODO: Test exception handling
        fail("Test not implemented");
    }}
}}
"""

        output = f"JUnit Test Template\n" + "=" * 60 + "\n\n"
        output += f"Generated test template for {class_name}.{method_name}\n\n"
        output += "Template Code:\n" + "-" * 60 + "\n"
        output += template

        return output
    except Exception as e:
        return f"Error generating test template: {e}"


# ============================================================================
# Creative Extension: Specification-Based Testing (Phase 5)
# ============================================================================


@mcp.tool()
def generate_boundary_value_tests(
    class_path: str, method_name: str, param_ranges: str
) -> str:
    """
    Generate boundary value analysis test cases for a method.

    Args:
        class_path: Relative path to Java source file
        method_name: Name of the method to test
        param_ranges: JSON string defining parameter ranges, e.g.,
                     '{"param1": {"min": 0, "max": 100, "type": "int"}}'

    Returns:
        Boundary value test cases
    """
    try:
        import json

        ranges = json.loads(param_ranges)
        class_name = class_path.split("/")[-1].replace(".java", "")

        output = f"Boundary Value Test Cases\n" + "=" * 60 + "\n\n"
        output += f"Method: {class_name}.{method_name}\n"
        output += f"Parameters: {list(ranges.keys())}\n\n"

        test_cases = []

        for param_name, config in ranges.items():
            param_type = config.get("type", "int")

            if param_type in ["int", "long", "double", "float"]:
                min_val = config.get("min", 0)
                max_val = config.get("max", 100)

                # Boundary values: min-1, min, min+1, nominal, max-1, max, max+1
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_BelowMin",
                        "values": {param_name: min_val - 1},
                        "expected": "Exception or rejection",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_AtMin",
                        "values": {param_name: min_val},
                        "expected": "Valid",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_JustAboveMin",
                        "values": {param_name: min_val + 1},
                        "expected": "Valid",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_Nominal",
                        "values": {param_name: (min_val + max_val) // 2},
                        "expected": "Valid",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_JustBelowMax",
                        "values": {param_name: max_val - 1},
                        "expected": "Valid",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_AtMax",
                        "values": {param_name: max_val},
                        "expected": "Valid",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_AboveMax",
                        "values": {param_name: max_val + 1},
                        "expected": "Exception or rejection",
                    }
                )

            elif param_type == "String":
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_Null",
                        "values": {param_name: "null"},
                        "expected": "Exception or special handling",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_Empty",
                        "values": {param_name: '""'},
                        "expected": "Valid or special handling",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_SingleChar",
                        "values": {param_name: '"a"'},
                        "expected": "Valid",
                    }
                )

            elif param_type == "array":
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_Null",
                        "values": {param_name: "null"},
                        "expected": "Exception or special handling",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_Empty",
                        "values": {param_name: "new int[]{}"},
                        "expected": "Valid or special handling",
                    }
                )
                test_cases.append(
                    {
                        "name": f"test{method_name.capitalize()}_{param_name}_Single",
                        "values": {param_name: "new int[]{1}"},
                        "expected": "Valid",
                    }
                )

        output += "Generated Test Cases:\n" + "-" * 60 + "\n"
        for i, tc in enumerate(test_cases, 1):
            output += f"\n{i}. {tc['name']}\n"
            output += f"   Input: {tc['values']}\n"
            output += f"   Expected: {tc['expected']}\n"

        return output
    except Exception as e:
        return f"Error generating boundary value tests: {e}"


@mcp.tool()
def generate_equivalence_class_tests(
    class_path: str, method_name: str, equivalence_classes: str
) -> str:
    """
    Generate equivalence class partitioning test cases.

    Args:
        class_path: Relative path to Java source file
        method_name: Name of the method to test
        equivalence_classes: JSON string defining classes, e.g.,
                            '{"valid": ["positive", "zero"], "invalid": ["negative"]}'

    Returns:
        Equivalence class test cases
    """
    try:
        import json

        classes = json.loads(equivalence_classes)
        class_name = class_path.split("/")[-1].replace(".java", "")

        output = f"Equivalence Class Partitioning\n" + "=" * 60 + "\n\n"
        output += f"Method: {class_name}.{method_name}\n\n"

        output += "Test Cases:\n" + "-" * 60 + "\n"

        for class_type, partitions in classes.items():
            output += f"\n{class_type.upper()} Classes:\n"
            for partition in partitions:
                output += f"  - Test {partition} input\n"

        output += "\n\nRecommendation: Generate at least one test case from each equivalence class\n"
        output += "to ensure comprehensive coverage with minimal redundancy.\n"

        return output
    except Exception as e:
        return f"Error generating equivalence class tests: {e}"


# ============================================================================
# Creative Extension: Static Analysis Integration (Phase 5)
# ============================================================================


@mcp.tool()
def run_static_analysis(project_path: Optional[str] = None) -> str:
    """
    Run static analysis tools (Checkstyle, PMD) on the project.

    Args:
        project_path: Path to Maven project (defaults to benchmark-codebase)

    Returns:
        Static analysis results and recommendations
    """
    if project_path is None:
        project_path = str(BENCHMARK_PATH)

    try:
        output = "Static Analysis Report\n" + "=" * 60 + "\n\n"

        # Run Checkstyle
        output += "Running Checkstyle...\n"
        checkstyle_result = subprocess.run(
            ["mvn", "checkstyle:check"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if "BUILD SUCCESS" in checkstyle_result.stdout:
            output += "✓ Checkstyle: No violations found\n\n"
        else:
            output += "✗ Checkstyle: Violations detected\n"
            # Extract violation count if available
            if "violations" in checkstyle_result.stdout.lower():
                for line in checkstyle_result.stdout.split("\n"):
                    if "violation" in line.lower():
                        output += f"  {line.strip()}\n"
            output += "\n"

        # Run PMD
        output += "Running PMD...\n"
        pmd_result = subprocess.run(
            ["mvn", "pmd:check"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if "BUILD SUCCESS" in pmd_result.stdout:
            output += "✓ PMD: No violations found\n\n"
        else:
            output += "✗ PMD: Violations detected\n\n"

        output += "Recommendations:\n" + "-" * 60 + "\n"
        output += "- Address any code style violations to improve maintainability\n"
        output += "- Fix potential bugs identified by static analysis\n"
        output += (
            "- Consider refactoring complex methods (high cyclomatic complexity)\n"
        )
        output += "- Add tests for code with high error potential\n"

        return output
    except subprocess.TimeoutExpired:
        return "Error: Static analysis timed out"
    except Exception as e:
        return f"Error running static analysis: {e}"


@mcp.tool()
def detect_code_smells(class_path: str) -> str:
    """
    Detect common code smells in a Java class using simple heuristics.

    Args:
        class_path: Relative path to Java source file from benchmark-codebase/src/main/java

    Returns:
        List of detected code smells and refactoring suggestions
    """
    try:
        full_path = BENCHMARK_PATH / "src" / "main" / "java" / class_path

        if not full_path.exists():
            return f"Error: File not found at {full_path}"

        with open(full_path, "r") as f:
            content = f.read()
            lines = content.split("\n")

        output = f"Code Smell Detection: {class_path}\n" + "=" * 60 + "\n\n"

        smells = []

        # Long Method (>50 lines)
        import re

        method_pattern = r"(public|private|protected)\s+(?:static\s+)?[\w<>]+\s+(\w+)\s*\([^)]*\)\s*\{"

        current_method = None
        method_start = 0
        brace_count = 0

        for i, line in enumerate(lines):
            method_match = re.search(method_pattern, line)
            if method_match and brace_count == 0:
                if current_method:
                    method_length = i - method_start
                    if method_length > 50:
                        smells.append(
                            {
                                "type": "Long Method",
                                "location": f"Line {method_start}",
                                "method": current_method,
                                "severity": "Medium",
                                "suggestion": "Consider breaking down into smaller methods",
                            }
                        )
                current_method = method_match.group(2)
                method_start = i

            brace_count += line.count("{") - line.count("}")

        # Large Class (>500 lines)
        if len(lines) > 500:
            smells.append(
                {
                    "type": "Large Class",
                    "location": "Entire file",
                    "method": "N/A",
                    "severity": "High",
                    "suggestion": "Consider splitting into multiple classes",
                }
            )

        # Magic Numbers
        magic_number_pattern = r"\b\d{2,}\b"
        for i, line in enumerate(lines):
            if "final" not in line and "static" not in line:
                matches = re.findall(magic_number_pattern, line)
                if matches:
                    smells.append(
                        {
                            "type": "Magic Number",
                            "location": f"Line {i + 1}",
                            "method": "Various",
                            "severity": "Low",
                            "suggestion": "Extract to named constant",
                        }
                    )
                    break  # Only report once per file

        # Duplicate Code (simple check for repeated lines)
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if len(stripped) > 20 and not stripped.startswith("//"):
                line_counts[stripped] = line_counts.get(stripped, 0) + 1

        duplicates = {k: v for k, v in line_counts.items() if v > 2}
        if duplicates:
            smells.append(
                {
                    "type": "Duplicate Code",
                    "location": "Multiple locations",
                    "method": "N/A",
                    "severity": "Medium",
                    "suggestion": "Extract common code to helper method",
                }
            )

        if smells:
            output += f"Found {len(smells)} potential code smell(s):\n\n"
            for i, smell in enumerate(smells, 1):
                output += f"{i}. {smell['type']} ({smell['severity']})\n"
                output += f"   Location: {smell['location']}\n"
                output += f"   Suggestion: {smell['suggestion']}\n\n"
        else:
            output += "No obvious code smells detected. Code appears clean!\n"

        return output
    except Exception as e:
        return f"Error detecting code smells: {e}"


# ============================================================================
# Run MCP Server
# ============================================================================

if __name__ == "__main__":
    mcp.run(transport="sse")
