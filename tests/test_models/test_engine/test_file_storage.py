#!/usr/bin/python3

import unittest
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.fs = FileStorage()

    def tearDown(self):
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_all(self):
        self.assertIsInstance(self.fs.all(), dict)

    def test_new(self):
        bm = BaseModel()
        self.fs.new(bm)
        key = "{}.{}".format(type(bm).__name__, bm.id)
        self.assertEqual(bm, self.fs.all()[key])

    def test_save(self):
        bm = BaseModel()
        self.fs.new(bm)
        self.fs.save()
        with open(FileStorage._FileStorage__file_path, "r") as f:
            file_content = f.read()
        self.assertIn(type(bm).__name__, file_content)
        self.assertIn(bm.id, file_content)

    def test_reload(self):
        bm = BaseModel()
        self.fs.new(bm)
        self.fs.save()
        self.fs.reload()
        key = "{}.{}".format(type(bm).__name__, bm.id)
        self.assertEqual(bm.to_dict(), self.fs.all()[key].to_dict())
