# Changelog

## 0.7.11

- Added action to enable and disable maintenance mode on a given node
  Contributed by John Schoewe (Encore Technologies)

## 0.7.10

- More linting fixes

## 0.7.9

- Minor linting fix

## 0.7.8

- Fixed issue where get_node_id can return a null.
- Silenced SSL warnings.
  Contributed by Bradley Bishop (Encore Technologies)

## 0.7.7

- Added badges to README and fixed unit tests.
  Contributed by Nick Maludy (Encore Technologies) #17

## 0.7.6

- Added the ability to get agent information without getting the node.
  Contributed by Bradley Bishop (Encore Technologies)

## 0.7.5

- Added a new aciton `query` that can be used to execute generic SWQL queries.
  Contributed by Nick Maludy (Encore Technologies)

## 0.7.4

- Added new action `get_node_custom_properties` to retrieve custom properties set on
  a node object.
- Fixed a bug in `list_sdk_verbs` that caused issues when the API returned `None` for
  `EntityName` or `MethodName`

## 0.7.3

- Migrate maintainer to Encore Technologies <code@encore.tech>

## 0.7.2

- Minor linting fix

## 0.7

- Addition of get_agent_id action
- Addition of agent_delete action
- Addition of node_delete action
- Addition of agent information to Node definition
  - Accepts agent_id and angent_uri
- Addition of agent query to get agent information
  - Uses Node ID information to query for Agent
- Addition of date inputs for node_unmanage
  - kept minutes functionality
  - allows unmanage to be scheduled for future if needed

## 0.6

- Addition of get_node_id action
- Addition of software_inventory action

## 0.5.1

- Added example configuration file
- Updated README, added actions

## 0.5.0

- Renamed node\_pollnow action to nodes\_pollnow and extended it to
  support multiple nodes, count of polls and a pause between them.
- Added list\_nodes\_by\_poller action.
- Added update\_node\_poller action.
- Added list\_nodes\_by\_status action.
- Add drain\_poller workflow.
- Fix naming of node\_unmanage and node\_remanage.
- Migrate `config.yaml` to `config.schema.yaml`.
  - Due to this migration only a single Orion platform is now supported.
  - For SNMP Communities the special values `internal` and `customer`
    will be replaced with the config values.
- Remove std\_community parameter from node\_create and use the
  standard function.

## 0.3.1

- In the Orion.node\_status alias set the color for the result so it
  reflects it status.

## 0.3

- Added the following actions:
   - node\_create (tbc).
   - node\_remanage.
   - node\_unmanage.
   - node\_custom\_prop\_list (tbc).
   - ncm\_node\_add (tbc).
   - node\_custom\_prop\_update (tbc).
- Renamed action status to node\_status.
- Fixes to ncm\_config\_download action & alias.

## 0.1

- Added action & alias status.
- Added action & alias ncm\_config\_download.
