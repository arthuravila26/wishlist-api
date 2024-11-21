package database

import (
	"log"

	"github.com/arthuravila26/wishlist-api/products-api/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var (
	DB  *gorm.DB
	err error
)

func DatabaseConection() {
	DB_URI := "host=localhost user=postgres password=postgres dbname=postgres port=5432"
	DB, err = gorm.Open(postgres.Open(DB_URI))
	if err != nil {
		log.Panic("Database connection failed.")
	}
	DB.AutoMigrate(&models.Product{})
}
