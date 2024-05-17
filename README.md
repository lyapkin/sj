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
    "id": 1 (Данные аутентифицированного пользователя),
    "cart": [
        {
            "id": 15,
            "type": "Маска",
            "name": "Продукт 4",
            "actual_price": 123,
            "current_price": 123,
            "img_url": "/media/images/products/produkt-4/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60.jpg",
            "quantity": 1
        }
    ],
    "favorite_products": [2, 5] (список id)
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
    "id": 1 (Данные аутентифицированного пользователя),
    "cart": [
        {
            "id": 15,
            "type": "Маска",
            "name": "Продукт 4",
            "actual_price": 123,
            "current_price": 123,
            "img_url": "/media/images/products/produkt-4/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60.jpg",
            "quantity": 1
        }
    ],
    "favorite_products": [2, 5] (список id)
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

Список подкатегорий выбранной категории
```
/[en || ru]/api/products/categories/[category]/ GET
{
    "id": 4,
    "name": "Первая",
    "slug": "pervaia",
    "children": [
        {
            "id": 9,
            "name": "Вторая",
            "slug": "vtoraia"
        },
        {
            "id": 10,
            "name": "Вторая 2",
            "slug": "vtoraia-2"
        }
    ]
}
```

Список товаров
type = null | {} (null если не переведен)
is_prioritized = true | false (true если надо выделить большим размером в выдаче)
actual_price (цена)
current_price (цена со скидкой)
? - необязательная часть пути
```
/[en || ru]/api/products/catalog/?[category]/?[subcategory]/?[subcategory-2]/ GET
{
    "count": 3,
    "next": "http://localhost:8000/ru/api/products/catalog/pervaia-angl/?page=2",
    "previous": null,
    "results": [
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
            "id": 14,
            "slug": "produkt-3",
            "name": "Продукт 3",
            "type": null,
            "actual_price": 123,
            "current_price": 123,
            "img_urls": [
                {
                    "id": 14,
                    "img_url": "/media/images/products/produkt-3/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60_4h5bxW5.jpg"
                }
            ],
            "is_present": false,
            "is_prioritized": false
        }
    ],
    "section": {
        "id": 12,
        "name": "первая англ",
        "slug": "pervaia-angl"
    }
}
```

Один продукт
```
/[en || ru]/api/products/item/[slug]/ GET
{
    "id": 12,
    "slug": "produkt-1",
    "type": "Маска",
    "name": "Продукт 1",
    "code": "123",
    "brand": "Бренд 1",
    "brand_country": "Россия",
    "description": "123",
    "is_present": false,
    "actual_price": 123,
    "current_price": 123,
    "charachteristics": [
        {
            "id": 1,
            "charachteristic_key": "Для кого",
            "value": "Мужчин"
        },
        {
            "id": 3,
            "charachteristic_key": "Применение",
            "value": "Лицо"
        }
    ],
    "img_urls": [
        {
            "id": 12,
            "img_url": "http://localhost:8000/media/images/products/produkt-1/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60_qXvjRZV.jpg"
        }
    ]
}
```

Список фильтров
```
/[en || ru]/api/products/filters/ GET
{
    "filters": [
        {
            "title": "product_type",
            "request_key": "product-type",
            "id": -3,
            "values": [
                {
                    "id": 1,
                    "name": "Маска",
                    "slug": "maska"
                },
                {
                    "id": 2,
                    "name": "Крем",
                    "slug": "krem"
                },
                {
                    "id": 3,
                    "name": "Шампунь",
                    "slug": "shampun"
                }
            ]
        },
        {
            "title": "brand",
            "request_key": "brand",
            "id": -2,
            "values": [
                {
                    "id": 1,
                    "name": "Бренд 1",
                    "slug": "brand-1"
                },
                {
                    "id": 2,
                    "name": "Бренд 2",
                    "slug": "brand-2"
                },
                {
                    "id": 3,
                    "name": "Бренд 3",
                    "slug": "brand-3"
                },
                {
                    "id": 4,
                    "name": "Бренд 4",
                    "slug": "brand-4"
                },
                {
                    "id": 5,
                    "name": "Бренд 5",
                    "slug": "brand-5"
                }
            ]
        },
        {
            "title": "brand_country",
            "request_key": "brand-country",
            "id": -1,
            "values": [
                {
                    "id": 1,
                    "name": "Россия",
                    "slug": "russia"
                },
                {
                    "id": 2,
                    "name": "Англия",
                    "slug": "england"
                },
                {
                    "id": 3,
                    "name": "Белорусь",
                    "slug": "belarus"
                }
            ]
        },
        {
            "title": "Для кого",
            "request_key": "dlia-kogo",
            "id": 1,
            "values": [
                {
                    "id": 1,
                    "slug": "muzhchin",
                    "name": "Мужчин"
                },
                {
                    "id": 2,
                    "slug": "zhknshchin",
                    "name": "Женщин"
                }
            ]
        },
        {
            "title": "Применение",
            "request_key": "priminenie",
            "id": 2,
            "values": [
                {
                    "id": 3,
                    "slug": "litso",
                    "name": "Лицо"
                },
                {
                    "id": 4,
                    "slug": "ruki",
                    "name": "Руки"
                }
            ]
        }
    ],
    "other_filter_keys": [
        "price-max",
        "price-min",
        "is_present",
        "discount"
    ],
    "sort": [
        {
            "id": 1,
            "slug": "relevance",
            "value": "relevance"
        },
        {
            "id": 2,
            "slug": "popularity",
            "value": "popularity"
        },
        {
            "id": 3,
            "slug": "price-up",
            "value": "price_up"
        },
        {
            "id": 1,
            "slug": "price-down",
            "value": "price_down"
        }
    ]
}
```

Фильтрация
sort=... - сортировка
is_present=1 - в наличии
is_present=0 - под заказ
discount=1 - скидки
price-min=... - нижний порог цены
price-max=... - верхний порог цены
Сортировка по популярности пока не работает
Сортировка по релевантности - от вновь добавленных к добавленным давно
```
/[ru | en]/api/products/catalog/[category]?dlia-kogo=muzhchin&dlia-kogo=zhknshchin&sort=price-up&sort=price-up
```

# Бренды

Список брендов
```
/[ru | en]/api/products/brands/
{
    "A": [
        {
            "id": 6,
            "name": "Alfa-brand",
            "slug": "alfa-brand"
        }
    ],
    "B": [
        {
            "id": 1,
            "name": "Brand 1",
            "slug": "brand-1"
        },
        {
            "id": 4,
            "name": "Brand 4",
            "slug": "brand-4"
        },
        {
            "id": 5,
            "name": "Brand 5",
            "slug": "brand-5"
        }
    ]
}
```

Список товаров
type = null | {} (null если не переведен)
is_prioritized = true | false (true если надо выделить большим размером в выдаче)
actual_price (цена)
current_price (цена со скидкой)
? - необязательная часть пути
```
/[en || ru]/api/products/brands/[brand-slug]/ GET
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 16,
            "slug": "produkt-5",
            "name": "Продукт 5",
            "type": {
                "id": 3,
                "name": "Шампунь",
                "slug": "shampun"
            },
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
        },
        {
            "id": 12,
            "slug": "produkt-1",
            "name": "Продукт 1",
            "type": {
                "id": 1,
                "name": "Маска",
                "slug": "maska"
            },
            "actual_price": 123,
            "current_price": 123,
            "img_urls": [
                {
                    "id": 12,
                    "img_url": "/media/images/products/produkt-1/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60_qXvjRZV.jpg"
                },
                {
                    "id": 17,
                    "img_url": "/media/images/products/produkt-1/1.png"
                }
            ],
            "is_present": false,
            "is_prioritized": false
        }
    ],
    "section": {
        "id": 1,
        "name": "Бренд 1",
        "slug": "brand-1"
    }
}
```


# Поиск
```
/[ru | en]/api/products/search?q=еть
{
    "products": [],
    "categories": [
        {
            "id": 11,
            "name": "Первая / Вторая / Третья",
            "slug": "tretia"
        },
        {
            "id": 15,
            "name": "первая англ / Вторая 4 англ / Третья 2 англ",
            "slug": "tretia-2-angl"
        },
        {
            "id": 16,
            "name": "Первая / Вторая 2 / Третья 3",
            "slug": "tretia-3"
        }
    ],
    "brands": []
}
```


# Избранные продукты

Добавление продукта в избранное
```
/[ru | en]/api/products/favorite-products/ POST auth-required csrf-token

Request:
{
    "id": 16 (id товара)
}

Response:
201 {
    "product": 16,
    "user": 1
}
```

Список избранных продуктов
```
/[ru | en]/api/products/favorite-products/ GET auth-required
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 16,
            "slug": "produkt-5",
            "name": "Продукт 5",
            "type": {
                "id": 3,
                "name": "Шампунь",
                "slug": "shampun"
            },
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
}
```

Удаление продукта из избранного
```
/[ru | en]/api/products/favorite-products/16/ DELETE
Response 204
```


# Избранные бренды

Добавление бренда в избранное
```
/[ru | en]/api/products/favorite-brands/ POST auth-required csrf-token

Request:
{
    "id": 1 (id бренд)
}

Response:
201 {
    "brand": 1,
    "user": 1
}
```

Список избранных брендов
```
/[ru | en]/api/products/favorite-brands/ GET auth-required
[
    {
        "id": 1,
        "name": "Бренд 1",
        "slug": "brand-1"
    }
]
```

Удаление бренда из избранного
```
/[ru | en]/api/products/favorite-brands/1/ DELETE
Response 204
```


# Документация 
```
/[ru | en]/api/docs/ GET
[
    {
        "id": 1,
        "name": "Документ 1",
        "sections": [
            {
                "id": 1,
                "title": "Раздел 1",
                "content": "<p>Текст 1</p>"
            },
            {
                "id": 2,
                "title": "Раздел 2",
                "content": "<p>Текст 2</p>"
            }
        ]
    },
    {
        "id": 2,
        "name": "Документ 2",
        "sections": [
            {
                "id": 3,
                "title": "Раздел 1",
                "content": "<p>Текст 1</p>"
            },
            {
                "id": 4,
                "title": "Раздел 2",
                "content": "<p>Текст 2</p>"
            }
        ]
    }
]
```


# FAQ
```
/[ru | en]/api/faq/ GET
[
    {
        "id": 1,
        "name": "Категория 1",
        "faqs": [
            {
                "id": 1,
                "question": "Вопрос 1",
                "answer": "<p>Ответ 1</p>"
            },
            {
                "id": 2,
                "question": "Вопрос 2",
                "answer": "<p>Ответ 2</p>"
            }
        ]
    },
    {
        "id": 2,
        "name": "Категория 2",
        "faqs": [
            {
                "id": 3,
                "question": "Вопрос 3",
                "answer": "<p>Ответ 3</p>"
            },
            {
                "id": 4,
                "question": "Вопрос 4",
                "answer": "<p>Ответ 4</p>"
            }
        ]
    }
]
```


# Корзина

Тело ответа для всех запросов - корзина для данного пользователя (массив с данными, либо пустой)
```
[
    {
        "id": 16,
        "type": "Shampoo",
        "name": "Продукт 5",
        "actual_price": 123,
        "current_price": 123,
        "img_url": "/media/images/products/produkt-5/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60.jpg",
        "quantity": 1
    },
    {
        "id": 15,
        "type": "Mask",
        "name": "Продукт 4",
        "actual_price": 123,
        "current_price": 123,
        "img_url": "/media/images/products/produkt-4/1%D0%93%D0%B0%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B9_%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%B8_%D1%81_%D1%80%D1%83%D1%87%D0%BA%D0%BE%D0%B9_%D0%BE%D1%86%D0%B8%D0%BD%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_D60.jpg",
        "quantity": 1
    }
]
```

Добавление товара в корзину/Обновление количества товара в корзине
```
/[ru | en]/api/cart/ POST auth-required csrf-token
Request:
{
    "id": 16, (id продукта)
    "quantity": 1 (количество)
}

Response status: 200 | 201
```

Удаление единицы товара из корзины
```
/[ru | en]/api/cart/[product_id]/ DELETE auth-required csrf-token

Response status: 204
```

Очистка корзины
```
/[ru | en]/api/cart/clean/ DELETE auth-required csrf-token

Response status: 204
```


# Слайдер, табы на главной
slides - первый экран (три типа: 'category', 'brand', 'product')
tabs - под первы экраном (два типа: 'category', 'brand')
modules - над футером (два типа: 'category', 'brand')
```
/[ru | en]/api/links/ GET
{
    "slides": [
        {
            "id": 15,
            "title": "заголовок2",
            "text": "текст",
            "button_text": "текст ссылки2",
            "type": "category",
            "link": "pervaia-angl/",
            "img": "/media/images/links/slider/2024/05/17/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2024-05-16_103633_e4uNMDz.png"
        },
        {
            "id": 14,
            "title": "заголовок",
            "text": "текст",
            "button_text": "текст ссылки",
            "type": "product",
            "link": "produkt-1/",
            "img": "/media/images/links/slider/2024/05/17/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2024-05-16_103633.png"
        }
    ],
    "tabs": [
        {
            "id": 1,
            "title": "заголовок",
            "type": "category",
            "link": "pervaia/vtoraia/?sort=popularity",
            "img": "/media/images/links/tab/2024/05/17/Card.png",
            "background": "/media/images/links/tab/2024/05/17/background/Card.jpg"
        },
        {
            "id": 2,
            "title": "заголовок2",
            "type": "category",
            "link": "pervaia-angl/vtoraia-4-angl/tretia-2-angl/?sort=popularity",
            "img": "/media/images/links/tab/2024/05/17/Card_WGwLJkq.png",
            "background": "/media/images/links/tab/2024/05/17/background/Card_Ne1KQci.jpg"
        },
        {
            "id": 3,
            "title": "заголовок3",
            "type": "category",
            "link": "pervaia/vtoraia-2/?sort=popularity",
            "img": "/media/images/links/tab/2024/05/17/Card_yj1fZO2.png",
            "background": "/media/images/links/tab/2024/05/17/background/Card_tt9lFPD.jpg"
        },
        {
            "id": 4,
            "title": "заголовок4",
            "type": "category",
            "link": "pervaia/?sort=popularity",
            "img": "/media/images/links/tab/2024/05/17/Card_nJcErWB.png",
            "background": "/media/images/links/tab/2024/05/17/background/Card_xGoJNry.jpg"
        }
    ],
    "modules": [
        {
            "id": 1,
            "title": "Заголовок",
            "text": "текст",
            "button_text": "текст ссылки",
            "type": "category",
            "link": "pervaia-angl/",
            "img": "/media/images/links/module/2024/05/17/Card.png",
            "background": "/media/images/links/module/2024/05/17/background/Card.jpg"
        },
        {
            "id": 2,
            "title": "заголовок2",
            "text": "текст",
            "button_text": "текст ссылки",
            "type": "brand",
            "link": "brand-2/",
            "img": "/media/images/links/module/2024/05/17/Card_BnU2xB8.png",
            "background": "/media/images/links/module/2024/05/17/background/Card_iIOSnVi.jpg"
        }
    ]
}
```