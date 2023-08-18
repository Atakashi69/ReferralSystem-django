# API для реализации простой реферальной системы

## Документация к API

### Авторизация
Авторизация производится путём использования токена. Вы должны включать токен в заголовки запроса:

`Authorization: Token YOUR_TOKEN`


### Регистрация пользователя
### Запрос

`GET /api/register/`

### Параметры запроса

- `username`: Номер телефона
- `password`: Пароль

### Ответ

Статус код: 200 OK

```jsonc
{
    "message": "Code sent successfully",
    "code": "7553"
}
```


### Подтверждение профиля пользователя
### Запрос

`GET /api/verify/`

### Параметры запроса

- `username`: Номер телефона
- `auth_code`: Код подтверждения

### Ответ

Статус код: 201 Created

```jsonc
{
    "message": "Profile verified",
    "token": "eeee0b5393080729e30360cf5d67ea9dd59d4707",
    "invite_code": "982765"
}
```


### Получение токена пользователя
### Запрос

`GET /api/login/`

### Параметры запроса

- `username`: Номер телефона
- `password`: Код подтверждения

### Ответ

Статус код: 200 OK

```jsonc
{
    "token": "eeee0b5393080729e30360cf5d67ea9dd59d4707"
}
```


### Получение информации о профиле пользователя
### Запрос

`GET /api/profile/`

### Ответ

Статус код: 200 OK

```jsonc
{
    "id": 6,
    "username": "123456789",
    "invite_code": "982765",
    "referral_invite_code": null,
    "referrals": []
}
```

### Ответ при наличии рефералов:
```jsonc
{
    "id": 6,
    "username": "123456789",
    "invite_code": "982765",
    "referral_invite_code": null,
    "referrals": [
        "987654321"
    ]
}
```

### Ответ при активираном реферальном коде:

```jsonc
{
    "id": 7,
    "username": "987654321",
    "invite_code": "7c9959",
    "referral_invite_code": "982765",
    "referrals": []
}
```


### Активирование реферального кода
### Запрос

`GET /api/activate/`

### Параметры запроса

- `invite_code`: Реферальный код

### Ответ

Статус код: 200 OK

```jsonc
{
    "message": "Code activated successfully"
}
```
