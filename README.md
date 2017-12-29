# wazo-auth-cli
A command line interface for the wazo-auth service

## Configuration

Configuration file can be added at the following locations:

```
~/.config/wazo-auth-cli/*.yml
/etc/wazo-auth-cli/conf.d/*.yml
/etc/wazo-auth-cli/config.yml
```

The `/etc/wazo-auth-cli/config.yml` is the default configuration file shipped with the debian package. This file should not be modified but can be used as a reference.

The `/etc/wazo-auth-cli/conf.d/*.yml` files will be used to override the default configuration file. System-wide configurations should be dropped in this directory.

The `~/.config/wazo-auth-cli/*.yml` files will be used to override the global configuration files for a given user. This directory will generally include files containing credentials.

The user's configuration file directory are not read automatically at the moment. wazo-auth-cli can be launched using the --config option to read this directory.

```sh
wazo-auth-cli --config ~/.config/wazo-auth-cli
```

The `WAZO_AUTH_CLI_CONFIG` environment variable can also be used to avoid having to use the `--config` option.

```sh
export WAZO_AUTH_CLI_CONFIG=~/.config/wazo-auth-cli
```

This line can also be added to the user's `~/.bashrc` to avoid typing it at each session

A credential files should be created for the root user when wazo-auth is installed

```sh
# cat ~/.config/wazo-auth-cli/050-credentials.yml
auth:
  username: wazo-auth-cli
  password: uwt1V5GILaJ6tFEZZzFM
  backend: wazo_user
```

If a similar file does not exists it can be recreated with the following commands:

```sh
wazo-auth-bootstrap setup
systemctl restart wazo-auth
```


## Commands

### Users

Creating a new user

```sh
wazo-auth-cli --hostname mywazo --insecure --auth-username test --auth-password test --backend xivo_service user create --passwd baz --email "baz@example.com" baz
```

Listing users

```sh
wazo-auth-cli --hostname mywazo --insecure --auth-username test --auth-password test --backend xivo_service user list
```

Deleting a user

```sh
wazo-auth-cli --hostname mywazo --insecure --auth-username test --auth-password test --backend xivo_service user delete <uuid> 
```

### Policies

Creating a policy

```sh
wazo-auth-cli --hostname mywazo --insecure --auth-username test --auth-password test --backend xivo_service policy create --acl "auth.users.*.read" "auth.users.create" -- mypolicy
```
