import os
from docx import Document

folder_path = 'files'


def create_product_certificate_map(folder_path):
    product_certificate_map = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.docx'):  # Проверяем, что это файл DOCX
            cert_type = os.path.splitext(file_name)[0]
            file_path = os.path.join(folder_path, file_name)
            doc = Document(file_path)
            items = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
            # Создаем список товаров для каждого типа сертификата
            for item in items:
                product_certificate_map[item.lower()] = cert_type

    return product_certificate_map


def find_certificates_for_product(product):
    product = product.lower()
    product_certificate_map = create_product_certificate_map(os.path.join(os.path.dirname(__file__), 'files'))

    matched_items = [(item, cert_type) for item, cert_type in product_certificate_map.items() if product in item]

    if matched_items:
        return matched_items
    else:
        return [("Тип сертификата для этого товара не найден.", "")]


# Пример взаимодействия с пользователем
# if __name__ == "__main__":
#     product_name = input("Введите название товара: ")
#     certificates = find_certificates_for_product(product_name)
#
#     if certificates:
#         print(f"Найденные совпадения для товара '{product_name}':")
#         for item, cert_type in certificates:
#             print(f"- '{item}' (Тип сертификата: {cert_type})")
#     else:
#         print("Тип сертификата для этого товара не найден.")
