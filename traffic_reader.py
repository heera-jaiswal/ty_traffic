def get_hits():
	from datetime import datetime,timedelta
	cur_date=datetime.now()-timedelta(minutes=1)
	cur_time=cur_date.strftime("%H:%M")
	file_name=cur_date.strftime("%Y_%m_%d*")
	search_keyword="/api/search/"
	year=cur_date.strftime("%Y")
	month=cur_date.strftime("%b")
	path="/mnt/data/flume/logs/servers/ty/%s/%s/access-logs" %(year,month)
	cmd="""grep "%s:" %s/%s|grep "%s" |tail|awk -F " " '{print $5}'""" %(cur_time,path,file_name,search_keyword)
	print cmd
	return execute(cmd)
	

def execute(cmd):
	from subprocess import check_output
	return check_output(cmd,shell=True)

def process_result(logs,city_list):
	#/api/search/?mode=oneway&departDate=04-04-2015&fromCity=Coimbatore&toCity=Bangalore&pickups=1&_=142805861700
	items=logs.split("\n")
	result=[]
	for item in items:
		dict_item={}
		print item
		for param in item.split("?")[1].split("&"):
			key=param.split("=")[0]
			val=param.split("=")[1]
			dict_item[key]=val
		print dict_item
		if "fromCity" in dict_item and "toCity" in dict_item:
			try:
				from_id = city_list[dict_item["fromCity"].lower()]["cid"]
				to_id = city_list[dict_item["toCity"].lower()]["cid"]
				result.append({"from":from_id,"to":to_id})
			except Exception as e:
				pass
	return result

if __name__=="__main__":
	#sl=execute("dir")
	import json
	city_list_path="city_to_id.json"
	city_list=None
	with open(city_list_path,"rb") as t:
		city_list=json.loads(t.read())
	logs=get_hits()
	result=process_result(logs,city_list)
	print json.dumps({"hits":result},indent=4)
	print len(result)

	#print sl