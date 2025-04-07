---
title: Lessons Learned on Ansible Vault
date: 2025-04-04
tags:
---

Ansible has fair documentation. Many of the docs however focus narrowly on a given command and its functions. While this can be useful to a seasoned user, some, such as {% linkprimary "Ansible's Vault docs", "https://docs.ansible.com/ansible/latest/vault_guide/index.html" %} don't provide the larger context on how a `ansible-vault` encrypted sudo password is incorporated and deployed in a playbook in conjunction with the Ansible vault password. In this post I'm offering a quick write up of my understanding of this context from early in my study of Ansible.

## When Sudo Requires a Password
One of the trickiest parts of getting started with Ansible has been figuring out how Ansible handles a remote host's password prompts for activities requiring sudo privileges. To remedy this, I created an `ansible-vault` file with the sudo password.

The steps weren't complicated, but how they all fit together was unclear. First, I created a file that would store my password, encrypted, with the dedicated Ansible command.
```shell
ansible-vault create <SOME_FILE.yaml>
```

When the command runs it'll prompted me to create an Ansible vault password for use in decrypting the file. I saved that Ansible Vault password somewhere safe.

Then, to take advantage of that stored password when prompted by the remote host during Ansible's run I had to specify path to that password file in a playbook.

Say, for example, I wanted to ensure the correct timezone was set on a remote host. I might create the following task in a playbook. 
```yaml
- name: Set timezone to Los_Angeles
 become: true
 community.general.timezone:
  name: America/Los_Angeles
```

The `become: true` ensures that the task will seek elevated privileges to carry out the timezone change, but it won't have the password for sudo. To add that, I included the following after `become:true`:
```yaml
 {% raw %}
 vars:
  ansible_become_password: "{{ lookup('ansible.builtin.file', '/PATH/TO/SECRET/PASSWORD/FILE.yml') }}"
 {% endraw %}
```

The `ansible_become_password` variable ensured Ansible seeks out the password file I created to complete the sudo password prompt.

Now I was ready to run the playbook. To run the Ansible playbook with that task, I made sure to add `--ask-vault-pass` as a parameter to the `ansible-playbook` command, ensuring Ansible would obtain the Vault password needed decrypt the file containing the sudo password when it reached the task.
