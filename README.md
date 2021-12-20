[![Build Status](https://circleci.com/gh/StackStorm-Exchange/stackstorm-orion.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/StackStorm-Exchange/stackstorm-orion) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# SolarWinds Orion Integration Pack

This pack integrates with SolarWinds Orion (a commercial monitoring
platform).

## Issues

- If you don't have Orion NCM installed extra errors appear in the logs.

## Configuration

Copy the example configuration in [orion.yaml.example](./orion.yaml.example)
to `/opt/stackstorm/configs/orion.yaml` and edit as required.

It must contain:

```yaml
---
orion_label: "The label to use when referencing the Orion platform."
orion_host: "Name/IP of primary Orion server"
orion_user: "Username for Orion"
orion_password: "Password for Orion"
unmanage_max: "Max time in minutes that node can be put in unmanaged state"
snmp_default: "SNMP community to use by default"
snmp_customer: "SNMP community to use if customer specified"
snmp_internal: "SNMP community to use if internal specified"
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Actions

* `add_custom_pollers_to_node` - Add a list of custom (Universal Device) pollers to a Node
* `add_node_to_ncm` - Add an Orion Node to NCM
* `drain_poller` - Drain nodes from one Orion poller to another.
* `get_discovery_progress` - Get the progress of an SolarWinds Orion Discovery.
* `list_node_custom_properties` - List the custom properties for a SolarWinds Orion nodes
* `list_nodes_by_poller` - List the nodes on a SolarWinds Orion poller
* `list_nodes_by_status` - List the nodes by status
* `list_sdk_verb_args` - List all the arguments for an entity and verb that can be invoked via SolarWinds Orion.
* `list_sdk_verbs` - List all the verbs that can be invoked via SolarWinds Orion
* `ncm_config_download` - Download config(s) from SolarWinds NCM Orion module.
* `ncm_execute_script` - Execute an script on an Orion NCM Node.
* `node_create` - Create a node in SolarWinds Orion.
* `node_create_snmpv3` - Create a node in SolarWinds Orion with SNMPv3.
* `node_discover_and_add_interfaces` - Discover and add Interfaces for a SolarWinds Orion node.
* `node_discover_and_add_interfaces_by_name_and_type` - Discover and add Interfaces for a SolarWinds Orion node based upon the ifName, ifType, and (optional) ifAdminStatus
* `node_remanage` - Re-manage a SolarWinds Orion nodes
* `node_status` - Query SolarWinds Orion for a node's status (i.e. Up/Down)
* `node_unmanage` - Unmanage a SolarWinds Orion node
* `nodes_pollnow` - Force multiple polls of a list of SolarWinds Orion nodes.
* `query` - Execute generic SWQL queries.
* `start_discovery` - Create a discovery profile in SolarWinds Orion.
* `update_interface_custom_properties` - Update the custom properties of an interface on an Orion Node
* `update_interface_properties` - Update the "standard" properties (e.g. Unpluggable) on an interface of an Orion Nodes 
* `update_node_custom_properties` - Update an Orion Nodes custom properties
* `update_node_poller` - Update an Orion Nodes poller

## Rules

### Start Discovery Webhook

The JSON that should be posted to URL (XXXX) is as follows:

```json
{"orion_start_discovery": {
   "name": "My Example Discovery",
   "platform": "orion",
   "poller": "(primary|poller_name)",
   "snmp_communities": ["internal", "public"],
   "nodes": null | ["ip_address", "dns_name"],
   "subnets": null | ["10.1.0.0/255.0.0.0", "192.168.1.0/255.255.255.0" ]
   "ip_ranges": null | ["10.2.0.1:10.2.0.9", "192.168.2.1:"192.168.2.9"],
   "no_icmp_only": true | false,
   "auto_import": true | false
  }
}
```

The Discovery process in Orion only supports a single choice out of
the following:

- nodes
- subnets
- ip\_ranges

So only pick one or the action will fail.

It's most useful if auto\_import is set to true, as currently no action
exists to call the `ImportDiscoveryResults` Verb. If it's set to
false, someone will need to visit the Orion WebUI and complete it by
importing the discovery.

*Note:* The entries in the `snmp_communities` array can be standard
entries in `orion.yaml` or a community. Either way, the community
*must* already be in use in Orion and the `Orion.Credential` table.
