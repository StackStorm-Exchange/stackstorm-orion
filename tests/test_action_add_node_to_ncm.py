# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import yaml
from mock import Mock, MagicMock

from st2tests.base import BaseActionTestCase

from add_node_to_ncm import AddNodeToNCM

__all__ = [
    'AddNodeToNCMTestCase'
]


class AddNodeToNCMTestCase(BaseActionTestCase):
    action_cls = AddNodeToNCM

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          AddNodeToNCM,
                          yaml.safe_load(
                              self.get_fixture_content('blank.yaml')))

    def test_run_is_instance(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        self.assertIsInstance(action, AddNodeToNCM)

    def test_run_connect_fail(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = Mock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "router1")

    def test_run_node_not_in_npm(self):
        query_data = [{'results': []}]

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)

        self.assertRaises(UserWarning,
                          action.run,
                          "orion",
                          "router1")

    def test_run_node_already_in_ncm(self):
        query_data = [
            yaml.safe_load(
                self.get_fixture_content("orion_npm_results.yaml")),
            yaml.safe_load(
                self.get_fixture_content("orion_ncm_results.yaml"))]

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)

        self.assertRaises(UserWarning,
                          action.run,
                          "orion",
                          "router1")

    def test_run_add_node_to_ncm(self):
        expected = "abc-1234"

        query_data = [
            yaml.safe_load(
                self.get_fixture_content("orion_npm_results.yaml")),
            {'results': []}]

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)
        action.invoke = MagicMock(return_value="abc-1234")

        result = action.run("router1",
                            "orion")

        self.assertEqual(result, expected)