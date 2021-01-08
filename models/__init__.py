from dreamtools import tools
from dreamtools.cfgmng import CFGBases


def savingbyref(d, filename, *args, **kwargs):
    """
    Récupération des parametres de configuration du fichier <filepath> section <r>

    :param str filename: Fichier de configuration
    """
    filepath = tools.path_build(CFGBases.CFG_DIR, f'{filename}.yml')
    return CFGBases.save_cfg(d, filepath, *args, **kwargs)
