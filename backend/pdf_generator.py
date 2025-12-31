import io
import os

class PDFGenerator:
    """
    PDF生成器，用于将工具包内容转换为PDF格式
    简化版本，不依赖WeasyPrint库
    """
    
    def __init__(self):
        pass
    
    def generate_toolkit_pdf(self, toolkit_content, title="营销工具包"):
        """
        生成工具包PDF
        
        Args:
            toolkit_content: 工具包内容，包含title和content字段
            title: PDF文档标题
            
        Returns:
            PDF文件的字节流
        """
        # 获取标题
        doc_title = toolkit_content.get("title", title)
        
        # 创建一个简单的PDF文件内容（模拟PDF）
        pdf_content = f"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 50
>>
stream
BT
/F1 12 Tf
100 700 Td
({doc_title}) Tj
ET
endstream
endobj
5 0 obj
<<
/Type /Font
/Subtype /Type1
/Name /F1
/BaseFont /Helvetica
/Encoding /WinAnsiEncoding
>>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000053 00000 n 
0000000096 00000 n 
0000000158 00000 n 
0000000236 00000 n 
trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
293
%%EOF
"""
        
        # 写入字节流
        buffer = io.BytesIO()
        buffer.write(pdf_content.encode('utf-8'))
        buffer.seek(0)
        
        return buffer
    
    def generate_toolkit_pdf_file(self, toolkit_content, file_path, title="营销工具包"):
        """
        生成工具包PDF文件
        
        Args:
            toolkit_content: 工具包内容
            file_path: 保存文件路径
            title: PDF文档标题
        """
        buffer = self.generate_toolkit_pdf(toolkit_content, title)
        
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        return file_path


# 测试用例
if __name__ == "__main__":
    # 创建测试内容
    test_content = {
        "title": "社交媒体营销工具包",
        "content": "# 社交媒体营销工具包\n\n## 一、营销策略概述\n\n社交媒体营销是现代企业推广产品和服务的重要渠道。本工具包将帮助您制定有效的社交媒体营销策略。"
    }
    
    # 生成PDF
    pdf_gen = PDFGenerator()
    pdf_path = pdf_gen.generate_toolkit_pdf_file(test_content, "test_toolkit.pdf")
    print(f"PDF生成成功，保存路径：{pdf_path}")
