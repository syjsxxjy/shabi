#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO
import sys
import adt7410
import pt1000

class PIinit:
	"初始化板子参数设定"
	flag=0

	#设置输出PIN
	# LED0=27  #程序开始指示灯
	TempOUT1=23

	def __init__(self):
		RPi.GPIO.setmode(RPi.GPIO.BCM)
		# RPi.GPIO.setup(PIinit.LED0, RPi.GPIO.OUT)
		RPi.GPIO.setup(PIinit.TempOUT1, RPi.GPIO.OUT)
		# RPi.GPIO.output(PIinit.LED0, True) #点亮LED0
		print ("进入__init__方法")

class pidCtr:
	"PID控制器"
	flag=1  
	Sv=120.2 #用户输入 pdms60 72.60度 pdms72 91.5度 pdms90  120.2度
	Pv=0.000
	T=250.000 #ms PID计算周期
	Kp=5.000 #比例系数
	Ti=20000.000 #ms 积分时间
	Td=125.000 #ms 微分时间
	Ek=0.000 #本次偏差
	Ek_1=0.000 #上次偏差
	SEk=0.000 #历史偏差总和
	Iout=0.000
	Pout=0.000
	Dout=0.000
	OUT0=1.000
	OUT=0.000
	pwmcycle=200 #ms PWM周期

	def calc(self):
		self.Ek=self.Sv-self.Pv #计算当前偏差
		# print("Ek==%s"%self.Ek)
		# print("Ek_1==%s"%self.Ek_1)
		self.Pout=self.Kp*self.Ek  #1-比例项输出
		# print("Pout==%s"%self.Pout)
		self.SEk+=self.Ek  #历史偏差总和
		# print("SEk==%s"%self.SEk)
		DeltaEK=self.Ek-self.Ek_1  #上一次和本次的偏差之差
		ti=self.T/self.Ti  #pid周期/积分时间
		# print("ti==%s"%ti)
		Ki=ti*self.Kp  #积分系数
		# print("Ki==%s"%Ki)
		self.Iout=Ki*self.SEk #2-积分输出
		# print("Iout==%s"%self.Iout)
		td=self.Td/self.T #微分时间/pid周期
		Kd=self.Kp*td #微分系数
		self.Dout=Kd*DeltaEK #3-微分项输出
		# print("Dout==%s"%self.Dout)
		out=self.Pout+self.Iout+self.Dout+self.OUT0 #4-pid计算结果
		# print("calc.out==%s"%out)
		#pid计算结果处理‘’
		if out>self.pwmcycle:
			self.OUT=self.pwmcycle
		elif out<0:
			self.OUT=0
		elif 0<=out<=self.pwmcycle:
			self.OUT=out
		self.Ek_1=self.Ek 


if __name__ == "__main__":
	try:
		pi=PIinit()
		print("初始化完毕，创建PIinit对象pi，flag==%s"%pi.flag)
		# RPi.GPIO.output(pi.TempOUT1, True)
		# print("TempOUT1开始输出1")
		pid=pidCtr()
		print("创建pidCtr对象pid，flag==%s"%pid.flag)
		#设置pwm
		pwm=RPi.GPIO.PWM(pi.TempOUT1,5)#pwm周期200ms
		pwm.start(1)
		file_handle=open('70Templog.txt',mode='w')
		while True:
			time.sleep(0.5)
			# pid.Pv=adt7410.read_adt7410()
			pid.Pv=float(pt1000.calcTemp(2,3))
			# pt1000temp=float(pt1000.calcTemp(2,3))
			# print("Pt1000で測温[2,3]==%s"%pt1000temp)
			print("Pt1000で測温[2,3]==%s"%pid.Pv)
			# pid.Pv=max31855.sensor.readTempC()
			sensortemp=max31855.sensor.readTempC()
			print("温度传感器测温(热电偶)==%s度"%sensortemp)
			# print("温度传感器测温(热电偶)==%s度"%pid.Pv)
			file_handle.write("%s | "%pid.Pv)
			file_handle.write("%s \n"%sensortemp)
			# file_handle.write("%s \n"%pt1000temp)
			pid.calc()
			print("pidCr.OUTの計算結果==%s"%pid.OUT)
			dc=pid.OUT/pid.pwmcycle*100
			pwm.ChangeDutyCycle(dc)
			print("PWM信号のDutyCyle：%s"%dc)
			# file_handle.write("%s ;\n"%dc)
			print("-----------------------------")
			
			pass
			
		file_handle.close()
	except Exception as e:
		raise
	else:
		pass
	finally:
		file_handle.close()
		RPi.GPIO.cleanup()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO
import sys
import adt7410
import pt1000

class PIinit:
	"初始化板子参数设定"
	flag=0

	#设置输出PIN
	# LED0=27  #程序开始指示灯
	TempOUT1=23

	def __init__(self):
		RPi.GPIO.setmode(RPi.GPIO.BCM)
		# RPi.GPIO.setup(PIinit.LED0, RPi.GPIO.OUT)
		RPi.GPIO.setup(PIinit.TempOUT1, RPi.GPIO.OUT)
		# RPi.GPIO.output(PIinit.LED0, True) #点亮LED0
		print ("进入__init__方法")

class pidCtr:
	"PID控制器"
	flag=1  
	Sv=120.2 #用户输入 pdms60 72.60度 pdms72 91.5度 pdms90  120.2度
	Pv=0.000
	T=250.000 #ms PID计算周期
	Kp=5.000 #比例系数
	Ti=20000.000 #ms 积分时间
	Td=125.000 #ms 微分时间
	Ek=0.000 #本次偏差
	Ek_1=0.000 #上次偏差
	SEk=0.000 #历史偏差总和
	Iout=0.000
	Pout=0.000
	Dout=0.000
	OUT0=1.000
	OUT=0.000
	pwmcycle=200 #ms PWM周期

	def calc(self):
		self.Ek=self.Sv-self.Pv #计算当前偏差
		# print("Ek==%s"%self.Ek)
		# print("Ek_1==%s"%self.Ek_1)
		self.Pout=self.Kp*self.Ek  #1-比例项输出
		# print("Pout==%s"%self.Pout)
		self.SEk+=self.Ek  #历史偏差总和
		# print("SEk==%s"%self.SEk)
		DeltaEK=self.Ek-self.Ek_1  #上一次和本次的偏差之差
		ti=self.T/self.Ti  #pid周期/积分时间
		# print("ti==%s"%ti)
		Ki=ti*self.Kp  #积分系数
		# print("Ki==%s"%Ki)
		self.Iout=Ki*self.SEk #2-积分输出
		# print("Iout==%s"%self.Iout)
		td=self.Td/self.T #微分时间/pid周期
		Kd=self.Kp*td #微分系数
		self.Dout=Kd*DeltaEK #3-微分项输出
		# print("Dout==%s"%self.Dout)
		out=self.Pout+self.Iout+self.Dout+self.OUT0 #4-pid计算结果
		# print("calc.out==%s"%out)
		#pid计算结果处理‘’
		if out>self.pwmcycle:
			self.OUT=self.pwmcycle
		elif out<0:
			self.OUT=0
		elif 0<=out<=self.pwmcycle:
			self.OUT=out
		self.Ek_1=self.Ek 


if __name__ == "__main__":
	try:
		pi=PIinit()
		print("初始化完毕，创建PIinit对象pi，flag==%s"%pi.flag)
		# RPi.GPIO.output(pi.TempOUT1, True)
		# print("TempOUT1开始输出1")
		pid=pidCtr()
		print("创建pidCtr对象pid，flag==%s"%pid.flag)
		#设置pwm
		pwm=RPi.GPIO.PWM(pi.TempOUT1,5)#pwm周期200ms
		pwm.start(1)
		file_handle=open('70Templog.txt',mode='w')
		while True:
			time.sleep(0.5)
			# pid.Pv=adt7410.read_adt7410()
			pid.Pv=float(pt1000.calcTemp(2,3))
			# pt1000temp=float(pt1000.calcTemp(2,3))
			# print("Pt1000で測温[2,3]==%s"%pt1000temp)
			print("Pt1000で測温[2,3]==%s"%pid.Pv)
			# pid.Pv=max31855.sensor.readTempC()
			sensortemp=max31855.sensor.readTempC()
			print("温度传感器测温(热电偶)==%s度"%sensortemp)
			# print("温度传感器测温(热电偶)==%s度"%pid.Pv)
			file_handle.write("%s | "%pid.Pv)
			file_handle.write("%s \n"%sensortemp)
			# file_handle.write("%s \n"%pt1000temp)
			pid.calc()
			print("pidCr.OUTの計算結果==%s"%pid.OUT)
			dc=pid.OUT/pid.pwmcycle*100
			pwm.ChangeDutyCycle(dc)
			print("PWM信号のDutyCyle：%s"%dc)
			# file_handle.write("%s ;\n"%dc)
			print("-----------------------------")
			
			pass
			
		file_handle.close()
	except Exception as e:
		raise
	else:
		pass
	finally:
		file_handle.close()
		RPi.GPIO.cleanup()
