import datetime
import os
import tempfile
from io import BytesIO
from typing import Dict, List
from app.models.db_tables import *
import matplotlib
import matplotlib.pyplot as plt
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


class OrganizerAnalyticsReportGenerator:
    def __init__(self, adapter):
        self.adapter = adapter
        self.temp_dir = tempfile.mkdtemp()
        self.report_data = {}

    async def collect_data(self):
        """Сбор и обработка данных для аналитического отчета организатора"""
        await self._collect_event_stats()
        await self._collect_donor_stats()
        await self._collect_registration_stats()
        await self._collect_medical_exemption_stats()

    async def _get_organizer_events(self) -> List:
        """Получение мероприятий организатора"""
        return await self.adapter.get_all(Event)

    async def _get_organizer_registrations(self) -> List:
        """Получение регистраций на мероприятия организатора"""
        events = await self._get_organizer_events()
        event_ids = [event.id for event in events]
        
        registrations = []
        for event_id in event_ids:
            event_regs = await self.adapter.get_by_value(Registration, "event_id", event_id)
            registrations.extend(event_regs)
            
        return registrations

    async def _collect_event_stats(self):
        """Сбор статистики по мероприятиям организатора"""
        events = await self._get_organizer_events()
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
        """Сбор статистики по донорам организатора"""
        registrations = await self._get_organizer_registrations()
        donor_ids = {reg.user_id for reg in registrations}
        
        donors = []
        for donor_id in donor_ids:
            donor = await self.adapter.get_by_id(User, donor_id)
            if donor:
                donors.append(donor)

        # Собираем информацию о донациях
        donations = []
        for donor in donors:
            info = await self.adapter.get_by_value(Information, "phone",donor.phone)
            if info:
                donations.append(info.donations)
            else:
                donations.append(0)

        # Категоризация донаций
        donation_distribution = self._categorize_donations(donations)

        # Сохранение статистик
        self.report_data["total_donors"] = len(donors)
        self.report_data["donation_distribution"] = donation_distribution
        self.report_data["avg_donations"] = sum(donations) / len(donors) if donors else 0

    async def _collect_registration_stats(self):
        """Сбор статистики по регистрациям организатора"""
        registrations = await self._get_organizer_registrations()
        total_registrations = len(registrations)
        self.report_data["total_registrations"] = total_registrations

        # Подсчет закрытых регистраций
        closed_registrations = [reg for reg in registrations if reg.closed]
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
        """Сбор статистики по медицинским отводам доноров организатора"""
        registrations = await self._get_organizer_registrations()
        donor_ids = {reg.user_id for reg in registrations}
        
        exemptions = []
        for donor_id in donor_ids:
            donor_exemptions = await self.adapter.get_by_value(MedicalExemption, "user_id", donor_id)
            exemptions.extend(donor_exemptions)

        total_exemptions = len(exemptions)
        self.report_data["total_exemptions"] = total_exemptions

        # Длительность отводов (только для отводов с указанной датой окончания)
        durations = []
        for exemption in exemptions:
            if exemption.end_date:
                duration = (exemption.end_date - exemption.start_date).days
                durations.append(duration)

        self.report_data["exemption_durations"] = durations

    def _categorize_donations(self, donations: list) -> Dict[str, int]:
        """Категоризация количества донаций"""
        categories = {
            "0": 0,
            "1": 0,
            "2-5": 0,
            "6-10": 0,
            "11-20": 0,
            "20+": 0
        }
        
        for count in donations:
            if count == 0:
                categories["0"] += 1
            elif count == 1:
                categories["1"] += 1
            elif 2 <= count <= 5:
                categories["2-5"] += 1
            elif 6 <= count <= 10:
                categories["6-10"] += 1
            elif 11 <= count <= 20:
                categories["11-20"] += 1
            else:
                categories["20+"] += 1
                
        return categories

    def generate_pdf_report(self) -> str:
        """Генерация PDF отчета организатора"""
        report_id = datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_path = os.path.join(self.temp_dir, f"organizer_report_{report_id}.pdf")

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

        # Статистика мероприятий
        self._create_event_stats_page(elements)
        elements.append(PageBreak())

        # Статистика доноров
        self._create_donor_stats_page(elements)
        elements.append(PageBreak())

        # Статистика регистраций
        self._create_registration_stats_page(elements)

        # Сборка документа
        doc.build(elements)
        return pdf_path

    def _create_cover_page(self, elements):
        """Создание титульной страницы"""
        elements.append(Paragraph(f"АНАЛИТИЧЕСКИЙ ОТЧЕТ ОРГАНИЗАТОРА", styles["Title"]))
        elements.append(Spacer(1, 1 * cm))
        elements.append(Paragraph("Анализ мероприятий и участников", styles["Heading2"]))
        elements.append(Spacer(1, 2 * cm))

        # Ключевые метрики
        metrics = [
            ("Общее количество мероприятий", self.report_data.get("total_events", 0)),
            ("Уникальных доноров", self.report_data.get("total_donors", 0)),
            ("Всего регистраций", self.report_data.get("total_registrations", 0)),
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

    def _create_donor_stats_page(self, elements):
        """Страница статистики доноров"""
        elements.append(Paragraph("СТАТИСТИКА ДОНОРОВ", styles["Title"]))
        elements.append(Spacer(1, 0.5 * cm))

        # Основная статистика
        elements.append(Paragraph("Общая статистика", styles["Heading2"]))
        elements.append(Paragraph(f"Всего доноров: {self.report_data.get('total_donors', 0)}", styles["Body"]))
        elements.append(Paragraph(f"Среднее количество донаций: {self.report_data.get('avg_donations', 0):.1f}", styles["Body"]))
        elements.append(Spacer(1, 0.5 * cm))

        # Распределение по количеству донаций
        elements.append(Paragraph("Распределение по количеству донаций", styles["Heading2"]))
        self._create_bar_chart(
            elements,
            self.report_data.get("donation_distribution", {}),
            "Количество донаций у доноров",
            "Количество донаций",
            "Количество доноров",
        )

    def _create_registration_stats_page(self, elements):
        """Страница статистики регистраций"""
        elements.append(Paragraph("СТАТИСТИКА РЕГИСТРАЦИЙ", styles["Title"]))
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
        plt.xticks(fontsize=10)
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


async def generate_organizer_report(adapter):
    """Генерация аналитического отчета для организатора"""
    report_generator = OrganizerAnalyticsReportGenerator(adapter)
    await report_generator.collect_data()
    report_path = report_generator.generate_pdf_report()
    return report_path