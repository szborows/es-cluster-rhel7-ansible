# es-cluster-rhel7-ansible-eucalyptus

simple ES setup - I didn't know that there is elasticsearch role on GitHub already - tailored for proxied
environments.

it's far from perfect, but it works.

Assuming asg_name (autoscaling group name in Eucalyptus), Eucalyptus credentials stored under
`~/euca_creds/` and private key under `~/cloud_key.pem`, run:

`./scripts/create_inventory.py ~/euca_creds/eucarc asg_name master:1,es:7 > inventory`

`ansible-playbook -i inventory.es --private-key ~/cloud_key.pem site.yml --forks=8`

And, you're done ;-) ES should listen on `head -n 2 inventory | tail -n 1`

TODO:
 - finish prometheus setup
 - ELK stack for logging
 - logspout deployment
