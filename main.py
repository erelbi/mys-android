from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem, OneLineIconListItem, IconLeftWidget
from kivy.utils import platform
from kivymd.uix.list import MDList
from kivy.properties import StringProperty
import sqlite3
import json
from datetime import datetime
from kivy.config import Config
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.storage.jsonstore import JsonStore
from android.permissions import request_permissions, Permission

##DB##
import os
import shutil
from datetime import datetime
from kivy.utils import platform


# SQLite veritabanı bağlantısı oluşturma
conn = None
cursor = None   
def create_connection():
        global conn, cursor
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(IconLeftWidget(icon=self.icon))

# SQLite veritabanı bağlantısı oluşturma
conn = sqlite3.connect('store.db')
cursor = conn.cursor()
    

# Tablo oluşturma (müşteri ve ürün için)
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    contact TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    stock INTEGER,
    stock_date TEXT,
    price REAL
)
''')
conn.commit()

KV = '''
ScreenManager:
    MainScreen:
    CustomerScreen:
    ProductScreen:
    SalesScreen:
    ProductSelectScreen:
    CustomerEditScreen:
    ProductEditScreen:

<MainScreen>:
    name: 'main'
    
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Mağaza Yönetim Sistemi"
            elevation: 2

        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                size_hint_y: 0.8

                BoxLayout:
                    spacing: dp(20)
                    size_hint_y: 0.25

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(10)
                        elevation: 5
                        on_release: app.root.current = 'customer'

                        MDIcon:
                            icon: "account-group"
                            halign: "center"
                            font_size: "36sp"

                        MDLabel:
                            text: "Müşteriler"
                            halign: "center"
                            font_style: "Caption"

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(10)
                        elevation: 5
                        on_release: app.root.current = 'product'

                        MDIcon:
                            icon: "package-variant-closed"
                            halign: "center"
                            font_size: "36sp"

                        MDLabel:
                            text: "Ürünler"
                            halign: "center"
                            font_style: "Caption"

                BoxLayout:
                    spacing: dp(20)
                    size_hint_y: 0.25

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(10)
                        elevation: 5
                        on_release: app.check_customers()

                        MDIcon:
                            icon: "cash-register"
                            halign: "center"
                            font_size: "36sp"

                        MDLabel:
                            text: "Satış"
                            halign: "center"
                            font_style: "Caption"

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(10)
                        elevation: 5
                        on_release: app.show_delete_customer_dialog()

                        MDIcon:
                            icon: "account-remove"
                            halign: "center"
                            font_size: "36sp"

                        MDLabel:
                            text: "Müşteri Sil"
                            halign: "center"
                            font_style: "Caption"

                BoxLayout:
                    spacing: dp(20)
                    size_hint_y: 0.25

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(10)
                        elevation: 5
                        on_release: app.show_delete_product_dialog()

                        MDIcon:
                            icon: "package-variant-remove"
                            halign: "center"
                            font_size: "36sp"

                        MDLabel:
                            text: "Ürün Sil"
                            halign: "center"
                            font_style: "Caption"

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(10)
                        elevation: 5
                        on_release: app.show_sales_history()

                        MDIcon:
                            icon: "history"
                            halign: "center"
                            font_size: "36sp"

                        MDLabel:
                            text: "Satış Geçmişi"
                            halign: "center"
                            font_style: "Caption"
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(50)

                    MDRaisedButton:
                        text: "DB Dışa Aktar"
                        icon: "database-export"
                        on_release: app.export_database()
                        size_hint_x: 0.5

                    MDRaisedButton:
                        text: "DB İçe Aktar"
                        icon: "database-import"
                        on_release: app.import_database()
                        size_hint_x: 0.5

            MDRaisedButton:
                text: "Veritabanını Sıfırla"
                icon: "database-refresh"
                on_release: app.reset_database()
                size_hint_y: None
                height: dp(50)
                md_bg_color: app.theme_cls.error_color
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_x: 1
         

<CustomerScreen>:
    name: 'customer'

    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Müşteri Ekle/Düzenle"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_main()]]
            elevation: 2

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(20)
                adaptive_height: True

                MDTextField:
                    id: customer_name
                    hint_text: "Müşteri Adı"

                MDTextField:
                    id: customer_address
                    hint_text: "Adres"

                MDTextField:
                    id: customer_contact
                    hint_text: "İletişim"

                MDRaisedButton:
                    text: "Müşteri Ekle"
                    pos_hint: {"center_x": .5}
                    on_release: app.save_customer()

                MDRaisedButton:
                    text: "Müşterileri Listele"
                    pos_hint: {"center_x": .5}
                    on_release: app.load_customer_list()

                ScrollView:
                    size_hint: (1, None)
                    height: dp(200)
                    BoxLayout:
                        id: customer_list
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height

<CustomerEditScreen>:
    name: 'customer_edit'
    
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Müşteri Düzenle"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_customer()]]
            elevation: 2

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(20)
                adaptive_height: True

                MDTextField:
                    id: edit_customer_name
                    hint_text: "Müşteri Adı"

                MDTextField:
                    id: edit_customer_address
                    hint_text: "Adres"

                MDTextField:
                    id: edit_customer_contact
                    hint_text: "İletişim"

                MDRaisedButton:
                    text: "Müşteriyi Güncelle"
                    pos_hint: {"center_x": .5}
                    on_release: app.update_customer()

<ProductScreen>:
    name: 'product'
    
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Ürün Ekle/Düzenle"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_main()]]
            elevation: 2

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(20)
                adaptive_height: True

                MDTextField:
                    id: product_name
                    hint_text: "Ürün İsmi"
                    helper_text: "Ürünün adını girin"
                    helper_text_mode: "on_focus"

                MDTextField:
                    id: product_stock
                    hint_text: "Stok Sayısı"
                    input_filter: 'int'
                    helper_text: "Stok miktarını sayı olarak girin"
                    helper_text_mode: "on_focus"

                MDTextField:
                    id: product_date
                    hint_text: "Stok Giriş Tarihi"
                    helper_text: "YYYY-MM-DD formatında girin"
                    helper_text_mode: "on_focus"

                MDTextField:
                    id: product_price
                    hint_text: "Fiyat"
                    input_filter: 'float'
                    helper_text: "Ürün fiyatını girin (örn: 10.99)"
                    helper_text_mode: "on_focus"

                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    adaptive_height: True
                    pos_hint: {'center_x': .5}

                    MDRaisedButton:
                        text: "Kaydet"
                        on_release: app.save_product()

                    MDRaisedButton:
                        text: "Ürünleri Listele"
                        on_release: app.load_product_list()

                MDLabel:
                    text: "Ürün Listesi"
                    font_style: "H6"
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1]
                    padding: [0, dp(20)]

                ScrollView:
                    size_hint: (1, None)
                    height: min(root.height * 0.4, dp(300))  # Ekranın %40'ı veya en fazla 300dp

                    MDList:
                        id: product_list
                        spacing: dp(4)
                        padding: dp(10)

<SalesScreen>:
    name: 'sales'
    
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Satış"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_main()]]
            elevation: 2

        MDLabel:
            text: "Müşteri Seçin"
            font_style: "H5"
            halign: "center"
            size_hint_y: None
            height: dp(50)

        ScrollView:
            BoxLayout:
                id: customer_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

<ProductSelectScreen>:
    name: 'product_select'
    
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Ürün Seçin"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_sales()]]
            elevation: 2

        ScrollView:
            MDList:
                id: product_list
                spacing: dp(4)
                padding: dp(10)

        MDLabel:
            id: total_label
            text: "Toplam: 0.00"
            halign: "center"
            font_style: "H6"
            size_hint_y: None
            height: dp(50)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(48)
            spacing: dp(10)
            padding: [dp(10), 0, dp(10), dp(10)]

            MDRaisedButton:
                text: "Hesapla"
                on_release: app.calculate_total()

            MDRaisedButton:
                text: "Satışı Tamamla"
                on_release: app.complete_sale()

            MDRaisedButton:
                text: "Paylaş"
                on_release: app.share_result()

<ProductEditScreen>:
    name: 'product_edit'
    
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Ürün Düzenle"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_product()]]
            elevation: 2

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(20)
                adaptive_height: True

                MDTextField:
                    id: edit_product_name
                    hint_text: "Ürün İsmi"

                MDTextField:
                    id: edit_product_stock
                    hint_text: "Stok Sayısı"
                    input_filter: 'int'

                MDTextField:
                    id: edit_product_date
                    hint_text: "Stok Giriş Tarihi"

                MDTextField:
                    id: edit_product_price
                    hint_text: "Fiyat"
                    input_filter: 'float'

                MDRaisedButton:
                    text: "Ürünü Güncelle"
                    pos_hint: {"center_x": .5}
                    on_release: app.update_product()
'''
class MainScreen(Screen):
    pass

class CustomerScreen(Screen):
    pass

class ProductScreen(Screen):
    pass

class SalesScreen(Screen):
    pass

class ProductSelectScreen(Screen):
    pass

class CustomerEditScreen(Screen):
    pass

class ProductEditScreen(Screen):
    pass

class DisclaimerPopup(MDDialog):
    def __init__(self, **kwargs):
        super(DisclaimerPopup, self).__init__(
            title="Disclaimer / Sorumluluk Reddi",
            text="[EN] This application is for educational purposes only. The information provided is not guaranteed, and the application developer cannot be held responsible for any consequences arising from its use. By using this application, you agree to these terms.\n\n[TR] Bu uygulama sadece eğitim amaçlıdır. Burada sunulan bilgiler garanti edilmez ve kullanımından doğacak sonuçlardan uygulama geliştiricisi sorumlu tutulamaz. Uygulamayı kullanarak bu şartları kabul etmiş sayılırsınız.",
            buttons=[
                MDFlatButton(
                    text="Accept / Kabul Et",
                    on_release=self.accept_disclaimer
                )
            ]
        )
        self.auto_dismiss = False
        self.app = kwargs.get('app')

    def accept_disclaimer(self, *args):
        store = JsonStore('disclaimer.json')
        store.put('accepted', value=True)
        self.dismiss()



class MainApp(MDApp):
   
       

    dialog = None
    total = 0
    selected_customer = None
    product_quantities = {}
    last_calculation_result = ""
    current_edit_customer_id = None
    current_edit_product_id = None
    sale_details = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        create_connection()

       

   

    def on_start(self):
        store = JsonStore('disclaimer.json')
        if not store.exists('accepted'):
            disclaimer = DisclaimerPopup(app=self)
            disclaimer.open()
    # Satış geçmişi tablosunu oluştur (eğer yoksa)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_history (
            id INTEGER PRIMARY KEY,
            customer_name TEXT,
            total_amount REAL,
            sale_date TEXT,
            sale_details TEXT
        )
        ''')
        conn.commit()

    #def on_start(self):
    #    # Satış geçmişi tablosunu oluştur (eğer yoksa)
    #    cursor.execute('''
    #    CREATE TABLE IF NOT EXISTS sales_history (
    #        id INTEGER PRIMARY KEY,
    #        customer_name TEXT,
    #        total_amount REAL,
    #        sale_date TEXT
    #    )
    #    ''')
    #    conn.commit()
    
    def get_product_price(self, product_id):
        cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"Ürün fiyatı bulunamadı: ID {product_id}")  # Debug bilgisi
            return 0


    def calculate_total(self):
        total = 0
        sale_items = []
        for product_id, quantity in self.product_quantities.items():
            cursor.execute("SELECT product_name, price FROM products WHERE id=?", (product_id,))
            product = cursor.fetchone()
            if product and product[1]:
                product_name, price = product
                item_total = quantity * float(price)
                total += item_total
                sale_items.append(f"{product_name} - Adet: {quantity} - Toplam: {item_total:.2f} TL")

        self.total = total
        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.sale_details = f"Müşteri: {self.selected_customer}\n"
        self.sale_details += f"Tarih: {sale_date}\n\n"
        self.sale_details += "\n".join(sale_items)
        self.sale_details += f"\n\nGenel Toplam: {total:.2f} TL"

        total_text = f"Toplam: {total:.2f}"
        self.root.get_screen('product_select').ids.total_label.text = total_text
        self.last_calculation_result = self.sale_details
        self.show_popup("Hesaplama Tamamlandı", self.last_calculation_result)
    
    def complete_sale(self):
        if not self.product_quantities:
            self.show_popup("Hata", "Lütfen önce ürün seçin ve hesaplayın.")
            return

        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        sale_details = []
        total = 0
        for product_id, quantity in self.product_quantities.items():
            cursor.execute("SELECT product_name, price FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()
            if product:
                product_name, price = product
                item_total = quantity * price
                total += item_total
                sale_details.append({
                    "product_name": product_name,
                    "quantity": quantity,
                    "price": price,
                    "item_total": item_total
                })

        sale_details_json = json.dumps(sale_details)

        cursor.execute('''
        INSERT INTO sales_history (customer_name, total_amount, sale_date, sale_details) 
        VALUES (?, ?, ?, ?)
        ''', (self.selected_customer, total, sale_date, sale_details_json))
        conn.commit()

        for product_id, quantity in self.product_quantities.items():
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
        conn.commit()

        self.show_popup("Başarılı", "Satış tamamlandı ve kaydedildi.")
        self.product_quantities.clear()
        self.root.current = 'main'
    
    #def complete_sale(self):
    #    if not self.product_quantities:
    #        self.show_popup("Hata", "Lütfen önce ürün seçin ve hesaplayın.")
    #        return
#
    #    # Satışı kaydet
    #    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #    cursor.execute('''
    #    INSERT INTO sales_history (customer_name, total_amount, sale_date, sale_details) 
    #    VALUES (?, ?, ?, ?)
    #    ''', (self.selected_customer, self.total, sale_date, self.sale_details))
    #    conn.commit()
#
    #    print(f"Satış kaydedildi: {self.selected_customer}, {self.total}, {sale_date}")  # Debug bilgisi
#
    #    for product_id, quantity in self.product_quantities.items():
    #        cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
    #    conn.commit()
#
    #    self.show_popup("Başarılı", "Satış tamamlandı ve kaydedildi.")
    #    self.product_quantities.clear()
    #    self.root.current = 'main'
    #def complete_sale(self):
    #    if not self.product_quantities:
    #        self.show_popup("Hata", "Lütfen önce ürün seçin ve hesaplayın.")
    #        return
#
    #    total = 0
    #    for product_id, quantity in self.product_quantities.items():
    #        price = self.get_product_price(product_id)
    #        total += quantity * price
#
    #    # Satışı kaydet
    #    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #    cursor.execute('''
    #    INSERT INTO sales_history (customer_name, total_amount, sale_date) 
    #    VALUES (?, ?, ?)
    #    ''', (self.selected_customer, total, sale_date))
    #    conn.commit()
#
    #    print(f"Satış kaydedildi: {self.selected_customer}, {total}, {sale_date}")  # Debug bilgisi
#
    #    for product_id, quantity in self.product_quantities.items():
    #        cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
    #    conn.commit()
#
    #    self.show_popup("Başarılı", "Satış tamamlandı ve kaydedildi.")
    #    self.product_quantities.clear()
    #    self.root.current = 'main'

#

    #def show_sales_history(self):
    #    cursor.execute("SELECT customer_name, total_amount, sale_date FROM sales_history ORDER BY sale_date DESC")
    #    sales = cursor.fetchall()
#
    #    print(f"Çekilen satış kayıtları: {sales}")  # Debug bilgisi
#
    #    if not sales:
    #        self.show_popup("Bilgi", "Henüz satış kaydı bulunmamaktadır.")
    #        return
#
    #    content = MDList()
    #    for sale in sales:
    #        item = ThreeLineListItem(
    #            text=f"Müşteri: {sale[0]}",
    #            secondary_text=f"Toplam: {sale[1]:.2f} TL",
    #            tertiary_text=f"Tarih: {sale[2]}"
    #        )
    #        content.add_widget(item)
#
    #    dialog = MDDialog(
    #        title="Satış Geçmişi",
    #        type="custom",
    #        content_cls=content,
    #        size_hint=(0.9, 0.9),
    #        buttons=[
    #            MDFlatButton(
    #                text="KAPAT",
    #                on_release=lambda x: dialog.dismiss()
    #            )
    #        ]
    #    )
    #    dialog.open()

    def show_sales_history(self):
        cursor.execute("SELECT id, customer_name, total_amount, sale_date, sale_details FROM sales_history ORDER BY sale_date DESC")
        sales = cursor.fetchall()

        if not sales:
            self.show_popup("Bilgi", "Henüz satış kaydı bulunmamaktadır.")
            return

        content = MDList()
        for sale in sales:
            sale_id, customer_name, total_amount, sale_date, sale_details = sale
            sale_details = json.loads(sale_details)
            
            item = ThreeLineListItem(
                text=f"Müşteri: {customer_name}",
                secondary_text=f"Tarih: {sale_date}",
                tertiary_text=f"Toplam: {total_amount:.2f} TL"
            )
            item.bind(on_release=lambda x, sale_id=sale_id: self.show_sale_details(sale_id))
            content.add_widget(item)

        dialog = MDDialog(
            title="Satış Geçmişi",
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.9),
            buttons=[
                MDFlatButton(
                    text="KAPAT",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    
    def show_sale_details(self, sale_id):
        cursor.execute("SELECT customer_name, total_amount, sale_date, sale_details FROM sales_history WHERE id = ?", (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            self.show_popup("Hata", "Satış detayları bulunamadı.")
            return

        customer_name, total_amount, sale_date, sale_details = sale
        sale_details = json.loads(sale_details)

        content = MDList()
        content.add_widget(OneLineListItem(text=f"Müşteri: {customer_name}"))
        content.add_widget(OneLineListItem(text=f"Tarih: {sale_date}"))
        
        for item in sale_details:
            content.add_widget(ThreeLineListItem(
                text=f"{item['product_name']}",
                secondary_text=f"Adet: {item['quantity']} x {item['price']:.2f} TL",
                tertiary_text=f"Toplam: {item['item_total']:.2f} TL"
            ))
        
        content.add_widget(OneLineListItem(text=f"Genel Toplam: {total_amount:.2f} TL"))

        dialog = MDDialog(
            title="Satış Detayları",
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.9),
            buttons=[
                MDFlatButton(
                    text="KAPAT",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
#
    # Veritabanı içeriğini kontrol etmek için yeni bir fonksiyon
    def check_database(self):
        cursor.execute("SELECT * FROM sales_history")
        sales = cursor.fetchall()
        print(f"Veritabanındaki tüm satış kayıtları: {sales}")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Veritabanındaki tablolar: {tables}")

    def reset_database(self):
        confirm_dialog = MDDialog(
            title="Onay",
            text="Tüm verileri silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.",
            buttons=[
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="EVET, SİL",
                    on_release=lambda x: self.perform_reset(confirm_dialog)
                ),
            ],
        )
        confirm_dialog.open()

    def clear_customer_list(self):
        customer_screen = self.root.get_screen('customer')
        customer_list = customer_screen.ids.customer_list
        customer_list.clear_widgets()

    def clear_product_list(self):
        product_screen = self.root.get_screen('product')
        product_list = product_screen.ids.product_list
        product_list.clear_widgets()

    def perform_reset(self, dialog):
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM sales_history")  
        conn.commit()
        dialog.dismiss()
        self.show_popup("Başarılı", "Veritabanı sıfırlandı.")


        self.clear_customer_list()
        self.clear_product_list()

        self.root.current = 'main'


    def go_back_to_main(self):
        self.root.current = 'main'

    def go_back_to_sales(self):
        self.product_quantities.clear()  
        self.root.current = 'sales'

    def go_back_to_customer(self):
        self.root.current = 'customer'
        self.load_customer_list() 

    def go_back_to_product(self):
        self.root.current = 'product'
        self.load_product_list()  


    def build(self):
        return Builder.load_string(KV)

    def save_customer(self):
        name = self.root.get_screen('customer').ids.customer_name.text
        address = self.root.get_screen('customer').ids.customer_address.text
        contact = self.root.get_screen('customer').ids.customer_contact.text

        if not name or not address or not contact:
            self.show_popup("Hata", "Lütfen tüm müşteri bilgilerini doldurun.")
            return
        
        cursor.execute("INSERT INTO customers (name, address, contact) VALUES (?, ?, ?)", (name, address, contact))
        conn.commit()

        self.show_popup("Başarılı", "Müşteri kaydedildi")
        self.clear_customer_inputs()
        self.load_customer_list()

    def show_popup(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="TAMAM",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()

    def clear_customer_inputs(self):
        customer_screen = self.root.get_screen('customer')
        customer_screen.ids.customer_name.text = ""
        customer_screen.ids.customer_address.text = ""
        customer_screen.ids.customer_contact.text = ""

    def save_product(self):
        product_name = self.root.get_screen('product').ids.product_name.text
        stock = self.root.get_screen('product').ids.product_stock.text
        stock_date = self.root.get_screen('product').ids.product_date.text
        price = self.root.get_screen('product').ids.product_price.text

        if not product_name or not stock or not stock_date or not price:
            self.show_popup("Hata", "Lütfen tüm ürün bilgilerini doldurun.")
            return

        cursor.execute("INSERT INTO products (product_name, stock, stock_date, price) VALUES (?, ?, ?, ?)", (product_name, stock, stock_date, price))
        conn.commit()

        self.show_popup("Başarılı", "Ürün kaydedildi")
        self.clear_product_inputs()
        self.load_product_list()

    def update_customer(self):
        name = self.root.get_screen('customer_edit').ids.edit_customer_name.text
        address = self.root.get_screen('customer_edit').ids.edit_customer_address.text
        contact = self.root.get_screen('customer_edit').ids.edit_customer_contact.text

        cursor.execute("UPDATE customers SET name = ?, address = ?, contact = ? WHERE id = ?",
                       (name, address, contact, self.current_edit_customer_id))
        conn.commit()

        self.show_popup("Başarılı", "Müşteri güncellendi")
        self.root.current = 'customer'
        self.load_customer_list()

  

    def load_customer_list(self):
        customer_screen = self.root.get_screen('customer')
        customer_list = customer_screen.ids.customer_list
        customer_list.clear_widgets()

        cursor.execute("SELECT id, name, address, contact FROM customers")
        customers = cursor.fetchall()

        if not customers:
            self.show_dialog("Bilgi", "Hiç müşteri bulunamadı.")
            return

        for customer in customers:
            item = ThreeLineListItem(
                text=customer[1],
                secondary_text=customer[2],
                tertiary_text=customer[3]
            )
            item.bind(on_release=lambda x, id=customer[0]: self.edit_customer(id))
            customer_list.add_widget(item)

    def load_sales_customer_list(self):
        sales_screen = self.root.get_screen('sales')
        customer_list = sales_screen.ids.customer_list
        customer_list.clear_widgets()

        cursor.execute("SELECT id, name, address, contact FROM customers")
        customers = cursor.fetchall()

        for customer in customers:
            item = ThreeLineListItem(
                text=customer[1],
                secondary_text=customer[2],
                tertiary_text=customer[3]
            )
            item.bind(on_release=lambda x, id=customer[0], name=customer[1]: self.select_customer(id, name))
            customer_list.add_widget(item)

    def load_product_list(self):
        product_screen = self.root.get_screen('product')
        product_list = product_screen.ids.product_list
        product_list.clear_widgets()

        cursor.execute("SELECT id, product_name, stock, price FROM products")
        products = cursor.fetchall()

        if not products:
            self.show_dialog("Bilgi", "Hiç ürün bulunamadı.")
            return

        for product in products:
            item = ThreeLineListItem(
                text=product[1],
                secondary_text=f"Stok: {product[2]}",
                tertiary_text=f"Fiyat: {product[3]}"
            )
            item.bind(on_release=lambda x, id=product[0]: self.edit_product(id))
            product_list.add_widget(item)

    def select_customer(self, customer_id, customer_name):
        self.selected_customer = customer_name
        self.load_product_select_screen(customer_id)
        self.root.current = 'product_select'

    #def load_product_select_screen(self, customer_id):
    #    product_screen = self.root.get_screen('product_select')
    #    product_list = product_screen.ids.product_list
    #    product_list.clear_widgets()
#
    #    cursor.execute("SELECT id, product_name, price, stock FROM products")
    #    products = cursor.fetchall()
#
    #    for product_id, product_name, price, stock in products:
    #        layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
    #        layout.add_widget(TwoLineListItem(text=product_name, secondary_text=f"Fiyat: {price}, Stok: {stock}"))
    #        quantity_input = MDTextField(hint_text="Adet", input_filter='int', size_hint=(0.3, None), height=48)
    #        quantity_input.bind(text=lambda instance, value, prod_id=product_id: self.update_quantity(prod_id, value))
    #        layout.add_widget(quantity_input)
    #        product_list.add_widget(layout)

    def load_product_select_screen(self, customer_id):
        product_screen = self.root.get_screen('product_select')
        product_list = product_screen.ids.product_list
        product_list.clear_widgets()

        cursor.execute("SELECT id, product_name, price, stock FROM products")
        products = cursor.fetchall()

        for product_id, product_name, price, stock in products:
            item = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(72), padding=[dp(16), dp(8)])
            
            info_box = BoxLayout(orientation='vertical', size_hint_x=0.7)
            info_box.add_widget(MDLabel(text=product_name, font_style="Subtitle1"))
            info_box.add_widget(MDLabel(text=f"Fiyat: {price}, Stok: {stock}", font_style="Caption"))
            
            item.add_widget(info_box)
            
            quantity_input = MDTextField(
                hint_text="Adet",
                input_filter='int',
                size_hint=(None, None),
                width=dp(96),
                height=dp(48)
            )
            quantity_input.bind(text=lambda instance, value, prod_id=product_id: self.update_quantity(prod_id, value))
            
            item.add_widget(quantity_input)
            product_list.add_widget(item)
    def update_quantity(self, product_id, value):
        try:
            quantity = int(value)
            self.product_quantities[product_id] = quantity
        except ValueError:
            pass

    

    def share_result(self):
        if self.last_calculation_result:
            if platform == 'android':
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                String = autoclass('java.lang.String')
                intent = Intent()
                intent.setAction(Intent.ACTION_SEND)
                intent.setType('text/plain')
                intent.putExtra(Intent.EXTRA_TEXT, String(self.last_calculation_result))
                chooser = Intent.createChooser(intent, String('Paylaş'))
                PythonActivity.mActivity.startActivity(chooser)
            else:
                self.show_dialog("Bilgi", "Bu özellik sadece Android'de çalışır.")
        else:
            self.show_dialog("Hata", "Paylaşılacak hesaplama sonucu bulunamadı.")
    


  

    def edit_customer(self, customer_id):
        self.current_edit_customer_id = customer_id
        cursor.execute("SELECT name, address, contact FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        if customer:
            edit_screen = self.root.get_screen('customer_edit')
            edit_screen.ids.edit_customer_name.text = customer[0]
            edit_screen.ids.edit_customer_address.text = customer[1]
            edit_screen.ids.edit_customer_contact.text = customer[2]
            self.root.current = 'customer_edit'



 

    


    def close_dialog(self, *args):
        self.dialog.dismiss()

    def update_product(self):
        name = self.root.get_screen('product_edit').ids.edit_product_name.text
        stock = self.root.get_screen('product_edit').ids.edit_product_stock.text
        date = self.root.get_screen('product_edit').ids.edit_product_date.text
        price = self.root.get_screen('product_edit').ids.edit_product_price.text

        if not name or not stock or not date or not price:
            self.show_popup("Hata", "Lütfen tüm ürün bilgilerini doldurun.")
            return

        cursor.execute("UPDATE products SET product_name = ?, stock = ?, stock_date = ?, price = ? WHERE id = ?",
                    (name, stock, date, price, self.current_edit_product_id))
        conn.commit()

        self.show_popup("Başarılı", "Ürün güncellendi.")
        self.root.current = 'product'
        self.load_product_list()

    def show_popup(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="TAMAM",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()

    def edit_product(self, product_id):
        self.current_edit_product_id = product_id
        cursor.execute("SELECT product_name, stock, stock_date, price FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if product:
            edit_screen = self.root.get_screen('product_edit')
            edit_screen.ids.edit_product_name.text = product[0]
            edit_screen.ids.edit_product_stock.text = str(product[1])
            edit_screen.ids.edit_product_date.text = product[2]
            edit_screen.ids.edit_product_price.text = str(product[3])
            self.root.current = 'product_edit'

    def load_product_list(self):
        product_screen = self.root.get_screen('product')
        product_list = product_screen.ids.product_list
        product_list.clear_widgets()

        cursor.execute("SELECT id, product_name, stock, price FROM products")
        products = cursor.fetchall()

        if not products:
            self.show_popup("Bilgi", "Hiç ürün bulunamadı.")
            return

        for product in products:
            item = ThreeLineListItem(
                text=product[1],
                secondary_text=f"Stok: {product[2]}",
                tertiary_text=f"Fiyat: {product[3]}"
            )
            item.bind(on_release=lambda x, id=product[0]: self.edit_product(id))
            product_list.add_widget(item)
    
  

    #def calculate_total(self):
    #    total = 0
    #    for product_id, quantity in self.product_quantities.items():
    #        cursor.execute("SELECT price FROM products WHERE id=?", (product_id,))
    #        price = cursor.fetchone()
    #        if price and price[0]:
    #            total += quantity * float(price[0])
#
    #    self.total = total
    #    total_text = f"Toplam: {total:.2f}"
    #    self.root.get_screen('product_select').ids.total_label.text = total_text
    #    self.last_calculation_result = f"Müşteri: {self.selected_customer}\n{total_text}"
    #    self.show_popup("Hesaplama Tamamlandı", self.last_calculation_result)
#
    def show_popup(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="TAMAM",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()

    def check_customers(self):
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]

        if customer_count == 0:
            self.show_popup("Müşteri Yok", "Lütfen önce müşteri ekleyin.")
            self.root.current = 'main'
        else:
            self.load_sales_customer_list()
            self.root.current = 'sales'

    def share_result(self):
        if self.last_calculation_result:
            if platform == 'android':
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                String = autoclass('java.lang.String')
                intent = Intent()
                intent.setAction(Intent.ACTION_SEND)
                intent.setType('text/plain')
                intent.putExtra(Intent.EXTRA_TEXT, String(self.last_calculation_result))
                chooser = Intent.createChooser(intent, String('Paylaş'))
                PythonActivity.mActivity.startActivity(chooser)
            else:
                self.show_popup("Bilgi", "Bu özellik sadece Android'de çalışır.")
        else:
            self.show_popup("Hata", "Paylaşılacak hesaplama sonucu bulunamadı.")



    
    def show_delete_customer_dialog(self):
        cursor.execute("SELECT id, name FROM customers")
        customers = cursor.fetchall()
        if not customers:
            self.show_popup("Bilgi", "Silinecek müşteri bulunmamaktadır.")
            return

        content = MDList(md_bg_color=self.theme_cls.bg_dark)
        for customer in customers:
            item = IconListItem(
                text=f"{customer[1]} (ID: {customer[0]})",
                icon="account",
                on_release=lambda x, id=customer[0]: self.delete_customer(id)
            )
            content.add_widget(item)

        dialog = MDDialog(
            title="Müşteri Sil",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=min(500, len(customers) * 56 + 100),
        )
        dialog.open()

    def show_delete_product_dialog(self):
        cursor.execute("SELECT id, product_name FROM products")
        products = cursor.fetchall()
        if not products:
            self.show_popup("Bilgi", "Silinecek ürün bulunmamaktadır.")
            return

        content = MDList(md_bg_color=self.theme_cls.bg_dark)
        for product in products:
            item = IconListItem(
                text=f"{product[1]} (ID: {product[0]})",
                icon="package-variant",
                on_release=lambda x, id=product[0]: self.delete_product(id)
            )
            content.add_widget(item)

        dialog = MDDialog(
            title="Ürün Sil",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=min(500, len(products) * 56 + 100),
        )
        dialog.open()



    def delete_customer(self, customer_id):
        confirm_dialog = MDDialog(
            title="Onay",
            text="Bu müşteriyi silmek istediğinizden emin misiniz?",
            buttons=[
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SİL",
                    on_release=lambda x: self.perform_customer_delete(customer_id, confirm_dialog)
                ),
            ],
        )
        confirm_dialog.open()

    def perform_customer_delete(self, customer_id, dialog):
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        dialog.dismiss()
        self.show_popup("Başarılı", "Müşteri silindi.")
        self.show_delete_customer_dialog()  # Listeyi yenile

    def delete_product(self, product_id):
        confirm_dialog = MDDialog(
            title="Onay",
            text="Bu ürünü silmek istediğinizden emin misiniz?",
            buttons=[
                MDFlatButton(
                    text="İPTAL",
                    on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SİL",
                    on_release=lambda x: self.perform_product_delete(product_id, confirm_dialog)
                ),
            ],
        )
        confirm_dialog.open()

    def perform_product_delete(self, product_id, dialog):
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        dialog.dismiss()
        self.show_popup("Başarılı", "Ürün silindi.")
        self.show_delete_product_dialog() 


    

    def clear_customer_inputs(self):
        customer_screen = self.root.get_screen('customer')
        customer_screen.ids.customer_name.text = ""
        customer_screen.ids.customer_address.text = ""
        customer_screen.ids.customer_contact.text = ""

    def clear_product_inputs(self):
        product_screen = self.root.get_screen('product')
        product_screen.ids.product_name.text = ""
        product_screen.ids.product_stock.text = ""
        product_screen.ids.product_date.text = ""
        product_screen.ids.product_price.text = ""


    def export_database(self):
        db_path = os.path.abspath('store.db')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"store_backup_{timestamp}.db"

        try:
            if platform == 'android':
                from android.storage import primary_external_storage_path
                export_dir = os.path.join(primary_external_storage_path(), 'Download')
                export_path = os.path.join(export_dir, export_filename)

                
                with open(db_path, 'rb') as src, open(export_path, 'wb') as dst:
                    dst.write(src.read())

                self.show_popup("Başarılı", f"Veritabanı dışa aktarıldı:\n{export_path}")
                self.share_file(export_path)
            else:
                export_dir = os.path.expanduser('~')
                export_path = os.path.join(export_dir, export_filename)

                shutil.copy2(db_path, export_path) #Burası Düzgün çalışmıyor. İzinler
                self.show_popup("Başarılı", f"Veritabanı dışa aktarıldı:\n{export_path}")
                self.share_file(export_path)

        except Exception as e:
            self.show_popup("Hata", f"Dışa aktarma başarısız: {str(e)}")



    def import_database(self):
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        global conn, cursor  

        if platform == 'android':
            from android.storage import primary_external_storage_path
            import_dir = os.path.join(primary_external_storage_path(), 'Download')
        else:
            import_dir = os.path.expanduser('~')  

        backup_files = [f for f in os.listdir(import_dir) if f.startswith("store_backup_") and f.endswith(".db")]
        if not backup_files:
            self.show_popup("Hata", "İçe aktarılacak yedek dosyası bulunamadı.")
            return
        
        latest_backup = max(backup_files)
        import_path = os.path.join(import_dir, latest_backup)
        
        try:
            conn.close()
            
            shutil.copy2(import_path, 'store.db')
            
            conn = sqlite3.connect('store.db')
            cursor = conn.cursor()
            
            self.show_popup("Başarılı", "Veritabanı içe aktarıldı.")
        except Exception as e:
            self.show_popup("Hata", f"İçe aktarma başarısız: {str(e)}")

    def share_file(self, file_path):
        if platform == 'android':
            from jnius import autoclass, cast
            from android import mActivity
            
            Intent = autoclass('android.content.Intent')
            File = autoclass('java.io.File')
            FileProvider = autoclass('androidx.core.content.FileProvider')
            Context = autoclass('android.content.Context')
            
            file = File(file_path)
            context = cast('android.content.Context', mActivity.getApplicationContext())
            file_uri = FileProvider.getUriForFile(context, context.getPackageName() + ".fileprovider", file)
            #file_uri = FileProvider.getUriForFile(context, "org.test.magazayonetim.fileprovider", file)

            
            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.setType("application/octet-stream")
            intent.putExtra(Intent.EXTRA_STREAM, file_uri)
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            
            chooser = Intent.createChooser(intent, 'Veritabanını Paylaş')
            mActivity.startActivity(chooser)
        else:
            self.show_popup("Bilgi", "Bu özellik sadece Android'de çalışır.")

if __name__ == '__main__':
    MainApp().run()