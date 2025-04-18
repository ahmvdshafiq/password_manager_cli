import argparse
from app import db, encryption, password_generator

def main():
    parser = argparse.ArgumentParser(description="Simple Password Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add-site
    add_parser = subparsers.add_parser("add-site", help="Add a new password entry")
    add_parser.add_argument("site", help="Website or service name")
    add_parser.add_argument("username", help="Username or email")
    add_parser.add_argument("password", help="Password to store")

    # Generate-password
    gen_parser = subparsers.add_parser("generate-password", help="Generate a secure random password")
    gen_parser.add_argument("--length", type=int, default=16, help="Length of the password (default 16)")

    # View-passwords
    view_parser = subparsers.add_parser("view-passwords", help="View all stored passwords")

    args = parser.parse_args()

    db.create_table()

    if args.command == "add-site":
        encrypted = encryption.encrypt_password(args.password)
        db.save_password(args.site, args.username, encrypted)
        print(f"🔐 Password for {args.site} saved.")

    elif args.command == "generate-password":
        password = password_generator.generate_password(args.length)
        print(f"🔐 Generated Password: {password}")
        pyperclip.copy(password)