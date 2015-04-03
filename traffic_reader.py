def get_hits():
	from datetime import datetime,timedelta
	cur_date=datetime.now()-timedelta(minutes=1)
	cur_time=cur_date.strftime("%H:%M")
	file_name=cur_date.strftime("%Y_%m_%d*")
	search_keyword="/ty2/search/"
	year=cur_date.strftime("%Y")
	month=cur_date.strftime("%b")
	path="/mnt/data/flume/logs/servers/ty/%s/%s/access-logs" %(year,month)
	cmd="""grep "%s:" %s/%s|grep "%s" |tail|awk -F " " '{print $5}'""" %(cur_time,path,file_name,search_keyword)
	return execute(cmd)
	

def execute(cmd):
	from subprocess import check_output
	return check_output(cmd,shell=True)

def process_result(result):
	pass

if __name__=="__main__":
	sl=execute("dir")
	print sl