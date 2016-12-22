from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection, NotFoundError
from requests_aws4auth import AWS4Auth
import ConfigParser
import sys


class ESearch:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open("./config/default.cfg"))

        access_key = config.get("AWS", "accessKeyId")
        secret_key = config.get("AWS", "secretAccessKey")
        region = config.get("AWS", "region")

        host = "search-foodtrack-acmnvxujgdedubqge77jatwpui.us-east-1.es.amazonaws.com"
        awsauth = AWS4Auth(access_key, secret_key, region, "es")

        self.es = Elasticsearch(
            hosts=[{"host": host, "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
        # print(self.es.info())

    def feed_data(self, index_name, foodtruck_id, body):
        res = None
        try:
            res = self.es.index(
                index=index_name,
                doc_type="tweets",
                id=foodtruck_id,
                body=body
            )
        except:
            for e in sys.exc_info():
                print "Unexpected error:", e
            pass

        return res

    def scroll(self, scroll_id, scroll):
        res = None
        try:
            res = self.es.scroll(scroll_id=scroll_id, scroll=scroll)
        except NotFoundError as e:
            print e
            res = {"hits": {"hits": []}}

        return res

    def get_id(self, index_name, index_type, index_id):
        res = self.es.get(index=index_name, doc_type=index_type, id=index_id)
        print(res["_source"])
        return res
        # self.es.indices.refresh(index=index_name)

    def get_all(self, index_name):
        res = self.es.search(
            index=index_name,
            scroll="2m",
            search_type="scan",
            size="20",
            body={"query": {"match_all": {}}})
        scroll_res = self.scroll(res["_scroll_id"], "2m")
        return {"count": res["hits"]["total"], "result": scroll_res["hits"]["hits"]}

    def search_content(self, index_name, key_word):
        res = self.es.search(
            index=index_name,
            scroll="2m",
            search_type="scan",
            size="20",
            body={"query": {"match": {"text": key_word}}})
        # print("Got %d Hits:" % res["hits"]["total"])
        # for hit in res["hits"]["hits"]:
        #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
        print res
        scroll_res = self.scroll(res["_scroll_id"], "2m")
        print scroll_res
        return {"count": res["hits"]["total"], "result": scroll_res["hits"]["hits"]}

    def search_geo(self, index_name, lat, lon, distance):
        if lat is not None and lon is not None and distance is not None:
            res = self.es.search(
                index=index_name,
                scroll="2m",
                search_type="scan",
                size="20",
                body=
                {"query": {
                    "filtered": {
                        "filter": {
                            "geo_distance": {
                                "distance": distance,
                                "geo": {
                                    "lat": lat,
                                    "lon": lon
                                }
                            }
                        }
                    }
                }}
            )
            scroll_res = self.scroll(res["_scroll_id"], "2m")
            return {"count": res["hits"]["total"], "result": scroll_res["hits"]["hits"]}
        return {"count": 0, "result": []}

