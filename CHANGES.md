# Changelog

## 0.6

- Addition of get_node_id action
- Addition of software_inventory action

## 0.5.1

- Added example configuration file
- Updated README, added actions

## 0.5

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
