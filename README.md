# 这是什么

ご注文はうさぎですか?? Wonderful party! ai翻译 (Windows)

[官网](https://game.mages.co.jp/gochiusa) 
[VNDB](https://vndb.org/v18457) 
[ymgal](https://www.ymgal.games/ga21816) 
[kungal](https://www.kungal.com/zh-cn/galgame/1106)

注意! 这是ai翻译!!!

本项目基于Windows移植版制作, 不保证PSV平台兼容!!!

项目尚未完成, 如果你对本项目有兴趣并且想要帮忙的话, 我们欢迎你提交pr或issue

游戏(生肉)下载: 

[One Drive](https://driver.listder.xyz/?file=/galgame/生肉/Gochuumon%20wa%20Usagi%20Desu%20ka%20Wonderful%20Party!.7z)
[Google Drive](https://drive.google.com/file/d/1uZftDmstMKKSYju34tqih8U0ri2sboAc/view?usp=sharing(无汉化)/Gochuumon%20wa%20Usagi%20Desu%20ka%20Wonderful%20Party!.7z)

顺带欢迎新增下载地址, QWQ

# 进度

## 字体

使用 [KaleidoADV_FontConverter](https://github.com/PlaMemo-VIE-FanTrans/KaleidoADV_FontConverter) 
修改 convert_font_to_bitmap.py 的第 50 行来添加字
修改 112 行来调整字体大小

请将翻译好后的所有文本扔进text.txt内, 然后使用char.cpp去重

## 剧本

已完成

## 嵌字和界面UI

之后再说（

## 其他

想好再写（

## 解包及封包

工具: [FreeMote](https://github.com/UlyssesWu/FreeMote/)

## 解包

 ```
 PsbDecompile.exe info-psb -k 38757621acf82 {name}_info.psb.m -a
 ```

## 封包

 ```
 PsBuild info-psb -k 38757621acf82 {name}_info.psb.m.json
 ```
 
 
# 奇怪的链接
 
 ```
 echo aHR0cHM6Ly9xbS5xcS5jb20vcS95U0k5Z3c1cUNj | base64 -d
 ```