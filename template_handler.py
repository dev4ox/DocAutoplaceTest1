import re

class TemplateHandler:
    def generate_html_from_template(self, template_content):
        # Замена всех меток *input* на поля для произвольного ввода с размером 60px
        template_html = template_content.replace('*input*', '<input type="text" class="inputField" name="custom_input">')

        # Заменяем *ФИО* на поле с автоподсказками и проверкой по маске
        template_html = re.sub(r'\*ФИО\*', '''
            <input type="text" class="fioInput" name="client_input" placeholder="Введите Фамилия И.О.">
            <div class="suggestions"></div>
        ''', template_html)

        return template_html
