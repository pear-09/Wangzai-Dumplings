namespace go user

include "model.thrift"

struct RegisterRequest {
    1: required string username,
    2: required string password,
}

struct RegisterResponse {
    1: required model.BaseResp base,
}

struct LoginRequest {
    1: required string username,
    2: required string password,
}

struct LoginResponse {
    1: required model.BaseResp base,
    2: string token,
}

service UserService {
    RegisterResponse Register(1: RegisterRequest req),
    LoginResponse Login(1: LoginRequest req),
}