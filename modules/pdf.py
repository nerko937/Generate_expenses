from reportlab.pdfgen import canvas


def create_pdf(expenses):
    h = 750
    c = canvas.Canvas("expenses.pdf")
    c.drawString(100, h, "kategoria")
    c.drawString(198, h, "nazwa")
    c.drawString(296, h, "kwota")
    c.drawString(394, h, "data")
    for row in expenses:
        if h >= 100:
            h -= 20
        else:
            h = 750
            c.showPage()
        c.drawString(100, h, row[4])
        c.drawString(198, h, row[1])
        c.drawString(296, h, str(row[2]))
        c.drawString(394, h, row[3].strftime('%m-%d-%Y'))
    c.save()