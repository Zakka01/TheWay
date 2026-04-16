
# A-Maze-ing

## Description

**A-Maze-ing** is a Python-based maze generator and solver project.
Its goal is to generate valid mazes from configuration files, encode them efficiently, and compute a valid path from entry to exit.

The project supports:
- Maze generation from configuration input
- Hex-encoded maze representation
- Pathfinding from start to finish
- Visual representation of the maze
- Debugging and validation tools

This project focuses on algorithmic thinking, file parsing, data structures, and pathfinding techniques.

---

## Instructions

### Installation

```bash
make install
```

---

### Run the program

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

---

### Debug mode

```bash
make debug
```

Uses Python's built-in debugger (`pdb`).

---

### Clean project

```bash
make clean
```

Removes:
- `__pycache__`
- `.mypy_cache`
- `.pyc` files

---

### Lint check

```bash
make lint
```

---

## Resources

### References

- [Maze Generation Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Hunt and Kill Algorithm — Jamis Buck's blog](http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm)
- [Python `pdb` documentation](https://docs.python.org/3/library/pdb.html)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)

### AI Usage

AI (Claude by Anthropic) was used as a **learning and debugging assistant** during this project. Specifically:

- **Debugging**: Identifying type errors flagged by `mypy` and `flake8`, and understanding their root causes
- **Makefile**: Improving the structure and target definitions of the Makefile
- **Algorithm explanations**: Clarifying how Hunt & Kill and DFS work step by step
- **Lint fixes**: Resolving line-length violations (E501) and annotation issues

AI was not used to generate the core logic, algorithms, or project structure. All implementation decisions were made by the team.

---

## Maze Configuration File Format

The configuration file uses a simple key=value format:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE = maze.txt
PERFECT=True
```

Fields:
- `WIDTH` → maze width (integer)
- `HEIGHT` → maze height (integer)
- `ENTRY` → starting coordinate as `x,y`
- `EXIT` → ending coordinate as `x,y`
- `OUTPUT_FILE` → the output file name `maze.txt`
- `PERFECT` → `True or False`


All four fields are required. Coordinates are zero-indexed and must lie within the bounds defined by `WIDTH` and `HEIGHT`.

---

## Maze Generation Algorithms

This project implements **two different generation algorithms**, one per team member.

### Agent 1 → Hunt and Kill Algorithm

The Hunt and Kill algorithm works by:
1. Starting from a random cell
2. Walking randomly to unvisited neighbors
3. When stuck, "hunting" for a new unvisited cell adjacent to a visited one
4. Repeating until all cells are visited

### Agent 2 → Depth-First Search (DFS)

The DFS algorithm works by:
1. Starting from the entry cell
2. Exploring as deep as possible into unvisited neighbors
3. Backtracking when reaching dead ends
4. Continuing until the maze is fully generated

---

## Why These Algorithms

- **DFS**: Simple to implement, reliable, and always produces a perfect maze (exactly one path between any two cells).
- **Hunt & Kill**: Introduces more randomness and less predictable corridor structure, resulting in visually distinct mazes.
- Having both algorithms allows the project to generate varied mazes without repeating the same structural patterns.

---

## Reusable Components

The following modules are designed to be reused independently of the rest of the project:

| Component | Location | How to reuse |
|---|---|---|
| Grid system | `maze/maze_generator.py` | Import the `Grid` class to create and manipulate any 2D grid structure |

---

## Team & Project Management

### Team Members

| Member | Role |
|---|---|
| Agent 1 | Implemented the Hunt and Kill generation algorithm, Makefile automation, and debugging setup |
| Agent 2 | Implemented the DFS generation algorithm, config file parser, and visualization system |

### Planning Evolution

- **Week 1**: Defined project structure and config file format; both members set up their environments
- **Week 2**: brel-bou implemented Hunt & Kill; zahrabar implemented DFS and the config parser
- **Week 3**: Integrated both algorithms under a shared interface; added pathfinding and visualization
- **Week 4**: Testing, lint fixes, debugging with `pdb`, and final cleanup

The initial plan underestimated the time needed to unify two separate algorithm implementations under a common interface, which required an extra integration phase.

### What Worked Well

- Clean modular design made integration between the two algorithms straightforward
- Separating responsibilities per team member avoided conflicts
- `pdb` made debugging complex recursive logic much easier
- `flake8` and `mypy` caught several subtle bugs early

### What Could Be Improved

- Performance optimization for large mazes (current implementation slows on grids above ~100×100)
- A* solver for more efficient pathfinding
- GUI visualization instead of ASCII output

### Tools Used

- **pdb** — interactive debugger
- **flake8** — linting and style enforcement
- **mypy** — static type checking
- **Makefile** — task automation

---

## Project Structure

```
Amaze/
├── a_maze_ing.py
├── maze/
│   ├── __init__.py
│   ├── maze_generator.py
│   ├── maze_solver.py
├── Makefile
├── config.txt
├── maze.txt
├── requirement.txt
├── README.md
```

---

## Final Note

This project demonstrates:
- Maze generation using two distinct algorithms
- Modular software design with reusable components
- Effective use of debugging and static analysis tools
- Team collaboration with clearly defined roles
