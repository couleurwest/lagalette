import pathlib
import sys

from dreamtools import tools
from dreamtools.cfgmng import CFGBases


def get_resource_path(relative_path):
    rel_path = pathlib.Path(relative_path)
    dev_base_path = pathlib.Path(__file__).resolve().parent.parent
    base_path = getattr(sys, "_MEIPASS", dev_base_path)

    return base_path / rel_path


def savingbyref(d, filename, *args, **kwargs):
    """
    Récupération des parametres de configuration du fichier <filepath> section <r>

    :param d:
    :param str filename: Fichier de configuration
    """
    filepath = tools.path_build(CFGBases.CFG_DIR, f'{filename}.yml')
    return CFGBases.save_cfg(d, filepath, *args, **kwargs)
