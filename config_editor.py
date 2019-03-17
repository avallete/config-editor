import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("config_editor")


def parser_creator():
    """Create and configure the argument parser for our program"""
    parser = argparse.ArgumentParser(
        description="Modifies arbitrary value in the configuration file on arbitrary position")
    parser.add_argument(
        "-f", "--file",
        type=argparse.FileType('r'),
        required=True,
        help="The json configuration file you want to change"
    )
    parser.add_argument(
        "-c", "--changes",
        type=argparse.FileType('r'),
        required=True,
        help="The file containing the instructions about the changes"
    )
    parser.add_argument(
        "-o", "--output",
        type=argparse.FileType('w'),
        help="Output file",
        default=sys.stdout
    )
    parser.add_argument(
        "-p", "--path-create",
        dest="force_create",
        action="store_true",
        default=False,
    )
    return parser
