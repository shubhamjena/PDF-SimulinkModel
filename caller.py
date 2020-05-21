from pdf_png import *
import os

if __name__ == '__main__':

    file_path = 'F:/AIRBUS/Internship/samplePdfs/untitled.pdf'
    os.chdir('F:/AIRBUS/Internship/intern_code/')

    print('converting to jpg')
    convert_pdf('untitled.pdf')
    print('pdf converted to jpg')

    print('calling segmentation.py')
    exec(open("segmentation.py").read())
    #os.system('segmentation.py')
    print('segmentation.py finished')