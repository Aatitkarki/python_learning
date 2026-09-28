"""00a transfer answer: run as a script or paste main's statements in a notebook."""
import sys

def main():
    hours_per_week = 15
    weeks = 80
    print('Hello, AI engineering')
    print('Interpreter:', sys.executable)
    print('Planned hours:', weeks * hours_per_week)
    assert weeks * hours_per_week == 1200

if __name__ == '__main__': main()
