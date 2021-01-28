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
# limitations under the License.

from lib.actions import OrionBaseAction
from lib.utils import send_user_error


class NodeMaintenanceModeChange(OrionBaseAction):
    def run(self, maintenance_mode_enabled, node):
        """
        Enable/disable maintenance mode in Solarwinds Orion to suppress/resume
        alerts for a given node
        """

        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.uri:
            error_msg = "Node not found for " + node
            send_user_error(error_msg)
            raise ValueError(error_msg)

        # Check if maintenance mode should be enabled or not
        if maintenance_mode_enabled:
            alert_action = "SuppressAlerts"
        else:
            alert_action = "ResumeAlerts"

        result = self.invoke("Orion.AlertSuppression",
                             alert_action,
                             [orion_node.uri])

        return result
