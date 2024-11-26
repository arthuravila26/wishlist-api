FROM golang:1.23.3-alpine

WORKDIR /app

COPY products-api/go.mod products-api/go.sum ./

RUN go mod tidy

COPY products-api/ .

EXPOSE 8080

CMD ["go", "run", "main.go"]