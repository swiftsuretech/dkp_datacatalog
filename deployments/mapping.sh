curl -XPUT "https://a966740a868a2412eba54023109ab905-1124658745.us-west-2.elb.amazonaws.com:443/elastic" -H "kbn-xsrf: reporting" -H -u "elastic:717q73YzUpuwA6WH20H4Jqq7" Content-Type: application/json" -d'
{
  "mappings": {
    "properties": {
      "ctime": {
        "type":   "date",
        "format": "EEE MMM dd HH:mm:ss z YYYY"
      },
      "domain": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "language": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "seendate": {
        "type":   "date",
        "format": "basic_date_time_no_millis"
        
      },
      "socialimage": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "sourcecountry": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "url": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "url_mobile": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}'