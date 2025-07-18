import datetime
import os
import tempfile
from io import BytesIO
from typing import Dict

import matplotlib
import matplotlib.pyplot as plt
from app.models.db_tables import (
    Event,
    Information,
    MedicalExemption,
    Registration,
    User,
)
from app.models.schemas import Role
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ======================
# FONT SETUP FOR CYRILLIC
# ======================
try:
    # Try to register Arial font (common on Windows)
    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "arialbd.ttf"))
    MAIN_FONT = "Arial"
    BOLD_FONT = "Arial-Bold"
except Exception:
    try:
        # Fallback to DejaVu Sans
        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        MAIN_FONT = "DejaVuSans"
        BOLD_FONT = "DejaVuSans"
    except Exception:
        MAIN_FONT = "Helvetica"
        BOLD_FONT = "Helvetica-Bold"

# Configure matplotlib
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Helvetica"]
plt.rcParams["axes.unicode_minus"] = False

# Create stylesheet with registered fonts
styles = getSampleStyleSheet()

# Обновляем стиль 'Title'
styles["Title"].fontName = BOLD_FONT
styles["Title"].fontSize = 24
styles["Title"].leading = 28
styles["Title"].alignment = 1
styles["Title"].spaceAfter = 12
styles["Title"].textColor = colors.HexColor("#2563eb")

# Обновляем стиль 'Heading1'
styles["Heading1"].fontName = BOLD_FONT
styles["Heading1"].fontSize = 18
styles["Heading1"].leading = 22
styles["Heading1"].alignment = 0
styles["Heading1"].spaceBefore = 20
styles["Heading1"].spaceAfter = 10
styles["Heading1"].textColor = colors.HexColor("#0f172a")

# Обновляем стиль 'Heading2'
styles["Heading2"].fontName = BOLD_FONT
styles["Heading2"].fontSize = 16
styles["Heading2"].leading = 20
styles["Heading2"].alignment = 0
styles["Heading2"].spaceBefore = 15
styles["Heading2"].spaceAfter = 8
styles["Heading2"].textColor = colors.HexColor("#2563eb")

# Создаем кастомные стили (если их нет)
if "Body" not in styles:
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName=MAIN_FONT,
            fontSize=12,
            leading=16,
            alignment=0,
            spaceAfter=6,
            textColor=colors.HexColor("#334155"),
        )
    )

if "Caption" not in styles:
    styles.add(
        ParagraphStyle(
            name="Caption",
            fontName=MAIN_FONT,
            fontSize=10,
            leading=12,
            alignment=1,
            spaceBefore=5,
            spaceAfter=15,
            textColor=colors.HexColor("#64748b"),
        )
    )

if "StatValue" not in styles:
    styles.add(
        ParagraphStyle(
            name="StatValue",
            fontName=BOLD_FONT,
            fontSize=14,
            leading=16,
            alignment=1,
            textColor=colors.HexColor("#2563eb"),
        )
    )


class AdminAnalyticsReportGenerator:
    def __init__(self, adapter):
        self.adapter = adapter
        self.temp_dir = tempfile.mkdtemp()
        self.report_data = {}

    async def collect_data(self):
        """Сбор и обработка данных для аналитического отчета"""
        await self._collect_user_stats()
        await self._collect_event_stats()
        await self._collect_donor_stats()
        await self._collect_registration_stats()
        await self._collect_medical_exemption_stats()
        await self._collect_organizer_stats()

    async def _collect_user_stats(self):
        """Сбор статистики по пользователям"""
        # Общее количество пользователей
        users = await self.adapter.get_all(User)
        self.report_data["total_users"] = len(users)

        # Распределение по ролям
        roles_count = {}
        for user in users:
            role = user.role.value
            roles_count[role] = roles_count.get(role, 0) + 1
        self.report_data["roles_distribution"] = roles_count

        # Динамика регистрации
        reg_dynamics = {}
        for user in users:
            month_key = user.created_at.strftime("%Y-%m")
            reg_dynamics[month_key] = reg_dynamics.get(month_key, 0) + 1

        # Сортировка по дате
        sorted_dynamics = sorted(reg_dynamics.items(), key=lambda x: x[0])
        self.report_data["registration_dynamics"] = sorted_dynamics

    async def _collect_event_stats(self):
        """Сбор статистики по мероприятиям"""
        # Общее количество мероприятий
        events = await self.adapter.get_all(Event)
        total_events = len(events)
        self.report_data["total_events"] = total_events

        # Статистика по завершенным/текущим мероприятиям
        now = datetime.now()
        past_events = 0
        upcoming_events = 0
        total_occupancy = 0

        for event in events:
            if event.end_date < now:
                past_events += 1
            else:
                upcoming_events += 1

            if event.max_donors > 0:
                occupancy = (event.registred / event.max_donors) * 100
                total_occupancy += occupancy

        self.report_data["past_events"] = past_events
        self.report_data["upcoming_events"] = upcoming_events

        # Среднее количество доноров на мероприятие
        avg_donors = sum(event.max_donors for event in events) / total_events if total_events else 0
        self.report_data["avg_donors_per_event"] = avg_donors

        # Процент заполняемости мероприятий
        self.report_data["avg_occupancy"] = total_occupancy / total_events if total_events else 0

    async def _collect_donor_stats(self):
        """Сбор статистики по донорам"""
        # Получаем всех пользователей-доноров
        donors = await self.adapter.get_by_value(User, "role", Role.DONOR)

        # Собираем информацию о донорах
        genders = {}
        ages = []
        weights = []
        universities = {}
        donor_experience = {}
        chronic_disease_count = 0

        for donor in donors:
            info = await self.adapter.get_by_id(Information, donor.id)
            if not info:
                continue

            # Пол
            gender = info.gender.value
            genders[gender] = genders.get(gender, 0) + 1

            # Возраст
            today = datetime.today()
            age = (
                today.year
                - info.birth_date.year
                - ((today.month, today.day) < (info.birth_date.month, info.birth_date.day))
            )
            ages.append(age)

            # Вес
            weights.append(info.weight)

            # Университет
            if info.university:
                universities[info.university] = universities.get(info.university, 0) + 1

            # Опыт донорства
            experience = info.donor_earlier.value
            donor_experience[experience] = donor_experience.get(experience, 0) + 1

            # Хронические заболевания
            if info.chronic_disease:
                chronic_disease_count += 1

        # Категоризация возрастов и весов
        age_distribution = self._categorize_ages(ages)
        weight_distribution = self._categorize_weights(weights)

        # Топ университетов
        sorted_universities = sorted(universities.items(), key=lambda x: x[1], reverse=True)[:10]
        top_universities = {uni: count for uni, count in sorted_universities}

        # Сохранение статистик
        self.report_data["gender_distribution"] = genders
        self.report_data["age_distribution"] = age_distribution
        self.report_data["weight_distribution"] = weight_distribution
        self.report_data["university_distribution"] = top_universities
        self.report_data["donor_experience"] = donor_experience
        self.report_data["chronic_disease_percentage"] = (chronic_disease_count / len(donors)) * 100 if donors else 0

    async def _collect_registration_stats(self):
        """Сбор статистики по регистрациям"""
        # Общее количество регистраций
        registrations = await self.adapter.get_all(Registration)
        total_registrations = len(registrations)
        self.report_data["total_registrations"] = total_registrations

        # Подсчет закрытых регистраций
        closed_registrations = await self.adapter.get_by_value(Registration, "closed", True)
        closed_count = len(closed_registrations)

        # Конверсия регистраций
        self.report_data["registration_conversion"] = (
            (total_registrations - closed_count) / total_registrations * 100 if total_registrations else 0
        )

        # Распределение по времени суток
        hours = {hour: 0 for hour in range(24)}

        for reg in registrations:
            hour = reg.opened_at.hour
            hours[hour] = hours.get(hour, 0) + 1

        self.report_data["registration_hours"] = hours

    async def _collect_medical_exemption_stats(self):
        """Сбор статистики по медицинским отводам"""
        # Общее количество отводов
        exemptions = await self.adapter.get_all(MedicalExemption)
        total_exemptions = len(exemptions)
        self.report_data["total_exemptions"] = total_exemptions

        # Длительность отводов
        durations = []
        for exemption in exemptions:
            if exemption.end_date:
                duration = (exemption.end_date - exemption.start_date).days
                durations.append(duration)

        self.report_data["exemption_durations"] = durations

    async def _collect_organizer_stats(self):
        """Сбор статистики по организаторам"""
        # Получаем все мероприятия
        events = await self.adapter.get_all(Event)

        # Считаем количество мероприятий по организаторам
        organizer_counts = {}
        for event in events:
            organizer_id = event.organizer
            organizer_counts[organizer_id] = organizer_counts.get(organizer_id, 0) + 1

        # Сортируем по убыванию и берем топ 10
        sorted_organizers = sorted(organizer_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        self.report_data["top_organizers"] = sorted_organizers

    def _categorize_ages(self, ages: list) -> Dict[str, int]:
        """Категоризация возрастов"""
        bins = [18, 25, 30, 35, 40, 45, 50, 55, 100]
        labels = ["18-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "55+"]
        distribution = {label: 0 for label in labels}

        for age in ages:
            if age < 18:
                continue
            for i, upper_bound in enumerate(bins[1:]):
                if age < upper_bound:
                    distribution[labels[i]] += 1
                    break
            else:
                distribution[labels[-1]] += 1

        return distribution

    def _categorize_weights(self, weights: list) -> Dict[str, int]:
        """Категоризация весов"""
        bins = [0, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 150]
        labels = ["<50", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-99", "100+"]
        distribution = {label: 0 for label in labels}

        for weight in weights:
            if weight < 50:
                distribution["<50"] += 1
                continue

            for i, upper_bound in enumerate(bins[1:]):
                if weight < upper_bound:
                    distribution[labels[i + 1]] += 1
                    break
            else:
                distribution["100+"] += 1

        return distribution

    def generate_pdf_report(self) -> str:
        """Генерация PDF отчета"""
        report_id = datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_path = os.path.join(self.temp_dir, f"admin_report_{report_id}.pdf")

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )
        elements = []

        # Титульная страница
        self._create_cover_page(elements)
        elements.append(PageBreak())

        # Статистика пользователей
        self._create_user_stats_page(elements)
        elements.append(PageBreak())

        # Статистика доноров
        self._create_donor_stats_page(elements)
        elements.append(PageBreak())

        # Статистика мероприятий
        self._create_event_stats_page(elements)
        elements.append(PageBreak())

        # Статистика регистраций и организаторов
        self._create_registration_stats_page(elements)

        # Сборка документа
        doc.build(elements)
        return pdf_path

    def _create_cover_page(self, elements):
        """Создание титульной страницы"""
        elements.append(Paragraph("АНАЛИТИЧЕСКИЙ ОТЧЕТ ДЛЯ АДМИНИСТРАТОРОВ", styles["Title"]))
        elements.append(Spacer(1, 1 * cm))
        elements.append(Paragraph("Полный анализ системы донорства", styles["Heading2"]))
        elements.append(Spacer(1, 2 * cm))

        # Ключевые метрики
        metrics = [
            ("Общее количество пользователей", self.report_data.get("total_users", 0)),
            ("Общее количество мероприятий", self.report_data.get("total_events", 0)),
            ("Общее количество регистраций", self.report_data.get("total_registrations", 0)),
            ("Активных медицинских отводов", self.report_data.get("total_exemptions", 0)),
        ]

        table_data = []
        for metric, value in metrics:
            table_data.append([Paragraph(metric, styles["Body"]), Paragraph(str(value), styles["StatValue"])])

        metrics_table = Table(table_data, colWidths=[10 * cm, 5 * cm])
        metrics_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f9ff")),
                    ("FONTNAME", (0, 0), (-1, -1), MAIN_FONT),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("PADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        elements.append(metrics_table)
        elements.append(Spacer(1, 3 * cm))
        elements.append(Paragraph(f"Сгенерировано {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles["Caption"]))

    def _create_user_stats_page(self, elements):
        """Страница статистики пользователей"""
        elements.append(Paragraph("СТАТИСТИКА ПОЛЬЗОВАТЕЛЕЙ", styles["Title"]))
        elements.append(Spacer(1, 0.5 * cm))

        # Распределение ролей
        elements.append(Paragraph("Распределение по ролям", styles["Heading2"]))
        self._create_pie_chart(
            elements, self.report_data.get("roles_distribution", {}), "Распределение ролей пользователей"
        )

        # Динамика регистраций
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("Динамика регистраций", styles["Heading2"]))
        self._create_registration_dynamics_chart(elements)

        # Таблица распределения ролей
        roles_data = [["Роль", "Количество"]]
        for role, count in self.report_data.get("roles_distribution", {}).items():
            roles_data.append([role, str(count)])

        roles_table = Table(roles_data, colWidths=[8 * cm, 7 * cm])
        roles_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
                    ("FONTNAME", (0, 1), (-1, -1), MAIN_FONT),
                ]
            )
        )
        elements.append(roles_table)

    def _create_donor_stats_page(self, elements):
        """Страница статистики доноров"""
        elements.append(Paragraph("СТАТИСТИКА ДОНОРОВ", styles["Title"]))
        elements.append(Spacer(1, 0.5 * cm))

        # Распределение по полу
        elements.append(Paragraph("Распределение по полу", styles["Heading2"]))
        self._create_pie_chart(
            elements, self.report_data.get("gender_distribution", {}), "Распределение доноров по полу"
        )

        # Распределение по возрасту
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("Распределение по возрасту", styles["Heading2"]))
        self._create_bar_chart(
            elements,
            self.report_data.get("age_distribution", {}),
            "Возрастные группы доноров",
            "Возрастная группа",
            "Количество",
        )

        # Распределение по весу
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("Распределение по весу", styles["Heading2"]))
        self._create_bar_chart(
            elements,
            self.report_data.get("weight_distribution", {}),
            "Весовая категория доноров",
            "Весовая группа (кг)",
            "Количество",
        )

        # Опыт донорства
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("Опыт донорства", styles["Heading2"]))
        self._create_pie_chart(elements, self.report_data.get("donor_experience", {}), "Опыт донорства")

    def _create_event_stats_page(self, elements):
        """Страница статистики мероприятий"""
        elements.append(Paragraph("СТАТИСТИКА МЕРОПРИЯТИЙ", styles["Title"]))
        elements.append(Spacer(1, 0.5 * cm))

        # Статус мероприятий
        past = self.report_data.get("past_events", 0)
        upcoming = self.report_data.get("upcoming_events", 0)
        status_data = {"Завершено": past, "Предстоящие": upcoming}
        elements.append(Paragraph("Статус мероприятий", styles["Heading2"]))
        self._create_pie_chart(elements, status_data, "Статус мероприятий")

        # Заполняемость мероприятий
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("Заполняемость мероприятий", styles["Heading2"]))
        elements.append(
            Paragraph(f"Средняя заполняемость: {self.report_data.get('avg_occupancy', 0):.1f}%", styles["Body"])
        )
        elements.append(
            Paragraph(
                f"Среднее количество доноров: {self.report_data.get('avg_donors_per_event', 0):.1f}", styles["Body"]
            )
        )

    def _create_registration_stats_page(self, elements):
        """Страница статистики регистраций и организаторов"""
        elements.append(Paragraph("РЕГИСТРАЦИИ И ОРГАНИЗАТОРЫ", styles["Title"]))
        elements.append(Spacer(1, 0.5 * cm))

        # Конверсия регистраций
        conversion = self.report_data.get("registration_conversion", 0)
        elements.append(Paragraph("Конверсия регистраций", styles["Heading2"]))
        elements.append(Paragraph(f"Успешные регистрации: {conversion:.1f}%", styles["Body"]))

        # Время регистраций
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("Активность регистраций по часам", styles["Heading2"]))
        self._create_line_chart(
            elements,
            self.report_data.get("registration_hours", {}),
            "Активность регистраций",
            "Час дня",
            "Количество регистраций",
        )

        # Топ организаторов
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("Топ организаторов", styles["Heading2"]))

        org_data = [["ID Организатора", "Количество мероприятий"]]
        for org_id, count in self.report_data.get("top_organizers", [])[:5]:
            org_data.append([str(org_id), str(count)])

        org_table = Table(org_data, colWidths=[8 * cm, 7 * cm])
        org_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
                    ("FONTNAME", (0, 1), (-1, -1), MAIN_FONT),
                ]
            )
        )
        elements.append(org_table)

    # Методы для создания графиков
    def _create_pie_chart(self, elements, data_dict, title):
        """Создание круговой диаграммы"""
        if not data_dict:
            return

        labels = list(data_dict.keys())
        sizes = list(data_dict.values())

        # Увеличиваем размер диаграммы
        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, textprops={"fontsize": 10})
        plt.axis("equal")
        plt.title(title, fontsize=14)

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        plt.close()
        buf.seek(0)

        elements.append(Image(buf, width=16 * cm, height=12 * cm))

    def _create_bar_chart(self, elements, data_dict, title, xlabel, ylabel):
        """Создание столбчатой диаграммы"""
        if not data_dict:
            return

        labels = list(data_dict.keys())
        values = list(data_dict.values())

        # Увеличиваем размер диаграммы
        plt.figure(figsize=(14, 8))
        bars = plt.bar(labels, values, color="#60a5fa")
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)

        # Добавление значений на столбцы
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{height}", ha="center", va="bottom", fontsize=10)

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        plt.close()
        buf.seek(0)

        elements.append(Image(buf, width=16 * cm, height=10 * cm))

    def _create_line_chart(self, elements, data_dict, title, xlabel, ylabel):
        """Создание линейного графика"""
        if not data_dict:
            return

        hours = sorted(data_dict.keys())
        values = [data_dict[h] for h in hours]

        # Увеличиваем размер диаграммы
        plt.figure(figsize=(14, 8))
        plt.plot(hours, values, marker="o", linestyle="-", color="#2563eb", linewidth=2, markersize=8)
        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.xticks(hours, fontsize=10)
        plt.yticks(fontsize=10)

        # Добавление значений в точки
        for h, v in zip(hours, values):
            plt.text(h, v + max(values) * 0.05, str(v), ha="center", va="bottom", fontsize=10, fontweight="bold")

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        plt.close()
        buf.seek(0)

        elements.append(Image(buf, width=16 * cm, height=10 * cm))

    def _create_registration_dynamics_chart(self, elements):
        """Создание графика динамики регистраций"""
        dynamics = self.report_data.get("registration_dynamics", [])
        if not dynamics:
            return

        dates, counts = zip(*dynamics)

        # Увеличиваем размер диаграммы
        plt.figure(figsize=(16, 8))
        plt.plot(dates, counts, marker="o", linestyle="-", color="#2563eb", linewidth=2, markersize=8)
        plt.title("Динамика регистраций пользователей", fontsize=14)
        plt.xlabel("Месяц", fontsize=12)
        plt.ylabel("Количество регистраций", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)

        # Добавление значений в точки
        for i, count in enumerate(counts):
            plt.text(
                i, count + max(counts) * 0.05, str(count), ha="center", va="bottom", fontsize=10, fontweight="bold"
            )

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        plt.close()
        buf.seek(0)

        elements.append(Image(buf, width=18 * cm, height=10 * cm))


async def generate_admin_report(adapter):
    """Генерация аналитического отчета для администратора"""
    report_generator = AdminAnalyticsReportGenerator(adapter)
    await report_generator.collect_data()
    report_path = report_generator.generate_pdf_report()
    return report_path
