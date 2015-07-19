import unittest
import mongodb_api

class ApiTest(unittest.TestCase):
    def test_insert_one_activity_adverts(self):
       dict_adverts = {"activity_id": "123", "data": "data"}
       mongodb_api.insert_one_activity_adverts(dict_adverts)
       rows = mongodb_api.get_activity_adverts_collection().find({"activity_id": "123"})
       self.assertNotEqual(rows.count(), 0) 


    def test_insert_many_activity_adverts(self):
       dict_adverts = [{"activity_id": "123", "data": "data"}, {"activity_id": "124", "data": "data"}]
       obj_ids = mongodb_api.insert_many_activity_adverts(dict_adverts)
       rows = mongodb_api.get_activity_adverts_collection().find({"activity_id": "123"})
       self.assertNotEqual(rows.count(), 0)


    def test_get_act_adverts_by_object_id(self):
       dict_adverts = {"activity_id": "123", "data": "data"}
       obj_id = mongodb_api.insert_one_activity_adverts(dict_adverts)
       print obj_id
       rows = mongodb_api.get_act_adverts_by_object_id(obj_id)
       self.assertNotEqual(len(rows), 0)

    def test_get_act_adverts_by_activity_id(self):
       dict_adverts = {"activity_id": "123", "data": "data"}
       obj_id = mongodb_api.insert_one_activity_adverts(dict_adverts)
       rows = mongodb_api.get_act_adverts_by_activity_id("123")
       self.assertNotEqual(len(rows), 0)


    def close_mongodb_connection(self):
       mongodb_api.close_mongodb_connection()
       self.assertNotEqual(1,0)
	
if __name__ == '__main__':
    unittest.main()

