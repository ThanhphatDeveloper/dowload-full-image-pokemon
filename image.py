import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

def download_image(img_url, img_name, folder):
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as e:
        print(f"Lỗi: {folder}: {e}")

    img_path = os.path.join(folder, img_name)

    try:
        img_response = requests.get(img_url)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f"Tải xuống ảnh: {img_name}")
    except Exception as e:
        print(f"Lỗi khi tải xuống ảnh {img_name}: {e}")

def download_pokemon_images(base_url, start_id, end_id, folder):
    downloaded_images = set()  # Tạo một tập hợp để lưu trữ tên ảnh đã tải xuống
    for pokemon_id in range(start_id, end_id + 1):
        for sub_id in range(0, 4):  # Kiểm tra cho số phụ từ 0 đến 3
            url = f"{base_url}/{pokemon_id:04d}_{sub_id}"
            response = requests.get(url)
            if response.status_code == 200:  # Kiểm tra xem trang tồn tại hay không
                soup = BeautifulSoup(response.content, 'html.parser')
                pokemon_no = soup.find('div', class_='contents').get('data-zukanid')
                
                # Kiểm tra nếu data-zukanid có giá trị từ 2 đến 4
                if 2 <= int(pokemon_no) <= 4:
                    pokemon_name_element = soup.find('p', class_='pokemon-slider__main-name')
                    pokemon_subname_element = soup.find('p', class_='pokemon-slider__main-subname')
                    
                    if pokemon_name_element and pokemon_subname_element:
                        pokemon_name = pokemon_name_element.text.strip().replace(' ', '_')
                        pokemon_subname = pokemon_subname_element.text.strip().replace(' ', '_')
                        pokemon_name_combined = f"{pokemon_name} {pokemon_subname}"
                    else:
                        print(f"Không thể tìm thấy thông tin cho Pokémon có ID: {pokemon_id}_{sub_id}")
                else:
                    pokemon_name = soup.find('p', class_='pokemon-slider__main-name').text.strip().replace(' ', '_')
                    pokemon_name_combined = pokemon_name
                
                if pokemon_no:
                    img_src = soup.find('img', class_='pokemon-img__front').get('src')
                    if img_src and img_src.endswith('.png'):
                        img_name = f"{pokemon_no}_{pokemon_name_combined}.png"
                        
                        # Kiểm tra nếu tên ảnh đã được tải xuống trước đó
                        while img_name in downloaded_images:
                            img_name = img_name[:-4] + f"_{sub_id}" + img_name[-4:]
                        
                        img_name = img_name.replace(' ', '_')  # Thêm dấu gạch dưới sau mã số của Pokémon
                        img_url = urllib.parse.urljoin(base_url, img_src)
                        download_image(img_url, img_name, folder)
                        downloaded_images.add(img_name)  # Thêm tên ảnh vào tập hợp
                else:
                    print(f"Không thể tìm thấy thông tin cho Pokémon có ID: {pokemon_id}_{sub_id}")

# Đường dẫn cơ sở của trang web và thư mục lưu trữ ảnh
base_url = 'https://vn.portal-pokemon.com/play/pokedex'
folder = 'pokemon_images'

# Phạm vi id của Pokémon bạn muốn tải xuống
start_id = 1
end_id = 905

# Gọi hàm để tải xuống ảnh
download_pokemon_images(base_url, start_id, end_id, folder)
