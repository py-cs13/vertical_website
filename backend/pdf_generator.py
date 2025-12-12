from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io


class PDFGenerator:
    """
    PDF生成器，用于将工具包内容转换为PDF格式
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """
        设置自定义样式
        """
        # 标题样式
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # 副标题样式
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#3c4043'),
            spaceAfter=12,
            spaceBefore=16,
            bold=True
        ))
        
        # 正文样式
        self.styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=self.styles['BodyText'],
            fontSize=12,
            textColor=colors.HexColor('#202124'),
            spaceAfter=8,
            leading=16
        ))
        
        # 列表项样式
        self.styles.add(ParagraphStyle(
            name='CustomList',
            parent=self.styles['BodyText'],
            fontSize=12,
            textColor=colors.HexColor('#202124'),
            leftIndent=20,
            spaceAfter=4,
            leading=14
        ))
    
    def generate_toolkit_pdf(self, toolkit_content, title="营销工具包"):
        """
        生成工具包PDF
        
        Args:
            toolkit_content: 工具包内容，包含title和content字段
            title: PDF文档标题
            
        Returns:
            PDF文件的字节流
        """
        buffer = io.BytesIO()
        
        # 创建PDF文档
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # 内容列表
        content = []
        
        # 添加标题
        content.append(Paragraph(toolkit_content.get("title", title), self.styles['CustomTitle']))
        content.append(Spacer(1, 30))
        
        # 添加内容
        content_text = toolkit_content.get("content", "")
        
        # 处理分段
        paragraphs = content_text.split('\n\n')
        
        for para in paragraphs:
            # 检查是否为标题（以#开头）
            if para.startswith('# '):
                # 一级标题
                content.append(Paragraph(para[2:], self.styles['CustomHeading2']))
            elif para.startswith('## '):
                # 二级标题
                content.append(Paragraph(para[3:], self.styles['Heading3']))
            elif para.startswith('- '):
                # 列表项
                content.append(Paragraph('• ' + para[2:], self.styles['CustomList']))
            elif para.strip():
                # 普通段落
                content.append(Paragraph(para.strip(), self.styles['CustomBodyText']))
        
        # 构建文档
        doc.build(content)
        
        # 重置缓冲区位置
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
        "content": "# 社交媒体营销工具包\n\n## 一、营销策略概述\n\n社交媒体营销是现代企业推广产品和服务的重要渠道。本工具包将帮助您制定有效的社交媒体营销策略。\n\n## 二、内容创作指南\n\n### 1. 内容类型\n\n- 博客文章\n- 短视频\n- 信息图表\n- 用户案例\n\n### 2. 内容发布频率\n\n- 微信公众号：每周2-3次\n- 抖音：每日1-2次\n- 知乎：每周3-4次\n\n## 三、数据分析\n\n使用以下指标评估营销效果：\n\n- 粉丝增长率\n- 内容互动率\n- 转化率\n- ROI\n\n## 四、总结\n\n通过本工具包的指导，您将能够建立一个有效的社交媒体营销体系，提升品牌知名度和销售业绩。"
    }
    
    # 生成PDF
    pdf_gen = PDFGenerator()
    pdf_path = pdf_gen.generate_toolkit_pdf_file(test_content, "test_toolkit.pdf")
    print(f"PDF生成成功，保存路径：{pdf_path}")
