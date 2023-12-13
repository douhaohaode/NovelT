# NovelT

## 描述

一个简单的推文视频制作工具，基于一些开源工具进行开发。



##  [使用教程视频网址]（https://www.bilibili.com/video/BV1bw411m7A7/?vd_source=faa4615f3c71b2b526ed2b1f48a70b2c）


## 特征

- OCR
- 文字转换语音
- 图文视频生成
- 待开发

## 运行

安装conda环境

```python
git clone https://github.com/douhaohaode/NovelT.git
cd NovelT
conda create -n novelt python=3.10 -y  
conda activate novelt
pip install -r requirements.txt
python app.py
```


mac 为例:

1. 安装
```python
brew install tesseract
brew install tesseract-lang
```




## 字幕功能
使用了moviepy中的添加字幕功能需要安装[ImageMagick](https://www.imagemagick.org/script/index.php) 才能使用全部功能


## 三方库:
感谢下列开源工具排名不分先后
- [gradio](https://github.com/gradio-app/gradio)
- [moviepy](https://github.com/Zulko/moviepy)
- [gfpgan](https://github.com/TencentARC/GFPGAN)
- opencv-python
- edge_tts
