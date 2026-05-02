import secrets
import os
from pathlib import Path
from dotenv import load_dotenv, set_key


def generate_omnilogistics_secret():

    new_secret = secrets.token_hex(32)


    root_dir = Path(__file__).resolve().parent.parent
    env_path = root_dir / ".env"


    if not env_path.exists():
        env_path.touch()
        print(f"Created new environment file at: {env_path}")


    set_key(str(env_path), "JWT_SECRET", new_secret)

    print("--- OmniLogistics Security Update ---")
    print(f"SUCCESS: Secure JWT_SECRET generated.")
    print(f"PATH: {env_path}")
    print("WARNING: Keep this secret out of version control and public git repos.")


if __name__ == "__main__":
    generate_omnilogistics_secret()