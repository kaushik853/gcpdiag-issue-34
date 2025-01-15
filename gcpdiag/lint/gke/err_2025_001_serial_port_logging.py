# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""GKE clusters must comply with serial port logging policy.

When the constraints/compute.disableSerialPortLogging policy is enabled,
GKE clusters must be created with logging disabled (serial-port-logging-enable: 'false'),
otherwise the creation of new nodes in Nodepool will fail.
"""

import logging
from typing import Optional
from gcpdiag import lint, models
from gcpdiag.queries import gke, orgpolicy

def check_serial_port_logging_policy(cluster: gke.Cluster) -> Optional[bool]:
  """
        Checks if serial port logging policy is enforced and if cluster complies with it.

        Returns:
            bool: True if cluster complies with policy, False if not compliant,
                 None if policy not enforced
        """
  try:
    # Get the policy constraint status
    constraint = orgpolicy.get_effective_org_policy(
        cluster.project_id, 'constraints/compute.disableSerialPortLogging')

    # If policy is not enforced, return None (no compliance check needed)
    if not isinstance(
        constraint,
        orgpolicy.BooleanPolicyConstraint) or not constraint.is_enforced():
      return None

    # Get cluster node pools
    for nodepool in cluster.nodepools:
      # Check if serial port logging is disabled in node config metadata
      metadata = nodepool.config.metadata or {}
      serial_logging_enabled = metadata.get('serial-port-logging-enable', 'true').lower() == 'true'

      # if policy is enforced and serial port logging is enabled, cluster has error.
      if serial_logging_enabled:
        return False

    return True

  except ValueError:
    # Policy not found or not supported
    return None
  except Exception as e:
    logging.error(f"Error checking serial port logging policy: {e}")
    return None

def is_serial_port_logging_compliant(cluster: gke.Cluster) -> bool:
  """
        Checks if the cluster is compliant with serial port logging policy.

        Returns:
            bool: True if compliant or policy not enforced, False if non-compliant
        """
  compliance = check_serial_port_logging_policy(cluster)
  # Return True if policy is not enforced (compliance is None) or cluster is compliant
  return compliance is None or compliance

def run_rule(context: models.Context, report: lint.LintReportRuleInterface):
  clusters = gke.get_clusters(context)
  if not clusters:
    report.add_skipped(None, 'No clusters found')
    return

  for cluster in clusters.values():
    # Skip Autopilot clusters as they are managed by Google
    if cluster.is_autopilot:
      report.add_skipped(
          cluster,
          'Skipping Autopilot cluster - serial port logging managed by Google')
      continue

    # Check if cluster complies with serial port logging policy
    if is_serial_port_logging_compliant(cluster):
      report.add_ok(cluster)
    else:
      report.add_failed(cluster)
