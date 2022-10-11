<p align="center">
  <img src="https://raw.githubusercontent.com/bali-framework/bali/master/docs/img/bali.png" alt='bali framework' />
</p>

<p align="center">
    <b>bali-cli</b> is 
    CLI tools to simplify gRPC services and clients
</p>

# bali-cli

<img src="https://img.shields.io/pypi/v/bali-cli" />

CLI tools to simplify gRPC services and clients


## Cli commands 

- `bali add`
> Add service to clients folder, syntax is **bali add {service}**
```bash
# Example: added a service named `user`
bali add user
```

- `bali build`
> Build current development service protobuf 
>
> Legacy protobuf path: <b>/services/rpc/*.proto</b>
> New protobuf path: <b>*/protos/*.proto*</b>
```bash
# Example: build in a service root directory
bali build
```

- `bali run`
> New in `2.5.0`
> 
> Start Bali App service, include `http`/`rpc`/`event`
```bash
# Example: start http
bali run http
# Example: start rpc
bali run rpc
# Example: start event
bali run event
```

- `bali shell`
> New in `2.5.0`
> 
```bash
# Enter Bali App shell
bali shell
```

## Related Projects

[![bali](https://github-readme-stats.vercel.app/api/pin/?username=bali-framework&repo=bali)](https://github.com/bali-framework/bali)


## CONTRIBUTE

**Developer Environment**

```bash
make init
``` 

```examples
# setup examples environments
git submodule update --init --recursive

# execute bali commands 
# cd examples/gateway_service && bali add greeter
```


**Tag a new release**

tag a version:

```bash
git tag -a v0.1.0
```

push tags to remote:

```bash
git push --tags
```

**Get a test report**
```bash
make test
``` 
