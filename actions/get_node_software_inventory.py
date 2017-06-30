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


class GetNodeSoftware(OrionBaseAction):
    def run(self, matchtype=None, matchstring=None):
        """
        Return Software asset list
        """

        self.connect()

        swql = """SELECT nodes.nodeid, nodes.sysname, nodes.caption, Software.Name, 
                Software.Version, Software.Publisher
                FROM Orion.Nodes
                INNER JOIN Orion.AssetInventory.Software ON Software.NodeId = Nodes.NodeId
                WHERE Nodes.UnManaged = False """

        if matchtype == "sysname":
            swql += " and nodes.sysname = '%s'" % matchstring
        elif matchtype == "caption":
            swql += " and nodes.Caption = '%s'" % matchstring
        elif matchtype == "nodeid":
            swql += " and nodes.nodeid = %s" % matchstring

        kargs = {}

        try:
            orion_data = self.query(swql, **kargs)
        except:
            orion_data['results'] = "empty"

        return orion_data
