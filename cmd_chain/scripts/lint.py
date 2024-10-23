import subprocess


def main():
    tools = ["black . --check", "pylint agent server tests", "mypy agent server tests"]

    for tool in tools:
        try:
            subprocess.run(tool, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed: {tool}")
            exit(1)


if __name__ == "__main__":
    main()
