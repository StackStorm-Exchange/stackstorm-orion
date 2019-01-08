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

from mock import MagicMock

from orion_base_action_test_case import OrionBaseActionTestCase

from query_action import QueryAction

__all__ = [
    'QueryTestCase'
]


class QueryTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = QueryAction

    def test_query_with_params(self):
        query = "SELECT Uri FROM Orion.Pollers WHERE PollerID=@pollerid"
        parameters = {"pollerid": 9}

        expected = {'blah': 'router1 (NodeId: 1; ip: 192.168.0.1)'}

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(return_value=expected)

        result = action.run(query, parameters)
        self.assertEquals(result, expected)

        action.connect.assert_called()
        action.query.assert_called_with(query, **parameters)
