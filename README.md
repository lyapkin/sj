# Auth
В консоль Django выводится письмо для аутентификации, которое содержит код
и ссылку вида http://localhost:3000/confirmation/bmV3QGFzc2Yucmk/Njc5OQ
Последние две части пути - параметры, где первый - email, второй - код.
Оба закодированы base64. Идея в том, что если пользователь переходит по ссылке,
декодировать параметры и отправить POST запросом на соответствующий поинт.
```
/[en || ru]/api/auth/code/ POST (получение кода, выводится в консоль Django)
Request:
{
    "email": "asd@asd.asd"
}

Response:
200 {
    "email": "(отправленная почта)"
}
400 {
    "email": ["Введите правильный адрес электронной почты." ||
              "Это поле не может быть пустым."]
}


/[en || ru]/api/auth/confirmation/ POST (аутентификация/регистрация)
Request:
{
    "email": "(отправленная почта)",
    "code": "1234"
}

Response:
200 {
    "email": "(отправленная почта)",
    "id": 1 (Данные аутентифицированного пользователя)
}
401 {
    "error": "...",
    "recode": true || false (Нужно ли запросить код еще раз.
                             На случай если код был введен неправильно несколько раз
                             или его время жизни закончилось)
}


/[en || ru]/api/auth/check/ GET || POST auth-required
Response:
200 {
    "email": "(отправленная почта)",
    "id": 1 (Данные аутентифицированного пользователя)
}
403 {
    "detail": "Учетные данные не были предоставлены."
}


/[en || ru]/api/auth/logout/ GET auth-required
Response:
200 {
    "success": "Вы успешно вышли из аккаунта."
}
403 {
    "detail": "Учетные данные не были предоставлены."
}
```

Любой POST, PUT, PATCH, DELETE запрос на поинт, где требуется аутентифицированный пользователь
должен содержать X-CSRFToken заголовок.
Его значение храниться в куках, код для его получения:
```
getCookie('csrftoken')

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```


# Catalog

Список категорий
```
/[en || ru]/api/products/categories/ GET
[
    {
        "id": 4,
        "name": "Первая",
        "slug": "pervaia",
        "children": [
            {
                "id": 9,
                "name": "Вторая",
                "slug": "vtoraia",
                "children": [
                    {
                        "id": 11,
                        "name": "Третья",
                        "slug": "tretia",
                        "children": []
                    }
                ]
            },
            {
                "id": 10,
                "name": "Вторая 2",
                "slug": "vtoraia-2",
                "children": [
                    {
                        "id": 16,
                        "name": "Третья 3",
                        "slug": "tretia-3",
                        "children": []
                    }
                ]
            }
        ]
    },
    {
        "id": 12,
        "name": "первая англ",
        "slug": "pervaia-angl",
        "children": [
            {
                "id": 13,
                "name": "Вторая 3",
                "slug": "vtoraia-3",
                "children": []
            },
            {
                "id": 14,
                "name": "Вторая 4 англ",
                "slug": "vtoraia-4-angl",
                "children": [
                    {
                        "id": 15,
                        "name": "Третья 2 англ",
                        "slug": "tretia-2-angl",
                        "children": []
                    }
                ]
            }
        ]
    }
]
```

Список товаров
type = null | {} (null если не переведен)
is_prioritized = true | false (true если надо выделить большим размером в выдаче)
actual_price (цена)
current_price (цена со скидкой)
? - необязательная часть пути
```
/[en || ru]/api/products/catalog/?[category]/?[subcategory]/?[subcategory-2] GET
[
    {
        "id": 13,
        "slug": "produkt-2",
        "name": "Продукт 2",
        "type": {
            "id": 2,
            "name": "Крем",
            "slug": "krem"
        },
        "actual_price": 123,
        "current_price": 123,
        "img_urls": [
            {
                "id": 13,
                "img_url": "/media/images/products/produkt-2/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60_ZUFD0fA.jpg"
            }
        ],
        "is_present": false,
        "is_prioritized": false
    },
    {
        "id": 16,
        "slug": "produkt-5",
        "name": "Продукт 5",
        "type": null,
        "actual_price": 123,
        "current_price": 123,
        "img_urls": [
            {
                "id": 16,
                "img_url": "/media/images/products/produkt-5/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60.jpg"
            }
        ],
        "is_present": false,
        "is_prioritized": false
    }
]
```

