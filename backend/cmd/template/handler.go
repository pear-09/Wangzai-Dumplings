package main

import (
	"context"
	template "ez-note/kitex_gen/template"
)

// TemplateServiceImpl implements the last service interface defined in the IDL.
type TemplateServiceImpl struct{}

// Ping implements the TemplateServiceImpl interface.
func (s *TemplateServiceImpl) Ping(ctx context.Context, req *template.PingRequest) (resp *template.PingResponse, err error) {
	// TODO: Your code here...
	return
}
