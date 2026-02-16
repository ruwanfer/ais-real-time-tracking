# test_function.py
from collect_ais import is_valid_ship_name

# Test the function
test_names = ["VIKING", "", "Unknown", None, "A", "ADRIATICBORG"]

for name in test_names:
    result = is_valid_ship_name(name)
    print(f"'{name}' -> {'VALID' if result else 'INVALID'}")