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

from orion_base_action_test_case import OrionBaseActionTestCase
from mock import MagicMock

from nodes_pollnow import NodesPollNow

__all__ = [
    'NodesPollNowTestCase'
]


class NodesPollNowTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = NodesPollNow

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          ["router1"],
                          2,
                          1)

    def test_run_node_not_exist(self):
        action = self.setup_query_blank_results()
        self.assertRaises(ValueError,
                          action.run,
                          ["router1"],
                          2,
                          1)

    def test_run_polled(self):
        action = self.setup_node_exists()
        expected = {'down': [], 'warning': [], 'extra_count': False, 'last_count': 2, 'up': [1]}

        query_data = []
        query_data.append(self.query_npm_node)
        query_data.append(self.query_ncm_node)
        query_data.append(self.query_node_agent)
        query_data.append({'results': [{'Status': 9}]})
        query_data.append({'results': [{'Status': 9}]})
        query_data.append({'results': [{'Status': 1}]})
        action.query = MagicMock(side_effect=query_data)

        result = action.run(["router1"], 5, 5)
        self.assertEqual(result, expected)
