package database

import (
	"log"

	"os"

	"github.com/arthuravila26/wishlist-api/products-api/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var (
	DB  *gorm.DB
	err error
)

func DatabaseConection() {
	DB_USER := os.Getenv("DB_USER")
	DB_PASS := os.Getenv("DB_PASS")
	DB_NAME := os.Getenv("DB_NAME")
	DB_HOST := os.Getenv("DB_HOST")
	DB_PORT := os.Getenv("DB_PORT")

	DB_URI := "host=" + DB_HOST + " user=" + DB_USER + " password=" + DB_PASS + " dbname=" + DB_NAME + " port=" + DB_PORT
	DB, err = gorm.Open(postgres.Open(DB_URI))
	if err != nil {
		log.Panic("Database connection failed.")
	}
	DB.AutoMigrate(&models.Product{})
}
