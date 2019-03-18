import json
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


def read_line_by_line(file):
    """Simple utils function allowing to easily iterate over the changes file"""
    line = file.readline()
    while line:
        yield line
        line = file.readline()


def load_json_config(file):
    """
    Simply load our json config file into memory
    :returns dict()
    """
    try:
        return json.load(file)
    except json.decoder.JSONDecodeError as e:
        logger.error("Error while loading config file it's probably not a valid json: %s" % e)
        raise e


def parse_changes_file(file):
    """
    Function who will read and parse our changes file.
    Will return a list of tuple, each containing the path into our object that we target, and the new value we want.
    :returns list(tuple(path, value))
    """
    changes = []
    fileit = read_line_by_line(file)
    for line in fileit:
        path, value = line.split(":", 1)  # Only get the fist split, to avoid errors with one line json into values
        changes.append((json.loads(path), json.loads(value)))
    return changes


def get_update_or_create_value(obj, path, value, force_create=False):
    subpaths = path.split(".")
    lastkey = subpaths[-1]
    if len(subpaths) > 1:
        subpaths.pop()  # Remove the last element since it will be assign at the end
        # Let's create our path into our config recursively
        for p in subpaths:
            if not obj.get(p):
                if force_create:
                    obj[p] = {}
                else:
                    raise KeyError("""
                        Cannot update %s because %s does not exist in the subpath.
                        Please use the -p option to force create.
                    """ % (path, p))
            obj = obj[p]
    # Assign our value to our last key
    obj[lastkey] = value
    # We don't need to return anything since obj is a dict and are so updated using references
    return


if __name__ == "__main__":
    parser = parser_creator()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    try:
        configfile = load_json_config(args.file)
        changes = parse_changes_file(args.changes)
        for path_to_change, value in changes:
            get_update_or_create_value(configfile, path_to_change, value, force_create=args.force_create)
        print(json.dumps(configfile), file=args.output)
        sys.exit(0)
    except Exception as e:
        logger.error("An error occured: %s" % e)
        sys.exit(1)
