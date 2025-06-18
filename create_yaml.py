import os
import yaml
from pypinyin import lazy_pinyin, Style

# 定义 company 和 logos 文件夹路径
company_dir = "company"
logos_dir = "src/assets/logos"
output_file = "generated_landscape.yml"

# 初始化 landscape 数据结构
landscape_data = []

# 存储一级分类和二级分类的映射
category_map = {}

# 获取中文名称的拼音首字母（取前5个字母）
def get_chinese_prefix(name):
    if all('\u4e00' <= c <= '\u9fa5' for c in name):  # 检查是否全为中文字符
        pinyin_list = lazy_pinyin(name, style=Style.FIRST_LETTER)
        prefix = ''.join(pinyin_list[:5])  # 取前5个拼音首字母
        return prefix
    return ''

# 遍历 company 文件夹中的所有 .md 文件
for filename in os.listdir(company_dir):
    if filename.endswith(".md") or filename.endswith(".txt"):
        file_path = os.path.join(company_dir, filename)

        # 读取并解析 .md 文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = {}
            for line in f:
                # 替换中文冒号为英文冒号，并去除首尾空白
                line = line.strip().replace("：", ":")
                if ":" in line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        key, value = parts
                        content[key.strip()] = value.strip()

        # 获取公司名称和 logo 文件名
        company_name = content.get("名称", "未知公司")
        raw_description = content.get("描述", "")
        founded_year = content.get("成立时间", "")
        homepage_url = content.get("官网网站", "")
        first_category = content.get("一级分类", "其他")
        second_category = content.get("二级分类", "其他")

        # 新增字段：展示大小、展示优先级
        display_size = content.get("展示大小", "").strip()
        display_priority_str = content.get("展示优先级", "").strip()

        display_priority = None
        if display_priority_str.isdigit():
            num = int(display_priority_str)
            if 1 <= num <= 5:
                display_priority = num

        # 构建 description 字段
        description_parts = []
        if raw_description:
            description_parts.append(raw_description)
        else:
            description_parts.append("科技公司")  # 默认描述

        if founded_year:
            description_parts.append(f"成立于 {founded_year}")

        description = "，".join(description_parts)

        # 在 logos 文件夹中查找匹配的 logo 文件（支持双向模糊匹配）
        logo_filename = None
        for logo in os.listdir(logos_dir):
            if logo.lower().endswith(".svg"):  # 只匹配 SVG 文件
                if company_name in logo or logo.replace(".svg", "") in company_name:
                    logo_filename = logo
                    break

        # 构建 item 数据（包含 description）
        prefixed_company_name = get_chinese_prefix(company_name) + company_name
        item_data = {
            "name": prefixed_company_name,
            "homepage_url": homepage_url,
            "logo": logo_filename if logo_filename else "",
            "description": description
        }

        # 添加 project 属性（仅当 display_size 是 “大”）
        if display_size == "大" and display_priority is not None:
            item_data["project"] = f"level{display_priority}"

        # 按照一级分类和二级分类组织数据
        if first_category not in category_map:
            category_map[first_category] = {}
        if second_category not in category_map[first_category]:
            category_map[first_category][second_category] = {"items": []}

        # 区分“大”、“小”类目
        if display_size == "大" and display_priority is not None:
            category_map[first_category][second_category]["items"].append(item_data)
        elif display_size == "小":
            category_map[first_category][second_category]["items"].append({
                "item": item_data,
                "priority": display_priority
            })
        else:
            # 忽略不合法的展示大小或展示优先级
            category_map[first_category][second_category]["items"].append({
                "item": item_data,
                "priority": None
            })

# 将分类结构转换为 landscape.yml 格式
for first_cat, subcats in category_map.items():
    category_entry = {
        "name": first_cat,
        "subcategories": []
    }
    for second_cat, items_dict in subcats.items():
        subcategory_entry = {
            "name": second_cat,
            "items": []
        }

        # 先加入“大”类型项目，并按 priority 排序
        large_items = sorted(
            [item for item in items_dict["items"] if "project" in item],
            key=lambda x: int(x.get("project", "level5").replace("level", ""))
        )

        # 再加入“小”类型项目，先排合法 priority，再排非法 priority
        small_items_sorted = sorted(
            [item for item in items_dict["items"] if "project" not in item and item.get("priority") is not None],
            key=lambda x: x["priority"]
        )
        small_items_invalid = [item for item in items_dict["items"] if "project" not in item and item.get("priority") is None]

        # 合并所有项目
        subcategory_entry["items"].extend(large_items)
        subcategory_entry["items"].extend([item["item"] for item in small_items_sorted])
        subcategory_entry["items"].extend([item["item"] for item in small_items_invalid])

        category_entry["subcategories"].append(subcategory_entry)
    landscape_data.append(category_entry)

# 写入生成的 YAML 文件
with open(output_file, "w", encoding="utf-8") as f:
    yaml.dump({"landscape": landscape_data}, f, allow_unicode=True, sort_keys=False, indent=2)

print(f"已成功生成 {output_file} 文件！")