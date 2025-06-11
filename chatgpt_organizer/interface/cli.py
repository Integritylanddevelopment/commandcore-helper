from explorer.controller import handle_input

def cli_loop():
    print("🖥️  CommandCore CLI - Type ':exit' to quit.")
    print("Available commands: :tree, :preview <path>, :contents <path>, :replay <file>, :search <term>\n")

    while True:
        try:
            user_input = input(">> ").strip()
            if user_input:
                handle_input(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
