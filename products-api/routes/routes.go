package routes

import (
	"github.com/arthuravila26/wishlist-api/products-api/controllers"
	"github.com/gin-gonic/gin"
)

func HandleRequests() {
	r := gin.Default()
	r.GET("/products", controllers.GetAllProducts)
	r.POST("/product", controllers.CreateNewProduct)
	r.GET("/product/:id", controllers.GetProductById)
	r.DELETE("/product/:id", controllers.DeleteProduct)
	r.PATCH("/product/:id", controllers.UpdateProduct)
	r.Run()
}
