import calendar
from datetime import datetime

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_calendar.common import GenericCalendar
from aiogram_calendar.schemas import (
    DialogCalAct,
    DialogCalendarCallback,
    highlight,
    superscript,
)


class DialogCalendarNoCancel(GenericCalendar):
    ignore_callback = DialogCalendarCallback(act=DialogCalAct.ignore).pack()

    async def _get_month_kb(self, year: int):
        today = datetime.now()
        now_month, now_year = today.month, today.year
        kb = []

        years_row = [
            InlineKeyboardButton(
                text=str(year) if year != now_year else highlight(year),
                callback_data=DialogCalendarCallback(act=DialogCalAct.start, year=year, month=-1, day=-1).pack(),
            ),
            InlineKeyboardButton(text=" ", callback_data=self.ignore_callback),
        ]
        kb.append(years_row)

        month6_row, month12_row = [], []
        for month in range(1, 7):
            month_str = self._labels.months[month - 1]
            label = highlight(month_str) if now_month == month and now_year == year else month_str
            month6_row.append(
                InlineKeyboardButton(
                    text=label,
                    callback_data=DialogCalendarCallback(act=DialogCalAct.set_m, year=year, month=month, day=-1).pack(),
                )
            )
        for month in range(7, 13):
            month_str = self._labels.months[month - 1]
            label = highlight(month_str) if now_month == month and now_year == year else month_str
            month12_row.append(
                InlineKeyboardButton(
                    text=label,
                    callback_data=DialogCalendarCallback(act=DialogCalAct.set_m, year=year, month=month, day=-1).pack(),
                )
            )

        kb.extend([month6_row, month12_row])
        return InlineKeyboardMarkup(row_width=6, inline_keyboard=kb)

    async def _get_days_kb(self, year: int, month: int):
        today = datetime.now()
        now_day, now_month, now_year = today.day, today.month, today.year
        now_weekday = self._labels.days_of_week[today.weekday()]
        kb = []

        header_row = [
            InlineKeyboardButton(
                text=str(year) if year != now_year else highlight(year),
                callback_data=DialogCalendarCallback(act=DialogCalAct.start, year=year, month=-1, day=-1).pack(),
            ),
            InlineKeyboardButton(
                text=self._labels.months[month - 1],
                callback_data=DialogCalendarCallback(act=DialogCalAct.set_y, year=year, month=-1, day=-1).pack(),
            ),
        ]
        kb.append(header_row)

        week_header = []
        for weekday in self._labels.days_of_week:
            label = (
                highlight(weekday) if weekday == now_weekday and year == now_year and month == now_month else weekday
            )
            week_header.append(InlineKeyboardButton(text=label, callback_data=self.ignore_callback))
        kb.append(week_header)

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(InlineKeyboardButton(text=" ", callback_data=self.ignore_callback))
                    continue

                date_to_check = datetime(year, month, day)
                if (self.min_date and date_to_check < self.min_date) or (
                    self.max_date and date_to_check > self.max_date
                ):
                    label = superscript(str(day))
                else:
                    label = str(day)

                if day == now_day and month == now_month and year == now_year:
                    label = highlight(label)

                row.append(
                    InlineKeyboardButton(
                        text=label,
                        callback_data=DialogCalendarCallback(
                            act=DialogCalAct.day, year=year, month=month, day=day
                        ).pack(),
                    )
                )
            kb.append(row)

        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)

    async def start_calendar(self, year: int = datetime.now().year, month: int = None) -> InlineKeyboardMarkup:
        now_year = datetime.now().year
        if month:
            return await self._get_days_kb(year, month)

        kb = []

        years_row = [
            InlineKeyboardButton(
                text=str(value) if value != now_year else highlight(value),
                callback_data=DialogCalendarCallback(act=DialogCalAct.set_y, year=value, month=-1, day=-1).pack(),
            )
            for value in range(year - 2, year + 3)
        ]
        kb.append(years_row)

        nav_row = [
            InlineKeyboardButton(
                text="<<",
                callback_data=DialogCalendarCallback(act=DialogCalAct.prev_y, year=year, month=-1, day=-1).pack(),
            ),
            InlineKeyboardButton(
                text=">>",
                callback_data=DialogCalendarCallback(act=DialogCalAct.next_y, year=year, month=-1, day=-1).pack(),
            ),
        ]
        kb.append(nav_row)

        return InlineKeyboardMarkup(row_width=5, inline_keyboard=kb)

    async def process_selection(self, query: CallbackQuery, data: DialogCalendarCallback) -> tuple:
        return_data = (False, None)

        if data.act == DialogCalAct.ignore:
            await query.answer(cache_time=60)
        elif data.act == DialogCalAct.set_y:
            await query.message.edit_reply_markup(reply_markup=await self._get_month_kb(int(data.year)))
        elif data.act == DialogCalAct.prev_y:
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(data.year) - 5))
        elif data.act == DialogCalAct.next_y:
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(data.year) + 5))
        elif data.act == DialogCalAct.start:
            await query.message.edit_reply_markup(reply_markup=await self.start_calendar(int(data.year)))
        elif data.act == DialogCalAct.set_m:
            await query.message.edit_reply_markup(reply_markup=await self._get_days_kb(int(data.year), int(data.month)))
        elif data.act == DialogCalAct.day:
            return await self.process_day_select(data, query)

        return return_data
