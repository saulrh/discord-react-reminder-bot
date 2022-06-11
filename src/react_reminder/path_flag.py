import pathlib
from absl import flags


class PathParser(flags.ArgumentParser):
    def __init__(self):
        super(PathParser, self).__init__()

    def parse(self, argument):
        return pathlib.Path(argument)

    def flag_type(self):
        return "string filepath"


class PathFlag(flags.Flag):
    def __init__(
        self, name, default, help, **args  # pylint: disable=redefined-builtin
    ):
        p = PathParser()
        g = flags.ArgumentSerializer()
        super(PathFlag, self).__init__(p, g, name, default, help, **args)


def DEFINE_path(
    name,
    default,
    help,
    flag_values=flags.FLAGS,
    module_name=None,
    required=False,
    **args
):
    return flags.DEFINE_flag(
        PathFlag(name, default, help, **args), flag_values, module_name, required
    )
