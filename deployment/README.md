# Deployment Ansible playbooks

Here is a set of [Ansible playbooks](https://www.ansible.com/) to provision,
install and update the project.


## Quickstart

Use `./hosts.example` as a blueprint for an [Ansible inventory
file](http://docs.ansible.com/ansible/intro_inventory.html). You can edit the
`/etc/ansible/hosts` file (Ansible default) or create a local `hosts` file and
reference it with the `-i` option.

Make sure your ssh public key is uploaded on every server you try to run a task
on.

Configure the servers and install the project on staging:

    ansible-playbook -i hosts -l staging site.yml

To deploy on production:

    ansible-playbook -i hosts -l production site.yml


## Playbooks

We tried to structure playbooks according to [Ansible's best
practices](http://docs.ansible.com/ansible/playbooks_best_practices.html),
splitting top-level playbooks into roles.

The top level playbook is `site.yml`. Running this playbook will entirely
configure the server and install the project on it. Check the file content to
see what top-level playbooks are available.


## Delivering different versions to different environments

What if you to run instances with different versions, e.g you want master
deployed in staging, and a specific tag in production? Simply define different
groups in your inventory, create a `/etc/ansible/group_vars/<group>.yml`, and
give the `project_version` variable the git commit name you want to fetch (can
be a branch or a tag).

You can also install additional applications using the `document_apps`
variable.

In `/etc/ansible/hosts`:

    [staging]
    staging.project.com

    [production]
    production.project.com

In `/etc/ansible/group_vars/staging.yml`:

    project_version: master

`project_version`'s default value is `master`.


## Local configuration

### SSH Config

Here is a sample `~/.ssh/config`:

    # Physical host
    Host myserver
        HostName myserver.com
        User root

    # The production instance on a LXC virtual machine and a public ip
    Host www.myserver.com
        HostName 1.2.3.4
        User root
        ForwardAgent yes

    # The staging instance on a LXC virtual machine and a local ip only
    Host staging.myserver.com
        User root
        ProxyCommand ssh myserver nc lxc_staging_machine_name 22
        ForwardAgent yes
