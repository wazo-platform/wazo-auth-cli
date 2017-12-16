# wazo-auth-cli
A command line interface for the wazo-auth service


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
