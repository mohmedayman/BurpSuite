from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit,QTextEdit
from PyQt5.QtCore import QObject
from requests import Response


class DNSRecordsService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QTextEdit) -> None:
        super().__init__(main)
        self.button = button
        self.output = output

    def before_request(self):
        self.button.setDisabled(True)

    def onError(self):
        self.button.setDisabled(False)

    def onResponse(self, **kwargs):
        res: Response = kwargs['response']
        self.button.setDisabled(False)
        data = res.json()['data']
        formatted_data=data
        if(isinstance(data,dict)):
            formatted_data = "\n".join(f"{key}: {', '.join(value)}" if value else f"{key}: (empty)" for key, value in data.items())
        
        self.output.setText(formatted_data)

            
    def records(self, target: str):

        if self.validator.domain(target).validate():

            self.request("get", "/enums/dns/records",
                         params={"domain_name": target})
