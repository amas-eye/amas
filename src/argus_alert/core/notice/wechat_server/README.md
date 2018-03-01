### Wechat Server for Argus alert module

## Api specification

The wechat service is seperated 2 parts:
1. The controller api
2. The official account application logic

# To Controll the OA
```GET: /controller/create_qrcode```
Query Parametric:
	username
	expire_seconds

```POST: /controller/push_alert```
Data:
	json formatted push content

```GET: /controller/delete_menus```

```GET: /controller/query_menus```

```POST: /controller/create_menu```
Data:
	json formatted menu data
