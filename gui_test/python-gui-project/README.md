# Python GUI Project

This project is a graphical user interface (GUI) application for managing game types and player availability. It allows users to select between different game types and view player availability in a structured format.

## Project Structure

```
python-gui-project
├── src
│   ├── main.py        # Entry point for the application
│   ├── gui.py         # Contains GUI components and layout
│   └── utils.py       # Utility functions for application logic
├── requirements.txt    # Lists project dependencies
└── README.md           # Project documentation
```

## Features

- Dropdown menu for selecting game types: "duo," "trio," and "squad."
- Grid layout displaying locations and player availability.
- Dynamic updates based on user interactions.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-gui-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage Guidelines

- Select a game type from the dropdown menu to view the corresponding player availability.
- The grid will update automatically based on the selected game type.

## License

This project is licensed under the MIT License.
