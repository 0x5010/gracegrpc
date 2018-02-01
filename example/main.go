/*
 *
 * modified from grpc-go/examples/helloworld/greeter_server/main.go
 *
 */

package main

import (
	"log"

	"github.com/0x5010/gracegrpc" // import
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	pb "google.golang.org/grpc/examples/helloworld/helloworld"
	"google.golang.org/grpc/reflection"
)

const (
	port = ":50051"
)

type server struct{}

func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
	return &pb.HelloReply{Message: "Hello " + in.Name}, nil
}

func main() {
	// lis, err := net.Listen("tcp", port)
	// if err != nil {
	// 	log.Fatalf("failed to listen: %v", err)
	// }
	// s := grpc.NewServer()
	// pb.RegisterGreeterServer(s, &server{})
	// // Register reflection service on gRPC server.
	// reflection.Register(s)
	// if err := s.Serve(lis); err != nil {
	// 	log.Fatalf("failed to serve: %v", err)
	// }

	pidPath := "example.pid"
	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})
	reflection.Register(s)
	gr, err := gracegrpc.New(s, "tcp", port, pidPath, nil)
	if err != nil {
		log.Fatalf("failed to new gracegrpc: %v", err)
	}
	if err := gr.Serve(); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
