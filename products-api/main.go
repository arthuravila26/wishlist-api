package main

import (
	"github.com/arthuravila26/wishlist-api/products-api/database"
	"github.com/arthuravila26/wishlist-api/products-api/routes"
)

func main() {
	database.DatabaseConection()
	routes.HandleRequests()
}
