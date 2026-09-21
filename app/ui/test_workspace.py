"""
Basic test for the OFFLINE GENIUS dashboard.
"""

from dashboard import Dashboard


def main():
    dashboard = Dashboard()

    print("OFFLINE GENIUS TEST")
    print("===================")
    print("Dashboard loaded successfully.")

    dashboard.display()


if __name__ == "__main__":
    main()
