namespace go api

struct UserRegisterRequest {
    1: required string username,
    2: required string password,
}

struct UserRegisterResponse {
    1: required i64 user_id,
    2: required string token,
}

struct UserLoginRequest {
    1: required string username,
    2: required string password,
}

struct UserLoginResponse {
    1: required i64 user_id,
    2: required string token,
}

service UserService {
    UserRegisterResponse UserRegister(1: UserRegisterRequest req) (api.post="/ez-note/api/user/register"),
    UserLoginResponse UserLogin(1: UserLoginRequest req) (api.post="/ez-note/api/user/login"),
}