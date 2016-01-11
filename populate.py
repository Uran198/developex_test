#!/usr/bin/env python
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from bank.terminal.factories import UserFactory

    for _ in range(10):
        UserFactory()
