# -*- encoding=utf8 -*-
__author__ = "xxxxxxtester"
 
from airtest.core.api import *

auto_setup(__file__)
# connect_device("android:///")
def swipexy(x,y,xx,yy):
    width, height = device().get_current_resolution()
    start_x = width * x
    start_y = height * y
    end_x = width * xx
    end_y = height * yy
    swipe((start_x, start_y), (end_x, end_y), duration=0.1)

print("start...")
wake()
time.sleep(2.0)
swipexy(0.5,0.95,0.5,0.1)

stop_app("com.miui.calculator")
start_app("com.miui.calculator")

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

poco("com.miui.calculator:id/btn_c_s").click()
poco("com.miui.calculator:id/digit_1").click()
poco("com.miui.calculator:id/op_add").click()
poco("com.miui.calculator:id/digit_2").click()

assert poco("com.miui.calculator:id/result").get_text() == "= 3"
assert_equal(poco("com.miui.calculator:id/result").get_text(), "= 3", "请填写测试点.")


