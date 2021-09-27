import re
from argparse import Namespace
from re import Pattern, Match
from typing import TextIO, Dict, NoReturn, Final, Callable, List
import argparse

HEADER: Final[str] = "Dwarf Fortress color scheme file (You can edit this line)"


class Color:

    PATTERNS: Final[Dict[str, Pattern]] = {
        "hex": re.compile("(?:#|)([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})"),
        "rgb": re.compile(r"rgb\((\d{1,3}), (\d{1,3}), (\d{1,3})\)")
    }

    def __init__(self, color: str) -> NoReturn:
        self.value: Dict[str, int] = self._from_string(color)

    @staticmethod
    def _from_string(color: str) -> Dict[str, int]:
        color: str = color.strip()
        string_parser = Color._get_string_parser(color)
        return string_parser(color)

    @staticmethod
    def _get_string_parser(color: str) -> Callable:
        if Color._is_hex(color):
            return Color._from_hex
        elif Color._is_rgb(color):
            return Color._from_rgb
        else:
            raise ValueError("Not a valid color value format")

    @staticmethod
    def _from_hex(color: str) -> Dict[str, int]:
        return Color._parse_hex_color_to_rgb(color)

    @staticmethod
    def _from_rgb(color: str) -> Dict[str, int]:
        return Color._parse_rgb_color_to_rgb(color)

    @staticmethod
    def _is_hex(color: str) -> Match:
        return re.fullmatch(Color.PATTERNS["hex"], color)

    @staticmethod
    def _is_rgb(color: str) -> Match:
        return re.fullmatch(Color.PATTERNS["rgb"], color)

    @staticmethod
    def _parse_rgb_color_to_rgb(color: str) -> Dict[str, int]:
        match: Match = re.fullmatch(Color.PATTERNS["rgb"], color)
        return {
            "r": match[0],
            "g": match[1],
            "b": match[2]
        }

    @staticmethod
    def _parse_hex_color_to_rgb(color_hex: str) -> Dict[str, int]:
        match = re.fullmatch(Color.PATTERNS["hex"], color_hex)
        color_rgb: Dict[str, int] = {
            "r": match[0],
            "g": match[1],
            "b": match[2]
        }
        return color_rgb


class ColorFileParser:

    @staticmethod
    def parse_color_file(filepath: str) -> Dict[str, str]:
        file: TextIO = ColorFileParser.open_color_file(filepath)
        colors: dict[str, str] = dict()
        for line in file:
            line_contents: list[str, str] = ColorFileParser._parse_line(line)
            ColorFileParser._update_colors(colors, line_contents)
        return colors

    @staticmethod
    def open_color_file(filepath: str) -> TextIO:
        with open(filepath, "r") as f:
            return f

    @staticmethod
    def _update_colors(colors: dict[str, str], line_contents: list[str, str]) -> NoReturn:
        color_name: str
        color_value: str
        color_name, color_value = line_contents
        colors.update({
            color_name: color_value
        })

    @staticmethod
    def _parse_line(line: str) -> List[str, str]:
        line_contents: list[str, str] = line.split("=")
        ColorFileParser._check_line_contents_if_valid(line_contents)
        line_contents = ColorFileParser._strip_whitespaces(line_contents)
        return line_contents

    @staticmethod
    def _strip_whitespaces(line_contents: list[str, str]) -> List[str, str]:
        line_contents = [x.strip() for x in line_contents.copy()]
        return line_contents

    @staticmethod
    def _check_line_contents_if_valid(line_contents: list[str, str]) -> NoReturn:
        if len(line_contents) == 1 or len(line_contents) > 2:
            color_name, color_value, *other = line_contents
            raise ValueError(f"Invalid color file format.\nParsed line content: {color_name}, {color_value}, {other}")


def main() -> NoReturn:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert a color list file to a Dwarf Fortress colors.txt file")
    parser.add_argument("color_file", metavar="COLOR_FILE", type=str,
                        help="Path to the color list file")
    parser.add_argument("dwarf_fortress_color_scheme_file_path", metavar="OUTPUT", type=str,
                        help="colors.txt file path")

    args: Namespace = parser.parse_args()

    color_values: Dict[str, str] = ColorFileParser.parse_color_file(args.color_file)

    rgb_values: dict[str, dict[str, int]] = get_rgb_values(color_values)

    write_color_scheme_file(args.dwarf_fortress_color_scheme_file_path, rgb_values)


def write_color_scheme_file(outfile: str, rgb_values: dict[str, dict[str, int]]) -> NoReturn:
    with open(outfile, "a") as color_scheme_file:
        color_scheme_file.write(HEADER)
        for color_name, color in rgb_values.items():
            for component_name, component_value in color.items():
                line: str = f"[{color_name.upper()}_{component_name.upper()}:{component_value}]"
                color_scheme_file.write(line)
            color_scheme_file.write("\n")


def get_rgb_values(color_values: dict[str, str]) -> Dict[str, Dict[str, int]]:
    rgb_values: Dict[str, Dict[str, int]] = dict()
    for color_name, color_value in color_values.items():
        color: Color = Color(color_value)
        rgb_values.update({color_name: color.value})
    return rgb_values
