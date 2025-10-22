# Simple Calculator

A GUI-based calculator application built with Python and Tkinter.

## Requirements
- Python 3.x with Tkinter support
- Windows, macOS, or Linux

## Installation & Usage

1. Ensure Python is installed on your system
2. Run the calculator:
   ```bash
   python simple_calculator.py
   ```

## Features

### Basic Operations
- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Square function (`x²`)

### Input Methods
- **Mouse**: Click buttons to input numbers and operations
- **Keyboard**: Type directly using number keys, operators, and decimal point
- **Clipboard**: Paste numbers using Ctrl+V (or Cmd+V on macOS)

### Smart Input Handling
- Prevents multiple decimal points in a single number
- Removes unnecessary leading zeros
- Supports negative numbers with leading minus sign
- Limits numbers to 15 significant digits for accuracy

### Special Functions
- **C**: Clear all input
- **DEL**: Delete last character (backspace)
- **=**: Calculate result
- **x²**: Square the current number

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `0-9` | Input digits |
| `+ - * /` | Mathematical operators |
| `.` | Decimal point |
| `Enter` | Calculate (equals) |
| `Backspace` | Delete last character |
| `Escape` | Clear all |
| `Ctrl+V` | Paste number |

### Error Handling
- Shows "Error" for invalid expressions
- Blocks input when error is displayed until cleared
- Validates pasted content to ensure only numbers are accepted

## Interface

The calculator features a modern dark theme with:
- Large, easy-to-read display
- Color-coded buttons (numbers, operators, functions)
- Hover effects for better user interaction
- Responsive button layout

## Technical Notes

- Uses Python's `eval()` function for calculations on sanitized input
- Input validation prevents code injection
- Results are formatted to maintain readability
- Supports both integer and floating-point arithmetic

## Troubleshooting

**Calculator won't start:**
- Ensure Python is installed and accessible from command line
- Check that Tkinter is available (`python -m tkinter` should open a test window)

**Keyboard input not working:**
- Click on the calculator window to ensure it has focus
- Try clicking in the display area first

**Paste not working:**
- Only plain numbers (with optional +/- sign) can be pasted
- Complex expressions cannot be pasted for security reasons
