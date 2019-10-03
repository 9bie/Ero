package novel

import (
	"eroauz/models"
	"eroauz/serializer"
)

type CreateService struct {
	Title       string `json:"title" form:"title"`
	Author      string `json:"author" form:"title"`
	Cover       string `json:"cover" form:"cover"`
	Description string `json:"description" form:"description"`
	result      models.Novel
}

func (service *CreateService) Create(create uint) *serializer.Response {
	u, _ := models.GetUser(create)
	novel := models.Novel{
		Title:       service.Title,
		Author:      service.Author,
		Cover:       service.Cover,
		Description: service.Description,
		Ended:       false,
		Level:       models.Level1,
		Subscribed:  0,
		Create:      u,
	}
	if err := models.DB.Create(&novel).Error; err != nil {
		return &serializer.Response{
			Status: 40007,
			Msg:    "创建失败",
			Error:  err.Error(),
		}
	}

	service.result = novel
	return nil
}
func (service *CreateService) Response() interface{} {
	return serializer.BuildNovelResponse(service.result)
}
