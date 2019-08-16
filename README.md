# 介绍
## 1.更新Annotate_Console.ui文件后
* 1.1 需要在导入  
    ````
    from m4_QLabel import *
    ````
* 1.2 将  
    ````
    self.m4_ShowImage = QtWidgets.QLabel(self.centralwidget)
    ````
    改为：   
    ```
    self.m4_ShowImage = m4_QLabel(self.centralwidget)
    ````
