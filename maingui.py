from datetime import datetime, timedelta
from statistics import mode

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtNetwork import QNetworkAccessManager
from PyQt6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QLabel, QListWidgetItem, QFrame, QHBoxLayout, \
    QInputDialog, QMessageBox

from connection import get_db_handle


class ListItem(QWidget):
    def __init__(self, date, average_temp, min_temperature, max_temperature, average_wind_speed, average_humidity, dominant_weather, dominant_weather_icon):
        super().__init__()

        item_layout = QVBoxLayout(self)
        item_layout.setContentsMargins(0, 0, 0, 10)
        label_date = QLabel(date)
        label_date.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_date.setFont(QFont(label_date.font().family(), 11))
        label_date.setStyleSheet("background-color: #1f2e39; color: white; font-weight: 800; border: 1px solid #fff; radius: 0px; border-radius: 0px; border-top-left-radius: 8px; border-top-right-radius: 8px; padding:8px")
        item_layout.addWidget(label_date)
        h_layout = QHBoxLayout()

        label_dominan_weather_icon = QLabel()
        label_dominan_weather_icon.setPixmap(QtGui.QPixmap(f"images/{dominant_weather_icon}_w@4x.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        label_dominan_weather_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(label_dominan_weather_icon)

        dominant_weather_label = QLabel(dominant_weather)
        dominant_weather_label.setFont(QFont('Segoe UI', 10))
        dominant_weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(dominant_weather_label)
        h_layout.setContentsMargins(0,0,0,0)

        h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        item_layout.addLayout(h_layout)

        label_avg_temp = QLabel(f'Avg Temp: {average_temp} \xb0C')
        label_avg_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_avg_temp.setFont(QFont('Segoe UI', 10))
        item_layout.addWidget(label_avg_temp)

        label_min_max = QLabel(f"Min: {min_temperature} \xb0C, Max: {max_temperature} \xb0C")

        label_min_max.setStyleSheet('padding-left:10px; padding-right:10px;')
        label_min_max.setFont(QFont('Segoe UI', 10))
        item_layout.addWidget(label_min_max)

        horizontal_layout = QHBoxLayout()
        label_windspeed_icon = QLabel()


        label_windspeed_icon.setPixmap(QtGui.QPixmap('icons/b_humidity_1.png'))
        label_windspeed_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_windspeed_text = QLabel(f'{average_wind_speed} m/s')

        label_humidity_icon = QLabel()
        label_humidity_icon.setPixmap(QtGui.QPixmap('icons/b_wind_speed_1.png'))
        label_humity_text = QLabel(f'{average_humidity} %')

        horizontal_layout.addWidget(label_windspeed_icon)
        horizontal_layout.addWidget(label_windspeed_text)
        horizontal_layout.addWidget(label_humidity_icon)
        horizontal_layout.addWidget(label_humity_text)
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        item_layout.addLayout(horizontal_layout)

        frame = QFrame()
        frame.setStyleSheet("border-radius: 8px; background-color: white; solid #ccc;")
        frame.setLayout(item_layout)

        vbox_layout  = QVBoxLayout()
        vbox_layout.addWidget(frame)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        vbox_layout.addItem(spacerItem)

        self.setLayout(vbox_layout)

        
class CustomLabel(QLabel):
    def __init__(self, text, parent = None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 20px; padding: 10px;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.click_count = 0
        self.temp = 0

    def setTemp(self, temperature):
        self.temp = temperature
        self.setText(f'{temperature} \xb0C')

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_count += 1

            #Celsius
            if self.click_count % 3 == 0:
                self.setText(f'{round(self.kelvin_to_celsius(self.temp), 2)} \xb0C')

            if self.click_count % 3 == 1:
                self.setText(f'{self.temp} K')

            if self.click_count % 3 == 2:
                self.setText(f'{round(self.kelvin_to_fahrenheit(self.temp), 2)} \xb0F')

    def kelvin_to_celsius(self, temp_kelvin):
        return temp_kelvin - 273.15

    def kelvin_to_fahrenheit(self, temp_kelvin):
        return (temp_kelvin - 273.15) * 1.8 + 32



city = 'Delhi'
class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.db = get_db_handle()
        self.temperature_list = []
        self.threshold = -1
        self.setupUi(Form)

        self.request_manager = QNetworkAccessManager()
        self.timer = QTimer()

        self.timer.timeout.connect(self.retrieve)
        self.timer.start(300000)

        self.retrieve()

    def retrieve(self):
        self.listWidget.clear()
        self.get_weather_update()
        self.retrieve_seven_days_weather()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(734, 375)
        Form.setStyleSheet("background-color: #1f2e39;")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, -1, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.searchedit = QtWidgets.QLineEdit()

        self.button_threshold = QtWidgets.QPushButton(parent=Form)
        self.button_threshold.setObjectName("button_threshold")
        self.button_threshold.setIcon(QIcon('icons/filter_1.png'))
        self.button_threshold.setToolTip("Set Threshold")

        self.button_threshold.setFixedSize(28, 24)
        self.button_threshold.setStyleSheet("border: none;")
        self.button_threshold.clicked.connect(self.show_threshold_dialog)

        self.searchhorizontalLayout = QHBoxLayout()
        self.searchhorizontalLayout.addWidget(self.searchedit)

        self.searchhorizontalLayout.addWidget(self.button_threshold)
        self.searchhorizontalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addLayout(self.searchhorizontalLayout)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_city = QtWidgets.QLabel(parent=Form)
        self.label_city.setObjectName("label_city")
        self.label_city.setStyleSheet("color:white; padding-bottom: -1;")

        label_city_font = QFont('Segoe UI', 15)
        label_city_font.setWeight(600)
        self.label_city.setFont(label_city_font)
        self.label_city.setContentsMargins(0,0,0,0)
        self.label_city.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_city, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_time = QtWidgets.QLabel(parent=Form)
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_time.setObjectName("label_time")
        self.label_time.setStyleSheet("color:white;")
        self.label_time.setContentsMargins(0,0,0,0)

        label_time_font = QFont('Segoe UI', 10)
        label_time_font.setWeight(500)
        self.label_time.setFont(label_time_font)
        self.label_time.setFont(label_time_font)

        self.verticalLayout_3.addWidget(self.label_time, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_image = QtWidgets.QLabel(parent=Form)
        self.label_image.setText("")

        self.label_image.setStyleSheet("margin: 0; background-color: white; border: 1px solid white; border-radius: 10px; padding: 2.5px")

        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setObjectName("label")
        self.label_image.setScaledContents(True)
        self.horizontalLayout_3.addWidget(self.label_image, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.label_image.setContentsMargins(0,0,0,0)


        self.horizontalLayout_3.setContentsMargins(0,0,0,0)
        self.label_weather_main = QtWidgets.QLabel(parent=Form)
        self.label_weather_main.setContentsMargins(0, 0, 0, 0)
        self.label_weather_main.setObjectName("label_weather_main")
        self.label_weather_main.setStyleSheet("color: white; margin: 0;  padding-top: -5; padding-bottom: -5; ")

        label_weather_main_font = QFont('Century Gothic', 15)
        label_weather_main_font.setWeight(700)
        self.label_weather_main.setFont(label_weather_main_font)

        self.label_weather_main.adjustSize()
        self.horizontalLayout_3.addWidget(self.label_weather_main, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_temperature = CustomLabel(text = "", parent = Form)


        sans_font = QFont('Microsoft Sans Serif', 45)
        sans_font.setBold(True)
        self.label_temperature.setFont(QFont(sans_font))
        self.label_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_temperature.setStyleSheet("color: white; padding-top: -15; padding-bottom: -15; margin:0")
        self.label_temperature.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        font = QtGui.QFont()
        font.setPointSize(50)
        font.setBold(True)



        self.label_temperature.setFont(font)
        self.label_temperature.setObjectName("label_temperature")
        self.verticalLayout_7.addWidget(self.label_temperature, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_5.addLayout(self.verticalLayout_7)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_feels_like = QtWidgets.QLabel(parent=Form)
        self.label_feels_like.setObjectName("label_feels_like")
        self.label_feels_like.setStyleSheet("color:white;")
        self.label_feels_like.setFont(QFont('Segoe UI', 12))

        self.verticalLayout_6.addWidget(self.label_feels_like, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_windspeed = QtWidgets.QLabel(parent=Form)
        self.label_windspeed.setObjectName("label_windspeed")
        self.label_windspeed.setStyleSheet("color:white;")

        self.label_humidity = QtWidgets.QLabel(parent=Form)
        self.label_humidity.setObjectName("label_humidity")
        self.label_humidity.setStyleSheet("color:white;")

        font_humidity_ws = QFont('Segoe UI', 10)
        font_humidity_ws.setBold(True)
        self.label_humidity.setFont(font_humidity_ws)
        self.label_windspeed.setFont(font_humidity_ws)

        self.label_windspeed_icon = QtWidgets.QLabel(parent=Form)
        self.label_windspeed_icon.setObjectName("label_windspeed_icon")
        self.label_windspeed_icon.setPixmap(QtGui.QPixmap('icons/wind_speed_1.png'))
        self.horizontalLayout_2.addWidget(self.label_windspeed_icon, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_windspeed, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label_humidity_icon = QtWidgets.QLabel(parent=Form)
        self.label_humidity_icon.setObjectName("label_humidity_icon")
        self.label_humidity_icon.setPixmap(QtGui.QPixmap('icons/humidity_1.png'))
        self.horizontalLayout_2.addWidget(self.label_humidity_icon, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_humidity, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.listWidget = QListWidget()
        self.listWidget.setFlow(QListWidget.Flow.LeftToRight)
        self.listWidget.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.listWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.listWidget.setStyleSheet("background-color: #1f2e39")

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        citiesList = ['Delhi', 'Mumbai', 'Chennai', 'Bengaluru', 'Kolkata', 'Hyderabad']
        self.searchedit.setPlaceholderText('Enter City')
        self.searchedit.setStyleSheet("background-color: white; border: 1px solid white; border-radius: 5px; padding: 5px")
        self.auto_completer = QtWidgets.QCompleter(citiesList)
        self.auto_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.searchedit.setCompleter(self.auto_completer)

        self.auto_completer.activated.connect(self.perform)

    def perform(self):
        global city
        city = self.searchedit.text()
        self.temperature_list = []
        self.retrieve()

    def show_threshold_dialog(self):
        dialog = QInputDialog(self)
        dialog.setStyleSheet(
            """
                QInputDialog {
                    background-color: #1f2e39;
                }
                QLabel {
                    color: white;
                    font-size: 12px;
                }
                QPushButton{
                    color: white;
                    background-color: #3f596d;
                }
            """)
        dialog.setWindowTitle("Set Threshold")
        dialog.setLabelText("Enter Temperature Threshold in (\xb0C)")
        dialog.setInputMode(QInputDialog.InputMode.IntInput)
        pressed = dialog.exec()

        if pressed:
            threshold = dialog.intValue()
            self.threshold = threshold

    def show_alert(self):
        if len(self.temperature_list) >= 2:
            if abs(self.temperature_list[-1] - self.temperature_list[-2]) >= self.threshold:
                QMessageBox.critical(self, 'Threshold Breached', 'Temperature Breaks Threshold Value')


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Weather App"))
        Form.setWindowIcon(QIcon('icons/weather_icon.png'))
        self.label_city.setText(_translate("Form", "Mumbai"))
        self.label_time.setText(_translate("Form", "05:50 am"))
        self.label_weather_main.setText(_translate("Form", "Rain"))
        self.label_temperature.setText(_translate("Form", "25 C"))
        self.label_feels_like.setText(_translate("Form", "Feels Like: 20"))


        self.label_windspeed.setText(_translate("Form", "0 m/sec"))
        self.label_humidity.setText(_translate("Form", "0 %"))


    def get_weather_update(self):
        print('Executing')
        print('Weather Data Fetched at', datetime.now())
        collections = self.db["weather_data"]
        print('City Is', city)

        query_by_city_date = {"city": city, "date": (datetime.today()).date().isoformat()}

        documentlatest = collections.find_one(query_by_city_date, sort = {'_id': -1})
        print('Latest', documentlatest)
        weather_main = documentlatest['weather_main']
        feels_like = documentlatest['feels_like']
        current_temp = documentlatest['temperature']
        humidity = documentlatest['humidity']
        wind_speed = documentlatest['wind_speed']

        self.label_temperature.setTemp(current_temp)

        #For threshold
        self.temperature_list.append(round(self.kelvin_to_celsius(current_temp), 2))

        print('Temp List', self.temperature_list)
        if self.threshold >= 0:
            self.show_alert()

        self.label_temperature.setText(f'{round(self.kelvin_to_celsius(current_temp), 2)} \xb0C')
        self.label_feels_like.setText(f'Feels like: {round(self.kelvin_to_celsius(feels_like), 2)} \xb0C')
        self.label_weather_main.setText(weather_main)
        self.label_time.setText(datetime.fromtimestamp(documentlatest['date_time_unix']).strftime('%a, %b %d, %y %I:%M %p'))

        self.label_image.setPixmap(QtGui.QPixmap(f"images/{documentlatest['weather_icon_code']}_w@4x.png").scaled(140,140, Qt.AspectRatioMode.KeepAspectRatio))
        self.label_humidity.setText(f'{humidity} %')
        self.label_windspeed.setText(f'{wind_speed} m/sec') #meter/sec


        # documents = collections.find(query_by_city_date).sort({'_id': -1})

        self.label_city.setText(city)

    def kelvin_to_celsius(self, temp_kelvin):
        return (temp_kelvin - 273.15)

    def retrieve_seven_days_weather(self):
        print('Seven Days Data Fetched at', datetime.now())

        collections = self.db["weather_data"]

        start_date = (datetime.now() - timedelta(days = 7)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        pipeline = [
            {
                "$match": {
                    "city": city,
                    "date": {
                        '$gte': start_date,
                        '$lte': end_date
                    }
                }
            },
            {
                "$group":
                    {
                        '_id': {
                            'city': '$city',
                            'date': '$date'
                        },
                        'average_temp': {'$avg': '$temperature'},
                        'average_ws': {'$avg': '$wind_speed'},
                        'average_humidity' : {'$avg': '$humidity'},
                        'min_temperature': {'$min': '$temperature'},
                        'max_temperature': {'$max': '$temperature'},
                        'weather_condition_values': {'$push': '$weather_main'},
                        'weather_icon_code': {'$push': '$weather_icon_code'}
                    }
            },
            {
                '$sort': {'_id.date': 1}
            }
        ]

        documents = collections.aggregate(pipeline)

        for data in documents:
            date = date = datetime.strptime(data['_id']['date'], '%Y-%m-%d').strftime('%a, %b %d, %y')
            average_temp = round(self.kelvin_to_celsius(data['average_temp']), 2)
            min_temperature = round(self.kelvin_to_celsius(data['min_temperature']), 2)
            max_temperature = round(self.kelvin_to_celsius(data['max_temperature']), 2)
            average_wind_speed = round(data['average_ws'], 2)
            average_humidity = round(data['average_humidity'], 2)
            dominant_weather = mode(data['weather_condition_values'])
            dominant_weather_icon = mode(data['weather_icon_code'])
            item = ListItem(date, average_temp, min_temperature, max_temperature, average_wind_speed, average_humidity, dominant_weather, dominant_weather_icon)

            list_item = QListWidgetItem(self.listWidget)
            list_item.setSizeHint(item.sizeHint())

            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, item)

        self.horizontalLayout.addWidget(self.listWidget, 0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    Form.show()
    sys.exit(app.exec())
