package main

import (
	template "ez-note/kitex_gen/template/templateservice"
	"log"
)

func main() {
	svr := template.NewServer(new(TemplateServiceImpl))

	err := svr.Run()

	if err != nil {
		log.Println(err.Error())
	}
}
