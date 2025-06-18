import os
import base64
from pathlib import Path
from PIL import Image

def get_content_bbox(img):
    """获取图片中有颜色内容的边界框"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    width, height = img.size
    left, top, right, bottom = width, height, 0, 0

    pixels = img.getdata()
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            r, g, b, a = pixels[idx]
            # 如果不是接近白色且不是完全透明
            if not (r > 240 and g > 240 and b > 240) and a > 10:
                if x < left:
                    left = x
                if x > right:
                    right = x
                if y < top:
                    top = y
                if y > bottom:
                    bottom = y

    # 如果找到了内容，返回边界框，否则返回None
    if left < right and top < bottom:
        return (left, top, right + 1, bottom + 1)
    return None


def get_minimal_size(img, bbox=None):
    """获取图片内容的最小尺寸"""
    if bbox:
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])
    else:
        return img.size
def convert_images_to_svg(input_dir: Path, output_dir: Path, white_threshold=240):
    """
    将指定目录中的所有图片转换为SVG格式并保存到输出目录
    :param input_dir: 包含原始图片的目录
    :param output_dir: 保存SVG文件的目标目录
    :return: 转换的文件数量
    """
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.jpeg', '.webp']
    converted_count = 0

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    for file in input_dir.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:

            svg_path = output_dir / file.with_suffix('.svg').name

            # 检查是否需要跳过已存在的文件
            if svg_path.exists():
                print(f"跳过已存在的文件: {svg_path.name}")
                continue

            try:
                # 打开图片获取尺寸
                img = Image.open(file)

                bbox = get_content_bbox(img)
                if bbox:
                    print(f"检测到内容区域: {bbox}")
                    img = img.crop(bbox)  # 裁剪到有效区域
                else:
                    print("未检测到有效内容区域，使用原图尺寸")
                # 步骤2：转换为RGBA模式以便处理透明度
                img = img.convert("RGBA")
                # 获取最简尺寸
                width, height = get_minimal_size(img, bbox)
                # 获取图片数据
                datas = img.getdata()
                # 创建新的像素数据列表
                new_data = []
                # 处理每个像素
                for item in datas:
                    # 如果像素是白色或接近白色，则将其设为透明
                    if item[0] > white_threshold and item[1] > white_threshold and item[2] > white_threshold:
                        new_data.append((0, 0, 0, 0))  # 完全透明
                    else:
                        new_data.append(item)  # 保留原始像素
                # 应用新的像素数据
                img.putdata(new_data)

                # 创建临时文件保存处理后的图片
                temp_file = Path("temp_image.png")
                img.save(temp_file, "PNG")

                # 读取图片数据
                with open(temp_file, 'rb') as f:
                    img_data = f.read()
                
                # 构建Base64编码的SVG内容
                svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <image href="data:image/png;base64,{base64.b64encode(img_data).decode('utf-8')}" width="{width}" height="{height}"/>
</svg>'''

                # 构造SVG文件路径
                svg_filename = file.with_suffix('.svg').name
                svg_path = output_dir / svg_filename

                # 写入SVG文件
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)

                print(f"成功转换图片: {file.name} -> {svg_filename}")
                converted_count += 1
            except Exception as e:
                print(f"图片转换失败: {file.name} - {str(e)}")
                if temp_file.exists():
                    temp_file.unlink()

    return converted_count

def main():
    # 定义根目录、输入目录和输出目录
    root_dir = Path.cwd()
    input_dir = root_dir / "company" / "logos"
    output_dir = root_dir / "src" / "assets" / "logos"

    # 检查输入目录是否存在
    if not input_dir.exists():
        print(f"错误：输入目录 {input_dir} 不存在")
        return

    # 调用转换函数
    total_converted = convert_images_to_svg(input_dir, output_dir)

    # 输出总计
    print(f"已完成图片转换，共转换 {total_converted} 个图片文件")

if __name__ == "__main__":
    main()