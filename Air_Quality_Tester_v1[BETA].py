import requests
import json
from datetime import date
from datetime import timedelta
from tkinter import *
from tkinter import messagebox
today = date.today()
DaysBefore = today - timedelta(days = 2)


root = Tk()
root.title("Air Quality Testing App")
root.geometry("620x400")

global MyInput
global resultLabelCOLOR

def chk():
	try:

		url = "https://api.waqi.info/feed/"+MyInput.get().lower()+"/?token=09962c1686db104e9dfe63c37794fb8dfc03fb73"
		res = requests.get(url)

		unload = json.loads(res.content)
		if unload['status'] =='error':
			try:
				ErrorLabel.destroy()
				ErrorLabel = Label(root,text="Please Check Location Name",font=("Helvetica",10)).grid(row=2,column=1)
			except:
				ErrorLabel = Label(root,text="Please Check Location Name",font=("Helvetica",10)).grid(row=2,column=1)

		else:	
			city_name = unload['data']['city']['name'].split(',')[1]
			pm10_data = unload['data']['forecast']['daily']['pm10']
			ozone_data = unload['data']['forecast']['daily']['o3']
			pm25_data = unload['data']['forecast']['daily']['pm25']
			uv_data = unload['data']['forecast']['daily']['uvi']

			total = 0

			for var in ozone_data:
				for x in var:
					#Var is a dictionary
					if var[x]==str(DaysBefore):
						total+=var['avg']

			for var in pm10_data:
				for x in var:
					#Var is a dictionary
					if var[x]==str(DaysBefore):
						total+=var['avg']


			for var in pm25_data:
				for x in var:
					#Var is a dictionary
					if var[x]==str(DaysBefore):
						total+=var['avg']
			try:
				global total_intelligence
				intelli_data = unload['data']['iaqi']
				intelli_data_co2 = intelli_data['co']['v']
				intelli_data_so2 = intelli_data['so2']['v']
				intelli_data_no2 = intelli_data['no2']['v']
				intelli_data_o3 = intelli_data['o3']['v']
				intelli_data_pm10 = intelli_data['pm10']['v']
				total_intelligence = intelli_data_co2+intelli_data_pm10+intelli_data_o3+intelli_data_no2+intelli_data_so2
				# print("Real Time Data is: ",int(round(total_intelligence)))

			except KeyError:
				total_intelligence = 150
				# print("Real Time Data is: ",total_intelligence)

			global val
			val = round(total/1.12)			
			print("Total: "+str(total))
			if val<=50 and val>=0:
				resultLabelCOLOR="green"
				root.configure(bg="green")
				MyInputL = Label(root,text="Enter City Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
				resultLabelG = Label(root,text="Intelli Total: "+str(val),bg=resultLabelCOLOR,font=("Helvetica",20))
				resultLabelG.grid(row=2,column=1)
			elif val>=51 and val<=100:
				resultLabelCOLOR="#ffde33"
				root.configure(bg=resultLabelCOLOR)
				MyInputL = Label(root,text="Enter City Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
				resultLabelM = Label(root,text="Intelli Total: "+str(val),bg=resultLabelCOLOR,font=("Helvetica",20))
				resultLabelM.grid(row=2,column=1)
			elif val>=101 and val<=150:
				resultLabelCOLOR="#ff9933"
				root.configure(bg=resultLabelCOLOR)
				MyInputL = Label(root,text="Enter City Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
				resultLabelH = Label(root,text="Intelli Total: "+str(val),bg=resultLabelCOLOR,font=("Helvetica",20))
				resultLabelH.grid(row=2,column=1)
			elif val>=151 and val<=200 and total_intelligence!=150:
				resultLabelCOLOR="#ff9933"
				root.configure(bg=resultLabelCOLOR)
				MyInputL = Label(root,text="Enter City Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
				resultLabelU = Label(root,text="Intelli Total: "+str(int(total_intelligence)),bg=resultLabelCOLOR,font=("Helvetica",20))
				resultLabelU.grid(row=2,column=1)
			elif val>=151 and val<=200 and total_intelligence==150:
				resultLabelCOLOR="#cc0033"
				root.configure(bg=resultLabelCOLOR)
				MyInputL = Label(root,text="Enter City Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
				resultLabelU = Label(root,text="Intelli Total: "+str(val),bg=resultLabelCOLOR,font=("Helvetica",20))
				resultLabelU.grid(row=2,column=1)
			elif val>=201 and val<=290:
				resultLabelCOLOR="#660099"
				root.configure(bg=resultLabelCOLOR)
				MyInputL = Label(root,text="Enter City Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
				resultLabelD = Label(root,text="Intelli Total: "+str(val),bg=resultLabelCOLOR,font=("Helvetica",20))
				resultLabelD.grid(row=2,column=1)
			else:
				resultLabelCOLOR="#7e0023"
				root.configure(bg=resultLabelCOLOR)
				MyInputL = Label(root,text="Enter City Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
				resultLabelMAX = Label(root,text="Intelli Total: "+str(val),bg=resultLabelCOLOR,font=("Helvetica",20))
				resultLabelMAX.grid(row=2,column=1)


	except(ConnectionError, Exception):
		ErrorLabel = Label(root,text="Unable to Connect to server").grid(row=2,column=1)
try:
	MyInputL = Label(root,text="Enter Name: ",pady=10,bg=resultLabelCOLOR,font=("Helvetica",12)).grid(row=0,column=0)
except NameError:
	MyInputL = Label(root,text="Enter City Name: ",pady=10,font=("Helvetica",12)).grid(row=0,column=0)
MyInput = Entry(root,width=60,borderwidth=3)
MyInput.grid(row=0,column=1)

my_Button = Button(root,text="Check Status",command=lambda: chk())
my_Button.grid(row=1,column=1)

root.mainloop()