import ollama
import time

# ------------------ ROLES ------------------
roles = {
    "1": {
        "name": "Python Tutor",
        "prompt": "You are a helpful Python tutor. Explain clearly with examples."
    },
    "2": {
        "name": "Fitness Coach",
        "prompt": "You are a fitness coach. Give workout and diet advice."
    },
    "3": {
        "name": "Travel Guide",
        "prompt": "You are a travel expert. Suggest trips and tips."
    }
}

# ------------------ UTIL ------------------
def count_tokens(text):
    # Approx token count (simple method)
    return len(text.split())

def show_roles():
    print("\n📌 Available Roles:")
    for key, role in roles.items():
        print(f"{key}. {role['name']}")
    print("add → Add custom role")

def select_role():
    while True:
        show_roles()
        choice = input("\nSelect role: ").strip()

        if choice == "add":
            name = input("Role name: ")
            prompt = input("System prompt: ")
            key = str(len(roles) + 1)
            roles[key] = {"name": name, "prompt": prompt}
            print(f"✅ Added role: {name}")

        elif choice in roles:
            return roles[choice]

        else:
            print("❌ Invalid choice")

# ------------------ CHAT ------------------
def chat_loop(role):
    print(f"\n🎭 Role: {role['name']}")
    print("Commands: switch | quit\n")

    messages = [{"role": "system", "content": role["prompt"]}]

    while True:
        user_input = input("👤 You: ")

        if user_input.lower() == "quit":
            print("👋 Exiting...")
            exit()

        if user_input.lower() == "switch":
            return

        messages.append({"role": "user", "content": user_input})

        start = time.time()

        print("🤖 AI: ", end="", flush=True)

        full_response = ""

        # 🔥 Streaming response
        stream = ollama.chat(
            model="llama3",
            messages=messages,
            stream=True
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
            full_response += content

        end = time.time()

        messages.append({"role": "assistant", "content": full_response})

        # 📊 Stats
        token_count = count_tokens(full_response)

        print("\n")
        print(f"⏱ Response time: {round(end - start, 2)} sec")
        print(f"🔢 Tokens (approx): {token_count}")
        print("-" * 50)

# ------------------ MAIN ------------------
def main():
    print("🚀 Role-Based Chat (Advanced)")

    while True:
        role = select_role()
        chat_loop(role)

if __name__ == "__main__":
    main()