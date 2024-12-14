# Buddy System Memory Allocation Algorithm

## _A Visual and Interactive Memory Management Tool_

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

![Buddy System Memory Allocation Algorithm Demo Tool UI](./images/buddy-system-demo-ui)

This project implements a **Buddy System Memory Allocation** algorithm with a graphical user interface (GUI) built using **Python** and **Tkinter**. The Buddy System is a classic memory management technique designed to minimize fragmentation and streamline allocations and deallocations.

- Add and remove processes with ease
- Observe real-time changes in memory allocation
- Dynamically adjust total memory size
- View internal fragmentation and memory usage stats
- Responsive layout and interactive visualization

✨ **No personal data is stored or processed.** ✨

## Key Features

- **Dynamic Allocation & Deallocation:**  
  Add processes by specifying memory requirements and remove them when done. The interface responds instantly, updating the memory map.

- **Visual Memory Map:**  
  The GUI displays allocated and free memory blocks:

  - **Green blocks:** Free memory
  - **Red/Blue blocks:** Allocated memory (blue highlights selected process)

- **Internal Fragmentation Stats:**  
  The system calculates and displays:

  - Total allocated memory
  - Total free memory
  - Internal fragmentation

- **Adjustable Total Memory:**  
  Modify the total memory capacity on the fly. The Buddy System automatically restructures its memory blocks accordingly.

- **Process Management & Auto-Naming:**  
  Processes are listed in a panel. Each newly added process increments its name (e.g., Process-1, Process-2...). Removing a process automatically selects the next one for quick workflow.

- **Responsive UI & Logging:**  
  Resize the window to see the UI adapt. Logs (with timestamps) show actions and events, helping you understand the system's decisions.

## Technology Stack

- **Python 3.x**: Core language
- **Tkinter**: GUI framework
- **Logging**: For action/event tracking
- **Buddy System Logic**: Implemented in Python

This project is inspired by classical Buddy System memory allocation strategies taught in operating systems and computer architecture courses.

## Installation & Setup

1. **Clone or Download the Repository:**
   ```bash
   git clone https://github.com/yourusername/buddy-system-allocation.git
   cd buddy-system-allocation

   ```
2. **(Optional) Create & Activate a Virtual Environment:**
   On linux
   ```bash
   python3 -m venv bds_env
   source bds_env/bin/activate
   ```
   On Windows (Command Prompt):
   ```bash
   python -m venv bds_env
   bds_env\Scripts\activate
   ```
3. **Run the Application:**
   ```bash
   python buddy_system_gui.py
   ```

## Usage

- **Set Total Memory:** Enter a new total memory size and update.
- **Add Process:** Enter process name and memory size, then click "Add Process".
- **Remove Process:** Select a process and click "Remove Process".
- **Observe Visualization:** Changes reflect in real-time on the memory map.
- **Adjust Window Size:** The interface responds to resizing.

## Credits

Developer: N.S. Udara Sampath Kavinda
Institution: The Open University of Sri Lanka, Department of Electrical and Computer Engineering.

## License

This project is licensed under the MIT License, allowing free use, modification, and distribution, provided the original author is credited.
