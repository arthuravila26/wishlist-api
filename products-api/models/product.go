package models

import "gorm.io/gorm"

type Product struct {
	gorm.Model
	Price       float64 `json:"price"`
	Image       string  `json:"image"`
	Brand       string  `json:"brand"`
	Title       string  `json:"title"`
	ReviewScore float64 `json:"reviewScore"`
}
