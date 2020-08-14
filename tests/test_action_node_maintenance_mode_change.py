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

import mock
from orion_base_action_test_case import OrionBaseActionTestCase
from node_maintenance_mode_change import NodeMaintenanceModeChange

__all__ = [
    'NodeMaintenanceModeChangeTestCase'
]


class NodeMaintenanceModeChangeTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = NodeMaintenanceModeChange

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        with self.assertRaises(ValueError):
            action.run(False, "node1")

    def test_run_node_not_found(self):
        action = self.setup_query_blank_results()
        with self.assertRaises(ValueError):
            action.run(False, "node1")

    @mock.patch('lib.actions.OrionBaseAction.invoke')
    @mock.patch('lib.actions.OrionBaseAction.get_node')
    @mock.patch('lib.actions.OrionBaseAction.connect')
    def test_run_mm_enabled(self, mock_connect, mock_get_node, mock_invoke):
        action = self.get_action_instance(config=self.full_config)

        test_mm_enabled = True
        test_node = "test-node.fqdn"
        test_sw_uri = "swis://solarwinds.com/Orion/Orion.Nodes/NodeID=sw123"

        expected_result = "maintenance mode enabled"

        mock_connect.return_value = "orion"
        type(mock_get_node.return_value).uri = mock.PropertyMock(return_value=test_sw_uri)
        mock_invoke.return_value = expected_result

        result = action.run(test_mm_enabled, test_node)

        self.assertEqual(result, expected_result)
        mock_get_node.assert_called_with(test_node)
        mock_invoke.assert_called_with("Orion.AlertSuppression",
                                       "SuppressAlerts",
                                       [test_sw_uri])

    @mock.patch('lib.actions.OrionBaseAction.invoke')
    @mock.patch('lib.actions.OrionBaseAction.get_node')
    @mock.patch('lib.actions.OrionBaseAction.connect')
    def test_run_mm_disabled(self, mock_connect, mock_get_node, mock_invoke):
        action = self.get_action_instance(config=self.full_config)

        test_mm_enabled = False
        test_node = "test-node.fqdn"
        test_sw_uri = "swis://solarwinds.com/Orion/Orion.Nodes/NodeID=sw123"

        expected_result = "maintenance mode disabled"

        mock_connect.return_value = "orion"
        type(mock_get_node.return_value).uri = mock.PropertyMock(return_value=test_sw_uri)
        mock_invoke.return_value = expected_result

        result = action.run(test_mm_enabled, test_node)

        self.assertEqual(result, expected_result)
        mock_get_node.assert_called_with(test_node)
        mock_invoke.assert_called_with("Orion.AlertSuppression",
                                       "ResumeAlerts",
                                       [test_sw_uri])
