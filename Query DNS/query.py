# -*- coding: utf-8 -*-
import sys, mechanize, re, time, timeout_decorator

'''
移动 - \u79fb\u52a8
铁通 - \u94c1\u901a
'''

url = "http://www.ipip.net/dns.php"
start = '"ips":{'
end = ',"dns_ip"'
result_flag = 0
duh = 1

def connect_ipip(domain_name):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.open(url)
	#print "已建立到ipip.net的连接\n"
	
	form_c = 0
	for frm in br.forms():
		if str(frm.attrs["id"])=="ps":
			break
		form_c += 1
	br.select_form(nr=form_c)
	br["host"] = domain_name
	
	return br

@timeout_decorator.timeout(10)
def loop(response, count, rounds, s, f2):
	while 1:
		content = response.read(1024)
		if not content:
			print "查询异常 - 结果为空"
			break
		tmp = content.split(start)[-1].split(end)[0]
		if "\u79fb\u52a8" in tmp or "\u94c1\u901a" in tmp:
			vector = tmp.split(",")
			for v in vector:
				if "\u8054\u901a" in v or "\u7535\u4fe1" in v:
					continue
				if "\u79fb\u52a8" in v or "\u94c1\u901a" in v:
					count += 1
					#print "v is: " + v
					if "\u79fb\u52a8" in v and "\u94c1\u901a" in v:
						isp = "(移动/铁通)"
					elif "\u79fb\u52a8" in v:
						isp = "(移动)"
					else:
						isp = "(铁通)"
					res = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', v)
					for r in res:
						if r not in s:
							result_flag = 1
							ip = r + "       " + isp + "\n"
							f2.write(ip)
							s.add(r)						
			
		rounds += 1
		if count == 2 or rounds == 16:
			if rounds == 16 and len(s)==0:
				f2.write("无结果\n")
			return
		# 每次查询间隔等待0.5秒
		time.sleep(0.5)


if __name__ == "__main__":
	print "程序启动..."
	
	with open("name.txt", "r") as f1:
		targets = f1.readlines()
		
	with open("result.txt", "w") as f2:	

		with open("long.txt", "w") as f3:
			
			for u in targets:
				if "." not in u:
					continue
				u = u.strip()
				result_flag = 0
				status = "查询域名: " + u
				print status
				f2.write("----------------------------------------\n")
				f2.write(status + "\n")

				br = connect_ipip(u)
				
				response = br.submit()
				print "正在解析结果"
				
				count = 0
				rounds = 0
				
				s = set()
				
				try:
					loop(response, count, rounds, s, f2)
				except timeout_decorator.TimeoutError:
					if result_flag == 0:
						print "当前域名超时！域名已记录到long.txt"
						f3.write(u + "\n")	

			print "\n所有域名查询完毕。结果请见result.txt"