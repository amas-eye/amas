#API DOC

	Hint:
		PLEASE USE /api/stats FIRST TO CHECK OUT THE NEWEST STATUS CODE.
		defaut offset=0 limit=12, only suppport  positive integer currently.
		using "^$" as tags delimiter i.e. "tags": "tag1^$tag2".
		does not support canoncial urls so no trailing slash "/".
---

#Endpoint1

	/api/collector/metric?limit=***&offset=***
	VERB:
		GET & POST

	GET /api/collector/metric?offset=2&limit=10 HTTP/1.1
	RESPONSE: 
	1. ok
	{
    	"code": 0,
    	"data": [
        	{
            	"description": null,
            	"last_update": -1,
            	"metric_name": "aaa.day.test.A",
            	"tags": null
        	},
        	{
            	"description": null,
            	"last_update": -1,
            	"metric_name": "net.stat.tcp.invalid_sack",
            	"tags": null
        	},
			...
    		]
	}
	2.db error 
	{
		"code": 1002 (db error),
		"msg": "error detail"

	}


	POST /api/collector/metric
	BODY:
	1.a dict
	{
		"metric_name": "???",
		"description": "???",
		"tags": "???"
	}
	2.a list	
	[
		{
			"metric_name": "???",
			"description": "???",
			"tags": "???"
		},
		{
			"metric_name": "???",
			"description": "???",
			"tags": "???"
		}
		...
	]
	Response:
	1.if everyting goes right your will get:
	{
    	"code": 2000,
    	"refused": 0,
    	"refused_list": [],
    	"unknown": 0,
    	"unknown_list": [],
    	"updated": 3
	}
	2.or one of your json missing some field such as tags
	{
    	"code": 3000,
    	"refused": 1,
    	"refused_list": [
        	{
            	"description": "cli count 2",
            	"metric_name": "dns_day_count"
        	}
    	],
    	"unknown": 0,
    	"unknown_list": [],
    	"updated": 2
	}
	3.or the metric_names you postd does not existed in db, deleted? you miss constructed? ...
	{
    	"code": 3000, 
    	"refused": 0, 
    	"refused_list": [], 
    	"unknown": 1, 
    	"unknown_list": [
        	{
            	"description": "cli count 2", 
            	"metric_name": "dns_day_sizeX", 
            	"tags": "dns size 3"
        	}
    	], 
    	"updated": 2
	}
	4.or even worst your post was ignored by the server
	{
    	"code": 2001, 
    	"refused": 1, 
    	"refused_list": [
        	{
            	"metric_name": "dns_lag", 
            	"tags": "dns lag 3"
        	}
    	], 
    	"unknown": 2, 
    	"unknown_list": [
        	{
            	"description": "cli count 2", 
            	"metric_name": "dns_day_coun", 
            	"tags": "dns count 3"
        	}, 
        	{
            	"description": "cli count 2", 
            	"metric_name": "dns_day_sizeX", 
            	"tags": "dns size 3"
        	}
    	], 
    	"updated": 0
	}
	5.db error
	{
		"code": 1002,
		"msg": "error detail"

	}


----


#Endpoint 2

	/api/collector/metric/something-you-want?limit=10&offset
	VERB:
		GET

	RESPONSE:
	1.ok
	{
    	"code": 0, 
    	"data": [ # "data" might be a empty []
        	{
            	"description": "xxxxxxxxxxxxxxx", 
            	"last_update": 1503039129000, 
            	"metric_name": "ooo.t", 
            	"tags": "232"
        	},
		...
    	]
	}
	2.db error
	{
		"code": 1002 (db error),
		"msg": "error detail"

	}
