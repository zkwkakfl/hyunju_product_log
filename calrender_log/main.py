import json
import os
import sqlite3
from datetime import datetime
from calendar import monthcalendar

# Kivy 라이브러리 임포트
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.core.text import LabelBase

# 앱의 디자인과 레이아웃을 정의하는 kv 언어 문자열
# UI의 구조를 한눈에 파악하기 쉽습니다.
KV = """
<Manager>:
    CalendarScreen:
        name: 'main'
    MainScreen:
        name: 'write'
    ModelManagementScreen:
        name: 'model_management'

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        spacing: '10dp'

        Label:
            text: '새 생산 기록 작성'
            font_name: 'korean'
            font_size: '32sp'
            size_hint_y: None
            height: self.texture_size[1]
            bold: True

        GridLayout:
            cols: 2
            spacing: '10dp'
            size_hint_y: None
            height: '200dp'

            Label:
                text: '날짜:'
                font_name: 'korean'
                font_size: '18sp'
                size_hint_y: None
                height: '40dp'
                valign: 'middle'
            Button:
                id: date_button
                font_name: 'korean'
                font_size: '18sp'
                text: '날짜 선택'
                on_press: root.show_date_picker()
                size_hint_y: None
                height: '40dp'

            Label:
                text: '생산 모델:'
                font_name: 'korean'
                font_size: '18sp'
                size_hint_y: None
                height: '40dp'
                valign: 'middle'
            Spinner:
                id: model_spinner
                font_name: 'korean'
                font_size: '18sp'
                text: '모델을 선택하세요'
                values: []
                size_hint_y: None
                height: '40dp'
                

            Label:
                text: '수량:'
                font_name: 'korean'
                font_size: '18sp'
                size_hint_y: None
                height: '40dp'
                valign: 'middle'
            TextInput:
                id: quantity_input
                font_name: 'korean'
                font_size: '18sp'
                hint_text: '숫자만 입력'
                multiline: False
                input_filter: 'int'
                size_hint_y: None
                height: '40dp'

        Button:
            text: '저장하기'
            font_name: 'korean'
            font_size: '20sp'
            size_hint_y: None
            height: '50dp'
            on_press: root.save_data()

        Label:
            id: result_label
            text: ''
            font_name: 'korean'
            font_size: '16sp'
            size_hint_y: 0.5

        BoxLayout:
            size_hint_y: None
            height: '60dp'
            Button:
                text: '달력으로 돌아가기'
                font_name: 'korean'
                font_size: '20sp'
                on_press: root.manager.current = 'main'

<CalendarScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'

        Label:
            text: '생산 기록 관리'
            font_name: 'korean'
            font_size: '32sp'
            size_hint_y: None
            height: self.texture_size[1]
            bold: True

        BoxLayout:
            size_hint_y: None
            height: '40dp'
            Button:
                text: '< 이전 달'
                font_name: 'korean'
                font_size: '14sp'
                size_hint_x: 0.3
                on_press: root.change_month(-1)
            Label:
                id: month_label
                text: root.current_month_str
                font_name: 'korean'
                font_size: '20sp'
                size_hint_x: 0.4
            Button:
                text: '다음 달 >'
                font_name: 'korean'
                font_size: '14sp'
                size_hint_x: 0.3
                on_press: root.change_month(1)

        Label:
            id: monthly_total_label
            text: '이번 달 총 금액: 0원'
            font_name: 'korean'
            font_size: '16sp'
            size_hint_y: None
            height: '25dp'
            color: [0.2, 0.6, 0.2, 1]

        GridLayout:
            cols: 7
            spacing: '1dp'
            size_hint_y: None
            height: '25dp'
            # 요일 표시
            Label:
                text: '일'
                font_name: 'korean'
                font_size: '12sp'
                color: 1, 0.3, 0.3, 1
            Label:
                text: '월'
                font_name: 'korean'
                font_size: '12sp'
            Label:
                text: '화'
                font_name: 'korean'
                font_size: '12sp'
            Label:
                text: '수'
                font_name: 'korean'
                font_size: '12sp'
            Label:
                text: '목'
                font_name: 'korean'
                font_size: '12sp'
            Label:
                text: '금'
                font_name: 'korean'
                font_size: '12sp'
            Label:
                text: '토'
                font_name: 'korean'
                font_size: '12sp'
                color: 0.3, 0.3, 1, 1

        GridLayout:
            id: calendar_grid
            cols: 7
            spacing: '1dp'
            size_hint_y: None
            height: '250dp'



        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '10dp'
            Button:
                text: '새 기록 작성'
                font_name: 'korean'
                on_press: root.manager.current = 'write'
            Button:
                text: '모델 관리'
                font_name: 'korean'
                on_press: root.manager.current = 'model_management'

<DayButton>:
    background_normal: ''
    background_color: [0.9, 0.9, 0.9, 1] if self.text else [0,0,0,0]
    color: [0,0,0,1]
    font_name: 'korean'
    font_size: '9sp'
    size_hint_y: None
    height: '50dp'
    text_size: self.width, None
    halign: 'center'
    valign: 'middle'
    # 기록이 있는 날은 다른 색으로 표시
    canvas.before:
        Color:
            rgba: [0.6, 0.8, 1, 1] if self.has_record else [0.9, 0.9, 0.9, 1]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [5]

<RecordPopup>:
    title: '해당 날짜의 생산 기록'
    size_hint: 0.9, 0.8
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        Label:
            id: popup_content
            text: root.content_text
            font_name: 'korean'
            font_size: '16sp'
            text_size: self.width, None
            halign: 'left'
            valign: 'top'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '10dp'
            Button:
                text: '새 기록 작성'
                font_name: 'korean'
                on_press: root.write_new_record()
            Button:
                text: '기록 수정'
                font_name: 'korean'
                on_press: root.edit_records()
            Button:
                text: '닫기'
                font_name: 'korean'
                on_press: root.dismiss()

<DatePickerPopup>:
    title: '날짜 선택'
    size_hint: 0.8, 0.6
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'
        
        Label:
            text: '년도와 월을 선택하세요'
            font_name: 'korean'
            font_size: '18sp'
            size_hint_y: None
            height: '40dp'
        
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '10dp'
            
            Label:
                text: '년도:'
                font_name: 'korean'
                font_size: '16sp'
                size_hint_x: 0.3
            Spinner:
                id: year_spinner
                font_name: 'korean'
                font_size: '16sp'
                text: '2024'
                values: ['2023', '2024', '2025', '2026']
                size_hint_x: 0.7
            
            Label:
                text: '월:'
                font_name: 'korean'
                font_size: '16sp'
                size_hint_x: 0.3
            Spinner:
                id: month_spinner
                font_name: 'korean'
                font_size: '16sp'
                text: '1'
                values: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                size_hint_x: 0.7
        
        GridLayout:
            id: date_grid
            cols: 7
            spacing: '2dp'
            size_hint_y: 0.7
        
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '10dp'
            Button:
                text: '취소'
                font_name: 'korean'
                on_press: root.dismiss()
            Button:
                text: '확인'
                font_name: 'korean'
                on_press: root.confirm_date()

<DateButton>:
    background_normal: ''
    background_color: [0.9, 0.9, 0.9, 1] if self.text else [0,0,0,0]
    color: [0,0,0,1]
    font_name: 'korean'
    font_size: '14sp'
    # 선택된 날짜는 다른 색으로 표시
    canvas.before:
        Color:
            rgba: [0.3, 0.7, 1, 1] if self.is_selected else [0.9, 0.9, 0.9, 1]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [3]

<ModelManagementScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        spacing: '10dp'

        Label:
            text: '모델 관리'
            font_name: 'korean'
            font_size: '32sp'
            size_hint_y: None
            height: self.texture_size[1]
            bold: True

        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '10dp'
            TextInput:
                id: model_name_input
                font_name: 'korean'
                font_size: '16sp'
                hint_text: '모델명 입력'
                multiline: False
            TextInput:
                id: model_price_input
                font_name: 'korean'
                font_size: '16sp'
                hint_text: '단가 입력'
                multiline: False
                input_filter: 'int'
            Button:
                text: '추가'
                font_name: 'korean'
                size_hint_x: 0.3
                on_press: root.add_model()

        ScrollView:
            id: model_list_scroll
            size_hint_y: 0.7

        BoxLayout:
            size_hint_y: None
            height: '60dp'
            Button:
                text: '달력으로 돌아가기'
                font_name: 'korean'
                font_size: '20sp'
                on_press: root.manager.current = 'main'

<ModelItem>:
    size_hint_y: None
    height: '60dp'
    BoxLayout:
        orientation: 'horizontal'
        padding: '10dp'
        spacing: '10dp'
        
        Label:
            text: root.model_name
            font_name: 'korean'
            font_size: '18sp'
            size_hint_x: 0.4
            valign: 'middle'
        
        Label:
            text: f"{root.model_price:,}원"
            font_name: 'korean'
            font_size: '16sp'
            size_hint_x: 0.3
            valign: 'middle'
        
        BoxLayout:
            size_hint_x: 0.3
            spacing: '5dp'
            Button:
                text: '수정'
                font_name: 'korean'
                font_size: '12sp'
                size_hint_x: 0.5
                on_press: root.edit_model()
            Button:
                text: '삭제'
                font_name: 'korean'
                font_size: '12sp'
                size_hint_x: 0.5
                on_press: root.delete_model()

<ModelEditPopup>:
    title: '모델 수정'
    size_hint: 0.8, 0.4
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        spacing: '10dp'
        
        Label:
            text: '모델명:'
            font_name: 'korean'
            font_size: '16sp'
            size_hint_y: None
            height: '30dp'
        
        TextInput:
            id: edit_name_input
            font_name: 'korean'
            font_size: '16sp'
            multiline: False
            size_hint_y: None
            height: '40dp'
        
        Label:
            text: '단가:'
            font_name: 'korean'
            font_size: '16sp'
            size_hint_y: None
            height: '30dp'
        
        TextInput:
            id: edit_price_input
            font_name: 'korean'
            font_size: '16sp'
            multiline: False
            input_filter: 'int'
            size_hint_y: None
            height: '40dp'
        
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '10dp'
            Button:
                text: '취소'
                font_name: 'korean'
                on_press: root.dismiss()
            Button:
                text: '저장'
                font_name: 'korean'
                on_press: root.save_changes()

<RecordEditPopup>:
    title: '기록 수정'
    size_hint: 0.95, 0.85
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        spacing: '15dp'
        
        # 제목과 총금액 표시
        BoxLayout:
            size_hint_y: None
            height: '80dp'
            orientation: 'vertical'
            spacing: '10dp'
            
            Label:
                text: f'[{root.selected_date}] 기록 수정'
                font_name: 'korean'
                font_size: '20sp'
                size_hint_y: 0.5
                valign: 'middle'
                halign: 'center'
                bold: True
            
            BoxLayout:
                size_hint_y: 0.5
                orientation: 'horizontal'
                spacing: '20dp'
                
                Label:
                    text: '총 금액:'
                    font_name: 'korean'
                    font_size: '18sp'
                    valign: 'middle'
                    halign: 'right'
                    size_hint_x: 0.5
                
                Label:
                    id: total_amount_label
                    text: f"{root.total_amount:,}원"
                    font_name: 'korean'
                    font_size: '20sp'
                    valign: 'middle'
                    halign: 'left'
                    size_hint_x: 0.5
                    color: [0.2, 0.6, 0.2, 1]
                    bold: True
        
        # 테이블 헤더
        BoxLayout:
            size_hint_y: None
            height: '40dp'
            padding: '10dp'
            spacing: '10dp'
            canvas.before:
                Color:
                    rgba: [0.8, 0.8, 0.8, 1]
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [5]
            
            Label:
                text: '모델명'
                font_name: 'korean'
                font_size: '16sp'
                size_hint_x: 0.4
                valign: 'middle'
                halign: 'center'
                bold: True
                color: [0, 0, 0, 1]
            
            Label:
                text: '수량'
                font_name: 'korean'
                font_size: '16sp'
                size_hint_x: 0.3
                valign: 'middle'
                halign: 'center'
                bold: True
                color: [0, 0, 0, 1]
            
            Label:
                text: '삭제'
                font_name: 'korean'
                font_size: '16sp'
                size_hint_x: 0.3
                valign: 'middle'
                halign: 'center'
                bold: True
                color: [0, 0, 0, 1]
        
        ScrollView:
            id: records_scroll
            size_hint_y: 0.7
            bar_width: '10dp'
            bar_color: [0.3, 0.3, 0.3, 0.8]
        
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '10dp'
            Button:
                text: '모든 변경사항 저장'
                font_name: 'korean'
                font_size: '16sp'
                background_color: [0.2, 0.6, 0.2, 1]
                on_press: root.save_all_changes()
            Button:
                text: '닫기'
                font_name: 'korean'
                font_size: '16sp'
                background_color: [0.5, 0.5, 0.5, 1]
                on_press: root.dismiss()

<RecordEditItem>:
    size_hint_y: None
    height: '70dp'
    canvas.before:
        Color:
            rgba: [0.95, 0.95, 0.95, 1]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [8]
    
    BoxLayout:
        orientation: 'horizontal'
        padding: '15dp'
        spacing: '15dp'
        
        # 모델명 (읽기 전용)
        Label:
            text: root.model_name
            font_name: 'korean'
            font_size: '18sp'
            size_hint_x: 0.5
            valign: 'middle'
            halign: 'left'
            bold: True
            color: [0.2, 0.2, 0.2, 1]
        
        # 수량 (수정 가능)
        TextInput:
            id: edit_quantity_input
            text: str(root.quantity)
            font_name: 'korean'
            font_size: '18sp'
            multiline: False
            input_filter: 'int'
            size_hint_x: 0.3
            hint_text: '수량 입력'
            valign: 'middle'
            halign: 'center'
            background_color: [1, 1, 1, 1]
            foreground_color: [0, 0, 0, 1]
        
        # 삭제 버튼
        Button:
            text: '삭제'
            font_name: 'korean'
            font_size: '16sp'
            size_hint_x: 0.2
            background_color: [0.8, 0.2, 0.2, 1]
            color: [1, 1, 1, 1]
            bold: True
            on_press: root.delete_record()
"""

# --- 데이터 파일 설정 ---
# 생산 기록을 저장할 데이터베이스 파일 이름
DB_FILE = 'production_data.db'

# 한글 폰트 등록 함수
def register_korean_fonts():
    """Windows에서 한글 폰트를 등록하는 함수"""
    try:
        # Windows에서 사용 가능한 한글 폰트들
        korean_fonts = [
            'C:/Windows/Fonts/malgun.ttf',  # 맑은 고딕
            'C:/Windows/Fonts/gulim.ttc',   # 굴림
            'C:/Windows/Fonts/batang.ttc',  # 바탕
            'C:/Windows/Fonts/dotum.ttc',   # 돋움
            'C:/Windows/Fonts/gungsuh.ttc', # 궁서
        ]
        
        # 사용 가능한 첫 번째 폰트를 등록
        for font_path in korean_fonts:
            if os.path.exists(font_path):
                LabelBase.register(
                    name='korean',
                    fn_regular=font_path,
                    fn_bold=font_path,
                    fn_italic=font_path,
                    fn_bolditalic=font_path
                )
                print(f"한글 폰트 등록 완료: {font_path}")
                return True
        
        # 폰트를 찾지 못한 경우 기본 폰트 사용
        print("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        return False
        
    except Exception as e:
        print(f"폰트 등록 중 오류 발생: {e}")
        return False


# --- 화면(Screen) 클래스 정의 ---

# 메인 화면: 데이터 입력
class MainScreen(Screen):
    def on_kv_post(self, base_widget):
        """KV 파일이 로드된 후 실행되는 메서드"""
        # 화면에 들어올 때마다 오늘 날짜를 자동으로 설정
        if hasattr(self, 'ids') and 'date_button' in self.ids:
            self.ids.date_button.text = datetime.now().strftime('%Y-%m-%d')
            self.ids.result_label.text = ''
    
    def on_enter(self, *args):
        """화면에 들어올 때 실행되는 메서드"""
        # 날짜 업데이트
        if hasattr(self, 'ids') and 'date_button' in self.ids:
            self.ids.date_button.text = datetime.now().strftime('%Y-%m-%d')
            self.ids.result_label.text = ''
        
        # 모델 목록 업데이트
        self.load_models()
    
    def show_date_picker(self):
        """날짜 선택 팝업을 표시하는 함수"""
        popup = DatePickerPopup()
        popup.bind(on_confirm=self.on_date_selected)
        popup.open()
    
    def on_date_selected(self, instance, date_str):
        """날짜가 선택되었을 때 호출되는 함수"""
        if hasattr(self, 'ids') and 'date_button' in self.ids:
            self.ids.date_button.text = date_str
    
    def load_models(self):
        """데이터베이스에서 모델 목록을 불러와서 스피너에 설정"""
        if not hasattr(self, 'ids') or 'model_spinner' not in self.ids:
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT model_name FROM models ORDER BY model_name")
        models = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.ids.model_spinner.values = models
        if models:
            self.ids.model_spinner.text = '모델을 선택하세요'
        else:
            self.ids.model_spinner.text = '등록된 모델이 없습니다'

    def save_data(self):
        """입력된 데이터를 데이터베이스에 저장하는 함수"""
        date_str = self.ids.date_button.text
        model = self.ids.model_spinner.text.upper()  # 대문자로 통일
        quantity_str = self.ids.quantity_input.text

        # 1. 입력 값 유효성 검사
        if not (date_str and model and quantity_str) or model == '모델을 선택하세요':
            self.ids.result_label.text = "오류: 모든 항목을 입력해주세요."
            return
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            self.ids.result_label.text = "오류: 날짜 형식이 올바르지 않습니다 (YYYY-MM-DD)."
            return
        
        quantity = int(quantity_str)

        # 2. 데이터베이스에서 모델 단가 조회
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT unit_price FROM models WHERE model_name = ?", (model,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            self.ids.result_label.text = f"오류: '{model}'은(는) 등록되지 않은 모델입니다."
            return
        
        unit_price = result[0]
        amount = unit_price * quantity

        # 3. 데이터베이스에 데이터 저장
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO records (date, model, quantity, unit_price, amount)
                VALUES (?, ?, ?, ?, ?)
            ''', (date_str, model, quantity, unit_price, amount))
            conn.commit()
            conn.close()
        except Exception as e:
            self.ids.result_label.text = f"DB 저장 오류: {e}"
            return

        # 4. 결과 표시 및 입력 필드 초기화
        self.ids.result_label.text = f"저장 완료!\n금액: {amount:,} 원"
        self.ids.model_spinner.text = "모델을 선택하세요"
        self.ids.quantity_input.text = ""
        
        # 달력 화면으로 돌아가기 (2초 후)
        from kivy.clock import Clock
        Clock.schedule_once(self.return_to_calendar, 2)
    
    def return_to_calendar(self, dt):
        """달력 화면으로 돌아가기"""
        self.manager.current = 'main'

# 달력 화면: 데이터 조회
class CalendarScreen(Screen):
    current_month_str = StringProperty()

    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.today = datetime.now()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.records_by_date = {}

    def on_enter(self):
        """화면에 들어올 때마다 달력을 새로고침"""
        self.load_all_records()
        # ids가 초기화되었는지 확인
        if hasattr(self, 'ids') and 'calendar_grid' in self.ids:
            self.update_calendar()
    
    def on_kv_post(self, base_widget):
        """KV 파일이 로드된 후 실행"""
        self.load_all_records()
        self.update_calendar()

    def load_all_records(self):
        """데이터베이스에서 기록을 불러와 날짜별로 정리"""
        self.records_by_date = {}
        if not os.path.exists(DB_FILE):
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, model, quantity, unit_price, amount FROM records")
        all_rows = cursor.fetchall()
        conn.close()

        for row in all_rows:
            # DB에서 가져온 튜플 데이터를 딕셔너리로 변환
            record = {
                'id': row[0],
                'date': row[1],
                'model': row[2],
                'quantity': row[3],
                'unit_price': row[4],
                'amount': row[5]
            }
            date_str = record['date']
            if date_str not in self.records_by_date:
                self.records_by_date[date_str] = []
            self.records_by_date[date_str].append(record)

    def update_calendar(self):
        """현재 년/월에 맞춰 달력 UI를 생성"""
        self.current_month_str = f"{self.current_year}년 {self.current_month}월"
        grid = self.ids.calendar_grid
        grid.clear_widgets()

        # 월별 총 금액 계산
        monthly_total = 0
        for date_str, records in self.records_by_date.items():
            if date_str.startswith(f"{self.current_year}-{self.current_month:02d}-"):
                for record in records:
                    monthly_total += record['amount']
        
        # 월별 총 금액 표시
        if hasattr(self, 'ids') and 'monthly_total_label' in self.ids:
            self.ids.monthly_total_label.text = f"이번 달 총 금액: {monthly_total:,}원"


        cal = monthcalendar(self.current_year, self.current_month)

        for week in cal:
            for day in week:
                if day == 0:
                    # 빈 칸은 비활성화된 버튼처럼 표시
                    grid.add_widget(Label(text=""))
                else:
                    date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    
                    # 해당 날짜에 기록이 있으면 총합계 계산하고 버튼 텍스트에 표시
                    if date_str in self.records_by_date:
                        daily_total = sum(record['amount'] for record in self.records_by_date[date_str])
                        # 날짜와 금액을 함께 표시 (줄바꿈 사용)
                        button_text = f"{day}\n{daily_total:,}원"
                        day_btn = DayButton(text=button_text)
                        day_btn.has_record = True
                        day_btn.daily_total = f"{daily_total:,}원"
                    else:
                        # 기록이 없는 날은 날짜만 표시
                        day_btn = DayButton(text=str(day))
                        day_btn.has_record = False
                        day_btn.daily_total = ''
                    
                    # 버튼 클릭 시 팝업 표시 함수 연결
                    day_btn.bind(on_press=self.show_records_for_day)
                    grid.add_widget(day_btn)


    def change_month(self, month_delta):
        """이전/다음 달로 이동"""
        self.current_month += month_delta
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def show_records_for_day(self, instance):
        """특정 날짜의 기록을 팝업으로 보여주는 함수"""
        day = int(instance.text.split('\n')[0])
        date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"

        content_text = f"[{date_str}]\n\n"
        if date_str in self.records_by_date:
            records_for_day = self.records_by_date[date_str]
            total_amount = 0
            for record in records_for_day:
                content_text += (
                    f"- 모델: {record['model']}\n"
                    f"  수량: {record['quantity']:,}\n"
                    f"  단가: {record['unit_price']:,} 원\n"
                    f"  금액: {record['amount']:,} 원\n\n"
                )
                total_amount += record['amount']
            content_text += f"총 금액: {total_amount:,} 원"
        else:
            content_text += "기록이 없습니다."

        popup = RecordPopup(content_text=content_text, selected_date=date_str)
        popup.open()


# --- 커스텀 위젯 클래스 ---

# 날짜 버튼 (기록 유무에 따라 스타일 변경)
class DayButton(Button):
    has_record = ObjectProperty(False)
    daily_total = StringProperty('')

# 날짜 선택 팝업
class DatePickerPopup(Popup):
    selected_date = StringProperty('')
    
    def __init__(self, **kwargs):
        super(DatePickerPopup, self).__init__(**kwargs)
        self.selected_day = None
        # 현재 날짜로 초기화
        today = datetime.now()
        if hasattr(self, 'ids'):
            self.ids.year_spinner.text = str(today.year)
            self.ids.month_spinner.text = str(today.month)
            self.ids.year_spinner.bind(text=self.on_date_change)
            self.ids.month_spinner.bind(text=self.on_date_change)
    
    def on_kv_post(self, base_widget):
        """KV 파일이 로드된 후 실행"""
        today = datetime.now()
        self.ids.year_spinner.text = str(today.year)
        self.ids.month_spinner.text = str(today.month)
        self.ids.year_spinner.bind(text=self.on_date_change)
        self.ids.month_spinner.bind(text=self.on_date_change)
        self.update_calendar()
    
    def on_date_change(self, instance, value):
        """년도나 월이 변경될 때 호출"""
        self.update_calendar()
    
    def update_calendar(self):
        """선택된 년/월에 맞춰 달력을 업데이트"""
        if not hasattr(self, 'ids'):
            return
            
        year = int(self.ids.year_spinner.text)
        month = int(self.ids.month_spinner.text)
        
        # 현재 날짜로 초기화
        today = datetime.now()
        if year == today.year and month == today.month:
            self.selected_day = today.day
        
        grid = self.ids.date_grid
        grid.clear_widgets()
        
        # 요일 헤더
        weekdays = ['일', '월', '화', '수', '목', '금', '토']
        for day in weekdays:
            label = Label(text=day, font_name='korean', font_size='12sp')
            if day in ['일', '토']:
                label.color = [1, 0.3, 0.3, 1] if day == '일' else [0.3, 0.3, 1, 1]
            grid.add_widget(label)
        
        # 달력 생성
        cal = monthcalendar(year, month)
        for week in cal:
            for day in week:
                if day == 0:
                    grid.add_widget(Label(text=""))
                else:
                    date_btn = DateButton(text=str(day))
                    if self.selected_day == day:
                        date_btn.is_selected = True
                    date_btn.bind(on_press=self.select_date)
                    grid.add_widget(date_btn)
    
    def select_date(self, instance):
        """날짜를 선택하는 함수"""
        # 이전 선택 해제
        for child in self.ids.date_grid.children:
            if hasattr(child, 'is_selected'):
                child.is_selected = False
        
        # 새 선택 적용
        instance.is_selected = True
        self.selected_day = int(instance.text)
    
    def confirm_date(self):
        """날짜 선택을 확인하는 함수"""
        if self.selected_day:
            year = int(self.ids.year_spinner.text)
            month = int(self.ids.month_spinner.text)
            date_str = f"{year}-{month:02d}-{self.selected_day:02d}"
            self.selected_date = date_str
            self.dispatch('on_confirm', date_str)
        self.dismiss()
    
    def on_confirm(self, date_str):
        """날짜 확인 이벤트"""
        pass

# 날짜 버튼 (날짜 선택용)
class DateButton(Button):
    is_selected = ObjectProperty(False)

# 기록 표시 팝업
class RecordPopup(Popup):
    content_text = StringProperty('')
    selected_date = StringProperty('')
    
    def write_new_record(self):
        """새 기록 작성 화면으로 이동"""
        # App 인스턴스를 통해 화면 관리자에 접근
        app = App.get_running_app()
        if app and hasattr(app, 'root'):
            # MainScreen에 선택된 날짜 전달
            main_screen = app.root.get_screen('write')
            if hasattr(main_screen, 'ids') and 'date_button' in main_screen.ids:
                main_screen.ids.date_button.text = self.selected_date
            # 화면 전환
            app.root.current = 'write'
        self.dismiss()
    
    def edit_records(self):
        """기록 수정 팝업 표시"""
        # App 인스턴스를 통해 달력 화면에 접근
        app = App.get_running_app()
        if app and hasattr(app, 'root'):
            calendar_screen = app.root.get_screen('main')
            if hasattr(calendar_screen, 'records_by_date'):
                records = calendar_screen.records_by_date.get(self.selected_date, [])
                if records:
                    popup = RecordEditPopup(selected_date=self.selected_date, records=records)
                    popup.open()
        self.dismiss()

# 모델 관리 화면
class ModelManagementScreen(Screen):
    def on_enter(self):
        """화면에 들어올 때 모델 목록을 새로고침"""
        self.load_models()
    
    def load_models(self):
        """데이터베이스에서 모델 목록을 불러와서 화면에 표시"""
        scroll_view = self.ids.model_list_scroll
        # 기존 위젯들 제거
        if hasattr(scroll_view, 'children') and scroll_view.children:
            scroll_view.clear_widgets()
        
        # 모델 목록을 담을 BoxLayout 생성
        model_list = BoxLayout(orientation='vertical', spacing='5dp', size_hint_y=None)
        model_list.bind(minimum_height=model_list.setter('height'))
        
        # 데이터베이스에서 모델 목록 조회
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT model_name, unit_price FROM models ORDER BY model_name")
        models = cursor.fetchall()
        conn.close()
        
        # 각 모델을 ModelItem으로 표시
        for model_name, unit_price in models:
            model_item = ModelItem()
            model_item.model_name = model_name
            model_item.model_price = unit_price
            model_item.parent_screen = self
            model_list.add_widget(model_item)
        
        scroll_view.add_widget(model_list)
    
    def add_model(self):
        """새 모델 추가"""
        model_name = self.ids.model_name_input.text.strip()
        price_text = self.ids.model_price_input.text.strip()
        
        # 입력 검증
        if not model_name or not price_text:
            return
        
        try:
            unit_price = int(price_text)
        except ValueError:
            return
        
        # 데이터베이스에 모델 추가
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO models (model_name, unit_price) VALUES (?, ?)", 
                         (model_name, unit_price))
            conn.commit()
            
            # 입력 필드 초기화
            self.ids.model_name_input.text = ''
            self.ids.model_price_input.text = ''
            
            # 모델 목록 새로고침
            self.load_models()
            
        except sqlite3.IntegrityError:
            # 중복된 모델명
            pass
        finally:
            conn.close()
    
    def edit_model(self, old_name, new_name, new_price):
        """모델 수정"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE models SET model_name = ?, unit_price = ? WHERE model_name = ?", 
                         (new_name, new_price, old_name))
            conn.commit()
            self.load_models()
        finally:
            conn.close()
    
    def delete_model(self, model_name):
        """모델 삭제"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM models WHERE model_name = ?", (model_name,))
            conn.commit()
            self.load_models()
        finally:
            conn.close()

# 모델 아이템 위젯
class ModelItem(BoxLayout):
    model_name = StringProperty('')
    model_price = ObjectProperty(0)
    parent_screen = ObjectProperty(None)
    
    def edit_model(self):
        """모델 수정 팝업 표시"""
        popup = ModelEditPopup()
        popup.ids.edit_name_input.text = self.model_name
        popup.ids.edit_price_input.text = str(self.model_price)
        popup.old_name = self.model_name
        popup.parent_screen = self.parent_screen
        popup.open()
    
    def delete_model(self):
        """모델 삭제"""
        if self.parent_screen:
            self.parent_screen.delete_model(self.model_name)

# 모델 수정 팝업
class ModelEditPopup(Popup):
    old_name = StringProperty('')
    parent_screen = ObjectProperty(None)
    
    def save_changes(self):
        """수정사항 저장"""
        new_name = self.ids.edit_name_input.text.strip()
        price_text = self.ids.edit_price_input.text.strip()
        
        if not new_name or not price_text:
            return
        
        try:
            new_price = int(price_text)
        except ValueError:
            return
        
        if self.parent_screen:
            self.parent_screen.edit_model(self.old_name, new_name, new_price)
        
        self.dismiss()

# 기록 수정 팝업
class RecordEditPopup(Popup):
    selected_date = StringProperty('')
    records = ObjectProperty([])
    total_amount = ObjectProperty(0)
    
    def __init__(self, **kwargs):
        super(RecordEditPopup, self).__init__(**kwargs)
        self.calculate_total_amount()
        self.load_records()
    
    def calculate_total_amount(self):
        """총금액 계산"""
        total = sum(record['amount'] for record in self.records)
        self.total_amount = total
        if hasattr(self, 'ids') and 'total_amount_label' in self.ids:
            self.ids.total_amount_label.text = f"{total:,}원"
    
    def load_records(self):
        """선택된 날짜의 기록들을 수정 가능한 형태로 표시"""
        scroll_view = self.ids.records_scroll
        # 기존 위젯들 제거
        if hasattr(scroll_view, 'children') and scroll_view.children:
            scroll_view.clear_widgets()
        
        # 기록 목록을 담을 BoxLayout 생성
        records_list = BoxLayout(orientation='vertical', spacing='8dp', size_hint_y=None)
        records_list.bind(minimum_height=records_list.setter('height'))
        
        # 각 기록을 RecordEditItem으로 표시
        for record in self.records:
            record_item = RecordEditItem()
            record_item.record_id = record.get('id', 0)
            record_item.model_name = record['model']
            record_item.quantity = record['quantity']
            record_item.unit_price = record['unit_price']
            record_item.amount = record['amount']
            record_item.parent_popup = self
            record_item.load_models()
            records_list.add_widget(record_item)
        
        scroll_view.add_widget(records_list)
    
    def refresh_calendar(self):
        """달력 화면 새로고침"""
        app = App.get_running_app()
        if app and hasattr(app, 'root'):
            calendar_screen = app.root.get_screen('main')
            if hasattr(calendar_screen, 'load_all_records'):
                calendar_screen.load_all_records()
                calendar_screen.update_calendar()
    
    def save_all_changes(self):
        """모든 변경사항을 저장"""
        # 모든 RecordEditItem의 변경사항을 저장
        scroll_view = self.ids.records_scroll
        if hasattr(scroll_view, 'children') and scroll_view.children:
            for child in scroll_view.children[0].children:  # BoxLayout의 children
                if hasattr(child, 'save_changes'):
                    child.save_changes()
        
        # 달력 새로고침
        self.refresh_calendar()

# 기록 수정 아이템
class RecordEditItem(BoxLayout):
    record_id = ObjectProperty(0)
    model_name = StringProperty('')
    quantity = ObjectProperty(0)
    unit_price = ObjectProperty(0)
    amount = ObjectProperty(0)
    parent_popup = ObjectProperty(None)
    
    def load_models(self):
        """수량 입력 필드에 이벤트 바인딩"""
        if not hasattr(self, 'ids') or 'edit_quantity_input' not in self.ids:
            return
        
        # 수량 입력에 이벤트 바인딩
        self.ids.edit_quantity_input.bind(text=self.on_quantity_changed)
    
    def on_quantity_changed(self, instance, value):
        """수량이 변경될 때 금액 업데이트"""
        try:
            quantity = int(value) if value else 0
            self.quantity = quantity
            self.update_amount()
            # 총금액 업데이트
            if self.parent_popup:
                self.parent_popup.calculate_total_amount()
        except ValueError:
            pass
    
    def update_amount(self):
        """금액 업데이트"""
        self.amount = self.unit_price * self.quantity
    
    def save_changes(self):
        """수정사항 저장"""
        new_quantity_text = self.ids.edit_quantity_input.text.strip()
        
        if not new_quantity_text:
            return
        
        try:
            new_quantity = int(new_quantity_text)
        except ValueError:
            return
        
        # 수량만 업데이트 (모델과 단가는 변경하지 않음)
        new_amount = self.unit_price * new_quantity
        
        # 기록 업데이트
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE records 
            SET quantity = ?, amount = ?
            WHERE id = ?
        """, (new_quantity, new_amount, self.record_id))
        
        conn.commit()
        conn.close()
        
        # 현재 객체의 값도 업데이트
        self.quantity = new_quantity
        self.amount = new_amount
    
    def delete_record(self):
        """기록 삭제"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = ?", (self.record_id,))
        conn.commit()
        conn.close()
        
        # 팝업 새로고침
        if self.parent_popup:
            self.parent_popup.load_records()
            self.parent_popup.refresh_calendar()


# 화면 관리자
class Manager(ScreenManager):
    pass


# --- 메인 앱 클래스 ---
class ProductionApp(App):
    def build(self):
        # 한글 폰트 등록
        register_korean_fonts()
        
        self.init_db()  # 앱 시작 시 데이터베이스 초기화
        # 창 크기를 스마트폰과 유사하게 설정 (테스트용)
        Window.size = (360, 640)
        print("창 크기 설정 완료")
        # kv 문자열을 로드하여 UI 규칙을 등록하고, Manager 위젯의 인스턴스를 반환합니다.
        print("KV 문자열 로드 시작")
        Builder.load_string(KV)
        print("KV 문자열 로드 완료")
        manager = Manager()
        print("Manager 생성 완료")
        return manager

    def init_db(self):
        """데이터베이스와 테이블을 생성하는 함수"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 생산 기록 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                model TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        
        # 모델 정보 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                model_name TEXT PRIMARY KEY,
                unit_price INTEGER NOT NULL
            )
        ''')
        
        # 기본 모델 데이터 추가 (기존 데이터가 없을 때만)
        cursor.execute("SELECT COUNT(*) FROM models")
        if cursor.fetchone()[0] == 0:
            default_models = [
                ('MODEL-A', 1500),
                ('MODEL-B', 2200),
                ('MODEL-C', 1850),
                ('MODEL-D', 3100),
            ]
            cursor.executemany("INSERT INTO models (model_name, unit_price) VALUES (?, ?)", default_models)
        
        conn.commit()
        conn.close()

# 앱 실행
if __name__ == '__main__':
    try:
        print("=== 앱 시작 ===")
        
        # Windows에서 Kivy 앱 실행을 위한 설정
        import sys
        print(f"Python 버전: {sys.version}")
        print(f"플랫폼: {sys.platform}")
        
        if sys.platform == 'win32':
            # Windows에서 OpenGL 컨텍스트 문제 해결
            import os
            os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
            print("Windows용 OpenGL 백엔드 설정 완료")
        
        print("Kivy 임포트 테스트...")
        from kivy.app import App
        print("Kivy 임포트 성공!")
        
        print("앱을 시작합니다...")
        app = ProductionApp()
        print("앱 인스턴스 생성 완료")
        
        app.run()
        print("앱 실행 완료")
        
    except Exception as e:
        print(f"앱 실행 중 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()
        input("엔터를 눌러 종료하세요...")