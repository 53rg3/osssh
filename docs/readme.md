# How to install

1. Clone the repo

2. Configure `config.yml` and set up `pathToOpenStackProjectsYamlFile` to the file on your system.

3. Install via `pip3 install .`

4. Put a link to `osssh.py` into `$PATH` (maybe you'll need a `chmod +x` as well), e.g. 

   ```
   chmod +x /home/james/Desktop/osssh/osssh.py
   sudo ln -s /home/james/Desktop/osssh/osssh.py /usr/local/bin/osssh
   ```

5. Execute `osssh --update` to load the list of instances into the cache



# How to update the cache

`osssh` caches the list of instances from `openstack server list` in `.cache/`. Every time you fail to find or connect to a desired instance it means that the cache is outdated. Just run `osssh --update` again and download the list of instances of the desired OpenStack project.



# Example for os_projects.yml

Credentials for the OpenStack projects are sourced from a file configured in `config.yml`. The file must be a list of objects. You can store multiple OpenStack projects there. 

The credentials for OpenStack must be set up in `env`, the rest is meta data for establishing the SSH & SCP connections.

Meta data:

- `targetUser`: SSH user on the target machine
- `pathToSshKey`: SSH key for the target machine & the jump host
- `userAtJumpHost`: The user@someIP of the jump host
- `allowSelfSignedCert`: This will use `openstack --insecure server list`

Example:

```yaml
- id: prod1
  targetUser: james
  pathToSshKey: /home/cc/.osssh/prod1-key 
  userAtJumpHost: james@172.11.0.1

  env:
    OS_USERNAME: prod1_user
    OS_PROJECT_ID: 7bb91610aa7b40bcad3bf2a144fd5bfe
    OS_PASSWORD: e61c77926a1e0a7bf59f7ee6369c7299af3c00b2
    OS_AUTH_URL: https://openstack-prod1.cool-company.com:5000/v3
    OS_USER_DOMAIN_NAME: production
    OS_CACERT: ""


- id: int1
  targetUser: james
  pathToSshKey: /home/cc/.osssh/int1-key 
  userAtJumpHost: james@172.12.0.1
  allowSelfSignedCert: true

  env:
    OS_USERNAME: int1_user
    OS_PROJECT_ID: e1daa34506f14462a29ddfaa19247005
    OS_PASSWORD: 561ebcceca45d53a626942c3e5e344f70bb5b1a8
    OS_AUTH_URL: https://openstack-int1.cool-company.com:5000/v3
    OS_USER_DOMAIN_NAME: testing
    OS_CACERT: ""
```



# Potential improvements

- [ ] Make `osssh` usable for automation.

  - Currently no values can be passed as arguments. So a Jenkins couldn't run it. This will get tricky due to instance selection process. E.g. you need to pass the instance name that it is unique.

  - What would be possible is if you would introduce options like `--match-all` & `--match-any` which selects matching instances from the `InstanceIndex` and instead of executing it just outputs the SSH or SCP terminal commands so that you feed into something that actually executes them. This would allow parallelization. Or you could just pipe the results to `xargs`, e.g.

    ```
    osssh --match-all elastic-\d+,10.0.99.0/24 | xargs -I {} "echo {}"
    ```

  - When providing parameters then it might make sense just to use them as overrides. I.e. no prompts will be provided if requirements are fulfilled and if an argument conflicts with something from the `os_projects.yml` then it will be just overridden by the argument.

- [ ] Allow to execute remote commands

  Without automation capabilities this wouldn't make sense, but if you could pass values as arguments then it would be sense to be able to execute a command (or Bash script file) on multiple machines at once.

- [ ] When selecting the jump host as instance, then `osssh` connects to the jump host over the jump host. It works, but...

- [ ] Add support for different authentication mechanism

  Currently only SSH keys work. `osssh` won't even work if they're left out.

- [ ] Delete cache if a OpenStack project is removed from `os_projects.yml`. 

  Not really important. If a project is removed then it will also not get loaded into the `InstanceIndex`. So all cool.

- [ ] Add `--debug` flag

  Won't execute anything but exit after displaying the command it wants to use.

- [ ] Add support for ports

  Currently only the default port 22 will be used.

