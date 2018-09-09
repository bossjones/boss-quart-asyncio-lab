"""Debug module using ipython."""

import sys
import signal
import logging
import os

logger = logging.getLogger(__name__)

# SOURCE: https://github.com/mjumbewu/jokosher/blob/e181d738674a98242b10dd697a9628be54c3121a/bin/jokosher
# if platform.system() == "Windows":
# 	ENV_PATHS = {"JOKOSHER_DATA_PATH" : ".\\",
# 			"JOKOSHER_IMAGE_PATH" : ".\\pixmaps\\",
# 			"JOKOSHER_LOCALE_PATH" : ".\\locale\\",
# 			"JOKOSHER_HELP_PATH" : ".\\help\\",
# 			"GST_PLUGIN_PATH" : ".\\"
# 			}
# else:
# 	ENV_PATHS = {"JOKOSHER_DATA_PATH" : "/usr/share/jokosher/",
# 			"JOKOSHER_IMAGE_PATH" : "/usr/share/jokosher/pixmaps/",
# 			"JOKOSHER_LOCALE_PATH" : "/usr/share/locale/",
# 			"JOKOSHER_HELP_PATH" : "/usr/share/gnome/jokosher/"
# 			}
# #must set variables before importing Globals because it requires them
# for var, path in ENV_PATHS.iteritems():
# 	#if it is not already set, set the enviroment variable.
# 	os.environ.setdefault(var, path)

# NOTE:
# enable path to dump dot files
# this *must* be done before 'import Gst' because it reads the env var on startup. ( Double check if this is still true or not )

# source: https://github.com/kevinseelbach/generic_utils/blob/8b5636359fd248f5635160358fa237f9333f246f/src/generic_utils/debug_utils/__init__.py
def enable_thread_dump_signal(signum=signal.SIGUSR1, dump_file=sys.stderr):
    """Turns on the ability to dump all of the threads to
    Currently this is just a wrapper around the faulthandler module
    :param signum: The OS signal to listen for and when signalled the thread dump should be outputted to `dump_file`.
        The default is the SIGUSR1 signal
    :type signum: int
    :param dump_file: The dump_file to output the threaddump to upon the signal being sent to the process.
    :type dump_file: file
    """
    # Utilities for debugging a python application/process.
    # This is not specifically related testing, but related more to
    # just debugging of code and process which could be in production.
    import faulthandler

    faulthandler.register(signum, file=dump_file, all_threads=True, chain=True)


def init_debugger():
    import sys

    from IPython.core.debugger import Tracer  # noqa
    from IPython.core import ultratb

    sys.excepthook = ultratb.FormattedTB(
        mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
    )


# http://stackoverflow.com/questions/582056/getting-list-of-parameter-names-inside-python-function
# https://docs.python.org/3/library/inspect.html

def init_rconsole_server():
    try:
        from rfoo.utils import rconsole

        rconsole.spawn_server()
    except ImportError:
        logger.error("No socket opened for debugging -> please install rfoo")


# source: http://blender.stackexchange.com/questions/1879/is-it-possible-to-dump-an-objects-properties-and-methods
def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


# NOTE: What is a lexer - A lexer is a software program that performs lexical analysis. Lexical analysis is the process of separating a stream of characters into different words, which in computer science we call 'tokens' . When you read my answer you are performing the lexical operation of breaking the string of text at the space characters into multiple words.
def dump_color(obj):
    # source: https://gist.github.com/EdwardBetts/0814484fdf7bbf808f6f
    from pygments import highlight

    # Module name actually exists, but pygments loads things in a strange manner
    from pygments.lexers import Python3Lexer  # pylint: disable=no-name-in-module
    from pygments.formatters.terminal256 import (
        Terminal256Formatter
    )  # pylint: disable=no-name-in-module

    for attr in dir(obj):
        if hasattr(obj, attr):
            obj_data = "obj.%s = %s" % (attr, getattr(obj, attr))
            print(highlight(obj_data, Python3Lexer(), Terminal256Formatter()))


# SOURCE: https://github.com/j0nnib0y/gtao_python_wrapper/blob/9cdae5ce40f9a41775e29754b51325652584cf25/debug.py
def dump_magic(obj, magic=False):
    """Dumps every attribute of an object to the console.
    Args:
        obj (any object): object you want to dump
        magic (bool, optional): True if you want to output "magic" attributes (like __init__, ...)
    """
    for attr in dir(obj):
        if magic is True:
            print("obj.%s = %s" % (attr, getattr(obj, attr)))
        else:
            if not attr.startswith("__"):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))


def get_pprint():
    import pprint

    # global pretty print for debugging
    pp = pprint.PrettyPrinter(indent=4)
    return pp


def pprint_color(obj):
    # source: https://gist.github.com/EdwardBetts/0814484fdf7bbf808f6f
    from pygments import highlight

    # Module name actually exists, but pygments loads things in a strange manner
    from pygments.lexers import PythonLexer  # pylint: disable=no-name-in-module
    from pygments.formatters.terminal256 import (
        Terminal256Formatter
    )  # pylint: disable=no-name-in-module
    from pprint import pformat

    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))


__all__ = ("pprint_color", "get_pprint", "dump_magic", "dump_color", "dump")
