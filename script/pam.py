#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main file to excute the pam."""

import utils.pam_argparser as pap
from utils.pam_manager import Pam_manager
import utils.update_global as ug

if __name__ == '__main__':
    ARGS = pap.get_pam_argparse()
    ug.define_path_config(ARGS.config)
    ug.define_path_forms(ARGS.forms)
    print(Pam_manager(ARGS))
