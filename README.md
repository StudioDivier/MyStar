**My Star**

*End-points*

* http://192.168.1.131:8080/login/ - логин

response: 

    201

* http://192.168.1.131:8080/registration/ - регистрация пользователя

response: 

    201

* http://192.168.1.131:8080/categories/ - GET категории

response: 

    201

* http://192.168.1.131:8080/star/create/- регистрация звезды

response: 

    201

* http://192.168.1.131:8080/star/getlist/ - список всех звезд

response: 

    201

* http://192.168.1.131:8080/star/id/ - [GET] звезду по id

request:

    {
        "star_id" : "3"
    }

response:

    {
        "username": "zemfira",
        "phone": 9787896546,
        "email": "zemfira@star.com",
        "price": "15000.00",
        "cat_name_id": 2,
        "rating": 2,
        "is_star": true
    }

* http://192.168.1.131:8080/star/category/ - [GET] звезд по id категории

request:

    {
        "cat_name_id": "1"
    }

response:

    [
        {
            "username": "niletto",
            "phone": 9787892356,
            "email": "niletto@star.com",
            "price": "15000.00",
            "cat_name_id": 1,
            "rating": 2,
            "is_star": true
        }
    ]

* http://192.168.1.131:8080/ratestar/ - [PUT] проголосовать за звезду

request:

    {
        "rating": "1",
        "adresat": 1,
        "adresant": 3
    }

response: 

    201

* http://192.168.1.131:8080/order/ - [POST] сделать заказ

request:

    {
        "customer_id": "1",
        "star_id": "3",
        "order_price": "4000.00",
        "for_whom": "Для Мамы",
        "comment": "Хочу поздравить маму с днем рождения",
        "status_order": "0"
    }

response: 

    201


* http://192.168.1.131:8080/orderaccept/ - [POST] звезда принимает/отклоняет заказ

request:

    {
        "order_id" : "5",
        "accept": "accept"
    }

response: 

    201

* http://192.168.1.131:8080/personal/ - лк для звезды и заказчика

request:

    {
        "user_id": "1",
        "is_star": 0
    }

response:

    [
        {
            "username": "myname",
            "phone": 9941622229,
            "email": "poor@test.com",
            "date_of_birth": "1999-08-05",
            "is_star": false
        },
        {
            "orders": [
                {
                    "customer_id": 1,
                    "star_id": 3,
                    "payment_id": "",
                    "order_price": "4000.00",
                    "ordering_time": "2020-09-23T06:34:49.397971Z",
                    "for_whom": "Для Мамы",
                    "comment": "Хочу поздравить маму с днем рождения",
                    "status_order": 0
                },
                {
                    "customer_id": 1,
                    "star_id": 3,
                    "payment_id": "28153142-0a0c-47cd-b253-01e337034a69",
                    "order_price": "4000.00",
                    "ordering_time": "2020-09-22T13:45:05.643858Z",
                    "for_whom": "Для Мамы",
                    "comment": "Хочу поздравить маму с днем рождения",
                    "status_order": 1
                },
                {
                    "customer_id": 1,
                    "star_id": 2,
                    "payment_id": "",
                    "order_price": "15000.00",
                    "ordering_time": "2020-09-22T13:22:17.143066Z",
                    "for_whom": "Для Мамы",
                    "comment": "Хочу поздравить маму с днем рождения",
                    "status_order": -1
                }
            ]
        }
    ]

