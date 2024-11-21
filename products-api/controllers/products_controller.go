package controllers

import (
	"net/http"

	"github.com/arthuravila26/wishlist-api/products-api/database"
	"github.com/arthuravila26/wishlist-api/products-api/models"
	"github.com/gin-gonic/gin"
)

func GetAllProducts(c *gin.Context) {
	var products []models.Product
	database.DB.Find(&products)
	c.JSON(200, products)
}

func CreateNewProduct(c *gin.Context) {
	var product models.Product
	if err := c.ShouldBindJSON(&product); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error()})
		return
	}
	database.DB.Create(&product)
	c.JSON(http.StatusOK, product)
}

func GetProductById(c *gin.Context) {
	var product models.Product
	id := c.Params.ByName("id")
	database.DB.First(&product, id)

	if product.ID == 0 {
		c.JSON(http.StatusNotFound, gin.H{
			"Not found": "Product Not Found"})
		return
	}

	c.JSON(http.StatusOK, product)
}

func DeleteProduct(c *gin.Context) {
	var product models.Product
	id := c.Params.ByName("id")
	database.DB.Delete(&product, id)
	c.JSON(http.StatusOK, gin.H{"data": "Product Deleted"})
}

func UpdateProduct(c *gin.Context) {
	var product models.Product
	id := c.Params.ByName("id")
	database.DB.First(&product, id)

	if err := c.ShouldBindJSON(&product); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error()})
		return
	}

	database.DB.Model(&product).UpdateColumns(product)
	c.JSON(http.StatusOK, product)
}
