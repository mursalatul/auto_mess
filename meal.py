from openpyxl import Workbook, load_workbook
import calendar
from datetime import datetime, timedelta, date


class Meal:
    def __init__(self, filec: str) -> None:
        self.xl_file = filec # targeted xlsx file, store meal data(date, meal of a person)

    async def getDaysInMonth(self, year: int, month: int):
        """
        return number of days in the following month of the year
        """
        last_day = calendar.monthrange(year, month)[1]
        return last_day

    async def initializeSheet(self, names: list):
        """
        this method will only called first day of the month to create and initialize the sheet.
        previous date will be removed as new sheet will be created
        """
        # adding dates in the sheet creating date
        present_day = datetime.now().strftime("%d-%m-%Y")
        year = date.today().year
        month = date.today().month
        num_of_days_in_month = self.getDaysInMonth(year, month)

        # creating workbook and sheet
        # workbook = load_workbook(self.xl_file)
        workbook = Workbook()
        sheet1 = workbook.active

        # adding dates in the 1st column
        for i in range(0, num_of_days_in_month):
            next_day = (datetime.now() + timedelta(days=i)
                        ).strftime("%d-%m-%Y")
            cell = sheet1.cell(row=i + 2, column=1)
            cell.value = next_day

        # adding names in the 1st row
        for i, ele in enumerate(names):
            cell = sheet1.cell(row=1, column=i + 2)
            cell.value = ele
        # saving the sheet
        workbook.save(filename="mealdataxx.xlsx")

    async def readMeal(self, date: datetime, name: str = 'All') -> dict:
        """
        return meal of a specific date.
        Args:
            date(DD-MM-YYYY) : date of meal
            name(optional) : name of a particular participant
        Return:
            dict    : name with number of meal
        """
        wb = load_workbook(self.xl_file)
        sheet1 = wb.active
        all_meals = {
            'Adil': 0,
            'Elias': 0,
            'Labib': 0,
            'Nahid': 0,
            'Nurul': 0,
            'Pallob': 0,
            'Prottus': 0,
            'Swadhin': 0
        }

        # converting datetime -> str
        date = date.strftime('%d-%m-%Y')

        # iterating the sheet for the specific date row
        date_row = 0
        for i in range(1, 32):
            cell = sheet1.cell(row=i, column=1)
            if cell.value == date:
                date_row = i

        # getting all the meals from that that row and saving in the dict
        for meal_number in range(2, 10):
            cell = sheet1.cell(row=1, column=meal_number)
            cell_head = cell.value
            cell = sheet1.cell(row=date_row, column=meal_number)
            all_meals[cell_head] = str(cell.value)

        # if no name provided, return all meal, else particular name meal
        if name == 'All':
            return all_meals
        else:
            return {name: all_meals[name]}

    async def writeAMeal(self, date: datetime, name: str, total_meal: str) -> None:
        """
        Write meal for a particular person
        Args:
            date(datetime object)    : date of the meal
            name    : meal holder name
            total_meal : number of meals(meal can be 00, 11, 01, 10)
        Return:
            None
        """
        # edit meal from current date to future dates. not previous dates
        present_day = datetime.today().date()
        if (date >= present_day):
            wb = load_workbook(self.xl_file)
            sheet1 = wb.active
            # finding the row of date
            date_row = date.day + 1
            date = date.strftime("%d-%m-%Y") # converting datetime -> str

            # finding the name culumn
            name_col = 0
            for c in range (2, 10):
                cell = sheet1.cell(row=1, column=c)
                if cell.value == name:
                    name_col = c
                    break
            # setting the meal
            sheet1.cell(row=date_row, column=name_col).value = str(total_meal)
            wb.save(self.xl_file)

    async def writeAllMeal(self, date: datetime, name: str, total_meal: str):
        """
        write all the meal from 'date' to last date of the into total_meal
        Args:
            date(datetime object)    : date of the meal
            name    : meal holder name
            total_meal : number of meals(meal can be 00, 11, 01, 10)
        Return:
            None
        """
        present_day = datetime.today().date()
        #write meal only for today and next days. not previous days
        if (date >= present_day):
            total_days = await self.getDaysInMonth(date.year, date.month)
            print(total_days, date.day)
            reminding_days = total_days - date.day
            for i in range(reminding_days + 1):
                await self.writeAMeal(date + timedelta(i), name, total_meal)
