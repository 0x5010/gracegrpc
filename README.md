gracegrpc is used to wrap a grpc server that can be gracefully terminated & restarted.

[![LICENSE](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Build Status](https://travis-ci.org/0x5010/gracegrpc.png?branch=master)](https://travis-ci.org/0x5010/gracegrpc)
[![Go Report Card](https://goreportcard.com/badge/github.com/0x5010/gracegrpc)](https://goreportcard.com/report/github.com/0x5010/gracegrpc)

Installation
-----------

	go get github.com/0x5010/gracegrpc

Usage
-----------

Wrap grpc server and start server:
```go
s := grpc.NewServer()
pb.RegisterDeployServer(s, &server{})
reflection.Register(s)
gr, err := gracegrpc.New(s, "tcp", addr, pidPath, nil)
if err != nil {
	log.Fatalf("failed to new gracegrpc: %v", err)
}
if err := gr.Serve(); err != nil {
	log.Fatalf("failed to serve: %v", err)
}

```

Custom logger
```go
import log "github.com/sirupsen/logrus"

...
gr, err := gracegrpc.New(s, "tcp", addr, pidPath, log.StandardLogger())
...
```

In a terminal trigger a graceful server restart (using the pid from your output):
```bash
kill -USR2 pid
```


