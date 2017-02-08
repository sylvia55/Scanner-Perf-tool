import xlsxwriter


class WriteResult(object):

    count = 0
    def __init__(self, worksheet):
        self.worksheet = worksheet

    def write_excel(self, result):

        self.write_result(self.worksheet, result)
        # workbook.close()

    def write_result(self, worksheet, result):

        row = 0
        col = 0

        for l in result:
            worksheet.write(row+self.count, col, l)
            col += 1
            # worksheet.write('B'+self.count, )
        print self.count
        self.count += 1


def main():
    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet = workbook.add_worksheet()
    w = WriteResult(worksheet)
    list = [1,2]
    w.write_excel(list)
    w.write_excel(list)

if __name__ == '__main__':
    main()
