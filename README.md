# bali-cli
CLI tools to simplify gRPC services and clients


## Cli commands 

**bali add {service}**

> Add service to clients folder 

**bali build**

> Build current development service protobuf 
>
> Protobuf Path: /services/rpc/*.proto 

## Related Projects

[![bali](https://github-readme-stats.vercel.app/api/pin/?username=JoshYuJump&repo=bali)](https://github.com/JoshYuJump/bali)


## CONTRIBUTE

**Developer Environment**

```bash
make init
``` 

```examples
# setup examples environments
cd examples && git clone https://github.com/JoshYuJump/bali-cli-example-proto proto

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
