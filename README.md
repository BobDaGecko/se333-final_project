# SE333 - Final Project: Intelligent Testing Agent via Model Context Protocol

---

### Project Metadata

**Author:** Kellen Siczka  
**GitHub:** [bobdagecko](https://github.com/bobdagecko)

**Course:** SE333 - Software Testing  
**Professor:** Dong Jae Kim  
**Institution:** DePaul University  
**Term:** Fall Quarter 2025  
**Date:** November 16, 2025

### License

This project is submitted as academic coursework for SE333 - Software Testing at DePaul University. All code is provided for educational purposes.

(c) Kellen Siczka 2025. All rights reserved.

---

## AI Assistance Disclosure

This project, centered on building and utilizing intelligent agents via the Model Context Protocol (MCP) for software development automation, inherently involves the strategic use of AI tools.

Please refer to my [Universal Statement on AI Integration and Ethical Practice](AI_DISCLOSURE.md) for my overarching philosophy and ethical stance on AI.

### Approach to AI Usage in This Project

My general approach to AI integration, as outlined in my Universal Statement, is consistently applied here. In software engineering, AI serves as an augmentative force—accelerating routine tasks, providing insights, and generating scaffolding—while the core design, strategy, and nuanced decision-making remain firmly human-driven.

I recognize that generative AI tools, despite their utility, are inherently flawed with limitations such as hallucinations, lack of context retention, and superficial understanding of complex domains that require not just human insight but deep expertise to navigate effectively. Therefore, I maintain strict ownership of all generated code and architectural decisions. My methodology involves rigorous validation of AI-generated content through cross-referencing with authoritative sources and ensuring alignment with established best practices in software engineering. This balanced approach harnesses AI for boilerplate generation, debugging assistance, and conceptual exploration, while upholding the primacy of human judgment, deep domain expertise, and critical thinking in the development process.

### AI Tools Utilized in This Project

The following AI tools were employed in this project, primarily to augment human effort and accelerate specific tasks:

- **Intelligent Agent Implementation:** Developing and configuring the MCP agent for automated test generation, execution, and iteration based on defined prompts.
- **Prompt Engineering:** Designing, refining, and validating natural language prompts that guide the agent's behavior and logic in generating tests and analyzing code.
- **Code Generation & Refinement:** Assisting in scaffolding, boilerplate generation, and refactoring to improve code quality and organization for MCP tools and project utilities.
- **Documentation & Clarity:** Enhancing the structure, clarity, and readability of technical documentation, including the `README.md` and reflection report.
- **Debugging Assistance:** Providing suggestions for identifying and resolving issues within the agent's logic or the tested codebase.
- **Coverage Analysis & Recommendations:** Interpreting JaCoCo/PIT reports and generating insights or recommendations for improving code coverage patterns.
- **Technology Reference & Learning:** Using generative AI as a reference guide to understand and implement various technologies, frameworks, and best practices throughout the project development process.

### Original Work and Human Contributions

All critical aspects of this project, including fundamental design choices, strategic analysis, and the synthesis of solutions, represent my own understanding and reasoning. Key human contributions include:

- **Core System Design:** Architecting the overall structure of the MCP tools and the intelligent agent, including design decisions and trade-offs.
- **Framework Implementation:** Writing the foundational code for MCP integration, test execution pipelines, and parsing coverage reports.
- **Strategic Prompt Design:** The critical thinking behind _how_ to prompt the AI agent effectively to achieve specific testing goals and coverage improvements.
- **Performance Evaluation & Reflection:** Analyzing quantitative and qualitative metrics, identifying unexpected findings, discussing challenges, and formulating future enhancements.
- **Comparative Analysis:** The critical assessment and interpretation of the agent's performance, contrasting AI-generated outcomes with established software engineering principles.

All fundamental design choices, critical analysis of agent behavior, and the strategic implementation of the intelligent testing solution represent my own understanding and reasoning.

### Documentation and Reference Materials Consulted

Beyond any AI-assisted references, the following resources were extensively consulted to inform and validate the work in this project.

#### Personal Resources

- **SE333 Course Materials:** Lecture notes, assignments, and discussions provided foundational knowledge on software testing principles and practices.
- **Previous Coursework:** Insights and techniques from prior classes in software engineering, programming languages, and AI/ML applications informed various aspects of the project.
- **Personal Documentation:** Typically stored as private gists, this includes notes, and snippets accumulated over years of programming experience.
- **Personal Projects:** Some personal projects and experiments related to software testing and AI-assisted development provided practical insights and inspiration.

#### Official Documentation and Specific Resources

- **Model Context Protocol:** [MCP Specification](https://spec.modelcontextprotocol.io/), [MCP Documentation](https://modelcontextprotocol.io/docs)
- **FastMCP Framework:** [FastMCP GitHub](https://github.com/jlowin/fastmcp), [FastMCP Documentation](https://gofastmcp.com)
- **Python:** [Python 3.10+ Documentation](https://docs.python.org/3/), [Python Standard Library](https://docs.python.org/3/library/)
- **Java:** [Java SE Documentation](https://docs.oracle.com/en/java/javase/), [Java Language Specification](https://docs.oracle.com/javase/specs/)
- **Maven:** [Apache Maven Documentation](https://maven.apache.org/guides/), [Maven POM Reference](https://maven.apache.org/pom.html)
- **JaCoCo:** [JaCoCo Documentation](https://www.jacoco.org/jacoco/trunk/doc/), [JaCoCo Maven Plugin](https://www.jacoco.org/jacoco/trunk/doc/maven.html)
- **JUnit:** [JUnit 4 Documentation](https://junit.org/junit4/), [JUnit Assertions Guide](https://junit.org/junit4/javadoc/latest/)
- **Apache Commons Lang3:** [Commons Lang Documentation](https://commons.apache.org/proper/commons-lang/), [Commons Lang API](https://commons.apache.org/proper/commons-lang/apidocs/)
- **Git:** [Git Documentation](https://git-scm.com/doc), [GitHub CLI Documentation](https://cli.github.com/manual/)
- **VS Code:** [VS Code Documentation](https://code.visualstudio.com/docs), [VS Code Extension API](https://code.visualstudio.com/api)

#### General Programming and Community Resources

- **Stack Overflow:** [stackoverflow.com](https://stackoverflow.com/) - Programming Q\&A and troubleshooting.
- **Reddit:** [r/programming](https://www.reddit.com/r/programming/), [r/Python](https://www.reddit.com/r/Python/), [r/java](https://www.reddit.com/r/java/) - Community discussions and best practices.
- **W3Schools:** [w3schools.com](https://www.w3schools.com/) - Web development and programming tutorials.
- **GeeksforGeeks:** [geeksforgeeks.org](https://www.geeksforgeeks.org/) - Computer science algorithms and data structures.
- **Baeldung:** [baeldung.com](https://www.baeldung.com/) - Java and Spring framework tutorials.
- **Real Python:** [realpython.com](https://realpython.com/) - Python tutorials and best practices.
- **DigitalOcean Tutorials:** [digitalocean.com/community/tutorials](https://www.digitalocean.com/community/tutorials) - DevOps and software development guides.
- **Wikipedia:** [wikipedia.org](https://www.wikipedia.org/) - General knowledge and technical concepts.
- **Medium Engineering Blogs:** Various technical articles on software testing, AI/ML integration, and development workflows.
- **GitHub Discussions:** Community support for open-source projects and frameworks.

---

## Project Overview

This project implements an intelligent software testing agent using the Model Context Protocol (MCP). The agent automates the generation, execution, and iterative improvement of JUnit test cases to maximize code coverage for Java Maven projects. By leveraging AI-assisted development through MCP, the system provides a powerful framework for automated testing workflows.

The testing agent analyzes the Apache Commons Lang3 library as a benchmark codebase, systematically identifying uncovered code segments, generating comprehensive test cases, and tracking coverage improvements through an iterative feedback loop.

### Key Capabilities

- **Automated Test Generation**: Analyzes Java source code and generates JUnit test templates
- **Coverage Analysis**: Parses JaCoCo reports to identify coverage gaps and prioritize testing targets
- **Git Automation**: Streamlines version control with automated staging, committing, and push operations
- **Specification-Based Testing**: Implements boundary value analysis and equivalence class partitioning
- **Static Analysis Integration**: Detects code smells and style violations to improve code quality
- **Iterative Improvement**: Continuously refines tests based on coverage feedback

---

## Architecture

The system consists of three primary components:

1. **MCP Server** (`mcp-server/server.py`): FastMCP-based server exposing testing tools
2. **Benchmark Codebase** (`supplementals/benchmark-codebase/`): Apache Commons Lang3 configured with JaCoCo
3. **Agent Prompt** (`.github/prompts/tester.prompt.md`): Defines intelligent agent behavior and workflow

---

## Installation & Setup

### Prerequisites

Before starting, ensure you have the following installed:

- **VS Code** (latest version)
- **Python 3.10+**
- **Node.js 18+** (LTS recommended)
- **Java 11+** and **Maven 3.6+**
- **Git** with active GitHub account
- **uv** package manager

### Step 1: Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd Final_Project-SE333-Kellen_Siczka-11_16_25

# Navigate to MCP server directory
cd mcp-server

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .
```

### Step 2: Configure VS Code

1. **Start the MCP Server**:

   ```bash
   .venv/bin/python server.py
   ```

   The server will display a URL (typically `http://127.0.0.1:8000`).

2. **Connect MCP Server to VS Code**:

   - Press `CTRL+SHIFT+P` (or `CMD+SHIFT+P` on Mac)
   - Search for `MCP: Add Server`
   - Paste the server URL
   - Give it a name (e.g., "Testing Agent")
   - Press Enter

3. **Enable Auto-Approve (YOLO Mode)**:

   - Press `CTRL+SHIFT+P`
   - Search for `Chat: Settings`
   - Enable `Auto-Approve` for tools
   - Ensure all tools are highlighted for use in the Chat view

4. **Configure Maven Auto-Approval** (if needed):
   - Press `CTRL+ALT+P`
   - Open `Auto-Approve Settings`
   - Add entry: `mvn test`

### Step 3: Verify Installation

Test the calculator tool to confirm the MCP server is working:

1. Open VS Code Chat view
2. Type: `what is 1+2`
3. The agent should use the calculator tool and return `3`

---

## MCP Tool Documentation

### Maven & Test Execution Tools

#### `run_maven_tests(project_path: Optional[str] = None) -> str`

Executes Maven tests on the specified project and generates JaCoCo coverage report.

**Parameters:**

- `project_path` (optional): Path to Maven project. Defaults to `benchmark-codebase`.

**Returns:** Maven test execution output including test results and coverage generation status.

**Example:**

```
run_maven_tests()
```

#### `analyze_coverage() -> str`

Parses JaCoCo XML coverage report and provides detailed statistics.

**Returns:** Coverage breakdown by line, branch, method, class, and package levels.

**Example Output:**

```
JaCoCo Coverage Analysis
============================================================

LINE         | Covered:  3421 | Missed:  1205 | Total:  4626 | Coverage:  73.96%
BRANCH       | Covered:  1823 | Missed:   892 | Total:  2715 | Coverage:  67.15%
METHOD       | Covered:   842 | Missed:   198 | Total:  1040 | Coverage:  80.96%
```

#### `identify_uncovered_code() -> str`

Identifies specific classes and methods with low or no coverage (<50%).

**Returns:** Prioritized list of uncovered code segments with line counts and coverage percentages.

**Example:**

```
identify_uncovered_code()
```

---

### Code Analysis Tools

#### `analyze_java_class(class_path: str) -> str`

Analyzes a Java class file and extracts method signatures for test generation.

**Parameters:**

- `class_path`: Relative path to Java source file from `benchmark-codebase/src/main/java`

**Returns:** Class structure analysis including package, class name, public methods, and testing recommendations.

**Example:**

```
analyze_java_class("org/apache/commons/lang3/StringUtils.java")
```

#### `generate_test_template(class_path: str, method_name: str) -> str`

Generates a JUnit test template for a specific method.

**Parameters:**

- `class_path`: Relative path to Java source file
- `method_name`: Name of the method to test

**Returns:** Complete JUnit test class template with normal, edge case, and exception test stubs.

**Example:**

```
generate_test_template("org/apache/commons/lang3/StringUtils.java", "isEmpty")
```

---

### Git Automation Tools

#### `git_status(repo_path: Optional[str] = None) -> str`

Gets current Git repository status including staged changes, unstaged changes, untracked files, and conflicts.

**Parameters:**

- `repo_path` (optional): Path to Git repository. Defaults to project root.

**Returns:** Formatted Git status report.

#### `git_add_all(repo_path: Optional[str] = None) -> str`

Stages all changes, intelligently excluding build artifacts and temporary files.

**Returns:** Confirmation of staged files with count and file list.

#### `git_commit(message: str, repo_path: Optional[str] = None) -> str`

Creates a Git commit with the specified message.

**Parameters:**

- `message`: Commit message (should include coverage stats when applicable)

**Returns:** Commit confirmation with hash.

**Example:**

```
git_commit("feat: improve StringUtils coverage - 65% → 82%")
```

#### `git_push(remote: str = "origin", branch: Optional[str] = None, repo_path: Optional[str] = None) -> str`

Pushes commits to remote repository.

**Parameters:**

- `remote`: Remote name (default: "origin")
- `branch`: Branch name (defaults to current branch)

**Returns:** Push confirmation with remote and branch information.

#### `git_pull_request(title: str, body: str, base: str = "main", repo_path: Optional[str] = None) -> str`

Creates a pull request using GitHub CLI.

**Parameters:**

- `title`: PR title
- `body`: PR description
- `base`: Base branch (default: "main")

**Returns:** Pull request URL.

**Note:** Requires GitHub CLI (`gh`) to be installed and authenticated.

---

### Specification-Based Testing Tools (Creative Extension)

#### `generate_boundary_value_tests(class_path: str, method_name: str, param_ranges: str) -> str`

Generates boundary value analysis test cases for a method.

**Parameters:**

- `class_path`: Relative path to Java source file
- `method_name`: Name of the method to test
- `param_ranges`: JSON string defining parameter ranges

**Example:**

```python
param_ranges = '{
  "index": {"min": 0, "max": 100, "type": "int"},
  "name": {"type": "String"}
}'
generate_boundary_value_tests("ArrayUtils.java", "get", param_ranges)
```

**Returns:** Comprehensive boundary value test cases including:

- Below minimum (min-1)
- At minimum (min)
- Just above minimum (min+1)
- Nominal value
- Just below maximum (max-1)
- At maximum (max)
- Above maximum (max+1)

#### `generate_equivalence_class_tests(class_path: str, method_name: str, equivalence_classes: str) -> str`

Generates equivalence class partitioning test cases.

**Parameters:**

- `class_path`: Relative path to Java source file
- `method_name`: Name of the method to test
- `equivalence_classes`: JSON string defining valid and invalid classes

**Example:**

```python
classes = '{
  "valid": ["positive", "zero"],
  "invalid": ["negative", "null"]
}'
generate_equivalence_class_tests("MathUtils.java", "abs", classes)
```

---

### Static Analysis Tools (Creative Extension)

#### `run_static_analysis(project_path: Optional[str] = None) -> str`

Runs static analysis tools (Checkstyle, PMD) on the project.

**Returns:** Static analysis results with recommendations for code quality improvements.

#### `detect_code_smells(class_path: str) -> str`

Detects common code smells using heuristics.

**Parameters:**

- `class_path`: Relative path to Java source file

**Returns:** List of detected code smells including:

- Long methods (>50 lines)
- Large classes (>500 lines)
- Magic numbers
- Duplicate code

**Example:**

```
detect_code_smells("org/apache/commons/lang3/ArrayUtils.java")
```

---

### Utility Tools

#### `calculator(expression: str) -> str`

Evaluates mathematical expressions.

**Parameters:**

- `expression`: Math expression string (supports +, -, \*, /, sqrt, sin, cos, tan, log, exp)

**Returns:** Result as string.

**Example:**

```
calculator("sqrt(16) + 2")  # Returns "6.0"
```

---

## Usage Guide

### Basic Workflow

1. **Start the MCP Server**:

   ```bash
   cd mcp-server
   source .venv/bin/activate
   python server.py
   ```

2. **Open VS Code Chat** and interact with the agent using the `.github/prompts/tester.prompt.md` prompt

3. **Run Initial Coverage Analysis**:

   - Agent will execute: `run_maven_tests()`, `analyze_coverage()`, `identify_uncovered_code()`

4. **Generate Tests**:

   - Agent analyzes low-coverage classes
   - Generates test templates
   - Creates test files in `src/test/java`

5. **Verify and Iterate**:

   - Re-run tests to measure coverage improvement
   - Identify remaining gaps
   - Generate additional tests

6. **Commit Progress**:
   - Agent uses Git tools to commit improvements
   - Commit messages include coverage metrics

### Example Agent Interaction

```
User: "Analyze the coverage of the benchmark codebase and generate tests for the lowest coverage methods"

Agent:
1. Running initial tests... [calls run_maven_tests()]
2. Analyzing coverage... [calls analyze_coverage()]
3. Identified 47 methods with <50% coverage
4. Analyzing ArrayUtils class... [calls analyze_java_class()]
5. Generating tests for indexOf method... [creates test file]
6. Running tests to verify... [calls run_maven_tests()]
7. Coverage improved: ArrayUtils 65% → 78%
8. Committing changes... [calls git_commit()]
```

---

## Project Structure

```
Final_Project-SE333-Kellen_Siczka-11_16_25/
├── .github/
│   └── prompts/
│       └── tester.prompt.md          # Agent behavior definition
├── mcp-server/
│   ├── server.py                     # Main MCP server implementation
│   ├── pyproject.toml                # Python dependencies
│   └── README.md                     # Server-specific documentation
├── supplementals/
│   ├── benchmark-codebase/           # Apache Commons Lang3
│   │   ├── pom.xml                   # Maven config with JaCoCo
│   │   └── src/
│   │       ├── main/java/            # Source code
│   │       └── test/java/            # Test code (generated/existing)
│   ├── agent-demo/                   # Example agent implementation
│   └── training-text.md              # Writing style reference
├── report/
│   └── reflection.pdf                # LaTeX reflection report
├── README.md                         # This file
└── Final_Project_Instructions.md     # Assignment requirements
```

---

## Troubleshooting

### Common Issues

**Issue**: MCP server won't start

- **Solution**: Ensure all dependencies installed: `uv pip install -e .`
- Check Python version: `python --version` (must be 3.10+)

**Issue**: Maven tests fail

- **Solution**: Verify Java and Maven installed: `mvn --version`
- Check `JAVA_HOME` environment variable is set

**Issue**: Coverage report not found

- **Solution**: Run `run_maven_tests()` first to generate JaCoCo report
- Verify JaCoCo plugin in `pom.xml`

**Issue**: Git tools return errors

- **Solution**: Ensure working directory is a Git repository
- Check Git configuration: `git config --list`

**Issue**: `git_pull_request` fails

- **Solution**: Install GitHub CLI: `brew install gh` (Mac) or download from https://cli.github.com/
- Authenticate: `gh auth login`

### Debug Tips

1. **Check server logs**: MCP server outputs detailed logs in the terminal
2. **Verify tool availability**: Use VS Code Chat to list available MCP tools
3. **Test tools individually**: Try each tool separately before running complex workflows
4. **Check file paths**: All paths are relative to the benchmark-codebase directory
5. **Maven timeout**: If tests take >5 minutes, the tool will timeout

---

## Technical Insights

### Why MCP?

The Model Context Protocol provides a standardized way to expose tools and context to AI agents. Unlike traditional APIs, MCP enables:

- **Semantic tool discovery**: AI agents understand tool purposes from descriptions
- **Stateless interaction**: Each tool call is independent and composable
- **Easy extensibility**: Adding new tools requires minimal boilerplate
- **VS Code integration**: Native support in modern development environments

### Coverage Analysis Strategy

The agent prioritizes testing targets using a multi-factor approach:

1. **Zero-coverage methods first**: Maximum impact per test
2. **Public API methods**: User-facing functionality most critical
3. **Complex methods**: Higher bug potential
4. **Recently modified code**: Regression risk

### Test Generation Philosophy

Generated tests follow a three-tier strategy:

1. **Normal case**: Validates expected behavior with typical inputs
2. **Edge cases**: Tests boundaries, null, empty, and extreme values
3. **Exception handling**: Verifies graceful failure and error messages

This ensures comprehensive coverage without redundant tests.

---

## Future Enhancements

- **Mutation Testing Integration**: Use PIT to measure test quality beyond coverage
- **AI-Powered Test Assertions**: Generate meaningful assertions based on method semantics
- **Regression Test Selection**: Intelligently run only tests affected by code changes
- **Multi-Project Support**: Extend beyond single Maven projects
- **Coverage Visualization**: Generate interactive HTML reports with improvement tracking
- **Continuous Integration**: Integrate with CI/CD pipelines for automated testing

---

### Project Metadata

**Author:** Kellen Siczka  
**GitHub:** [bobdagecko](https://github.com/bobdagecko)

**Course:** SE333 - Software Testing  
**Professor:** Dong Jae Kim  
**Institution:** DePaul University  
**Term:** Fall Quarter 2025  
**Date:** November 16, 2025

### License

This project is submitted as academic coursework for SE333 - Software Testing at DePaul University. All code is provided for educational purposes.

(c) Kellen Siczka 2025. All rights reserved.
