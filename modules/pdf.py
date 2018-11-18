from reportlab.pdfgen import canvas


def create_pdf(expenses):
    current_height = 750
    c = canvas.Canvas("expenses.pdf")
    c.drawString(100, current_height, "kategoria")
    c.drawString(198, current_height, "nazwa")
    c.drawString(296, current_height, "kwota")
    c.drawString(394, current_height, "data")
    for row in expenses:
        if current_height >= 100:
            current_height -= 20
        else:
            current_height = 750
            c.showPage()
        c.drawString(100, current_height, row[4])
        c.drawString(198, current_height, row[1])
        c.drawString(296, current_height, str(row[2]))
        c.drawString(394, current_height, row[3].strftime('%m-%d-%Y'))
    c.save()
