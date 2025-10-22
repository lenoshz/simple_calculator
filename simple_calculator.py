import tkinter as tk
import re

# Configuration
MAX_DIGITS = 15
ALLOWED_CHARS = re.compile(r'^[0-9+\-*/().% ]+$')
NUMBER_PATTERN = re.compile(r'^[+-]?\d+(\.\d+)?$')

# Colors
SURFACE_COLOR = '#2C2C54'
NUM_BTN_COLOR = '#40407A'
BTN_TEXT_COLOR = '#F1F2F6'
DISP_BG_COLOR = '#F1F2F6'
FUNC_BTN_COLOR = '#706FD3'
OPERATOR_COLOR = '#FF5252'
EQUALS_COLOR = '#2ED573'

def is_operator(char):
    return char in '+-*/'

def get_current_number(expression):
    # Find the last number in the expression
    last_op_pos = -1
    for i in range(len(expression)-1, -1, -1):
        if is_operator(expression[i]) or expression[i] in '() ':
            last_op_pos = i
            break
    return expression[last_op_pos+1:]

def count_digits(text):
    return sum(1 for c in text if c.isdigit())

def add_digit(display, digit):
    current_text = display.get()
    if current_text == "Error":
        display.bell()
        return

    current_num = get_current_number(current_text)
    if count_digits(current_num) >= MAX_DIGITS:
        display.bell()
        return

    # Handle leading zeros
    if current_num == '0' and '.' not in current_num:
        if digit == '0':
            display.bell()
            return
        else:
            # Replace the leading zero
            start_pos = len(current_text) - len(current_num)
            display.delete(start_pos, tk.END)
            display.insert(tk.END, digit)
            return

    display.insert(tk.END, digit)

def add_decimal(display):
    current_text = display.get()
    if current_text == "Error":
        display.bell()
        return

    current_num = get_current_number(current_text)
    if '.' in current_num:
        display.bell()
        return
        
    if current_num == '':
        display.insert(tk.END, '0.')
    else:
        display.insert(tk.END, '.')

def add_operator(display, operator):
    current_text = display.get()
    if current_text == "Error":
        display.bell()
        return
        
    if not current_text:
        if operator == '-':
            display.insert(tk.END, '-')
        return
        
    # Replace existing operator
    if current_text[-1] in '+-*/':
        display.delete(len(current_text)-1, tk.END)
        display.insert(tk.END, operator)
    else:
        display.insert(tk.END, operator)

def delete_last(display):
    current_text = display.get()
    if current_text == "Error":
        display.delete(0, tk.END)
        return
    if current_text:
        display.delete(len(current_text)-1, tk.END)

def clear_display(display):
    display.delete(0, tk.END)

def is_valid_expression(expr):
    if not ALLOWED_CHARS.match(expr):
        return False, "Invalid characters"
    
    # Check for multiple decimals in numbers
    tokens = re.split(r'[+\-*/%() ]+', expr)
    for token in tokens:
        if token.count('.') > 1:
            return False, "Invalid number format"
    
    if expr.strip() == '':
        return False, "Empty expression"
    return True, ""

def format_number(num):
    try:
        return format(num, f'.{MAX_DIGITS}g')
    except:
        return str(num)

def calculate(display):
    if display.get() == "Error":
        return

    expression = display.get().strip()
    if not expression:
        return
        
    expression = expression.replace('×', '*').replace('÷', '/')
    is_valid, error_msg = is_valid_expression(expression)
    
    if not is_valid:
        display.delete(0, tk.END)
        display.insert(0, "Error")
        return
        
    try:
        result = eval(expression)
        if isinstance(result, int):
            result_str = str(result) if len(str(abs(result))) <= MAX_DIGITS else format_number(result)
        else:
            result_str = format_number(result)
            
        display.delete(0, tk.END)
        display.insert(0, result_str)
    except:
        display.delete(0, tk.END)
        display.insert(0, "Error")

def square_number(display):
    current_text = display.get()
    if current_text == "Error":
        display.bell()
        return

    current_num = get_current_number(current_text)
    if current_num == '':
        display.bell()
        return

    start_pos = len(current_text) - len(current_num)

    # Check for unary sign
    sign = ''
    sign_pos = start_pos - 1
    if sign_pos >= 0 and current_text[sign_pos] in '+-':
        if sign_pos == 0 or current_text[sign_pos-1] in '+-*/(':
            sign = current_text[sign_pos]
            start_pos = sign_pos
            current_num = sign + current_num

    try:
        if '.' in current_num:
            number = float(current_num)
        else:
            number = int(current_num)
    except:
        display.bell()
        return

    squared = number * number

    if isinstance(squared, float):
        if squared.is_integer():
            squared_int = int(squared)
            result_str = str(squared_int) if len(str(abs(squared_int))) <= MAX_DIGITS else format_number(squared)
        else:
            result_str = format_number(squared)
    else:
        result_str = str(squared) if len(str(abs(squared))) <= MAX_DIGITS else format_number(squared)

    display.delete(start_pos, tk.END)
    display.insert(tk.END, result_str)

# GUI Setup
root = tk.Tk()
root.title("Calculator")
root.resizable(False, False)
root.configure(bg=SURFACE_COLOR)

main_frame = tk.Frame(root, bg=SURFACE_COLOR, padx=20, pady=20)
main_frame.pack()

# Display
entry = tk.Entry(main_frame, font=("Segoe UI", 22, "normal"), justify='right', width=16,
                 bg=DISP_BG_COLOR, fg='#2C2C54', insertbackground='#2C2C54', 
                 bd=0, relief='flat', highlightthickness=2, highlightcolor=FUNC_BTN_COLOR)
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=(5, 15), ipady=15, sticky='ew')
entry.focus_set()

# Button layout
buttons = [
    ('7', lambda: add_digit(entry, '7')),
    ('8', lambda: add_digit(entry, '8')),
    ('9', lambda: add_digit(entry, '9')),
    ('/', lambda: add_operator(entry, '/')),

    ('4', lambda: add_digit(entry, '4')),
    ('5', lambda: add_digit(entry, '5')),
    ('6', lambda: add_digit(entry, '6')),
    ('*', lambda: add_operator(entry, '*')),

    ('1', lambda: add_digit(entry, '1')),
    ('2', lambda: add_digit(entry, '2')),
    ('3', lambda: add_digit(entry, '3')),
    ('-', lambda: add_operator(entry, '-')),

    ('0', lambda: add_digit(entry, '0')),
    ('.', lambda: add_decimal(entry)),
    ('x²', lambda: square_number(entry)),
    ('+', lambda: add_operator(entry, '+')),

    ('C', lambda: clear_display(entry)),
    ('DEL', lambda: delete_last(entry)),
    ('=', lambda: calculate(entry)),
]

# Create buttons
row = 1
col = 0
button_font = ("Segoe UI", 14, "bold")

for text, command in buttons:
    # Set button colors
    if text.isdigit() or text == '.':
        bg_color = NUM_BTN_COLOR
    elif text in '+-*/':
        bg_color = OPERATOR_COLOR
    elif text == '=':
        bg_color = EQUALS_COLOR
    else:
        bg_color = FUNC_BTN_COLOR

    btn = tk.Button(main_frame, text=text, width=5, height=2, command=command,
                    font=button_font, bg=bg_color, fg=BTN_TEXT_COLOR,
                    activebackground=bg_color, activeforeground=BTN_TEXT_COLOR,
                    bd=0, highlightthickness=0, relief='flat', cursor='hand2')
    
    if text == '+':
        btn.grid(row=row, column=col, padx=3, pady=3, rowspan=2, sticky='nsew', ipadx=5, ipady=5)
    else:
        btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew', ipadx=5, ipady=5)
    
    main_frame.grid_columnconfigure(col, weight=1)
    main_frame.grid_rowconfigure(row, weight=1)
    
    col += 1
    if col > 3:
        col = 0
        row += 1

# Button hover effects
def button_hover(event, original_color):
    color_map = {
        NUM_BTN_COLOR: '#5A5A8A',
        OPERATOR_COLOR: '#FF7979',
        EQUALS_COLOR: '#55E590',
        FUNC_BTN_COLOR: '#9C88FF'
    }
    event.widget.configure(bg=color_map.get(original_color, original_color))

def button_leave(event, original_color):
    event.widget.configure(bg=original_color)

for widget in main_frame.winfo_children():
    if isinstance(widget, tk.Button):
        original_bg = widget.cget('bg')
        widget.bind('<Enter>', lambda e, color=original_bg: button_hover(e, color))
        widget.bind('<Leave>', lambda e, color=original_bg: button_leave(e, color))

# Clipboard handling
def handle_paste(event=None):
    if entry.get() == "Error":
        root.bell()
        return "break"

    try:
        clipboard_text = root.clipboard_get().strip()
    except tk.TclError:
        return "break"
        
    if not clipboard_text or not NUMBER_PATTERN.match(clipboard_text):
        root.bell()
        return "break"

    # Normalize number format
    sign = ''
    number_body = clipboard_text
    if number_body and number_body[0] in '+-':
        sign = number_body[0]
        number_body = number_body[1:]

    if '.' not in number_body:
        number_body = number_body.lstrip('0') or '0'
    
    normalized = sign + number_body

    # Check digit limit
    current_num = get_current_number(entry.get())
    if count_digits(current_num) + count_digits(normalized) > MAX_DIGITS:
        root.bell()
        return "break"
        
    entry.insert(tk.END, normalized)
    return "break"

# Keyboard handling
def handle_keypress(event):
    if entry.get() == "Error" and event.keysym not in ('BackSpace', 'Escape'):
        entry.bell()
        return "break"

    key = event.keysym
    char = event.char

    if key in ('Left', 'Right', 'Home', 'End', 'Tab'):
        return None

    if key == 'Return':
        calculate(entry)
        return "break"
    elif key == 'BackSpace':
        delete_last(entry)
        return "break"
    elif key == 'Escape':
        clear_display(entry)
        return "break"

    # Handle Ctrl+V
    if (key.lower() == 'v' and (event.state & 0x4)) or (key == 'v' and (event.state & 0x100000)):
        return handle_paste(event)

    if char.isdigit():
        add_digit(entry, char)
        return "break"
    elif char in '+-*/':
        add_operator(entry, char)
        return "break"
    elif char == '.':
        add_decimal(entry)
        return "break"

    return "break"

# Bind events
entry.bind('<Control-v>', handle_paste)
entry.bind('<Control-V>', handle_paste)
entry.bind('<Command-v>', handle_paste)
entry.bind('<Button-2>', handle_paste)
entry.bind('<Key>', handle_keypress)

root.mainloop()
