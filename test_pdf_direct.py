from backend.pdf_generator import PDFGenerator
import io
import os

# 创建测试内容
test_content = {
    "title": "宝宝睡眠问题全解析",
    "content": "# 宝宝睡眠问题全解析\n\n## 一、婴儿睡眠的重要性\n\n睡眠对婴儿的生长发育至关重要。良好的睡眠有助于婴儿大脑和身体的发育。\n\n## 二、常见睡眠问题\n\n### 1. 入睡困难\n\n- 建立规律的睡眠时间\n- 创造舒适的睡眠环境\n- 避免过度刺激\n\n### 2. 夜间醒来频繁\n\n- 检查尿布是否湿了\n- 确保室内温度适宜\n- 建立安抚仪式\n\n## 三、解决方案\n\n1. 制定睡眠时间表\n2. 建立睡前仪式\n3. 培养自主入睡能力\n\n## 四、总结\n\n通过以上方法，您可以帮助宝宝建立良好的睡眠习惯，让宝宝和家长都能拥有充足的睡眠。"
}

# 测试PDF生成
def test_pdf_generation():
    print("测试PDF生成功能...")
    
    # 创建PDF生成器实例
    pdf_generator = PDFGenerator()
    
    # 生成PDF
    pdf_buffer = pdf_generator.generate_toolkit_pdf(test_content, test_content["title"])
    
    # 保存文件
    filename = "test_chinese_pdf.pdf"
    with open(filename, "wb") as f:
        f.write(pdf_buffer.getvalue())
    
    print(f"PDF生成成功，保存为: {filename}")
    print(f"文件大小: {os.path.getsize(filename)} bytes")
    print(f"文件路径: {os.path.abspath(filename)}")
    print("请打开该文件检查中文是否正常显示")

if __name__ == "__main__":
    test_pdf_generation()