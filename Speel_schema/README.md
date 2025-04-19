# Python GUI Project

This project is a graphical user interface (GUI) application for managing game types and player availability. It allows users to select between different game types and view player availability in a structured format.

## Project Structure

```
Speel_schema
├── src
│   ├── gui_utils.py   # Contains GUI components and utility functions
│   ├── utils.py       # Core utility functions for scheduling logic
├── Gui.py             # Entry point for the GUI application
├── Terminal.py        # Command-line interface for generating schedules
├── requirements.txt   # Lists project dependencies
└── README.md          # Project documentation
```

## Features

- Dropdown menu for selecting game types: "duo," "trio," "squad," and "beker."
- Grid layout displaying locations and player availability.
- Dynamic updates based on user interactions.
- Command-line interface for advanced users to generate schedules.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Speel_schema
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   - For the GUI:
     ```
     python Gui.py
     ```
   - For the command-line interface:
     ```
     python Terminal.py
     ```

## Usage Guidelines

- Select a game type from the dropdown menu to view the corresponding player availability.
- The grid will update automatically based on the selected game type.
- Use the command-line interface for custom schedule generation.

## License

This project is licensed under the MIT License.
