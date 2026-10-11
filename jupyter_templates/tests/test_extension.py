# *****************************************************************************
#
# Copyright (c) 2024, the jupyter_templates authors.
#
# This file is part of the jupyter_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
# for Coverage
from unittest.mock import MagicMock

import pytest

from jupyter_templates.extension import TemplateNamesHandler, TemplatesHandler, _load_jupyter_server_extension, load_jupyter_server_extension


class TestExtension:
    @pytest.mark.parametrize("handler_type", [TemplatesHandler, TemplateNamesHandler])
    def test_handler_requires_loader(self, handler_type):
        handler = object.__new__(handler_type)
        with pytest.raises(ValueError, match="template loader"):
            handler.initialize()
        loader = MagicMock()
        handler.initialize(loader=loader)
        assert handler.loader is loader

    def test_template_names(self, monkeypatch):
        handler = object.__new__(TemplateNamesHandler)
        loader = MagicMock(template_label="Notebook")
        loader.get_templates.return_value = ({"examples": [{"name": "Example.ipynb"}]}, {})
        handler.initialize(loader)
        finish = MagicMock()
        monkeypatch.setattr(handler, "finish", finish)
        handler.get()
        finish.assert_called_once_with('{"templates": {"examples": [{"name": "Example.ipynb"}]}, "template_label": "Notebook"}')

    def test_load_jupyter_server_extension(self):
        m = MagicMock()

        m.web_app.settings = {}
        m.web_app.settings["base_url"] = "/test"
        _load_jupyter_server_extension(m)

    def test_load_jupyter_server_extension_nb6_server2(self):
        m = MagicMock()
        m.web_app.settings = {}
        m.web_app.settings["base_url"] = "/test"
        load_jupyter_server_extension(m)
