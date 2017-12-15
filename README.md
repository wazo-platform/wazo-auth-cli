# wazo-auth-cli
A command line interface for the wazo-auth service


## Commands

### Users

Creating a new user

```sh
wazo-auth-cli --verbose --hostname mywazo --port 9497 --verify false --username test --password test --backend xivo_service user create --passwd baz --email "baz@example.com" baz
```
