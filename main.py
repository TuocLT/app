import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class ExcelApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Adding Label for registration
        self.register_label = Label(text="Đăng kí sử dụng máy", size_hint=(1, 0.1))
        layout.add_widget(self.register_label)

        # Adding TextInput fields with labels
        labels = ["Tên nhân viên", "Mã nhân viên", "Tên máy", "Sản phẩm"]
        self.text_inputs = []  # List to store text input widgets
        for label_text in labels:
            row_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

            label = Label(text=label_text + ":", size_hint=(0.4, None), height=60)
            row_layout.add_widget(label)

            text_input = TextInput(hint_text=f'Enter {label_text.lower()}', size_hint=(0.6, None), height=60)
            self.text_inputs.append(text_input)
            row_layout.add_widget(text_input)

            layout.add_widget(row_layout)

        # Adding buttons
        button_layout = BoxLayout(size_hint=(1, 0.1))
        ok_button = Button(text='OK', size_hint=(0.5, None), height=40)
        ok_button.bind(on_press=self.save_values)
        button_layout.add_widget(ok_button)

        exit_button = Button(text='Thoát', size_hint=(0.5, None), height=40)
        exit_button.bind(on_press=self.exit_app)
        button_layout.add_widget(exit_button)

        layout.add_widget(button_layout)

        self.result_label = Label(text='', size_hint=(1, 0.7))
        layout.add_widget(self.result_label)

        # Display data from MySQL database
        display_data_btn = Button(text='Hiển thị dữ liệu', size_hint=(1, 0.1))
        display_data_btn.bind(on_press=self.display_data)
        layout.add_widget(display_data_btn)

        return layout

    def save_values(self, instance):
        try:
            # Get values from text inputs
            values = [text_input.text for text_input in self.text_inputs]

            # Save values to MySQL database
            conn = mysql.connector.connect(

                host="daian234.ddns.net",
                user="tuoc_nguyen",
                password="Tuoc2341997",
                database="test"

            )
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                            (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), employee_id VARCHAR(255), machine_name VARCHAR(255), product VARCHAR(255))''')
            sql = "INSERT INTO employees (name, employee_id, machine_name, product) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, tuple(values))
            conn.commit()
            conn.close()

            # Clear text inputs
            for text_input in self.text_inputs:
                text_input.text = ''

            # Move widgets down
            self.register_label.size_hint_y = 0.07
        except Exception as e :
            print(e)

    def display_data(self, instance):
        try:
            # Retrieve data from MySQL database
            conn = mysql.connector.connect(

                host="daian234.ddns.net",
                user="tuoc_nguyen",
                password="Tuoc2341997",
                database="test"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            data = cursor.fetchall()
            conn.close()

            # Display data
            data_text = "\n".join([" | ".join(map(str, row)) for row in data])
            self.result_label.text = data_text
        except Exception as e :
            print(e)

    def exit_app(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    ExcelApp().run()
