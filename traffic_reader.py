from datetime import datetime,timedelta
def get_hits():	
	cur_date=datetime.now()-timedelta(minutes=1)
	cur_time=cur_date.strftime("%H:%M")
	file_name=cur_date.strftime("%Y_%m_%d*")
	search_keyword="/api/search/"
	year=cur_date.strftime("%Y")
	month=cur_date.strftime("%b")
	path="/mnt/data/flume/logs/servers/ty/%s/%s/access-logs" %(year,month)
	cmd="""grep "%s:" %s/%s|grep "%s"|awk -F " " '{print $2"|"$5}'""" %(cur_time,path,file_name,search_keyword)
	print cmd
	return execute(cmd),cur_date
	

def execute(cmd):
	from subprocess import check_output
	return check_output(cmd,shell=True)
def send_to_server(data):
	from httplib2 import Http
	import json
	h = Http()	
	body=json.dumps(data)	
	headers={'Content-Type':'application/json'}
	resp, content = h.request("http://gds.beta.travelyaari.com/service_report_ajax/put_ty_traffic?shared_key=b218fad544980213a25ef18031c9127e", "POST",body=body,headers=headers )	
	#print content

def process_result(logs,city_list):
	#/api/search/?mode=oneway&departDate=04-04-2015&fromCity=Coimbatore&toCity=Bangalore&pickups=1&_=142805861700
	items=logs.split("\n")
	result=[]
	counter=0
	for item in items:		
		dict_item={}		
		try:
			path=item.split("|")[1]		
			hit_time=datetime.strptime(item.split("|")[0],"[%d/%b/%Y:%H:%M:%S")							
			for param in path.split("?")[1].split("&"):
				key=param.split("=")[0]
				val=param.split("=")[1]
				dict_item[key]=val
			#print dict_item

			if "fromCity" in dict_item and "toCity" in dict_item:
				try:
					hit_time=datetime.strptime(item.split("|")[0],"[%d/%b/%Y:%H:%M:%S")							
					from_id = city_list[dict_item["fromCity"].lower()]["cid"]
					to_id = city_list[dict_item["toCity"].lower()]["cid"]
					#{"data": [{"to": "2476", "from": "2461", "index": 0},
					result.append({"to":from_id,"from":to_id,"index":counter,"hit_time":hit_time.strftime("%Y-%m-%d %H:%M:%S")})
				except Exception as e:
					pass
		except Exception as e:
			pass
		counter+=1
	return result

if __name__=="__main__":
	#sl=execute("dir")
	import json	
	city_list_path="/home/ec2-user/data_platform/env26/ty_traffic/city_to_id.json"
	city_list=None
	with open(city_list_path,"rb") as t:
		city_list=json.loads(t.read())
	logs,cur_date=get_hits()
	result=process_result(logs,city_list)
	send_to_server({"data":result,"time":cur_date.strftime("%H:%M %Y-%m-%d")})	
	

	#print sl