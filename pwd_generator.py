import argparse
import random
import string


def generate_password(length=16, use_lowercase=True, use_uppercase=True, use_numbers=True, use_symbols=True):
    characters = ''
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character set must be selected")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def main():
    parser = argparse.ArgumentParser(description="Generate a random password.")
    
    # Argument for password length (required, default is 16)
    parser.add_argument("--length", type=int, default=16, help="Length of the password")

    # Optional flags to control which character sets to include
    parser.add_argument("--lowercase", action="store_true", help="Include lowercase letters")
    parser.add_argument("--uppercase", action="store_true", help="Include uppercase letters")
    parser.add_argument("--numbers", action="store_true", help="Include numbers")
    parser.add_argument("--symbols", action="store_true", help="Include symbols")

    args = parser.parse_args()

    # Default all options to True if no specific options are provided
    if not any([args.lowercase, args.uppercase, args.numbers, args.symbols]):
        args.lowercase = True
        args.uppercase = True
        args.numbers = True
        args.symbols = True

    # Generate the password
    password = generate_password(args.length, args.lowercase, args.uppercase, args.numbers, args.symbols)
    print(password)

if __name__ == "__main__":
    main()
	