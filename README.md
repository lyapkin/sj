# Auth
В консоль Django выводится письмо для аутентификации, которое содержит код
и ссылку вида http://localhost:3000/confirmation/bmV3QGFzc2Yucmk/Njc5OQ
Последние две части пути - параметры, где первый - email, второй - код.
Оба закодированы base64. Идея в том, что если пользователь переходит по ссылке,
декодировать параметры и отправить POST запросом на соответствующий поинт.
```
/[en || ru]/api/auth/code/ POST (получение кода, выводится в консоль Django)
Request {
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
Request {
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
200 {
    "email": "(отправленная почта)",
    "id": 1 (Данные аутентифицированного пользователя)
}
403 {
    "detail": "Учетные данные не были предоставлены."
}


/[en || ru]/api/auth/logout/ GET auth-required
200 {
    "success": "Вы успешно вышли из аккаунта."
}
403 {
    "detail": "Учетные данные не были предоставлены."
}
```

Любой POST, PUT, PATCH, DELETE запрос на поинт, где требуется аутентифицированный пользователь
должен содержать X-CSRFToken заголовок
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