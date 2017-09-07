#!/usr/bin/env python
import unittest
import lief
import tempfile
import sys
import subprocess
import stat
import os
import logging
import random
import itertools

from lief import Logger
Logger.set_level(lief.LOGGING_LEVEL.WARNING)
#Logger.set_level(lief.LOGGING_LEVEL.DEBUG)

from unittest import TestCase
from utils import get_sample


class TestNotes(TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)


    def test_change_note(self):
        _, output = tempfile.mkstemp(prefix="change_note_")

        etterlog = lief.parse(get_sample('ELF/ELF64_x86-64_binary_etterlog.bin'))
        build_id = etterlog[lief.ELF.NOTE_TYPES.BUILD_ID]

        new_desc = [i & 0xFF for i in range(500)]
        build_id.description = new_desc

        etterlog.write(output)

        etterlog_updated = lief.parse(output)

        self.assertEqual(etterlog[lief.ELF.NOTE_TYPES.BUILD_ID], etterlog_updated[lief.ELF.NOTE_TYPES.BUILD_ID])

        if os.path.isfile(output):
            os.remove(output)

    def test_remove_note(self):
        _, output = tempfile.mkstemp(prefix="remove_note_")
        self.logger.info("Output will be: {}".format(output))

        etterlog = lief.parse(get_sample('ELF/ELF64_x86-64_binary_etterlog.bin'))

        build_id = etterlog[lief.ELF.NOTE_TYPES.BUILD_ID]

        etterlog -= build_id

        etterlog.write(output)

        etterlog_updated = lief.parse(output)

        self.assertNotIn(lief.ELF.NOTE_TYPES.BUILD_ID, etterlog_updated)

    def test_add_note(self):
        _, output = tempfile.mkstemp(prefix="add_note_")
        self.logger.info("Output will be: {}".format(output))

        etterlog = lief.parse(get_sample('ELF/ELF64_x86-64_binary_etterlog.bin'))
        note = lief.ELF.Note("Foo", lief.ELF.NOTE_TYPES.GOLD_VERSION, [123])

        etterlog += note

        etterlog.write(output)

        etterlog_updated = lief.parse(output)

        self.assertIn(lief.ELF.NOTE_TYPES.GOLD_VERSION, etterlog_updated)




if __name__ == '__main__':

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    root_logger.addHandler(ch)

    unittest.main(verbosity=2)
