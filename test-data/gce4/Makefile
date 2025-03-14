PROJECT_ID  := $(shell terraform output -raw project_id)
PROJECT_ID_SUFFIX := $(shell terraform output -raw project_id_suffix)
PROJECT_NR  := $(shell terraform output -raw project_nr)
ORG_ID      := $(shell terraform output -raw org_id)
CURL         = ../../bin/curl-wrap.sh
JSON_CLEANER = ../../bin/json-cleaner
ZONE_1       = europe-west2-a

FAKE_PROJECT_ID = gcpdiag-gce4-aaaa
FAKE_PROJECT_ID_SUFFIX = runbook
FAKE_PROJECT_NR = 123456270
FAKE_ORG_ID = 11112222

COMPUTE_INSTANCES_MAXRESULTS=3

INSTANCE_NAME_GCE1=valid-linux-ssh
INSTANCE_NAME_GCE2=faulty-linux-ssh
INSTANCE_NAME_GCE3=valid-windows-ssh
INSTANCE_NAME_GCE4=faulty-windows-ssh

SED_SUBST_FAKE = sed -e "s/$(PROJECT_ID)/$(FAKE_PROJECT_ID)/" \
		     -e "s/$(PROJECT_NR)/$(FAKE_PROJECT_NR)/" \
		     -e "s/$(ORG_ID)/$(FAKE_ORG_ID)/"

all:	\
	json-dumps/compute-effective-firewalls-default.json \
	json-dumps/compute-instances-$(ZONE_1).json \
	json-dumps/compute-instances-empty.json \
	json-dumps/compute-disks-$(ZONE_1).json \
	json-dumps/compute-disks-empty.json \
	json-dumps/compute-network-default.json \
	json-dumps/compute-project.json \
	json-dumps/compute-regions.json \
	json-dumps/compute-zones.json \
	json-dumps/iam-policy.json \
	json-dumps/iam-service-accounts.json \
	json-dumps/monitoring-query.json \
	json-dumps/project.json \
	json-dumps/services.json \
	json-dumps/compute-serial-port-output-$(INSTANCE_NAME_GCE1).json \
	json-dumps/compute-serial-port-output-$(INSTANCE_NAME_GCE2).json \
	json-dumps/compute-serial-port-output-$(INSTANCE_NAME_GCE3).json \
	json-dumps/compute-serial-port-output-$(INSTANCE_NAME_GCE4).json \
	json-dumps/global-operations.json

include ../Makefile.inc

define MONITORING_QUERY
{ \
  "query": "fetch gce_instance \
            | metric 'compute.googleapis.com/instance/cpu/utilization' \
            | group_by 5m, [value_utilization_max: max(value.utilization)] \
            | every 5m \
  					" \
}
endef
json-dumps/monitoring-query.json:
	$(CURL) -fsS \
		'https://monitoring.googleapis.com/v3/projects/$(PROJECT_ID)/timeSeries:query' \
		--header "Content-Type: application/json" -X POST \
		--data '$(MONITORING_QUERY)' \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-serial-port-output-%.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/zones/$(ZONE_1)/instances/$*/serialPort?start=-1000000' \
		--header "Content-Type:text/json" \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-serial-port-output-%.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/zones/$(ZONE_1)/instances/$*/serialPort?start=-1000000' \
		--header "Content-Type:text/json" \
		| $(SED_SUBST_FAKE) >$@

json-dumps/compute-serial-port-output-%.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/zones/$(ZONE_1)/instances/$*/serialPort?start=-1000000' \
		--header "Content-Type:text/json" \
		| $(SED_SUBST_FAKE) >$@
json-dumps/compute-serial-port-output-%.json:
	$(CURL) -fsS \
		'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/zones/$(ZONE_1)/instances/$*/serialPort?start=-1000000' \
		--header "Content-Type:text/json" \
		| $(SED_SUBST_FAKE) >$@

json-dumps/global-operations.json:
	$(CURL) -fsS \
	  'https://compute.googleapis.com/compute/v1/projects/$(PROJECT_ID)/aggregated/operations' \
		| $(SED_SUBST_FAKE) >$@
