"""
Project: Phân tích xu hướng và giá cả hàng hóa theo thời gian
Module: Data Processing & Cleaning
Tác giả: Web Mining Analysis
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CoffeeDataProcessor:
    """Xử lý và làm sạch dữ liệu cà phê"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.df_processed = None
        
    def load_data(self):
        """Load dữ liệu từ CSV"""
        self.df = pd.read_csv(self.filepath)
        print(f"DONE Đã load {len(self.df)} bản ghi")
        print(f"DONE Cột dữ liệu: {list(self.df.columns)}")
        return self.df
    
    def extract_prices(self, text):
        """
        Trích xuất giá tiền từ text
        Ví dụ: "90.400 đồng/kg" -> [90400]
        """
        if pd.isna(text):
            return []
        
        text = str(text)
        # Pattern 1: "XXX.XXX đồng/kg" hoặc "XXX,XXX đồng/kg"
        pattern1 = r'(\d{1,3}[.,]\d{3})\s*(?:đồng|₫)(?:/kg)?'
        # Pattern 2: "XXX đồng/kg"
        pattern2 = r'(\d+)\s*(?:đồng|₫)(?:/kg)?'
        
        prices = []
        
        # Tìm pattern 1
        matches1 = re.findall(pattern1, text)
        for match in matches1:
            price_str = match.replace(',', '.').replace('.', '')
            if len(price_str) >= 4:  # Ít nhất 4 chữ số
                try:
                    price = int(price_str)
                    if 50000 < price < 200000:  # Range hợp lý cho cà phê
                        prices.append(price)
                except:
                    pass
        
        # Nếu không tìm được, tìm pattern 2
        if not prices:
            matches2 = re.findall(pattern2, text)
            for match in matches2:
                try:
                    price = int(match)
                    if 50000 < price < 200000:
                        prices.append(price)
                except:
                    pass
        
        return prices
    
    def extract_category(self, text):
        """Phân loại tin tức"""
        if pd.isna(text):
            return "Khác"
        
        text = str(text).lower()
        
        if 'arabica' in text or 'robusta' in text:
            return "Giá cà phê (Arabica/Robusta)"
        elif 'cà phê' in text or 'cafe' in text or 'coffee' in text:
            return "Tin về cà phê"
        elif 'tây nguyên' in text:
            return "Giá cà phê Tây Nguyên"
        elif 'hồ tiêu' in text or 'tiêu' in text:
            return "Giá hồ tiêu"
        elif 'gạo' in text or 'lúa' in text:
            return "Giá gạo"
        elif 'hàng hóa' in text or 'nông sản' in text:
            return "Giá nông sản chung"
        elif 'xuất khẩu' in text:
            return "Xuất khẩu"
        else:
            return "Khác"
    
    def process_data(self):
        """Xử lý dữ liệu chính"""
        df = self.df.copy()
        
        # Chuẩn hóa tên cột
        df.columns = df.columns.str.lower().str.strip()
        
        # Chuyển đổi cột time sang datetime
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        
        # Trích xuất giá từ tiêu đề
        df['prices'] = df['title'].apply(self.extract_prices)
        df['price_count'] = df['prices'].apply(len)
        
        # Lấy giá đầu tiên (nếu có)
        df['price'] = df['prices'].apply(lambda x: x[0] if len(x) > 0 else np.nan)
        
        # Phân loại tin tức
        df['category'] = df['title'].apply(self.extract_category)
        
        # Tạo các cột ngày tháng
        df['date'] = df['time'].dt.date
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        df['week'] = df['time'].dt.isocalendar().week
        df['dayofweek'] = df['time'].dt.dayofweek
        
        # Đếm từ trong tiêu đề
        df['title_length'] = df['title'].apply(lambda x: len(str(x).split()))
        
        # Lựa chọn các cột quan trọng
        self.df_processed = df[[
            'title', 'time', 'date', 'year', 'month', 'day', 'week', 
            'price', 'price_count', 'category', 'source', 'title_length'
        ]]
        
        # Loại bỏ các hàng không có timestamp
        self.df_processed = self.df_processed.dropna(subset=['time'])
        
        print(f"\n Kết quả xử lý:")
        print(f"   - Tổng bản ghi: {len(self.df_processed)}")
        print(f"   - Bản ghi có giá: {self.df_processed['price'].notna().sum()}")
        print(f"   - Ngày từ: {self.df_processed['date'].min()}")
        print(f"   - Ngày đến: {self.df_processed['date'].max()}")
        print(f"   - Số lượng categoria: {self.df_processed['category'].nunique()}")
        
        return self.df_processed
    
    def get_statistics(self):
        """Lấy thống kê cơ bản"""
        if self.df_processed is None:
            return None
        
        stats = {
            'total_records': len(self.df_processed),
            'records_with_price': self.df_processed['price'].notna().sum(),
            'avg_price': self.df_processed['price'].mean(),
            'min_price': self.df_processed['price'].min(),
            'max_price': self.df_processed['price'].max(),
            'std_price': self.df_processed['price'].std(),
            'date_range': f"{self.df_processed['date'].min()} đến {self.df_processed['date'].max()}",
            'sources_count': self.df_processed['source'].nunique(),
            'categories': self.df_processed['category'].value_counts().to_dict()
        }
        
        return stats
    
    def save_processed_data(self, output_path):
        """Lưu dữ liệu đã xử lý"""
        if self.df_processed is not None:
            self.df_processed.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"\nDONE Dữ liệu đã xử lý lưu vào: {output_path}")
        else:
            print("Chưa có dữ liệu đã xử lý!")


if __name__ == "__main__":
    # Khởi tạo processor
    processor = CoffeeDataProcessor('data_cafe.csv')
    
    # Load dữ liệu
    processor.load_data()
    
    # Xử lý dữ liệu
    df_processed = processor.process_data()
    
    # Lấy thống kê
    stats = processor.get_statistics()
    
    print("\n" + "="*60)
    print(" THỐNG KÊ CƠ BẢN")
    print("="*60)
    for key, value in stats.items():
        if key != 'categories':
            print(f"{key:.<40} {value}")
    
    print("\n PHÂN LOẠI TIN TỨC:")
    for category, count in stats['categories'].items():
        print(f"   {category:.<40} {count} bản ghi")
    
    # Lưu dữ liệu đã xử lý
    processor.save_processed_data('data_cafe_processed.csv')
    
    # Hiển thị mẫu dữ liệu
    print("\n" + "="*60)
    print(" MẪU DỮ LIỆU (5 hàng đầu với giá):")
    print("="*60)
    sample = df_processed[df_processed['price'].notna()].head()
    for idx, row in sample.iterrows():
        print(f"\n[{row['date']}] {row['category']}")
        print(f"  Tiêu đề: {row['title'][:70]}...")
        print(f"  Giá: {row['price']:,.0f} đ/kg | Nguồn: {row['source']}")
