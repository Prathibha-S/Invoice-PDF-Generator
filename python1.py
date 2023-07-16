from fpdf import FPDF
from datetime import datetime,date
#date=datetime.now(tz=pytz.timezone(TIMEZONE))
from flask import Flask, render_template, request, redirect, send_file,make_response
from num2words import num2words

app = Flask(__name__)

class InvoiceGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.total_amount = 0
    def header(self):
        self.set_font('Arial', '', 10)
        # Invoice Number and Date
        d = date.today()
        dlabel = f'Date: {d}'
        self.cell(0, 10, f'No: {self.invnumber}', 0, 1, 'R')
        self.cell(0, 10, dlabel, 0, 1, 'R')

        # Company Information
        self.set_font('Arial', 'B', 14)
        line_spacing = 4.5 * 1.15
        self.cell(0, line_spacing, 'HOME AND DECOR', 0, 1)
        self.set_font('Arial', '', 10)
        self.cell(0, line_spacing, 'AYSHA ROAD PONNURUNNI VYTTILA', 0, 1)
        self.cell(0, line_spacing, 'KOCHI ERNAKULAM PIN 682019', 0, 1)
        self.set_font('Arial', '', 9)
        self.cell(0, line_spacing, 'GSTIN: 32BPVPM1424H1ZV            Phone:8078551022', 0, 1)
        self.ln(1)  # Add a line break

        # Tax Invoice Heading
        self.set_font('Arial', 'B', 9)
        self.set_x((self.w - self.get_string_width('TAX INVOICE (CREDIT)')) / 2)
        self.cell(0, 10, 'TAX INVOICE (CREDIT)', 0, 1)
        self.line(self.l_margin, self.y, self.w - self.r_margin, self.y)
        self.ln(1)
        self.set_font('Arial', '', 9)
        self.cell(50, line_spacing, '           Party:', 0, 0, 'L')  # Align to the left
        self.set_font('Arial', 'B', 10)
        self.cell(90, line_spacing, 'TOTAL ASSOCIATES', 0, 0, 'C')  # Center-aligned cell for the party name
        self.ln(line_spacing)
        self.set_font('Arial', '', 10)
        self.cell(0, line_spacing, 'BREEZE BUILDING, RS ROAD, OTTAPPALAM', 0, 0, 'C')  # Align to the center
        self.set_font('Arial', '', 8)
        self.cell(0, line_spacing, 'Vehicle Details:', 0, 1, 'R')
        self.set_font('Arial', '', 10)
        self.cell(0, line_spacing, 'PALAKKAD,KERALA, PIN NO:679101', 0, 1, 'C')  # Center-aligned cell for the location
        self.cell(50, line_spacing, '               GSTIN : 32AXYPR8191A1Z0', 0, 0, 'L') 
        self.cell(90, line_spacing, '9847400040', 0, 1, 'C')
        self.ln()
    def footer(self):
        # TODO: Define the footer content
        self.set_y(-30)
        total_amount_words = num2words(self.total_amount, lang='en').title()
    # Set the font and size for the footer content
        self.set_font('Arial', '', 8)
        line_spacing = 4.5 * 1.15
    # Footer content: Amount and For
        total_amount_label = f'Amount: {total_amount_words} Only'
        self.cell(0, line_spacing, total_amount_label, 0, 0, 'L')
        self.cell(0, line_spacing, 'For: HOME AND DECOR', 0, 1, 'R')
        # Footer content: Declaration
        self.cell(0, line_spacing, 'Declaration',0,0,'L')
        self.ln(line_spacing)
        self.multi_cell(0, line_spacing,'We declare that this invoice shows the actual price of the goods described and that all particulars are true and correct', 0, 'L')
    def generate_invoices(self, items,quantities,rates,invnumber):
        self.invnumber = invnumber[0]
        self.add_page()  # Add a new page

        # Generate the table headers
        self.set_font('Arial', '', 8)
        self.cell(5, 5, 'SI', 1,0,'C')
        self.cell(40, 5, 'Item', 1,0,'C')
        self.cell(15, 5, 'HSN', 1,0,'C')
        self.cell(20, 5, 'Qty', 1,0,'C')
        self.cell(10, 5, 'Unit', 1,0,'C')
        self.cell(20, 5, 'Rate', 1,0,'C')
        self.cell(10, 5, 'Dis%', 1,0,'C')
        self.cell(20, 5, 'Dis', 1,0,'C')
        self.cell(13, 5, 'GST%', 1,0,'C')
        self.cell(20, 5, 'GST AMt', 1,0,'C')
        self.cell(25, 5, 'Total', 1,0,'C')  # Increased the cell width
        self.ln()  # Add a line break

        # Generate the table rows
        self.set_font('Arial', '', 8)
        sl_no = 1
        t = 0
        total_gst = 0
        qty = 0
        for item, quantity, rate in zip(items, quantities, rates):
            quantity = float(quantity)
            rate = float(rate)
            tot = quantity * rate
            gstamt = quantity * (rate*(18/100))
            t += tot
            total = tot + gstamt
            total_gst += gstamt
            qty += quantity
            self.cell(5, 10, str(sl_no), 1)
            self.cell(40, 10, item, 1)
            self.cell(15, 10, ' ', 1)
            self.cell(20, 10, str(quantity), 1)
            self.cell(10, 10, 'ROLL', 1)
            self.cell(20, 10, str(rate), 1)
            self.cell(10, 10, '0.00', 1)
            self.cell(20, 10, ' ', 1)
            self.cell(13, 10, '18 %', 1)
            self.cell(20, 10, str(gstamt), 1, 0, 'R')
            self.cell(25, 10, str(total), 1, 0, 'R')  # Increased the cell width
            self.total_amount += total
            self.ln()  # Add a line break
            sl_no += 1
          # Add a line break
        total_items = len(items)
        remaining_empty_columns = max(0, 11 - total_items)
        item_cell_widths = [5, 40, 15, 20, 10, 20, 10, 20, 13, 20, 25]  # Adjust the width of each column as per your requirement
        for _ in range(remaining_empty_columns):
            for cell_width in item_cell_widths:
                self.cell(cell_width, 90, '', 'LTRB', 0, 'C')
    # ... Add more empty cells for other columns
        self.ln()

        self.cell(5, 5, '', 'LTRB')  # Empty cell for spacing
        self.cell(40, 5, '', 'LTRB')  # Empty cell for spacing
        self.cell(15, 5, '', 'LTRB')  # Empty cell for spacing
        self.cell(20, 5, str(qty), 'LTRB', 0, 'R')  # Empty cell for spacing
        self.cell(10, 5, '', 'LTRB')  # Empty cell for spacing
        self.cell(20, 5, '', 'LTRB')  # Empty cell for spacing
        self.cell(10, 5, '', 'LTRB')  # Empty cell for spacing
        self.cell(20, 5, '0.00', 'LTRB')  # Empty cell for spacing
        self.cell(13, 5, '', 'LTRB')  # Empty cell for spacing
        self.cell(20, 5, str(total_gst), 'LTRB', 0, 'R')  # Cell for label
        self.cell(25, 5, str(self.total_amount), 'LTRB', 0 , 'R')  # Cell for calculated amount
        self.ln()
        bottom_labels = ['Kerala Flood Cess', 'Discount', 'Shipping Charge', 'Other Expenses', 'Round Off', 'Bill Amount']
        bottom_values = [' ', '0.00', '0.00', '0.00', '0.00', str(self.total_amount)]
        for i in range(len(bottom_labels)):
            self.cell(5, 5, '', 0)  # Empty cell for spacing
            self.cell(40, 5, '', 0)  # Empty cell for spacing
            self.cell(15, 5, '', 0)  # Empty cell for spacing
            self.cell(20, 5, '', 0)  # Empty cell for spacing
            self.cell(10, 5, '', 0)  # Empty cell for spacing
            self.cell(20, 5, '', 0)  # Empty cell for spacing
            self.cell(10, 5, '', 0)  # Empty cell for spacing
            self.cell(20, 5, '', 0)  # Empty cell for spacing
            #self.cell(13, 5, '', 0)  # Empty cell for spacing
            self.cell(33, 5, bottom_labels[i], 1, 0, 'R')  # Bottom label
            if bottom_labels[i] == 'Bill Amount':
                self.set_font('Arial', 'B', 9)
            self.cell(25, 5, bottom_values[i], 1, 0,'R')  # Bottom value
            if bottom_values[i] == self.total_amount :
                self.set_font('Arial', 'B', 9)
            self.ln()
        self.set_font('Arial', '', 7)
        self.cell(20, 3, 'Taxable')
        self.cell(15, 3, 'CGST %')
        self.cell(15, 3, 'CGST Amt')
        self.cell(15, 3, 'SGST %')
        self.cell(15, 3, 'SGST Amt')
        self.cell(15, 3, 'IGST %')
        self.cell(15, 3, 'IGST Amt')
        self.ln()

        # Generate the table content (one row)
        cgst = t*(9/100)
        sgst = t*(9/100)
        self.set_font('Arial', '', 7)
        self.cell(20, 5, str(t))
        self.cell(15, 5, '9 %')
        self.cell(15, 5, str(cgst))
        self.cell(15, 5, '9 %')
        self.cell(15, 5, str(sgst))
        self.cell(15, 5, ' ')
        self.cell(15, 5, '0.00')
        self.ln()
        filename = f'invoice_{date.today()}.pdf'

        # Save the invoice PDF file
        self.output(filename, 'F')

        # Return the filename for downloading the invoice PDF
        return filename
@app.route('/')
def home():
    return render_template('invoice_form.html')

@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    invnumber = request.form.getlist('invnumber')
    items = request.form.getlist('item[]')
    quantities = request.form.getlist('quantity[]')
    rates = request.form.getlist('rate[]')

    invoice = InvoiceGenerator()
    invoice.generate_invoices(items, quantities, rates, invnumber)
    invoice_filename = f'{invnumber[0]} TOTAL ASSOCIATES.pdf'
    invoice.output(invoice_filename)

    # Prepare the file for download
    response = make_response(send_file(invoice_filename, as_attachment=True))
    response.headers["Content-Disposition"] = f"attachment; filename={invoice_filename}"

    return response
if __name__ == '__main__':
    app.run(debug=True)