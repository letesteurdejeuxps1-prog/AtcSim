import json
import math
import pathlib
import pygame

from pages.Variables import Variables


class Main:

    def __init__(self, v: Variables, working_dir: str) -> None:
        self.variables = v
        self.root_directory = working_dir
