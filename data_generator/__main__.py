from time import sleep
from generator import generate


def main() -> None:
    while True:
        generate()
        sleep(1)


if __name__ == "__main__":
    main()
